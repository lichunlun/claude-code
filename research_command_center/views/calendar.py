"""日历与科研时间线：月视图、周视图、近期事件；整合实验、投稿期限、修改期限、里程碑、考试、会议与目标。"""
from __future__ import annotations

import calendar as pycal
from datetime import date, timedelta
from typing import Optional

import pandas as pd
import streamlit as st

from rcc.constants import CAL_SOURCE_LABELS, EVENT_TYPES, label
from rcc.services import calendar, projects
from rcc.ui import calendar_view
from rcc.ui.common import (
    is_repeat_submit,
    mark_submit_done,
    bootstrap,
    code_select,
    confirm_button,
    due_text,
    empty_state,
    page_header,
    project_selector,
    run_action,
    select_row,
    show_errors,
    show_flash,
)
from rcc.utils import ValidationError, today, week_start

bootstrap()
show_flash()
names = projects.project_name_map()


@st.dialog("日程", width="large")
def event_dialog(event_id: Optional[int] = None) -> None:
    e = next((x for x in calendar.list_events() if x["id"] == event_id), {}) if event_id else {}
    k = f"cf{event_id or 'new'}_"
    with st.form(k + "form", border=False):
        title = st.text_input("名称 *", e.get("title") or "", key=k + "title")
        c1, c2 = st.columns(2)
        with c1:
            et = code_select("类型", "event_type", EVENT_TYPES, key=k + "type", current=e.get("event_type") or "other")
        with c2:
            pid = project_selector("关联项目", key=k + "proj", current=e.get("project_id"))
        c3, c4 = st.columns(2)
        sd = c3.date_input("开始日期 *", value=e.get("start_date") or today(), key=k + "sd")
        ed = c4.date_input("结束日期（可选）", value=e.get("end_date"), key=k + "ed")
        loc = st.text_input("地点", e.get("location") or "", key=k + "loc")
        desc = st.text_area("说明", e.get("description") or "", height=80, key=k + "desc")
        done = st.checkbox("已完成 / 已结束", value=bool(e.get("is_done")), key=k + "done")
        if st.form_submit_button("保存", type="primary"):
            data = {"title": title, "event_type": et, "project_id": pid, "start_date": sd, "end_date": ed,
                    "location": loc, "description": desc, "is_done": done}
            if not event_id and is_repeat_submit(k, data):
                st.rerun()
            try:
                if event_id:
                    calendar.update_event(event_id, data)
                else:
                    calendar.create_event(data)
                    mark_submit_done(k, data)
                st.session_state.setdefault("_rcc_flash", []).append(("日程已保存", "✅"))
                st.rerun()
            except ValidationError as ex:
                show_errors(ex)


page_header("日历与时间线", "整合任务截止、实验日期、投稿/修改期限、项目里程碑，以及考试、会议、个人科研目标。")
if st.button("新建日程", type="primary", icon=":material/add:"):
    event_dialog()

ss = st.session_state
ss.setdefault("cal_anchor", today())
c1, c2, c3 = st.columns([2, 3, 3])
view = c1.segmented_control("视图", ["月视图", "周视图", "近期列表"], default="月视图", key="cal_view")
src_f = c2.multiselect("事件来源", list(CAL_SOURCE_LABELS.keys()), format_func=lambda x: CAL_SOURCE_LABELS[x],
                       key="cal_src", placeholder="全部来源")
proj_f = c3.multiselect("项目", list(names.keys()), format_func=lambda x: names[x], key="cal_proj", placeholder="全部项目")
anchor: date = ss["cal_anchor"]

