"""科研项目管理：列表、详情（时间线、任务、文献、实验、文件）、新建/编辑/归档。"""
from __future__ import annotations

from datetime import date
from typing import Optional

import pandas as pd
import streamlit as st

from rcc.constants import (
    FILE_CATEGORIES,
    MILESTONE_STATUSES,
    PROJECT_STATUSES,
    TASK_PRIORITIES,
    label,
)
from rcc.services import bioinfo, experiments, files, literature, projects, publications, tasks
from rcc.ui.common import (
    is_repeat_submit,
    mark_submit_done,
    nav_link,
    bootstrap,
    code_select,
    confirm_button,
    empty_state,
    esc,
    fmt_date,
    fmt_dt,
    kv_block,
    page_header,
    raw,
    render_paths,
    run_action,
    show_errors,
    show_flash,
    tag,
)
from rcc.utils import ValidationError, human_size

bootstrap()
show_flash()

D_MIN, D_MAX = date(1990, 1, 1), date(2100, 12, 31)


def _qp_project() -> Optional[int]:
    v = st.query_params.get("project")
    try:
        return int(v) if v else None
    except ValueError:
        return None


def _open(pid: Optional[int]) -> None:
    if pid is None:
        st.query_params.pop("project", None)
    else:
        st.query_params["project"] = str(pid)
    st.rerun()


@st.dialog("项目信息", width="large")
def project_dialog(project_id: Optional[int] = None) -> None:
    p = projects.get_project(project_id) or {}
    k = f"pf{project_id or 'new'}_"
    with st.form(f"{k}form", border=False):
        name = st.text_input("项目名称 *", p.get("name") or "", key=k + "name")
        c1, c2 = st.columns(2)
        with c1:
            status = code_select("当前状态", "project_status", PROJECT_STATUSES, key=k + "status",
                                 current=p.get("status"), allow_empty=True)
        progress = c2.number_input("完成进度（%）", min_value=0, max_value=100, step=5, value=p.get("progress"),
                                   placeholder="待填写", key=k + "progress")
        c3, c4 = st.columns(2)
        start = c3.date_input("开始时间", value=p.get("start_date"), min_value=D_MIN, max_value=D_MAX,
                              format="YYYY-MM-DD", key=k + "start")
        end = c4.date_input("预计完成时间", value=p.get("expected_end_date"), min_value=D_MIN, max_value=D_MAX,
                            format="YYYY-MM-DD", key=k + "end")
        c5, c6 = st.columns([1, 2])
        lead = c5.text_input("项目负责人", p.get("lead") or "", key=k + "lead")
        participants = c6.text_input("参与者", p.get("participants") or "", key=k + "participants")
        direction = st.text_area("研究方向", p.get("research_direction") or "", height=68, key=k + "dir")
        question = st.text_area("科学问题", p.get("scientific_question") or "", height=68, key=k + "q")
        hypothesis = st.text_area("核心假说", p.get("core_hypothesis") or "", height=68, key=k + "h")
        stage = st.text_area("当前研究阶段", p.get("current_stage") or "", height=68, key=k + "stage")
        next_steps = st.text_area("下一步计划", p.get("next_steps") or "", height=90, key=k + "next")
        risks = st.text_area("主要风险", p.get("main_risks") or "", height=68, key=k + "risk")
        key_paths = st.text_area("关键文件路径（每行一个绝对路径，仅作引用）", p.get("key_paths") or "", height=90,
                                 key=k + "paths")
        notes = st.text_area("备注", p.get("notes") or "", height=68, key=k + "notes")
        source = st.text_area("信息来源说明", p.get("source_note") or "", height=68, key=k + "src",
                              help="记录这些信息来自哪里，便于日后追溯。")
        st.caption("留空的字段会显示为“待填写”。请只填写已确认的信息。")
        submitted = st.form_submit_button("保存", type="primary")
    if submitted:
        data = {"name": name, "status": status, "progress": progress, "start_date": start, "expected_end_date": end,
                "lead": lead, "participants": participants, "research_direction": direction,
                "scientific_question": question, "core_hypothesis": hypothesis, "current_stage": stage,
                "next_steps": next_steps, "main_risks": risks, "key_paths": key_paths, "notes": notes,
                "source_note": source}
        if not project_id and is_repeat_submit(k, data):
            st.rerun()  # 重复提交（双击等）：已保存过，直接关闭
        try:
            if project_id:
                projects.update_project(project_id, data)
                st.session_state.setdefault("_rcc_flash", []).append(("项目已更新", "✅"))
            else:
                new_id = projects.create_project(data)
                mark_submit_done(k, data)
                st.session_state.setdefault("_rcc_flash", []).append(("项目已创建", "✅"))
                st.session_state["_open_project"] = new_id  # 在完整页面运行中跳转（不在对话框内修改 URL）
            st.rerun()
        except ValidationError as e:
            show_errors(e)


