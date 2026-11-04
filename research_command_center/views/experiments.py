"""实验记录：电子实验记录、待开展、日历、批次、参数对比、附件索引。"""
from __future__ import annotations

from datetime import date, timedelta
from typing import Optional

import pandas as pd
import streamlit as st

from rcc.constants import (
    ATTACHMENT_KINDS,
    EXPERIMENT_OUTCOMES,
    EXPERIMENT_STATUSES,
    label,
)
from rcc.services import calendar, experiments, files, projects
from rcc.ui import calendar_view
from rcc.ui.common import (
    is_repeat_submit,
    mark_submit_done,
    bootstrap,
    code_select,
    confirm_button,
    empty_state,
    esc,
    fmt_date,
    fmt_dt,
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
from rcc.utils import ValidationError, human_size, today

bootstrap()
show_flash()
names = projects.project_name_map()
D_MIN, D_MAX = date(1990, 1, 1), date(2100, 12, 31)


def _batch_options(project_id: Optional[int] = None) -> dict:
    return {b["id"]: b["code"] + (f"（{names.get(b['project_id'], '')}）" if b.get("project_id") else "")
            for b in experiments.list_batches()}


@st.dialog("实验记录", width="large")
def exp_dialog(exp_id: Optional[int] = None) -> None:
    e = experiments.get_experiment(exp_id) or {}
    k = f"ef{exp_id or 'new'}_"
    batches = _batch_options()
    with st.form(k + "form", border=False):
        name = st.text_input("实验名称 *", e.get("name") or "", key=k + "name")
        c1, c2, c3 = st.columns(3)
        with c1:
            pid = project_selector("所属项目", key=k + "proj", current=e.get("project_id"))
        bopts = [None] + list(batches.keys())
        bid = c2.selectbox("实验批次", bopts, index=bopts.index(e.get("batch_id")) if e.get("batch_id") in bopts else 0,
                           format_func=lambda x: "（无批次）" if x is None else batches.get(x, x), key=k + "batch")
        d = c3.date_input("实验日期", value=e.get("experiment_date"), min_value=D_MIN, max_value=D_MAX, key=k + "date")
        c4, c5 = st.columns(2)
        with c4:
            status = code_select("完成状态", "experiment_status", EXPERIMENT_STATUSES, key=k + "st",
                                 current=e.get("status") or "Planned")
        with c5:
            outcome = code_select("是否成功", "experiment_outcome", EXPERIMENT_OUTCOMES, key=k + "oc",
                                  current=e.get("outcome"), allow_empty=True, empty_label="尚未判定")
        purpose = st.text_area("实验目的", e.get("purpose") or "", height=68, key=k + "purpose")
        c6, c7 = st.columns(2)
        groups = c6.text_area("实验分组", e.get("groups") or "", height=68, key=k + "groups")
        model = c7.text_area("细胞或动物模型", e.get("model_system") or "", height=68, key=k + "model")
        c8, c9 = st.columns(2)
        reagents = c8.text_area("试剂（含批号）", e.get("reagents") or "", height=68, key=k + "reag")
        instruments = c9.text_area("仪器", e.get("instruments") or "", height=68, key=k + "inst")
        st.markdown("实验操作参数")
        params = pd.DataFrame(e.get("parameters_list") or [], columns=["name", "value", "unit"])
        params = st.data_editor(placeholder="—", data=params, num_rows="dynamic", hide_index=True, key=k + "params", width="stretch",
                                column_config={"name": st.column_config.TextColumn("参数", required=True),
                                               "value": st.column_config.TextColumn("值"),
                                               "unit": st.column_config.TextColumn("单位")})
        raw_path = st.text_input("原始数据文件路径（只引用，不修改）", e.get("raw_data_path") or "", key=k + "raw")
        result = st.text_area("实验结果摘要", e.get("result_summary") or "", height=80, key=k + "result")
        c10, c11 = st.columns(2)
        failure = c10.text_area("失败原因", e.get("failure_reason") or "", height=68, key=k + "fail")
        nxt = c11.text_area("下一步实验", e.get("next_experiment") or "", height=68, key=k + "next")
        notes = st.text_area("备注", e.get("notes") or "", height=68, key=k + "notes")
        submitted = st.form_submit_button("保存", type="primary")
    if submitted:
        data = {"name": name, "project_id": pid, "batch_id": bid, "experiment_date": d, "status": status,
                "outcome": outcome, "purpose": purpose, "groups": groups, "model_system": model, "reagents": reagents,
                "instruments": instruments, "parameters": params, "raw_data_path": raw_path, "result_summary": result,
                "failure_reason": failure, "next_experiment": nxt, "notes": notes}
        if not exp_id and is_repeat_submit(k, data):
            st.rerun()
        try:
            if exp_id:
                experiments.update_experiment(exp_id, data)
            else:
                experiments.create_experiment(data)
                mark_submit_done(k, data)
            if (status == "Failed" or outcome == "Failure") and not failure.strip():
                st.session_state.setdefault("_rcc_flash", []).append(("已保存。提示：建议补充失败原因，便于复盘。", "⚠️"))
            else:
                st.session_state.setdefault("_rcc_flash", []).append(("实验记录已保存", "✅"))
            st.rerun()
        except ValidationError as e:
            show_errors(e)


def render_detail(exp_id: int) -> None:
    e = experiments.get_experiment(exp_id)
    if not e:
        return
    with st.container(border=True):
        st.subheader(e["name"])
        st.html(f'<div style="margin:-.4rem 0 .4rem -.35rem">{tag(label("experiment_status", e["status"]), "accent")}'
                f'{tag(label("experiment_outcome", e["outcome"], empty="尚未判定"))}</div>')
        a, b = st.columns([3, 2], gap="large")
        batches = _batch_options()
        with a:
            kv_block([
                ("所属项目", names.get(e["project_id"]) if e["project_id"] else None),
                ("实验批次", batches.get(e["batch_id"]) if e["batch_id"] else None),
                ("实验日期", fmt_date(e["experiment_date"]) or None),
                ("实验目的", e["purpose"]), ("实验分组", e["groups"]), ("细胞/动物模型", e["model_system"]),
                ("试剂", e["reagents"]), ("仪器", e["instruments"]),
                ("原始数据", raw(render_paths(e["raw_data_path"])) if e.get("raw_data_path") else None),
                ("结果摘要", e["result_summary"]), ("失败原因", e["failure_reason"]), ("下一步实验", e["next_experiment"]),
                ("备注", e["notes"]), ("最近更新", fmt_dt(e["updated_at"])),
            ])
        with b:
            if st.button("编辑实验记录", key=f"ee_{exp_id}", width="stretch", type="primary", icon=":material/edit:"):
                exp_dialog(exp_id)
            new_st = st.selectbox("快速更改状态", EXPERIMENT_STATUSES, index=EXPERIMENT_STATUSES.index(e["status"]),
                                  format_func=lambda x: label("experiment_status", x), key=f"eqs_{exp_id}")
            if new_st != e["status"]:
                run_action(experiments.update_experiment, exp_id, {"status": new_st}, success="状态已更新")
            with st.popover("删除实验记录", width="stretch"):
                st.write("只删除数据库记录与附件引用，不会删除或修改任何原始数据文件。")
                if confirm_button("删除", key=f"edel_{exp_id}", confirm_text="确认删除"):
                    run_action(experiments.delete_experiment, exp_id, success="实验记录已删除")
            st.markdown("**实验参数**")
            if e["parameters_list"]:
                st.dataframe(placeholder="—", data=pd.DataFrame(e["parameters_list"]).rename(columns={"name": "参数", "value": "值", "unit": "单位"}),
                             hide_index=True, width="stretch")
            else:
                st.caption("未登记参数。")
        st.markdown("**附件与图片（仅引用路径；原始 WB 图片、测序文件等不会被修改）**")
        atts = experiments.list_attachments(exp_id)
        if atts:
            for at in atts:
                c1, c2, c3 = st.columns([6, 1, 1], vertical_alignment="center")
                c1.html(f'<div class="rcc-item"><div class="t">{esc(at["kind"] or "附件")}'
                        f'{"" if at["exists_last_check"] else tag("文件不存在", "danger")}</div>'
                        f'<div class="m"><code>{esc(at["path"])}</code> · {esc(human_size(at["file_size"]))}'
                        f' · 修改于 {esc(fmt_dt(at["file_mtime"]))}{(" · " + esc(at["description"])) if at.get("description") else ""}</div></div>')
                if c2.button("打开", key=f"ao_{at['id']}", disabled=not at["exists_last_check"]):
                    run_action(files.open_in_system, at["path"], rerun=False)
                if c3.button("移除", key=f"ar_{at['id']}", help="只移除引用，不删除文件"):
                    run_action(experiments.delete_attachment, at["id"], success="已移除附件引用")
                if at["exists_last_check"] and str(at["path"]).lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                    with st.expander("预览图片"):
                        st.image(at["path"])
            if st.button("重新检测附件状态", key=f"ar_ref_{exp_id}"):
                experiments.refresh_attachments(exp_id)
                st.rerun()
        else:
            st.caption("暂无附件。")
        with st.form(f"att_add_{exp_id}", clear_on_submit=True, border=False):
            c1, c2, c3 = st.columns([4, 2, 2])
            p = c1.text_input("附件绝对路径", key=f"aa_p_{exp_id}", placeholder=r"D:\Lab\WB\2026-11-01_GAPDH.tif")
            kind = c2.selectbox("类型", ATTACHMENT_KINDS, key=f"aa_k_{exp_id}")
            desc = c3.text_input("说明", key=f"aa_d_{exp_id}")
            if st.form_submit_button("添加附件引用"):
                run_action(experiments.add_attachment, exp_id, p, kind, desc, success="附件已关联")


page_header("实验记录", "电子实验记录 · 原始数据只建立引用与索引，绝不修改原文件。")
if st.button("新建实验记录", type="primary", icon=":material/add:"):
    exp_dialog()

t_rec, t_pending, t_cal, t_batch, t_cmp = st.tabs(["实验记录", "待开展", "实验日历", "批次管理", "参数对比"])

with t_rec:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        fp = project_selector("项目", key="ex_p", none_label="全部项目")
    fs = c2.multiselect("状态", EXPERIMENT_STATUSES, format_func=lambda x: label("experiment_status", x), key="ex_s",
                        placeholder="全部状态")
    batches = _batch_options()
    bopt = [None] + list(batches.keys())
    fb = c3.selectbox("批次", bopt, format_func=lambda x: "全部批次" if x is None else batches.get(x, x), key="ex_b")
    q = c4.text_input("搜索", key="ex_q", placeholder="名称 / 目的 / 模型")
    rows = experiments.list_experiments(fp, fs or None, fb, q or None)
    if not rows:
        empty_state("没有实验记录。")
    else:
        df = pd.DataFrame([{
            "id": r["id"], "实验": r["name"], "项目": names.get(r["project_id"], "—") if r["project_id"] else "—",
            "日期": r["experiment_date"], "状态": label("experiment_status", r["status"]),
            "判定": label("experiment_outcome", r["outcome"], empty=""), "模型": r["model_system"],
            "批次": batches.get(r["batch_id"], "") if r["batch_id"] else "",
        } for r in rows])
        sel = select_row(df, "ex_table", column_config={"日期": st.column_config.DateColumn(format="YYYY-MM-DD")})
        if sel:
            render_detail(sel)
        else:
            st.caption("选择一行以查看详情与附件。")

with t_pending:
    rows = experiments.pending_experiments()
    if not rows:
        empty_state("没有待开展或进行中的实验。")
    else:
        df = pd.DataFrame([{
            "实验": r["name"], "项目": names.get(r["project_id"], "—") if r["project_id"] else "—",
            "计划日期": r["experiment_date"], "状态": label("experiment_status", r["status"]),
            "提醒": "计划日期已过" if r["experiment_date"] and r["experiment_date"] < today() and r["status"] == "Planned" else "",
            "目的": r["purpose"],
        } for r in rows])
        st.dataframe(placeholder="—", data=df, hide_index=True, width="stretch",
                     column_config={"计划日期": st.column_config.DateColumn(format="YYYY-MM-DD")})

with t_cal:
    ss = st.session_state
    ss.setdefault("ex_cal_month", date(today().year, today().month, 1))
    m = ss["ex_cal_month"]
    a, b, c, d_ = st.columns([1, 1, 1, 5], vertical_alignment="center")
    if a.button("‹ 上月", key="exm_prev"):
        ss["ex_cal_month"] = date(m.year - (m.month == 1), 12 if m.month == 1 else m.month - 1, 1)
        st.rerun()
    if b.button("本月", key="exm_now"):
        ss["ex_cal_month"] = date(today().year, today().month, 1)
        st.rerun()
    if c.button("下月 ›", key="exm_next"):
        ss["ex_cal_month"] = date(m.year + (m.month == 12), 1 if m.month == 12 else m.month + 1, 1)
        st.rerun()
    d_.markdown(f"**{m.year} 年 {m.month} 月**")
    import calendar as _pycal

    last = date(m.year, m.month, _pycal.monthrange(m.year, m.month)[1])
    evs = calendar.aggregate(m.replace(day=1) - timedelta(days=7), last + timedelta(days=7), sources=["experiment"])
    calendar_view.month_view(m.year, m.month, evs)

with t_batch:
    bl = experiments.list_batches()
    if bl:
        df = pd.DataFrame([{"id": b["id"], "批次编号": b["code"], "项目": names.get(b["project_id"], "—") if b["project_id"] else "—",
                            "开始日期": b["start_date"], "说明": b["description"],
                            "实验数": len(experiments.list_experiments(batch_id=b["id"]))} for b in bl])
        sel_b = select_row(df, "batch_table", column_config={"开始日期": st.column_config.DateColumn(format="YYYY-MM-DD")})
    else:
        sel_b = None
        empty_state("暂无批次。")
    cur = next((b for b in bl if b["id"] == sel_b), None) if sel_b else None
    st.markdown("**编辑批次**" if cur else "**新建批次**")
    k = f"bf{cur['id'] if cur else 'new'}_"
    with st.form(k + "form", border=False):
        c1, c2, c3 = st.columns(3)
        code = c1.text_input("批次编号 *", (cur or {}).get("code") or "", key=k + "code")
        with c2:
            bp = project_selector("所属项目", key=k + "proj", current=(cur or {}).get("project_id"))
        sd = c3.date_input("开始日期", value=(cur or {}).get("start_date"), key=k + "sd")
        desc = st.text_input("说明", (cur or {}).get("description") or "", key=k + "desc")
        notes = st.text_area("备注", (cur or {}).get("notes") or "", height=68, key=k + "notes")
        if st.form_submit_button("保存批次", type="primary"):
            data = {"code": code, "project_id": bp, "start_date": sd, "description": desc, "notes": notes}
            if cur:
                run_action(experiments.update_batch, cur["id"], data, success="批次已更新")
            else:
                run_action(experiments.create_batch, data, success="批次已创建")
    if cur:
        with st.popover("删除批次"):
            st.write("批次内的实验记录会保留，仅清空其批次字段。")
            if confirm_button("删除", key=f"bdel_{cur['id']}", confirm_text="确认删除批次"):
                run_action(experiments.delete_batch, cur["id"], success="批次已删除")

with t_cmp:
    allx = experiments.list_experiments()
    opts = {x["id"]: f"#{x['id']} {x['name']}" + (f"（{x['experiment_date']}）" if x["experiment_date"] else "") for x in allx}
    chosen = st.multiselect("选择要对比的实验（2 个或以上）", list(opts.keys()), format_func=lambda i: opts[i], key="cmp_sel")
    if len(chosen) >= 2:
        df = experiments.parameter_comparison(chosen)
        if df.empty:
            empty_state("所选实验均未登记参数。")
        else:
            only_diff = st.toggle("只显示不同的参数", key="cmp_diff")
            view = df[df["是否一致"] == "不同"] if only_diff else df
            st.dataframe(placeholder="—", data=view, width="stretch")
    else:
        st.caption("选择至少两个实验以对比关键参数。")
