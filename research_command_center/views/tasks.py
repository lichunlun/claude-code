"""任务管理：列表与筛选、状态流转、四象限、逾期。"""
from __future__ import annotations

from typing import Optional

import pandas as pd
import streamlit as st

from rcc.constants import (
    QUADRANTS,
    TASK_OPEN_STATUSES,
    TASK_PRIORITIES,
    TASK_STATUSES,
    URGENT_WITHIN_DAYS,
    label,
)
from rcc.services import projects, tasks
from rcc.ui.common import (
    is_repeat_submit,
    mark_submit_done,
    bootstrap,
    code_select,
    confirm_button,
    due_text,
    empty_state,
    esc,
    fmt_dt,
    html_block,
    kv_block,
    page_header,
    project_selector,
    run_action,
    select_row,
    show_errors,
    show_flash,
    tag,
)
from rcc.utils import ValidationError

bootstrap()
show_flash()

TRI = {"auto": "自动判断", True: "是", False: "否"}


@st.dialog("任务", width="large")
def task_dialog(task_id: Optional[int] = None, project_id: Optional[int] = None) -> None:
    t = tasks.get_task(task_id) or {"project_id": project_id}
    k = f"tf{task_id or 'new'}_"
    with st.form(f"{k}form", border=False):
        title = st.text_input("任务名称 *", t.get("title") or "", key=k + "title")
        c1, c2 = st.columns(2)
        with c1:
            pid = project_selector("所属项目", key=k + "proj", current=t.get("project_id"))
        with c2:
            pr = code_select("优先级", "task_priority", TASK_PRIORITIES, key=k + "pr", current=t.get("priority") or "Medium")
        c3, c4, c5 = st.columns(3)
        with c3:
            status = code_select("状态", "task_status", TASK_STATUSES, key=k + "st", current=t.get("status") or "Todo")
        due = c4.date_input("截止日期", value=t.get("due_date"), format="YYYY-MM-DD", key=k + "due")
        hours = c5.number_input("预计耗时（小时）", min_value=0.0, max_value=10000.0, step=0.5,
                                value=t.get("estimated_hours"), placeholder="可留空", key=k + "hours")
        c6, c7 = st.columns(2)
        imp_opts = ["auto", True, False]
        imp = c6.selectbox("重要性（四象限）", imp_opts, format_func=lambda x: TRI[x], key=k + "imp",
                           index=imp_opts.index(t.get("is_important")) if t.get("is_important") is not None else 0,
                           help="自动：Critical / High 视为重要")
        urg = c7.selectbox("紧急性（四象限）", imp_opts, format_func=lambda x: TRI[x], key=k + "urg",
                           index=imp_opts.index(t.get("is_urgent")) if t.get("is_urgent") is not None else 0,
                           help=f"自动：截止日期在 {URGENT_WITHIN_DAYS} 天内（含已逾期）视为紧急")
        notes = st.text_area("备注", t.get("notes") or "", height=100, key=k + "notes")
        submitted = st.form_submit_button("保存", type="primary")
    if submitted:
        data = {"title": title, "project_id": pid, "priority": pr, "status": status, "due_date": due,
                "estimated_hours": hours, "is_important": imp, "is_urgent": urg, "notes": notes}
        if not task_id and is_repeat_submit(k, data):
            st.rerun()
        try:
            if task_id:
                tasks.update_task(task_id, data)
            else:
                tasks.create_task(data)
                mark_submit_done(k, data)
            st.session_state.setdefault("_rcc_flash", []).append(("任务已保存", "✅"))
            st.rerun()
        except ValidationError as e:
            show_errors(e)


page_header("任务管理", "跨项目任务：优先级、截止日期、状态流转与四象限。")
names = projects.project_name_map()
if st.button("新建任务", type="primary", icon=":material/add:"):
    task_dialog()

tab_list, tab_quad, tab_overdue = st.tabs(["任务列表", "四象限", "逾期任务"])