# ===================================================================== list
def render_list() -> None:
    page_header("科研项目", "创建、编辑与归档科研项目；点击“打开”查看项目详情、时间线与关联数据。")
    a, b, c = st.columns([2, 2, 1], vertical_alignment="bottom")
    statuses = a.multiselect("按状态筛选", PROJECT_STATUSES, format_func=lambda x: label("project_status", x),
                             key="pl_status", placeholder="全部状态")
    show_arch = b.toggle("显示已归档项目", key="pl_arch")
    if c.button("新建项目", type="primary", width="stretch", icon=":material/add:"):
        project_dialog()
    rows = projects.list_projects(include_archived=show_arch, statuses=statuses or None)
    if not rows:
        empty_state("没有符合条件的项目。")
        return
    cols = st.columns(3, gap="medium")
    for i, p in enumerate(rows):
        counts = projects.related_counts(p["id"])
        open_tasks = len(tasks.list_tasks(project_ids=[p["id"]], statuses=["Todo", "In Progress", "Blocked"]))
        with cols[i % 3]:
            with st.container(border=True):
                tags = tag(label("project_status", p["status"]), "accent" if p["status"] == "Active" else "")
                if p["is_archived"]:
                    tags += tag("已归档")
                st.html(f'<div style="font-weight:620;font-size:1.02rem;line-height:1.4">{esc(p["name"])}</div>'
                        f'<div style="margin:.25rem 0 .1rem -.35rem">{tags}</div>')
                direction = p.get("research_direction") or ""
                st.html(f'<div class="rcc-small" style="min-height:2.6rem">'
                        f'{esc(direction[:90] + ("…" if len(direction) > 90 else "")) or "研究方向：待填写"}</div>')
                if p["progress"] is not None:
                    st.progress(p["progress"] / 100, text=f"完成进度 {p['progress']}%")
                else:
                    st.html('<div class="rcc-small">完成进度：<span class="rcc-pending">待填写</span></div>')
                stage = p.get("current_stage") or ""
                st.html(f'<div class="rcc-small"><b>当前阶段</b>：{esc(stage[:70] + ("…" if len(stage) > 70 else "")) or "待填写"}</div>'
                        f'<div class="rcc-small" style="margin-top:.3rem">未完成任务 {open_tasks} · 实验 {counts["experiments"]} · '
                        f'文献 {counts["literature"]} · 文件 {counts["files"]}</div>')
                if st.button("打开", key=f"open_{p['id']}", width="stretch"):
                    _open(p["id"])


# =================================================================== detail
def render_overview_tab(p: dict) -> None:
    left, right = st.columns(2, gap="large")
    with left:
        kv_block([
            ("研究方向", p["research_direction"]),
            ("科学问题", p["scientific_question"]),
            ("核心假说", p["core_hypothesis"]),
            ("项目负责人", p["lead"]),
            ("参与者", p["participants"]),
            ("开始时间", fmt_date(p["start_date"]) or None),
            ("预计完成", fmt_date(p["expected_end_date"]) or None),
            ("当前状态", label("project_status", p["status"], empty="") or None),
            ("完成进度", f"{p['progress']}%" if p["progress"] is not None else None),
            ("当前研究阶段", p["current_stage"]),
        ])
    with right:
        kv_block([
            ("下一步计划", p["next_steps"]),
            ("主要风险", p["main_risks"]),
            ("关键文件路径", raw(render_paths(p["key_paths"]))),
            ("备注", p["notes"]),
            ("信息来源", p["source_note"]),
            ("最近更新", fmt_dt(p["updated_at"])),
        ])


