"""界面通用组件与引导逻辑。"""
from __future__ import annotations

import hashlib
import html
import time
from datetime import date, datetime
from typing import Any, Callable, Iterable, Optional

import pandas as pd
import streamlit as st

from ..config import get_settings
from ..constants import PENDING, label
from ..utils import ValidationError, humanize_days, days_until

# ------------------------------------------------------------------ bootstrap


@st.cache_resource(show_spinner=False)
def _bootstrap(db_path: str) -> dict:
    """每个数据库路径只执行一次：建表/迁移、首次初始化、自动备份、定时任务、孤儿运行修正。"""
    from pathlib import Path

    from .. import db, seed
    from ..services import backup, bioinfo, runner

    settings = get_settings()
    settings.ensure_dirs()
    db.init_engine(Path(db_path))
    seeded = seed.seed_initial_data()
    info: dict[str, Any] = {"seeded": seeded, "auto_backup": None, "scheduler": False, "reconciled": 0}
    try:
        b = backup.maybe_auto_backup()
        info["auto_backup"] = str(b) if b else None
    except Exception as e:  # noqa: BLE001
        info["auto_backup_error"] = str(e)
    info["reconciled"] = bioinfo.reconcile_orphan_runs(runner.running_pids())
    try:
        from apscheduler.schedulers.background import BackgroundScheduler

        if settings.auto_backup_hours > 0:
            sched = BackgroundScheduler(daemon=True)
            sched.add_job(backup.maybe_auto_backup, "interval", hours=max(settings.auto_backup_hours / 4, 1),
                          id="auto_backup", replace_existing=True, max_instances=1, coalesce=True)
            sched.start()
            info["scheduler"] = True
    except Exception as e:  # noqa: BLE001  APScheduler 是可选依赖
        info["scheduler_error"] = str(e)
    return info


def bootstrap() -> dict:
    from .. import db

    path = str(get_settings().db_path)
    info = _bootstrap(path)
    db.init_engine(get_settings().db_path)  # 恢复备份后重新连接（幂等）
    return info


# ------------------------------------------------------------------- layout
def page_header(title: str, subtitle: Optional[str] = None) -> None:
    st.title(title)
    if subtitle:
        st.html(f'<div class="rcc-sub">{html.escape(subtitle)}</div>')


def flash(message: str, icon: str = "✅") -> None:
    st.session_state.setdefault("_rcc_flash", []).append((message, icon))


def show_flash() -> None:
    for msg, icon in st.session_state.pop("_rcc_flash", []):
        st.toast(msg, icon=icon)


def _submit_sig(data: dict) -> str:
    return hashlib.sha1(repr(sorted((k, str(v)) for k, v in data.items())).encode("utf-8")).hexdigest()


def is_repeat_submit(form_key: str, data: dict, window: float = 8.0) -> bool:
    """防重复提交：同一表单、相同内容在成功保存后的短时间内再次提交（双击、网络重发）时返回 True。"""
    last = st.session_state.get("_rcc_submits", {}).get(form_key)
    return bool(last and last[0] == _submit_sig(data) and time.time() - last[1] < window)


def mark_submit_done(form_key: str, data: dict) -> None:
    st.session_state.setdefault("_rcc_submits", {})[form_key] = (_submit_sig(data), time.time())


def show_errors(e: ValidationError) -> None:
    for m in e.errors:
        st.error(m, icon="⚠️")


def run_action(fn: Callable, *args, success: Optional[str] = None, rerun: bool = True, **kwargs) -> Any:
    """执行服务层操作；校验错误就地显示；成功后提示并刷新。"""
    try:
        result = fn(*args, **kwargs)
    except ValidationError as e:
        show_errors(e)
        return None
    if success:
        flash(success)
    if rerun:
        st.rerun()
    return result


def html_block(body: str) -> None:
    """st.html 的安全版本：内容为空时不渲染（st.html 不接受空字符串）。"""
    if body and body.strip():
        st.html(body)


def nav_link(page: str, text: str) -> None:
    """跳转到其他页面的链接；单独运行某个页面（测试）时页面未注册，静默跳过。"""
    from streamlit.errors import StreamlitAPIException

    try:
        st.page_link(page, label=text, icon=":material/arrow_forward:")
    except StreamlitAPIException:
        pass


def esc(x: Any) -> str:
    return html.escape("" if x is None else str(x))


def pending(value: Any, fmt: Optional[Callable[[Any], str]] = None) -> str:
    """HTML：空值显示为灰色“待填写”。"""
    if value is None or value == "":
        return f'<span class="rcc-pending">{PENDING}</span>'
    return esc(fmt(value) if fmt else value)


