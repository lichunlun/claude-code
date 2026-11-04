"""数据库备份与恢复。

- 使用 SQLite 在线备份 API（应用运行中也能得到一致的快照）；
- 每个备份都做 PRAGMA integrity_check 校验；
- 自动备份（auto）按保留数量轮换；手动备份（manual）与恢复前备份（pre-restore）永不自动删除；
- 恢复前总会先备份当前数据库。
"""
from __future__ import annotations

import re
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from ..config import get_settings
from ..db import current_db_path, dispose_engine, get_meta, init_engine, set_meta
from ..utils import ValidationError

NAME_RE = re.compile(r"^research_(\d{8}_\d{6})_(auto|manual|pre-restore|scheduled)\.db$")
KINDS = ("auto", "manual", "pre-restore", "scheduled")


def _check(path: Path) -> tuple[bool, str]:
    try:
        # 以只读 URI 打开（as_uri 会正确处理 Windows 盘符、中文与特殊字符）
        con = sqlite3.connect(Path(path).resolve().as_uri() + "?mode=ro", uri=True)
        try:
            res = con.execute("PRAGMA integrity_check").fetchone()[0]
            tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        finally:
            con.close()
    except sqlite3.Error as e:
        return False, f"无法读取：{e}"
    if res != "ok":
        return False, f"完整性检查失败：{res}"
    if not {"projects", "tasks", "app_meta"} <= tables:
        return False, "不是本系统的数据库（缺少核心表）"
    return True, "ok"


def verify_backup(path: str | Path) -> tuple[bool, str]:
    p = Path(path)
    if not p.exists():
        return False, "文件不存在"
    return _check(p)


def backup_database(kind: str = "manual", db_path: Optional[Path] = None,
                    backup_dir: Optional[Path] = None) -> Path:
    if kind not in KINDS:
        raise ValidationError("未知的备份类型")
    settings = get_settings()
    src_path = Path(db_path) if db_path else current_db_path()
    if not src_path.exists():
        raise ValidationError(f"数据库文件不存在：{src_path}")
    out_dir = Path(backup_dir) if backup_dir else settings.backup_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = out_dir / f"research_{stamp}_{kind}.db"
    n = 1
    while target.exists():  # 同一秒内多次备份
        target = out_dir / f"research_{stamp}_{kind}.db".replace(".db", f"_{n}.db")
        n += 1
        if n > 50:
            raise ValidationError("备份文件名冲突")
    tmp = target.with_suffix(".tmp")
    src = sqlite3.connect(str(src_path))
    dst = sqlite3.connect(str(tmp))
    try:
        src.backup(dst)
    finally:
        dst.close()
        src.close()
    ok, msg = _check(tmp)
    if not ok:
        tmp.unlink(missing_ok=True)
        raise ValidationError(f"备份校验失败：{msg}")
    tmp.replace(target)
    if db_path is None:
        set_meta(f"last_backup_{kind}", datetime.now().isoformat(timespec="seconds"))
        set_meta("last_backup_at", datetime.now().isoformat(timespec="seconds"))
    if kind in ("auto", "scheduled"):
        prune_backups(out_dir, settings.backup_keep)
    return target


def list_backups(backup_dir: Optional[Path] = None) -> list[dict]:
    d = Path(backup_dir) if backup_dir else get_settings().backup_dir
    if not d.exists():
        return []
    out = []
    for p in d.glob("research_*.db"):
        m = re.match(r"^research_(\d{8}_\d{6})_([a-z\-]+?)(?:_\d+)?\.db$", p.name)
        if not m:
            continue
        try:
            created = datetime.strptime(m.group(1), "%Y%m%d_%H%M%S")
        except ValueError:
            continue
        out.append({"path": str(p), "name": p.name, "kind": m.group(2), "created": created,
                    "size": p.stat().st_size})
    out.sort(key=lambda r: r["created"], reverse=True)
    return out


def prune_backups(backup_dir: Path, keep: int) -> int:
    autos = [b for b in list_backups(backup_dir) if b["kind"] in ("auto", "scheduled")]
    removed = 0
    for b in autos[keep:]:
        Path(b["path"]).unlink(missing_ok=True)  # 只清理本系统生成的自动备份
        removed += 1
    return removed


def maybe_auto_backup() -> Optional[Path]:
    """距离上次自动备份超过设定间隔时执行一次（应用启动时调用）。"""
    settings = get_settings()
    if settings.auto_backup_hours <= 0:
        return None
    if not current_db_path().exists():
        return None
    last = get_meta("last_backup_auto")
    if last:
        try:
            if datetime.now() - datetime.fromisoformat(last) < timedelta(hours=settings.auto_backup_hours):
                return None
        except ValueError:
            pass
    return backup_database("auto")


def restore_database(backup_path: str | Path, db_path: Optional[Path] = None) -> Path:
    """用备份覆盖当前数据库。先校验备份，再为当前数据库做一次 pre-restore 备份。返回 pre-restore 备份路径。"""
    bp = Path(backup_path)
    ok, msg = verify_backup(bp)
    if not ok:
        raise ValidationError(f"备份文件不可用：{msg}")
    target = Path(db_path) if db_path else current_db_path()
    pre = backup_database("pre-restore", db_path=target) if target.exists() else None
    if db_path is None:
        dispose_engine()
    src = sqlite3.connect(str(bp))
    dst = sqlite3.connect(str(target))
    try:
        src.backup(dst)
    finally:
        dst.close()
        src.close()
    if db_path is None:
        init_engine(target)
        set_meta("last_restore_at", datetime.now().isoformat(timespec="seconds"))
        set_meta("last_restore_from", bp.name)
    return pre if pre else target


def export_excel(out_path: Path) -> Path:
    """把所有业务表导出为一个 Excel 文件（每表一个工作表），便于长期留存或迁移。"""
    import pandas as pd

    from ..db import get_engine
    from ..models import Base

    out_path.parent.mkdir(parents=True, exist_ok=True)
    engine = get_engine()
    with pd.ExcelWriter(out_path, engine="openpyxl") as xw:
        for table in Base.metadata.sorted_tables:
            df = pd.read_sql_table(table.name, engine)
            df.to_excel(xw, sheet_name=table.name[:31], index=False)
    return out_path