def render_timeline_tab(p: dict) -> None:
    left, right = st.columns([3, 2], gap="large")
    with left:
        st.markdown("**项目时间线**")
        items = projects.timeline(p["id"])
        if not items:
            empty_state("暂无带日期的事件。", "添加里程碑、任务截止日期或实验日期后会显示在这里。")
        else:
            parts = ['<div class="rcc-timeline">']
            for it in items:
                d = fmt_date(it["date"]) if it["date"] else "未定日期"
                st_txt = it.get("status") or ""
                parts.append(f'<div class="ti{" nodate" if not it["date"] else ""}"><div class="dt">{esc(d)} · {esc(it["kind"])}</div>'
                             f'<div>{esc(it["title"])}{tag(st_txt) if st_txt else ""}</div></div>')
            parts.append("</div>")
            st.html("".join(parts))
    with right:
        st.markdown("**里程碑**")
        ms = projects.list_milestones(p["id"])
        for m in ms:
            with st.container(border=True):
                a, b = st.columns([3, 2], vertical_alignment="center")
                a.html(f'<div class="t" style="font-weight:560">{esc(m["title"])}</div>'
                       f'<div class="rcc-small">{esc(fmt_date(m["due_date"]) or "未定日期")}'
                       f'{(" · " + esc(m["note"])) if m.get("note") else ""}</div>')
                new_status = b.selectbox("状态", MILESTONE_STATUSES, index=MILESTONE_STATUSES.index(m["status"]),
                                         format_func=lambda x: label("milestone_status", x), key=f"ms_st_{m['id']}",
                                         label_visibility="collapsed")
                if new_status != m["status"]:
                    run_action(projects.update_milestone, m["id"], {**m, "status": new_status}, success="里程碑已更新")
                with st.popover("编辑 / 删除", width="stretch"):
                    with st.form(f"ms_edit_{m['id']}", border=False):
                        t = st.text_input("名称", m["title"], key=f"ms_t_{m['id']}")
                        d = st.date_input("日期", value=m["due_date"], min_value=D_MIN, max_value=D_MAX,
                                          key=f"ms_d_{m['id']}")
                        n = st.text_input("备注", m.get("note") or "", key=f"ms_n_{m['id']}")
                        if st.form_submit_button("保存"):
                            run_action(projects.update_milestone, m["id"],
                                       {"title": t, "due_date": d, "note": n, "status": m["status"],
                                        "sort_order": m["sort_order"]}, success="已保存")
                    if confirm_button("删除里程碑", key=f"ms_del_{m['id']}", confirm_text="确认删除"):
                        run_action(projects.delete_milestone, m["id"], success="已删除")
        with st.expander("添加里程碑", expanded=not ms):
            with st.form(f"ms_add_{p['id']}", clear_on_submit=True, border=False):
                t = st.text_input("里程碑名称", key=f"ms_add_t_{p['id']}")
                c1, c2 = st.columns(2)
                d = c1.date_input("日期（可留空）", value=None, min_value=D_MIN, max_value=D_MAX, key=f"ms_add_d_{p['id']}")
                s = c2.selectbox("状态", MILESTONE_STATUSES, format_func=lambda x: label("milestone_status", x),
                                 key=f"ms_add_s_{p['id']}")
                n = st.text_input("备注", key=f"ms_add_n_{p['id']}")
                if st.form_submit_button("添加", type="primary"):
                    mdata = {"title": t, "due_date": d, "status": s, "note": n, "sort_order": len(ms)}
                    if not is_repeat_submit(f"ms_{p['id']}", mdata):
                        if run_action(projects.add_milestone, p["id"], mdata, rerun=False) is not None:
                            mark_submit_done(f"ms_{p['id']}", mdata)
                            run_action(lambda: None, success="里程碑已添加")


def render_tasks_tab(p: dict) -> None:
    rows = tasks.list_tasks(project_ids=[p["id"]])
    if rows:
        df = pd.DataFrame([{
            "id": r["id"], "任务": r["title"], "优先级": r["priority"], "状态": label("task_status", r["status"]),
            "截止日期": r["due_date"], "提醒": "已逾期" if r["is_overdue"] else "",
        } for r in rows])
        st.dataframe(placeholder="—", data=df, hide_index=True, column_order=[c for c in df.columns if c != "id"], width="stretch",
                     column_config={"截止日期": st.column_config.DateColumn(format="YYYY-MM-DD")})
    else:
        empty_state("该项目暂无任务。")
    with st.expander("快速添加任务"):
        with st.form(f"pt_add_{p['id']}", clear_on_submit=True, border=False):
            t = st.text_input("任务名称", key=f"pt_t_{p['id']}")
            c1, c2 = st.columns(2)
            pr = c1.selectbox("优先级", TASK_PRIORITIES, index=2, key=f"pt_p_{p['id']}")
            d = c2.date_input("截止日期", value=None, key=f"pt_d_{p['id']}")
            if st.form_submit_button("添加", type="primary"):
                qdata = {"title": t, "priority": pr, "due_date": d, "project_id": p["id"]}
                if not is_repeat_submit(f"pt_{p['id']}", qdata):
                    if run_action(tasks.create_task, qdata, rerun=False) is not None:
                        mark_submit_done(f"pt_{p['id']}", qdata)
                        run_action(lambda: None, success="任务已添加")
    nav_link("views/tasks.py", "在任务管理中查看全部任务")


