"""数据库引擎、会话与初始化（含轻量级“只增不删”的自动迁移与全文索引表）。"""
from __future__ import annotations

import logging
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from .config import get_settings
from .models import AppMeta, Base, now

log = logging.getLogger(__name__)

SCHEMA_VERSION = 1

_engine: Optional[Engine] = None
_SessionLocal: Optional[sessionmaker] = None
_db_path: Optional[Path] = None
_lock = threading.RLock()


def _set_pragmas(dbapi_conn, _record) -> None:
    cur = dbapi_conn.cursor()
    cur.execute("PRAGMA foreign_keys=ON")
    cur.execute("PRAGMA busy_timeout=30000")
    cur.close()


def init_engine(db_path: Optional[Path] = None) -> Engine:
    """创建（或重用）引擎并确保表结构存在。可重复调用。"""
    global _engine, _SessionLocal, _db_path
    with _lock:
        path = Path(db_path) if db_path else get_settings().db_path
        path = path.resolve()
        if _engine is not None and _db_path == path:
            return _engine
        if _engine is not None:
            _engine.dispose()
        path.parent.mkdir(parents=True, exist_ok=True)
        engine = create_engine(
            f"sqlite:///{path.as_posix()}",
            connect_args={"check_same_thread": False, "timeout": 30},
        )
        event.listen(engine, "connect", _set_pragmas)
        Base.metadata.create_all(engine)
        _add_missing_columns(engine)
        _create_fulltext_table(engine)
        _engine = engine
        _SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)
        _db_path = path
        with session_scope() as s:
            if s.get(AppMeta, "schema_version") is None:
                s.add(AppMeta(key="schema_version", value=str(SCHEMA_VERSION)))
                s.add(AppMeta(key="created_at", value=now().isoformat()))
        return engine


def dispose_engine() -> None:
    global _engine, _SessionLocal, _db_path
    with _lock:
        if _engine is not None:
            _engine.dispose()
        _engine, _SessionLocal, _db_path = None, None, None


def get_engine() -> Engine:
    if _engine is None:
        init_engine()
    assert _engine is not None
    return _engine


def current_db_path() -> Path:
    get_engine()
    assert _db_path is not None
    return _db_path


@contextmanager
def session_scope() -> Iterator[Session]:
    if _SessionLocal is None:
        init_engine()
    assert _SessionLocal is not None
    session: Session = _SessionLocal()
    try:
        yield session
        session.commit()
    except IntegrityError as e:
        session.rollback()
        from .utils import ValidationError

        raise ValidationError(integrity_message(e)) from e
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def integrity_message(exc: IntegrityError) -> str:
    """把数据库约束错误转换为可读的中文提示。"""
    msg = str(exc.orig) if exc.orig else str(exc)
    up = msg.upper()
    if "UNIQUE" in up:
        return "存在重复记录（唯一字段冲突）：" + msg.split(":")[-1].strip()
    if "FOREIGN KEY" in up:
        return "关联的记录不存在或仍被引用"
    if "NOT NULL" in up:
        return "缺少必填字段：" + msg.split(":")[-1].strip()
    return "数据库约束冲突：" + msg


# ----------------------------------------------------------------- meta helpers
def get_meta(key: str, default: Optional[str] = None) -> Optional[str]:
    with session_scope() as s:
        row = s.get(AppMeta, key)
        return row.value if row is not None else default


def set_meta(key: str, value: Optional[str]) -> None:
    with session_scope() as s:
        row = s.get(AppMeta, key)
        if row is None:
            s.add(AppMeta(key=key, value=value))
        else:
            row.value = value


# ------------------------------------------------------------------ migrations
def _add_missing_columns(engine: Engine) -> None:
    """只增不删的自动迁移：模型新增了可空列时，为旧数据库补列，保证升级后旧数据可用。"""
    insp = inspect(engine)
    with engine.begin() as conn:
        for table in Base.metadata.sorted_tables:
            if not insp.has_table(table.name):
                continue
            existing = {c["name"] for c in insp.get_columns(table.name)}
            for col in table.columns:
                if col.name in existing:
                    continue
                if not col.nullable and col.default is None and col.server_default is None:
                    log.warning("跳过非空且无默认值的新列 %s.%s", table.name, col.name)
                    continue
                coltype = col.type.compile(engine.dialect)
                default_sql = ""
                if col.default is not None and getattr(col.default, "is_scalar", False):
                    val = col.default.arg
                    if isinstance(val, bool):
                        default_sql = f" DEFAULT {1 if val else 0}"
                    elif isinstance(val, (int, float)):
                        default_sql = f" DEFAULT {val}"
                    elif isinstance(val, str):
                        escaped = val.replace("'", "''")
                        default_sql = f" DEFAULT '{escaped}'"
                conn.execute(text(f'ALTER TABLE "{table.name}" ADD COLUMN "{col.name}" {coltype}{default_sql}'))
                log.info("已为 %s 补充列 %s", table.name, col.name)


FTS_TABLE = "literature_fulltext"


def _create_fulltext_table(engine: Engine) -> None:
    """PDF 全文索引（FTS5）。trigram 分词器支持中文与任意子串检索；不可用时退回 unicode61。"""
    with engine.begin() as conn:
        exists = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name=:n"), {"n": FTS_TABLE}
        ).first()
        if exists:
            return
        try:
            conn.execute(text(
                f"CREATE VIRTUAL TABLE {FTS_TABLE} USING fts5("
                "content, literature_id UNINDEXED, page UNINDEXED, tokenize='trigram')"
            ))
        except Exception:  # 旧版 SQLite 无 trigram
            conn.execute(text(
                f"CREATE VIRTUAL TABLE {FTS_TABLE} USING fts5(content, literature_id UNINDEXED, page UNINDEXED)"
            ))