def kv_block(rows: Iterable[tuple[str, Any]]) -> None:
    parts = ['<div class="rcc-kv">']
    for k, v in rows:
        parts.append(f'<div class="k">{esc(k)}</div><div class="v">{v if isinstance(v, _Raw) else pending(v)}</div>')
    parts.append("</div>")
    st.html("".join(parts))


class _Raw(str):
    """kv_block 中已转义的 HTML 片段。"""


def raw(s: str) -> _Raw:
    return _Raw(s)


def tag(text: str, kind: str = "") -> str:
    return f'<span class="rcc-tag {kind}">{esc(text)}</span>'


def fmt_date(d: Optional[date]) -> str:
    return d.strftime("%Y-%m-%d") if d else ""


def fmt_dt(d: Optional[datetime]) -> str:
    return d.strftime("%Y-%m-%d %H:%M") if d else ""


def due_text(d: Optional[date]) -> str:
    if d is None:
        return ""
    return f"{fmt_date(d)}（{humanize_days(days_until(d))}）"


def empty_state(message: str, hint: Optional[str] = None) -> None:
    st.html(f'<div class="rcc-muted" style="padding:1.2rem 0">{esc(message)}'
            + (f'<div class="rcc-small" style="margin-top:.3rem">{esc(hint)}</div>' if hint else "") + "</div>")


# --------------------------------------------------------------- selectors
def project_selector(label_text: str, key: str, current: Optional[int] = None, include_none: bool = True,
                     none_label: str = "（不关联项目）", include_archived: bool = False) -> Optional[int]:
    from ..services import projects

    names = projects.project_name_map(include_archived=True)
    active = projects.project_name_map(include_archived=include_archived)
    options: list[Optional[int]] = ([None] if include_none else []) + list(active.keys())
    if current is not None and current not in options:
        options.append(current)
    idx = options.index(current) if current in options else 0
    return st.selectbox(label_text, options, index=idx if options else None, key=key,
                        format_func=lambda x: none_label if x is None else names.get(x, f"#{x}"))


def code_select(label_text: str, kind: str, options: list[str], key: str, current: Optional[str] = None,
                allow_empty: bool = False, empty_label: str = PENDING, help: Optional[str] = None) -> Optional[str]:
    opts: list[Optional[str]] = ([None] if allow_empty else []) + list(options)
    idx = opts.index(current) if current in opts else 0
    return st.selectbox(label_text, opts, index=idx, key=key, help=help,
                        format_func=lambda x: empty_label if x is None else label(kind, x))


def select_row(df: pd.DataFrame, key: str, column_config: Optional[dict] = None, height: Any = "auto",
               id_col: str = "id", hide: Iterable[str] = ("id",)) -> Optional[int]:
    """可单选的表格，返回选中行的 id。"""
    if df.empty:
        return None
    cols = [c for c in df.columns if c not in set(hide)]
    ev = st.dataframe(placeholder="—", data=df, key=key, on_select="rerun", selection_mode="single-row", hide_index=True,
                      column_order=cols, column_config=column_config or {}, height=height, width="stretch")
    rows = ev.selection.rows if ev is not None and hasattr(ev, "selection") else []
    if rows:
        return int(df.iloc[rows[0]][id_col])
    return None


def confirm_button(label_text: str, key: str, confirm_text: str = "我确认执行此操作",
                   type: str = "secondary") -> bool:
    """两步确认：先勾选，再点击。"""
    c1, c2 = st.columns([3, 2])
    ok = c1.checkbox(confirm_text, key=f"{key}_chk")
    clicked = c2.button(label_text, key=key, disabled=not ok, type=type, width="stretch")
    return bool(ok and clicked)


def path_lines_status(text: Optional[str]) -> list[tuple[str, bool]]:
    from ..utils import file_stat, split_lines

    return [(p, file_stat(p)["exists"]) for p in split_lines(text)]


def render_paths(text: Optional[str], empty: str = PENDING) -> str:
    items = path_lines_status(text)
    if not items:
        return f'<span class="rcc-pending">{esc(empty)}</span>'
    from pathlib import Path

    out = []
    for p, ok in items:
        pp = Path(p)
        out.append(f'<div class="rcc-path" title="{esc(p)}"><span>{esc(pp.name)}</span>'
                   f'{"" if ok else tag("不存在", "danger")}<div class="dir">{esc(pp.parent)}</div></div>')
    return "".join(out)