def render_literature_tab(p: dict) -> None:
    lits = literature.literature_for_project(p["id"])
    if lits:
        df = pd.DataFrame([{
            "id": x["id"], "标题": x["title"] or "（标题待核实）", "年份": x["year"], "期刊": x["journal"],
            "DOI": x["doi"], "核实": label("verification", x["verification_status"]),
            "阅读": label("reading_status", x["reading_status"]), "与项目关系": x.get("relevance"),
        } for x in lits])
        st.dataframe(placeholder="—", data=df, hide_index=True, column_order=[c for c in df.columns if c != "id"], width="stretch")
    else:
        empty_state("尚未关联文献。")
    all_lits = literature.search_literature()
    linked = {x["id"] for x in lits}
    candidates = [x for x in all_lits if x["id"] not in linked]
    c1, c2 = st.columns(2)
    with c1.expander("关联已有文献"):
        if not candidates:
            st.caption("文献库中没有可关联的文献。")
        else:
            with st.form(f"pl_link_{p['id']}", clear_on_submit=True, border=False):
                lid = st.selectbox("选择文献", [x["id"] for x in candidates], key=f"pl_lid_{p['id']}",
                                   format_func=lambda i: next((f"#{x['id']} {(x['title'] or x['doi'] or '标题待核实')[:70]}"
                                                               for x in candidates if x["id"] == i), str(i)))
                rel = st.text_area("与本项目的关系（可选）", height=68, key=f"pl_rel_{p['id']}")
                if st.form_submit_button("关联", type="primary"):
                    run_action(literature.link_project, lid, p["id"], rel, success="已关联")
    with c2.expander("取消关联"):
        if lits:
            uid = st.selectbox("选择文献", [x["id"] for x in lits], key=f"pl_uid_{p['id']}",
                               format_func=lambda i: next((f"#{x['id']} {(x['title'] or '标题待核实')[:70]}" for x in lits
                                                           if x["id"] == i), str(i)))
            if st.button("取消关联（不删除文献）", key=f"pl_unlink_{p['id']}"):
                run_action(literature.unlink_project, uid, p["id"], success="已取消关联")
    nav_link("views/literature.py", "前往文献库")


def render_experiments_tab(p: dict) -> None:
    rows = experiments.list_experiments(project_id=p["id"])
    if rows:
        df = pd.DataFrame([{
            "id": r["id"], "实验": r["name"], "日期": r["experiment_date"], "状态": label("experiment_status", r["status"]),
            "判定": label("experiment_outcome", r["outcome"], empty=""), "结果摘要": r["result_summary"],
        } for r in rows])
        st.dataframe(placeholder="—", data=df, hide_index=True, column_order=[c for c in df.columns if c != "id"], width="stretch",
                     column_config={"日期": st.column_config.DateColumn(format="YYYY-MM-DD")})
    else:
        empty_state("该项目暂无实验记录。")
    nav_link("views/experiments.py", "前往实验记录")


def render_outputs_tab(p: dict) -> None:
    st.markdown("**论文投稿**")
    pubs = publications.list_publications(project_id=p["id"])
    if pubs:
        df = pd.DataFrame([{"id": x["id"], "标题": x["title"], "状态": label("pub_status", x["status"]),
                            "目标期刊": x["target_journal"], "下一步": x["next_action"]} for x in pubs])
        st.dataframe(placeholder="—", data=df, hide_index=True, column_order=[c for c in df.columns if c != "id"], width="stretch")
    else:
        empty_state("暂无论文记录。")
    st.markdown("**生信分析任务**")
    jobs = bioinfo.list_jobs(project_id=p["id"])
    if jobs:
        df = pd.DataFrame([{"id": j["id"], "分析": j["name"], "语言": j["language"], "状态": j["status"],
                            "结果摘要": j["result_summary"]} for j in jobs])
        st.dataframe(placeholder="—", data=df, hide_index=True, column_order=[c for c in df.columns if c != "id"], width="stretch")
    else:
        empty_state("暂无分析任务。")


