"""Personal Research Command Center —— 入口。

启动：  Windows 双击 start.bat；macOS/Linux 运行 ./start.sh
或：    python -m streamlit run app.py
"""
from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="Research Command Center",
    page_icon=":material/biotech:",
    layout="wide",
    initial_sidebar_state="expanded",
)

from rcc import __version__  # noqa: E402
from rcc.config import get_settings  # noqa: E402
from rcc.db import get_meta  # noqa: E402
from rcc.ui.common import bootstrap, esc  # noqa: E402
from rcc.ui.theme import inject_css  # noqa: E402

info = bootstrap()
inject_css()

pages = {
    "总览": [
        st.Page("views/overview.py", title="首页", icon=":material/space_dashboard:", default=True),
    ],
    "科研工作": [
        st.Page("views/projects.py", title="科研项目", icon=":material/folder_open:"),
        st.Page("views/tasks.py", title="任务管理", icon=":material/checklist:"),
        st.Page("views/experiments.py", title="实验记录", icon=":material/science:"),
        st.Page("views/bioinfo.py", title="生信分析", icon=":material/terminal:"),
    ],
    "知识与成果": [
        st.Page("views/literature.py", title="文献库", icon=":material/menu_book:"),
        st.Page("views/publications.py", title="论文投稿", icon=":material/send:"),
    ],
    "规划": [
        st.Page("views/calendar.py", title="日历与时间线", icon=":material/calendar_month:"),
    ],
    "工具": [
        st.Page("views/ai_assistant.py", title="AI 科研助手", icon=":material/psychology:"),
        st.Page("views/files.py", title="文件中心", icon=":material/description:"),
        st.Page("views/settings.py", title="设置与备份", icon=":material/settings:"),
    ],
}
pg = st.navigation(pages, position="sidebar")

with st.sidebar:
    s = get_settings()
    last_backup = get_meta("last_backup_at")
    st.html(
        '<div class="rcc-small" style="margin-top:1.2rem;line-height:1.6">'
        f"Research Command Center v{__version__}<br>"
        f"数据库：<code>{esc(s.db_path.name)}</code>（本地）<br>"
        f"最近备份：{esc(last_backup.replace('T', ' ') if last_backup else '尚无')}"
        "</div>"
    )

pg.run()
