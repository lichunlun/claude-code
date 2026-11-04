"""生信分析：任务登记、路径管理、日志、结果索引；可选的安全脚本执行（需显式开启）。"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

from rcc.constants import BIO_LANGUAGES, BIO_STATUSES, label
from rcc.services import app_settings, bioinfo, projects, runner
from rcc.ui.common import (
    is_repeat_submit,
    mark_submit_done,
    bootstrap,
    code_select,
    confirm_button,
    empty_state,
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
from rcc.utils import ValidationError, human_size, loads

bootstrap()
show_flash()
names = projects.project_name_map()


@st.dialog("分析任务", width="large")
def job_dialog(job_id: Optional[int] = None) -> None:
    j = bioinfo.get_job(job_id) or {}
    k = f"bj{job_id or 'new'}_"
    with st.form(k + "form", border=False):
        name = st.text_input("分析名称 *", j.get("name") or "", key=k + "name")
        c1, c2, c3 = st.columns(3)
        with c1:
            pid = project_selector("所属项目", key=k + "proj", current=j.get("project_id"))
        lang = c2.selectbox("使用语言", [None] + BIO_LANGUAGES, format_func=lambda x: "按脚本扩展名识别" if x is None else x,
                            index=([None] + BIO_LANGUAGES).index(j.get("language")) if j.get("language") in BIO_LANGUAGES else 0,
                            key=k + "lang")
        with c3:
            status = code_select("运行状态", "bio_status", BIO_STATUSES, key=k + "st", current=j.get("status") or "Pending")
        purpose = st.text_area("分析目的", j.get("purpose") or "", height=68, key=k + "purpose")
        script = st.text_input("脚本路径（绝对路径）", j.get("script_path") or "", key=k + "script")
        args = st.text_area("脚本参数（每行一个，可选）", j.get("script_args") or "", height=68, key=k + "args")
        wd = st.text_input("工作目录（可选，默认脚本所在目录）", j.get("working_dir") or "", key=k + "wd")
        data_paths = st.text_area("数据文件路径（每行一个）", j.get("data_paths") or "", height=68, key=k + "data")
        source = st.text_input("数据来源（如 TCGA-LUAD、GEO 编号、本实验室测序批次）", j.get("data_source") or "", key=k + "src")
        outputs = st.text_area("输出文件路径（每行一个）", j.get("output_paths") or "", height=68, key=k + "out")
        result = st.text_area("分析结果摘要", j.get("result_summary") or "", height=80, key=k + "res")
        err = st.text_area("错误日志", j.get("error_log") or "", height=68, key=k + "err")
        notes = st.text_area("备注", j.get("notes") or "", height=68, key=k + "notes")
        submitted = st.form_submit_button("保存", type="primary")
    if submitted:
        data = {"name": name, "project_id": pid, "language": lang, "status": status, "purpose": purpose,
                "script_path": script, "script_args": args, "working_dir": wd, "data_paths": data_paths,
                "data_source": source, "output_paths": outputs, "result_summary": result, "error_log": err, "notes": notes}
        if not job_id and is_repeat_submit(k, data):
            st.rerun()
        try:
            if job_id:
                bioinfo.update_job(job_id, data)
            else:
                bioinfo.create_job(data)
                mark_submit_done(k, data)
            st.session_state.setdefault("_rcc_flash", []).append(("分析任务已保存", "✅"))
            st.rerun()
        except ValidationError as e:
            show_errors(e)


def run_panel(j: dict) -> None:
    if not app_settings.allow_script_execution():
        st.info("脚本执行功能当前关闭（默认）。本模块第一阶段仅做登记、路径管理、日志与结果索引。"
                "如需在本机执行已登记的 R / Python 脚本，请前往“设置与备份 → 脚本执行”开启。", icon="🔒")
        return
    if j["status"] == "Running":
        runs = [r for r in bioinfo.list_runs(j["id"]) if r["status"] in ("Running", "Cancelled") and r["source"] == "executed"]
        st.warning("任务正在运行…", icon="⏳")
        c1, c2 = st.columns(2)
        if c1.button("刷新状态", key=f"rf_{j['id']}"):
            st.rerun()
        if runs and c2.button("终止运行", key=f"kill_{j['id']}"):
            runner.cancel_run(runs[0]["id"])
            st.rerun()
        if runs and runs[0].get("log_path"):
            st.code(runner.tail_log(runs[0]["log_path"], 3000) or "（暂无输出）")
        return
    try:
        pv = runner.build_preview(j["id"])
    except ValidationError as e:
        show_errors(e)
        return
    st.markdown("**执行前检查**（每次运行都需要确认）")
    st.markdown("将要执行的命令：")
    st.code(" ".join(f'"{c}"' if " " in str(c) else str(c) for c in pv["command"]) or "（无法生成命令）", language="bash")
    st.caption(f"工作目录：{pv['cwd'] or '—'} · 超时：{pv['timeout_minutes']} 分钟 · 日志：{pv['log_path']}")
    if pv["script_sha256"]:
        st.caption(f"脚本 SHA-256：{pv['script_sha256']}")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("输入文件")
        if pv["inputs"]:
            st.dataframe(placeholder="—", data=pd.DataFrame([{"路径": x["path"], "存在": "是" if x["exists"] else "否"} for x in pv["inputs"]]),
                         hide_index=True, width="stretch")
        else:
            st.caption("未登记输入文件")
    with c2:
        st.markdown("输出路径")
        if pv["outputs"]:
            st.dataframe(placeholder="—", data=pd.DataFrame([{"路径": x["path"], "已存在": "是" if x["exists"] else "否"} for x in pv["outputs"]]),
                         hide_index=True, width="stretch")
        else:
            st.caption("未登记输出路径")
    for e in pv["errors"]:
        st.error(e)
    for w in pv["warnings"]:
        st.warning(w)
    ok = st.checkbox("我已核对上述命令、输入文件与输出路径，确认脚本来源可信，同意执行", key=f"runok_{j['id']}",
                     disabled=not pv["ok"])
    if st.button("执行脚本", type="primary", disabled=not (ok and pv["ok"]), key=f"run_{j['id']}"):
        run_action(runner.start_run, j["id"], ok, pv["script_sha256"], success="已开始运行，结果需人工核验")


def render_detail(job_id: int) -> None:
    j = bioinfo.get_job(job_id)
    if not j:
        return
    with st.container(border=True):
        st.subheader(j["name"])
        st.html(f'<div style="margin:-.4rem 0 .4rem -.35rem">{tag(label("bio_status", j["status"]), "accent")}'
                f'{tag(j["language"] or "语言未填写")}</div>')
        a, b = st.columns([3, 2], gap="large")
        with a:
            kv_block([
                ("所属项目", names.get(j["project_id"]) if j["project_id"] else None),
                ("分析目的", j["purpose"]), ("数据来源", j["data_source"]),
                ("脚本", raw(render_paths(j["script_path"]))), ("脚本参数", j["script_args"]),
                ("数据文件", raw(render_paths(j["data_paths"]))), ("输出文件", raw(render_paths(j["output_paths"]))),
                ("运行开始", fmt_dt(j["run_started_at"]) or None), ("运行结束", fmt_dt(j["run_finished_at"]) or None),
                ("结果摘要", j["result_summary"]), ("错误日志", j["error_log"]), ("备注", j["notes"]),
            ])
        with b:
            if st.button("编辑任务", key=f"je_{job_id}", width="stretch", type="primary", icon=":material/edit:"):
                job_dialog(job_id)
            ns = st.selectbox("更改运行状态", BIO_STATUSES, index=BIO_STATUSES.index(j["status"]),
                              format_func=lambda x: label("bio_status", x), key=f"jst_{job_id}",
                              help="“Completed”应在您核验输出结果后再标记")
            if ns != j["status"]:
                run_action(bioinfo.set_status, job_id, ns, success="状态已更新")
            with st.popover("删除任务记录", width="stretch"):
                st.write("只删除数据库记录与日志，不删除脚本、数据或输出文件。")
                if confirm_button("删除", key=f"jdel_{job_id}", confirm_text="确认删除"):
                    run_action(bioinfo.delete_job, job_id, success="已删除")
        t_paths, t_log, t_run = st.tabs(["路径检测", "运行日志", "运行脚本（第二阶段）"])
        with t_paths:
            rep = bioinfo.path_report(j)
            if rep:
                st.dataframe(placeholder="—", data=pd.DataFrame([{**r, "存在": "是" if r["存在"] else "否", "大小": human_size(r["大小"])} for r in rep]),
                             hide_index=True, width="stretch",
                             column_config={"修改时间": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm")})
            else:
                st.caption("未登记任何路径。")
        with t_log:
            runs = bioinfo.list_runs(job_id)
            if runs:
                for r in runs:
                    with st.expander(f"{fmt_dt(r['started_at'] or r['created_at'])} · {'系统执行' if r['source'] == 'executed' else '手动登记'}"
                                     f" · {r['status'] or ''}" + (f" · 退出码 {r['exit_code']}" if r["exit_code"] is not None else "")):
                        if r.get("command"):
                            st.code(" ".join(loads(r["command"], [])), language="bash")
                        if r.get("note"):
                            st.write(r["note"])
                        if r.get("log_path"):
                            st.caption(f"日志文件：{r['log_path']}")
                        if r.get("log_excerpt"):
                            st.code(r["log_excerpt"][-3000:])
            else:
                st.caption("暂无日志。")
            with st.form(f"mlog_{job_id}", clear_on_submit=True, border=False):
                st.markdown("**手动登记一次运行**（在 RStudio、终端或服务器上运行后记录结果）")
                note = st.text_area("日志内容 / 运行结果", height=80, key=f"ml_n_{job_id}")
                c1, c2 = st.columns(2)
                stt = c1.selectbox("运行结果状态", [None] + BIO_STATUSES, format_func=lambda x: "不更改任务状态" if x is None else label("bio_status", x),
                                   key=f"ml_s_{job_id}")
                lp = c2.text_input("日志文件路径（可选）", key=f"ml_p_{job_id}")
                if st.form_submit_button("登记"):
                    run_action(bioinfo.add_manual_log, job_id, stt, note, None, datetime.now() if stt else None,
                               lp or None, success="已登记")
        with t_run:
            run_panel(j)


page_header("生信分析", "R / Python 分析任务登记 · 脚本与数据路径管理 · 日志记录 · 结果索引。")
if st.button("登记分析任务", type="primary", icon=":material/add:"):
    job_dialog()
c1, c2 = st.columns([2, 4])
with c1:
    fp = project_selector("项目", key="bj_p", none_label="全部项目")
fs = c2.multiselect("状态", BIO_STATUSES, format_func=lambda x: label("bio_status", x), key="bj_s", placeholder="全部状态")
rows = bioinfo.list_jobs(fp, fs or None)
if not rows:
    empty_state("暂无分析任务。", "登记任务后可管理脚本路径、数据来源、输出文件与运行日志。")
else:
    df = pd.DataFrame([{
        "id": r["id"], "分析": r["name"], "项目": names.get(r["project_id"], "—") if r["project_id"] else "—",
        "语言": r["language"], "状态": label("bio_status", r["status"]),
        "脚本": Path(r["script_path"]).name if r["script_path"] else "", "最近运行": r["run_started_at"],
        "结果摘要": (r["result_summary"] or "")[:60],
    } for r in rows])
    sel = select_row(df, "bj_table", column_config={"最近运行": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm")})
    if sel:
        render_detail(sel)
    else:
        st.caption("选择一行以查看详情、日志与路径检测。")