def render_files_tab(p: dict) -> None:
    rows = files.list_files(project_id=p["id"])
    if rows:
        df = pd.DataFrame([{"id": f["id"], "存在": "是" if f["exists"] else "否", "文件名": f["file_name"],
                            "类别": f["category"], "修改时间": f["modified_at"], "大小": human_size(f["size_bytes"]),
                            "路径": f["path"]} for f in rows])
        st.dataframe(placeholder="—", data=df, hide_index=True, column_order=[c for c in df.columns if c != "id"], width="stretch",
                     column_config={"修改时间": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm")})
        if st.button("重新检测文件状态", key=f"pf_refresh_{p['id']}"):
            r = files.refresh_status([f["id"] for f in rows])
            run_action(lambda: None, success=f"已检测 {r['checked']} 个文件，{r['missing']} 个不存在")
    else:
        empty_state("尚未登记文件。")
    with st.expander("登记文件（只记录路径，不复制、不移动原文件）"):
        with st.form(f"pf_add_{p['id']}", clear_on_submit=True, border=False):
            path = st.text_input("文件绝对路径", key=f"pf_path_{p['id']}", placeholder=r"D:\Research\data\WB_2026-11-01.tif")
            c1, c2 = st.columns(2)
            cat = c1.selectbox("类别", [None] + FILE_CATEGORIES, format_func=lambda x: "按扩展名自动识别" if x is None else x,
                               key=f"pf_cat_{p['id']}")
            desc = c2.text_input("说明", key=f"pf_desc_{p['id']}")
            if st.form_submit_button("登记", type="primary"):
                run_action(files.register_file, path, p["id"], cat, desc, success="文件已登记")


def render_detail(pid: int) -> None:
    p = projects.get_project(pid)
    if st.button("← 返回项目列表", key="back"):
        _open(None)
    if p is None:
        st.error("项目不存在或已被删除。")
        return
    tags = tag(label("project_status", p["status"]), "accent" if p["status"] == "Active" else "")
    if p["is_archived"]:
        tags += tag("已归档")
    st.title(p["name"])
    st.html(f'<div style="margin:-.6rem 0 .8rem -.35rem">{tags}</div>')
    missing = projects.missing_fields(p)
    if missing:
        st.caption(f"{len(missing)} 项信息待填写：{'、'.join(missing)}")
    a, b, c, _ = st.columns([1, 1, 1, 3])
    if a.button("编辑项目", type="primary", width="stretch", icon=":material/edit:"):
        project_dialog(pid)
    if p["is_archived"]:
        if b.button("恢复项目", width="stretch"):
            run_action(projects.set_archived, pid, False, success="项目已恢复")
    else:
        if b.button("归档项目", width="stretch", help="归档后不在默认列表与统计中显示，数据完整保留"):
            run_action(projects.set_archived, pid, True, success="项目已归档")
    with c.popover("删除", width="stretch"):
        st.write("仅当项目没有任何关联数据时才能删除；否则请使用“归档”。不会删除任何磁盘文件。")
        if confirm_button("永久删除项目", key=f"del_{pid}", confirm_text="我确认删除该项目记录", type="primary"):
            try:
                projects.delete_project(pid)
                st.session_state.setdefault("_rcc_flash", []).append(("项目已删除", "🗑️"))
                _open(None)
            except ValidationError as e:
                show_errors(e)
    tabs = st.tabs(["概览", "时间线与里程碑", "任务", "文献", "实验", "投稿与分析", "文件"])
    with tabs[0]:
        render_overview_tab(p)
    with tabs[1]:
        render_timeline_tab(p)
    with tabs[2]:
        render_tasks_tab(p)
    with tabs[3]:
        render_literature_tab(p)
    with tabs[4]:
        render_experiments_tab(p)
    with tabs[5]:
        render_outputs_tab(p)
    with tabs[6]:
        render_files_tab(p)


if "_open_project" in st.session_state:
    st.query_params["project"] = str(st.session_state.pop("_open_project"))
selected = _qp_project()
if selected:
    render_detail(selected)
else:
    render_list()
