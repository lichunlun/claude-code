"""论文投稿管理：全生命周期、用户确认的状态变更、状态历史。"""
from __future__ import annotations

from datetime import date
from typing import Optional

import pandas as pd
import streamlit as st

from rcc.constants import PUB_PIPELINE, PUB_SIDE_STATUSES, PUB_STATUSES, PUB_UNCONFIRMED, label
from rcc.services import projects, publications
from rcc.ui.common import (
    is_repeat_submit,
    mark_submit_done,
    bootstrap,
    confirm_button,
    due_text,
    empty_state,
    esc,
    fmt_date,
    kv_block,
    page_header,
    project_selector,
    raw,
    render_paths,
    run_action,
    select_row,
    show_errors,
    show_flash,
    tag,
)
from rcc.utils import ValidationError

bootstrap()
show_flash()
names = projects.project_name_map()
D_MIN, D_MAX = date(1990, 1, 1), date(2100, 12, 31)


@st.dialog("论文信息", width="large")
def pub_dialog(pub_id: Optional[int] = None) -> None:
    p = publications.get_publication(pub_id) or {}
    k = f"pb{pub_id or 'new'}_"
    with st.form(k + "form", border=False):
        title = st.text_area("论文标题 *", p.get("title") or "", height=68, key=k + "title")
        c1, c2 = st.columns(2)
        with c1:
            pid = project_selector("所属项目", key=k + "proj", current=p.get("project_id"))
        journal = c2.text_input("目标期刊", p.get("target_journal") or "", key=k + "journal")
        authors = st.text_area("作者排序", p.get("author_order") or "", height=68, key=k + "authors")
        c3, c4 = st.columns(2)
        first = c3.text_input("第一作者", p.get("first_author") or "", key=k + "first")
        corr = c4.text_input("通讯作者", p.get("corresponding_author") or "", key=k + "corr")
        if not pub_id:
            init_opts = [s for s in PUB_STATUSES if s != PUB_UNCONFIRMED]
            status = st.selectbox("当前状态（请如实选择）", init_opts, format_func=lambda x: label("pub_status", x),
                                  key=k + "status")
        st.markdown("关键日期（可留空；系统不会根据日期推断状态）")
        d = {}
        cols = st.columns(4)
        for i, (f, lbl) in enumerate(publications.DATE_FIELDS.items()):
            d[f] = cols[i % 4].date_input(lbl, value=p.get(f), min_value=D_MIN, max_value=D_MAX, key=k + f)
        url = st.text_input("投稿系统链接", p.get("submission_url") or "", key=k + "url", placeholder="https://")
        paths = st.text_area("相关文件路径（每行一个）", p.get("file_paths") or "", height=68, key=k + "paths")
        nxt = st.text_area("下一步行动", p.get("next_action") or "", height=68, key=k + "next")
        notes = st.text_area("备注", p.get("notes") or "", height=68, key=k + "notes")
        src = st.text_area("信息来源说明", p.get("source_note") or "", height=68, key=k + "src")
        submitted = st.form_submit_button("保存", type="primary")
    if submitted:
        data = {"title": title, "project_id": pid, "target_journal": journal, "author_order": authors,
                "first_author": first, "corresponding_author": corr, "submission_url": url, "file_paths": paths,
                "next_action": nxt, "notes": notes, "source_note": src, **d}
        if not pub_id:
            data["status"] = status
            if is_repeat_submit(k, data):
                st.rerun()
        try:
            if pub_id:
                publications.update_publication(pub_id, data)
            else:
                publications.create_publication(data)
                mark_submit_done(k, data)
            st.session_state.setdefault("_rcc_flash", []).append(("论文信息已保存", "✅"))
            st.rerun()
        except ValidationError as e:
            show_errors(e)


def status_panel(p: dict) -> None:
    st.markdown("**确认状态变更**")
    opts = [s for s in PUB_STATUSES if s not in (p["status"], PUB_UNCONFIRMED)]
    k = f"sc{p['id']}_"
    new = st.selectbox("新状态", opts, format_func=lambda x: label("pub_status", x), key=k + "new")
    c1, c2 = st.columns(2)
    ev = c1.date_input("该状态发生的日期", value=None, min_value=D_MIN, max_value=D_MAX, key=k + "date",
                       help="例如收到编辑分配邮件的日期；可留空")
    journal = c2.text_input("期刊（转投时必填）", value="" if new == "Transferred" else (p.get("target_journal") or ""),
                            key=k + f"journal_{new}")
    note = st.text_input("备注（例如邮件主题、稿件编号）", key=k + "note")
    warn = publications.transition_warning(p["status"], new)
    if warn:
        st.warning(warn)
    ok = st.checkbox("我确认该状态变更已真实发生（系统不会根据日期自动推断投稿状态）", key=k + "ok")
    if st.button("确认变更", type="primary", disabled=not ok, key=k + "go"):
        run_action(publications.change_status, p["id"], new, ok, ev, note, journal or None,
                   success=f"状态已更新为：{label('pub_status', new)}")