if view in (None, "月视图", "周视图"):
    step_month = view in (None, "月视图")
    a, b, c, d_ = st.columns([1, 1, 1, 5], vertical_alignment="center")
    if a.button("‹ 上一" + ("月" if step_month else "周"), key="cal_prev"):
        if step_month:
            first = anchor.replace(day=1)
            ss["cal_anchor"] = (first - timedelta(days=1)).replace(day=1)
        else:
            ss["cal_anchor"] = anchor - timedelta(days=7)
        st.rerun()
    if b.button("今天", key="cal_today"):
        ss["cal_anchor"] = today()
        st.rerun()
    if c.button("下一" + ("月" if step_month else "周") + " ›", key="cal_next"):
        if step_month:
            last = anchor.replace(day=pycal.monthrange(anchor.year, anchor.month)[1])
            ss["cal_anchor"] = last + timedelta(days=1)
        else:
            ss["cal_anchor"] = anchor + timedelta(days=7)
        st.rerun()
    if step_month:
        d_.markdown(f"**{anchor.year} 年 {anchor.month} 月**")
        first = anchor.replace(day=1)
        last = anchor.replace(day=pycal.monthrange(anchor.year, anchor.month)[1])
        evs = calendar.aggregate(first - timedelta(days=7), last + timedelta(days=7), proj_f or None, src_f or None)
        calendar_view.month_view(anchor.year, anchor.month, evs)
    else:
        ws = week_start(anchor)
        d_.markdown(f"**{ws:%Y-%m-%d} 至 {(ws + timedelta(days=6)):%Y-%m-%d}**")
        evs = calendar.aggregate(ws, ws + timedelta(days=6), proj_f or None, src_f or None)
        calendar_view.week_view(ws, evs)
    st.caption("圆点颜色：蓝 = 一般事项，橙 = 投稿/修改期限，红 = 已逾期，灰 = 项目节点/分析运行；划线 = 已完成。悬停可看详情。")
else:
    days = st.slider("显示未来天数", 7, 180, 60, step=7, key="cal_days")
    items = calendar.aggregate(today(), today() + timedelta(days=days), proj_f or None, src_f or None, include_done=False)
    overdue = [e for e in calendar.upcoming(0) if e.get("overdue")]
    if proj_f:
        overdue = [e for e in overdue if e["project_id"] in proj_f]
    if src_f:
        overdue = [e for e in overdue if e["source"] in src_f]
    allitems = overdue + items
    if not allitems:
        empty_state("这段时间内没有未完成的事项。")
    else:
        df = pd.DataFrame([{
            "日期": e["date"], "距今": due_text(e["date"]).split("（")[-1].rstrip("）"), "事项": e["title"],
            "来源": CAL_SOURCE_LABELS.get(e["source"], e["source"]), "项目": e.get("project") or "—",
        } for e in allitems])
        st.dataframe(placeholder="—", data=df, hide_index=True, width="stretch",
                     column_config={"日期": st.column_config.DateColumn(format="YYYY-MM-DD")})

st.divider()
st.subheader("我的日程")
st.caption("考试、会议、个人科研目标等独立日程。任务、实验、投稿期限请在各自模块中维护，会自动汇总到日历。")
evs = calendar.list_events()
if not evs:
    empty_state("暂无日程。")
else:
    df = pd.DataFrame([{"id": e["id"], "日期": e["start_date"], "结束": e["end_date"], "名称": e["title"],
                        "类型": label("event_type", e["event_type"]), "项目": names.get(e["project_id"], "—") if e["project_id"] else "—",
                        "地点": e["location"], "已完成": "是" if e["is_done"] else ""} for e in evs])
    sel = select_row(df, "ev_table", column_config={"日期": st.column_config.DateColumn(format="YYYY-MM-DD"),
                                                   "结束": st.column_config.DateColumn(format="YYYY-MM-DD")})
    if sel:
        c1, c2, _ = st.columns([1, 1, 4])
        if c1.button("编辑", key=f"eve_{sel}", width="stretch"):
            event_dialog(sel)
        with c2.popover("删除", width="stretch"):
            if confirm_button("删除日程", key=f"evd_{sel}", confirm_text="确认删除"):
                run_action(calendar.delete_event, sel, success="日程已删除")
