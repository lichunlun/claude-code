"""设置与备份：数据位置、备份/恢复、导出、脚本执行开关、操作日志、外观。"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from rcc import __version__
from rcc.config import CONFIG_FILE, get_settings
from rcc.db import SCHEMA_VERSION, current_db_path, get_meta
from rcc.services import activity, app_settings, backup
from rcc.ui.common import (
    bootstrap,
    confirm_button,
    esc,
    kv_block,
    page_header,
    raw,
    run_action,
    show_errors,
    show_flash,
)
from rcc.utils import ValidationError, human_size

info = bootstrap()
show_flash()
s = get_settings()

page_header("设置与备份", "所有数据保存在本机。这里管理数据位置、备份与恢复、数据导出与安全选项。")
t_data, t_backup, t_exec, t_log, t_about = st.tabs(["数据位置", "备份与恢复", "脚本执行", "操作日志", "外观与关于"])

with t_data:
    db = current_db_path()
    kv_block([
        ("数据库文件", raw(f"<code>{esc(db)}</code>")),
        ("数据库大小", human_size(db.stat().st_size) if db.exists() else None),
        ("数据目录", raw(f"<code>{esc(s.data_dir)}</code>")),
        ("备份目录", raw(f"<code>{esc(s.backup_dir)}</code>")),
        ("运行日志目录", raw(f"<code>{esc(s.log_dir)}</code>")),
        ("上传副本目录", raw(f"<code>{esc(s.library_dir)}</code>")),
        ("结构版本", str(SCHEMA_VERSION)),
        ("数据库创建于", (get_meta("created_at") or "").replace("T", " ") or None),
        ("配置文件", raw(f"<code>{esc(CONFIG_FILE)}</code>" + ("" if CONFIG_FILE.exists() else "（未创建，使用默认值）"))),
    ])
    st.caption("如需把数据放到其他磁盘（例如 D:\\ResearchData），复制 config/settings.example.toml 为 config/settings.toml 并修改 "
               "data_dir / backup_dir，或设置环境变量 RCC_DATA_DIR / RCC_BACKUP_DIR，然后重启应用。")

with t_backup:
    last = get_meta("last_backup_at")
    st.markdown(f"最近一次备份：**{(last or '尚无').replace('T', ' ')}** · 自动备份间隔：{s.auto_backup_hours:g} 小时 · "
                f"自动备份保留最近 {s.backup_keep} 份（手动备份与恢复前备份不会被自动清理）")
    if info.get("auto_backup"):
        st.caption(f"本次启动已自动备份：{Path(info['auto_backup']).name}")
    c1, c2 = st.columns([1, 3])
    if c1.button("立即备份", type="primary", width="stretch"):
        try:
            p = backup.backup_database("manual")
            run_action(lambda: None, success=f"备份完成：{p.name}")
        except ValidationError as e:
            show_errors(e)
    bl = backup.list_backups()
    if not bl:
        st.caption("暂无备份。")
    else:
        kind_lbl = {"auto": "自动", "manual": "手动", "pre-restore": "恢复前", "scheduled": "定时"}
        df = pd.DataFrame([{"时间": b["created"], "类型": kind_lbl.get(b["kind"], b["kind"]), "大小": human_size(b["size"]),
                            "文件": b["name"]} for b in bl])
        st.dataframe(placeholder="—", data=df, hide_index=True, width="stretch",
                     column_config={"时间": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm:ss")})
        st.markdown("**从备份恢复**")
        st.caption("恢复会用所选备份覆盖当前数据库。系统会先自动为当前数据库做一次“恢复前备份”，因此可以撤销。")
        choice = st.selectbox("选择备份", [b["path"] for b in bl], format_func=lambda p: Path(p).name, key="rs_choice")
        okv, msg = backup.verify_backup(choice)
        st.caption("完整性检查：" + ("通过" if okv else f"失败（{msg}）"))
        if confirm_button("恢复所选备份", key="rs_go", confirm_text="我了解当前数据将被替换（已自动保留恢复前备份）",
                          type="primary"):
            try:
                pre = backup.restore_database(choice)
                run_action(lambda: None, success=f"已恢复。恢复前备份：{Path(pre).name}")
            except ValidationError as e:
                show_errors(e)
    st.divider()
    st.markdown("**导出全部数据为 Excel**（每张表一个工作表，便于长期留存或迁移）")
    if st.button("生成 Excel 导出"):
        out = s.data_dir / "exports" / f"research_export_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
        backup.export_excel(out)
        st.session_state["export_path"] = str(out)
    if st.session_state.get("export_path"):
        p = Path(st.session_state["export_path"])
        if p.exists():
            st.download_button("下载导出文件", p.read_bytes(), file_name=p.name,
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            st.caption(f"已保存到：{p}")

with t_exec:
    st.markdown("**本机脚本执行（生信分析第二阶段功能）**")
    st.caption("默认关闭。开启后，也只能执行已在“生信分析”中登记的 .R / .py 脚本；每次执行前都会展示完整命令、输入文件与输出路径，"
               "并要求您确认。系统不会自动执行任何脚本。")
    cur = app_settings.allow_script_execution()
    new = st.toggle("允许执行已登记的 R / Python 脚本", value=cur, key="exec_toggle")
    if new != cur:
        app_settings.set_allow_script_execution(new)
        run_action(lambda: None, success="已开启脚本执行" if new else "已关闭脚本执行")
    with st.form("interp", border=False):
        c1, c2, c3 = st.columns([3, 3, 1])
        py = c1.text_input("Python 解释器路径", app_settings.python_interpreter() or "", key="int_py",
                           help="留空则自动查找 PATH 中的 python")
        rs = c2.text_input("Rscript 路径", app_settings.rscript_interpreter() or "", key="int_r",
                           help=r"例如 C:\Program Files\R\R-4.4.1\bin\Rscript.exe")
        to = c3.number_input("超时（分钟）", 1, 10080, app_settings.script_timeout_minutes(), key="int_to")
        if st.form_submit_button("保存"):
            try:
                app_settings.set_interpreters(py or None, rs or None)
                app_settings.set_script_timeout_minutes(to)
                run_action(lambda: None, success="已保存")
            except ValidationError as e:
                show_errors(e)

with t_log:
    rows = activity.recent(300)
    if rows:
        df = pd.DataFrame([{"时间": r["created_at"], "对象": r["entity_type"], "编号": r["entity_id"], "操作": r["action"],
                            "摘要": r["summary"]} for r in rows])
        st.dataframe(placeholder="—", data=df, hide_index=True, width="stretch",
                     column_config={"时间": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm:ss")})
    else:
        st.caption("暂无操作记录。")

with t_about:
    st.markdown(
        f"**Personal Research Command Center** v{__version__}\n\n"
        "- **深色模式**：点击右上角 **⋮**，在菜单中选择 **Light（浅色）/ Dark（深色）/ System（跟随系统）**；选择会被浏览器记住。"
        "默认跟随操作系统（Windows 默认浅色模式下即为浅色）。\n"
        "- **关闭应用**：关闭启动时打开的命令行窗口，或在其中按 `Ctrl + C`；也可运行 `stop.bat`（Windows）/ `./stop.sh`。\n"
        "- **数据安全**：应用只监听本机 127.0.0.1；不会上传文献或实验数据；在线比对和 AI 调用只在您点击并确认时进行。\n"
        "- **原始文件**：所有文件只以绝对路径引用，系统从不修改、移动或删除原始科研文件。")