with tab_list:
    f1, f2, f3 = st.columns([3, 3, 2])
    proj_opts = [None] + list(names.keys())
    sel_proj = f1.multiselect("项目", proj_opts, format_func=lambda x: "（无项目）" if x is None else names.get(x, x),
                              key="tl_proj", placeholder="全部项目")
    sel_pr = f2.multiselect("优先级", TASK_PRIORITIES, key="tl_pr", placeholder="全部优先级")
    search = f3.text_input("搜索", key="tl_q", placeholder="任务名称或备注")
    g0, g1, g2 = st.columns([4, 2, 2], vertical_alignment="bottom")
    with g0:
        sel_st = st.pills("状态（可多选）", TASK_STATUSES, selection_mode="multi", default=TASK_OPEN_STATUSES,
                          format_func=lambda x: label("task_status", x), key="tl_st")
    d_from = g1.date_input("截止日期从", value=None, key="tl_from")
    d_to = g2.date_input("截止日期至", value=None, key="tl_to")
    rows = tasks.list_tasks(project_ids=sel_proj or None, statuses=sel_st or None, priorities=sel_pr or None,
                            due_from=d_from, due_to=d_to, search=search or None)
    st.caption(f"共 {len(rows)} 项" + (f"，其中 {sum(r['is_overdue'] for r in rows)} 项已逾期" if any(r["is_overdue"] for r in rows) else ""))
    if not rows:
        empty_state("没有符合条件的任务。")
    else:
        df = pd.DataFrame([{
            "id": r["id"], "任务": r["title"], "项目": names.get(r["project_id"], "—") if r["project_id"] else "—",
            "优先级": r["priority"], "状态": label("task_status", r["status"]), "截止日期": r["due_date"],
            "提醒": "已逾期" if r["is_overdue"] else "", "预计耗时(h)": r["estimated_hours"],
            "象限": QUADRANTS[r["quadrant"]],
        } for r in rows])
        sel = select_row(df, key="tl_table", column_config={
            "截止日期": st.column_config.DateColumn(format="YYYY-MM-DD"),
            "预计耗时(h)": st.column_config.NumberColumn(format="%.1f"),
        })
        if sel is None:
            st.caption("在表格中选择一行以查看详情、修改状态或编辑。")
        else:
            t = tasks.get_task(sel)
            if t:
                with st.container(border=True):
                    st.subheader(t["title"])
                    a, b = st.columns([3, 2], gap="large")
                    with a:
                        kv_block([
                            ("所属项目", names.get(t["project_id"]) if t["project_id"] else None),
                            ("优先级", t["priority"]),
                            ("状态", label("task_status", t["status"])),
                            ("截止日期", due_text(t["due_date"]) or None),
                            ("预计耗时", f"{t['estimated_hours']:g} 小时" if t["estimated_hours"] is not None else None),
                            ("备注", t["notes"]),
                            ("开始于", fmt_dt(t["started_at"]) or None),
                            ("完成于", fmt_dt(t["completed_at"]) or None),
                        ])
                    with b:
                        st.markdown("**更改状态**")
                        bc = st.columns(2)
                        for i, s in enumerate([x for x in TASK_STATUSES if x != t["status"]]):
                            if bc[i % 2].button(label("task_status", s), key=f"ts_{t['id']}_{s}", width="stretch",
                                                type="primary" if s == "Done" else "secondary"):
                                run_action(tasks.set_status, t["id"], s, success=f"状态已改为：{label('task_status', s)}")
                        st.divider()
                        if st.button("编辑任务", key=f"te_{t['id']}", width="stretch", icon=":material/edit:"):
                            task_dialog(t["id"])
                        with st.popover("删除任务", width="stretch"):
                            if confirm_button("删除", key=f"td_{t['id']}", confirm_text="确认删除此任务"):
                                run_action(tasks.delete_task, t["id"], success="任务已删除")

with tab_quad:
    st.caption(f"规则：重要 = Critical / High（可在任务中手动覆盖）；紧急 = 截止日期在 {URGENT_WITHIN_DAYS} 天内或已逾期（可手动覆盖）。"
               "仅显示未完成任务。")
    open_rows = tasks.list_tasks(statuses=TASK_OPEN_STATUSES)
    grid = [st.columns(2, gap="medium"), st.columns(2, gap="medium")]
    pos = {"Q1": grid[0][0], "Q2": grid[0][1], "Q3": grid[1][0], "Q4": grid[1][1]}
    for q, col in pos.items():
        items = sorted([r for r in open_rows if r["quadrant"] == q], key=lambda r: -r["score"])
        with col:
            with st.container(border=True, height=330):
                st.markdown(f"**{QUADRANTS[q]}** · {len(items)}")
                if not items:
                    st.caption("—")
                html_block("".join(
                    f'<div class="rcc-item"><div class="t">{esc(r["title"])}{tag(r["priority"])}</div>'
                    f'<div class="m">{esc(names.get(r["project_id"], "无项目") if r["project_id"] else "无项目")}'
                    f' · {esc(due_text(r["due_date"]) or "未设截止日期")}</div></div>' for r in items))

with tab_overdue:
    od = [r for r in tasks.list_tasks(statuses=TASK_OPEN_STATUSES) if r["is_overdue"]]
    if not od:
        empty_state("没有逾期任务。")
    else:
        df = pd.DataFrame([{
            "id": r["id"], "任务": r["title"], "项目": names.get(r["project_id"], "—") if r["project_id"] else "—",
            "优先级": r["priority"], "状态": label("task_status", r["status"]), "截止日期": r["due_date"],
            "逾期": due_text(r["due_date"]),
        } for r in sorted(od, key=lambda r: r["due_date"])])
        st.dataframe(placeholder="—", data=df, hide_index=True, column_order=[c for c in df.columns if c != "id"], width="stretch",
                     column_config={"截止日期": st.column_config.DateColumn(format="YYYY-MM-DD")})
