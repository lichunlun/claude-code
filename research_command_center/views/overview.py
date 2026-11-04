"""首页：Research Overview。"""
from __future__ import annotations

from datetime import timedelta

import streamlit as st

from rcc.constants import CAL_SOURCE_LABELS, label
from rcc.services import calendar, literature, overview, projects, publications, tasks
from rcc.ui import calendar_view, charts
from rcc.ui.common import (bootstrap, due_text, empty_state, esc, fmt_dt, html_block, nav_link, page_header, run_action,
                           show_flash, tag)
from rcc.utils import today

bootstrap()
show_flash()

t = today()
WEEK = "一二三四五六日"
page_header("Research Overview", f"{t:%Y 年 %m 月 %d 日} 星期{WEEK[t.weekday()]} · 所有数字均来自本地数据库实时统计")

c = overview.summary_counts()
m = st.columns(5)
m[0].metric("进行中的项目", c["active_projects"], border=True, height=128,
            help=f"未归档项目共 {c['projects_total']} 个，其中 {c['projects_status_unknown']} 个状态待填写")
m[1].metric("已发表论文", c["published"], border=True, height=128, help="投稿状态为 Published 的论文")
m[2].metric("投稿中论文", c["in_submission"], border=True, height=128,
            help="状态为 Submitted / Editor Assigned / Under Review / Revision 的论文"
                 + (f"；另有 {c['pubs_unconfirmed']} 篇状态待您确认" if c["pubs_unconfirmed"] else ""))
m[3].metric("待完成实验", c["pending_experiments"], border=True, height=128, help="状态为“待开展”或“进行中”的实验")
m[4].metric("待处理任务", c["open_tasks"], border=True, height=128,
            delta=f"逾期 {c['overdue_tasks']}" if c["overdue_tasks"] else None, delta_color="inverse",
            delta_arrow="off", help="待办 + 进行中 + 受阻")

notes = []
if c["pubs_unconfirmed"]:
    notes.append(f"{c['pubs_unconfirmed']} 篇论文的投稿状态待您确认")
if c["projects_status_unknown"]:
    notes.append(f"{c['projects_status_unknown']} 个项目的状态待填写")
if notes:
    st.caption("待确认：" + "；".join(notes) + "。系统不会自动推断这些信息。")

left, right = st.columns([3, 2], gap="medium")
with left:
    with st.container(border=True):
        st.subheader("当前最重要的三个任务")
        top = tasks.top_tasks(3)
        if not top:
            empty_state("暂无未完成任务。", "在“任务管理”中新建任务后，这里会按优先级与截止日期自动排序。")
        names = projects.project_name_map()
        for tk in top:
            a, b = st.columns([5, 1], vertical_alignment="center")
            pr_kind = "danger" if tk["priority"] == "Critical" else "accent" if tk["priority"] == "High" else ""
            meta = []
            if tk.get("project_id"):
                meta.append(esc(names.get(tk["project_id"], "")))
            if tk.get("due_date"):
                meta.append(("<b>" if tk["is_overdue"] else "") + esc(due_text(tk["due_date"])) + ("</b>" if tk["is_overdue"] else ""))
            else:
                meta.append("未设截止日期")
            a.html(f'<div class="rcc-item"><div class="t">{esc(tk["title"])}{tag(tk["priority"], pr_kind)}'
                   f'{tag(label("task_status", tk["status"]))}</div><div class="m">{" · ".join(meta)}</div></div>')
            if b.button("完成", key=f"done_{tk['id']}", width="stretch", help="标记为已完成"):
                run_action(tasks.set_status, tk["id"], "Done", success="任务已完成")
        st.caption("排序规则：优先级权重 × 10 + 截止紧迫度（逾期 +15，今天 +12，3 天内 +8，7 天内 +4）。")