def render_detail(pub_id: int) -> None:
    p = publications.get_publication(pub_id)
    if not p:
        return
    with st.container(border=True):
        st.subheader(p["title"])
        kind = "warn" if p["status"] == PUB_UNCONFIRMED else "accent"
        st.html(f'<div style="margin:-.4rem 0 .4rem -.35rem">{tag(label("pub_status", p["status"]), kind)}</div>')
        if p["status"] == PUB_UNCONFIRMED:
            st.info("该论文的投稿状态尚未经您确认。请在右侧“确认状态变更”中选择真实状态。", icon="ℹ️")
        a, b = st.columns([3, 2], gap="large")
        with a:
            kv_block([
                ("所属项目", names.get(p["project_id"]) if p["project_id"] else None),
                ("目标期刊", p["target_journal"]), ("作者排序", p["author_order"]),
                ("第一作者", p["first_author"]), ("通讯作者", p["corresponding_author"]),
                *[(lbl, fmt_date(p[f]) or None) for f, lbl in publications.DATE_FIELDS.items()],
                ("修改期限提醒", due_text(p["revision_due_date"]) if p["revision_due_date"] and p["status"] == "Revision" else None),
                ("投稿系统", raw(f'<a href="{esc(p["submission_url"])}" target="_blank">{esc(p["submission_url"])}</a>')
                 if p.get("submission_url") else None),
                ("相关文件", raw(render_paths(p["file_paths"]))),
                ("下一步行动", p["next_action"]), ("备注", p["notes"]), ("信息来源", p["source_note"]),
            ])
        with b:
            status_panel(p)
            st.divider()
            c1, c2 = st.columns(2)
            if c1.button("编辑信息", key=f"pe_{pub_id}", width="stretch", icon=":material/edit:"):
                pub_dialog(pub_id)
            with c2.popover("删除记录", width="stretch"):
                st.write("只删除数据库记录及状态历史，不删除任何文件。")
                if confirm_button("删除", key=f"pdel_{pub_id}", confirm_text="确认删除"):
                    run_action(publications.delete_publication, pub_id, success="论文记录已删除")
        st.markdown("**状态历史**")
        hist = publications.history(pub_id)
        df = pd.DataFrame([{"记录时间": h["recorded_at"], "事件日期": h["event_date"],
                            "从": label("pub_status", h["from_status"], empty="—"), "到": label("pub_status", h["to_status"]),
                            "期刊": h["journal"], "用户确认": "是" if h["confirmed_by_user"] else "否", "备注": h["note"]}
                           for h in hist])
        st.dataframe(placeholder="—", data=df, hide_index=True, width="stretch", column_config={
            "记录时间": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm"),
            "事件日期": st.column_config.DateColumn(format="YYYY-MM-DD")})


page_header("论文投稿", "Draft → Internal Review → Submitted → Editor Assigned → Under Review → Revision → Accepted → Published；"
                    "状态只由您手动确认。")
if st.button("新建论文记录", type="primary", icon=":material/add:"):
    pub_dialog()

counts = publications.status_counts()
chips = "".join(f'<span class="rcc-tag{" accent" if counts.get(s) else ""}">{esc(label("pub_status", s))} · {counts.get(s, 0)}</span>'
                for s in PUB_PIPELINE)
side = "".join(f'<span class="rcc-tag">{esc(label("pub_status", s))} · {counts.get(s, 0)}</span>'
               for s in PUB_SIDE_STATUSES + [PUB_UNCONFIRMED] if counts.get(s))
st.html(f'<div style="margin:.2rem 0 .8rem -.35rem;line-height:2">{chips}{side}</div>')

c1, c2 = st.columns([2, 4])
with c1:
    fp = project_selector("项目", key="pub_p", none_label="全部项目")
fs = c2.multiselect("状态", PUB_STATUSES, format_func=lambda x: label("pub_status", x), key="pub_s", placeholder="全部状态")
rows = publications.list_publications(fp, fs or None)
if not rows:
    empty_state("暂无论文记录。")
else:
    df = pd.DataFrame([{
        "id": r["id"], "标题": r["title"], "状态": label("pub_status", r["status"]), "目标期刊": r["target_journal"],
        "投稿日期": r["submission_date"], "修改期限": r["revision_due_date"], "下一步": r["next_action"],
        "项目": names.get(r["project_id"], "—") if r["project_id"] else "—", "更新": r["updated_at"],
    } for r in rows])
    sel = select_row(df, "pub_table", column_config={
        "投稿日期": st.column_config.DateColumn(format="YYYY-MM-DD"),
        "修改期限": st.column_config.DateColumn(format="YYYY-MM-DD"),
        "更新": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm")})
    if sel:
        render_detail(sel)
    else:
        st.caption("选择一行以查看详情、确认状态变更或查看状态历史。")