with right:
    with st.container(border=True):
        st.subheader("近期重要截止日期")
        items = calendar.upcoming(30)
        if not items:
            empty_state("未来 30 天没有登记的截止事项。", "任务截止、实验日期、修改期限、里程碑与日程都会汇总到这里。")
        html_items = []
        def _short(x, n=14):
            return x if not x or len(x) <= n else x[: n - 1] + "…"

        for e in items[:6]:
            dot = "danger" if e.get("overdue") else "warn" if e["source"] == "publication" else ""
            html_items.append(
                f'<div class="rcc-item"><div class="t"><span class="rcc-dot {dot}"></span>{esc(e["title"])}</div>'
                f'<div class="m">{esc(due_text(e["date"]))} · {esc(CAL_SOURCE_LABELS.get(e["source"], ""))}'
                f'{(" · " + esc(_short(e["project"]))) if e.get("project") else ""}</div></div>')
        if html_items:
            html_block("".join(html_items))
        if len(items) > 6:
            nav_link("views/calendar.py", f"查看全部 {len(items)} 项")

with st.container(border=True):
    st.subheader("可视化")
    t1, t2, t3, t4, t5 = st.tabs(["项目进度", "每周任务", "投稿状态", "任务优先级", "未来 30 天"])
    with t1:
        rows = overview.project_progress()
        if rows:
            st.plotly_chart(charts.project_progress(rows), config={"displayModeBar": False}, key="ch_prog")
            unknown = sum(1 for r in rows if r["progress"] is None)
            if unknown:
                st.caption(f"{unknown} 个项目的完成进度待填写（不会自动估算）。")
        else:
            empty_state("暂无项目。")
    with t2:
        wk = tasks.weekly_completion(8)
        if any(r["created"] or r["completed"] for r in wk):
            st.plotly_chart(charts.weekly_tasks(wk), config={"displayModeBar": False}, key="ch_week")
            st.caption("横轴为每周周一日期；“完成”按任务实际标记完成的时间统计。")
        else:
            empty_state("最近 8 周没有新建或完成的任务。")
    with t3:
        counts = publications.status_counts()
        if sum(counts.values()):
            st.plotly_chart(charts.publication_status(counts, publications.ALL_ORDER), config={"displayModeBar": False},
                            key="ch_pub")
            st.caption("按投稿流程顺序排列；状态均为手动确认，不根据日期推断。")
        else:
            empty_state("暂无论文记录。")
    with t4:
        dist = overview.task_priority_distribution()
        if sum(dist.values()):
            st.plotly_chart(charts.priority_distribution(dist), config={"displayModeBar": False}, key="ch_pri")
            st.caption("仅统计未完成任务（待办 / 进行中 / 受阻）。")
        else:
            empty_state("暂无未完成任务。")
    with t5:
        evs = calendar.aggregate(t, t + timedelta(days=29), include_done=False)
        calendar_view.compact_window(t, 30, evs)
        st.caption("格内数字为当天未完成事项数，颜色越深事项越多；鼠标悬停查看详情。")

l2, r2 = st.columns(2, gap="medium")
with l2:
    with st.container(border=True):
        st.subheader("最近新增文献")
        lits = literature.recent_literature(5)
        if not lits:
            empty_state("文献库为空。", "在“文献库 → 导入 PDF”中导入本地 PDF。")
        html_block("".join(
            f'<div class="rcc-item"><div class="t">{esc(x["title"] or "（标题待核实）")}'
            f'{tag(label("verification", x["verification_status"]), "warn" if x["verification_status"] != "Verified" else "accent")}</div>'
            f'<div class="m">{esc(x["journal"] or "期刊待核实")} · {esc(x["year"] or "年份待核实")} · 添加于 {esc(fmt_dt(x["created_at"]))}</div></div>'
            for x in lits))
with r2:
    with st.container(border=True):
        st.subheader("最近更新的项目")
        ps = overview.recent_projects(5)
        if not ps:
            empty_state("暂无项目。")
        html_block("".join(
            f'<div class="rcc-item"><div class="t">{esc(p["name"])}{tag(label("project_status", p["status"]))}</div>'
            f'<div class="m">更新于 {esc(fmt_dt(p["updated_at"]))} · 进度 {esc(str(p["progress"]) + "%" if p["progress"] is not None else "待填写")}</div></div>'
            for p in ps))
