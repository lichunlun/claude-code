"""文件中心：原始科研文件索引（只记录路径，不复制、不移动、不删除）。"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from rcc.constants import FILE_CATEGORIES
from rcc.services import files, projects
from rcc.ui.common import (
    bootstrap,
    confirm_button,
    empty_state,
    esc,
    fmt_dt,
    kv_block,
    page_header,
    project_selector,
    raw,
    run_action,
    select_row,
    show_errors,
    show_flash,
    tag,
)
from rcc.utils import ValidationError, human_size

bootstrap()
show_flash()
names = projects.project_name_map()

page_header("文件中心", "为 PDF、Word、Excel、R/Python 脚本、PPT、实验图片与分析结果建立索引。只记录绝对路径，绝不复制、移动或删除原始文件。")
t_idx, t_reg, t_scan = st.tabs(["文件索引", "登记文件", "扫描文件夹"])

with t_idx:
    c1, c2, c3, c4 = st.columns([2, 2, 1, 2])
    with c1:
        fp = project_selector("项目", key="fi_p", none_label="全部项目")
    fc = c2.multiselect("类别", FILE_CATEGORIES, key="fi_c", placeholder="全部类别")
    fe = c3.selectbox("存在性", ["全部", "存在", "不存在"], key="fi_e")
    q = c4.text_input("搜索路径 / 说明", key="fi_q")
    rows = files.list_files(fp, fc or None, None if fe == "全部" else fe == "存在", q or None)
    a, b = st.columns([1, 4], vertical_alignment="center")
    if a.button("重新检测全部文件", key="fi_refresh", width="stretch"):
        r = files.refresh_status()
        run_action(lambda: None, success=f"已检测 {r['checked']} 个文件：{r['missing']} 个不存在，{r['changed']} 个有变化")
    missing = sum(1 for r in rows if not r["exists"])
    b.caption(f"共 {len(rows)} 个文件" + (f"，其中 {missing} 个当前不存在（可能已移动或重命名）" if missing else ""))
    if not rows:
        empty_state("索引为空。", "在“登记文件”或“扫描文件夹”中添加。")
    else:
        df = pd.DataFrame([{
            "id": r["id"], "状态": "存在" if r["exists"] else "不存在", "文件名": r["file_name"], "类别": r["category"],
            "项目": names.get(r["project_id"], "—") if r["project_id"] else "—", "修改时间": r["modified_at"],
            "大小": human_size(r["size_bytes"]), "说明": r["description"], "路径": r["path"],
        } for r in rows])
        sel = select_row(df, "fi_table", column_config={"修改时间": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm")})
        if sel:
            f = next(r for r in rows if r["id"] == sel)
            with st.container(border=True):
                st.subheader(f["file_name"])
                st.html(f'<div style="margin:-.4rem 0 .4rem -.35rem">{tag("存在" if f["exists"] else "文件不存在", "accent" if f["exists"] else "danger")}'
                        f'{tag(f["category"] or "其他")}</div>')
                a, b = st.columns([3, 2], gap="large")
                with a:
                    kv_block([("绝对路径", raw(f'<code>{esc(f["path"])}</code>')), ("项目", names.get(f["project_id"]) if f["project_id"] else None),
                              ("最近修改", fmt_dt(f["modified_at"]) or None), ("大小", human_size(f["size_bytes"]) or None),
                              ("说明", f["description"]), ("登记时间", fmt_dt(f["created_at"])),
                              ("最近检测", fmt_dt(f["last_checked_at"]))])
                with b:
                    c1, c2 = st.columns(2)
                    if c1.button("打开文件", key=f"fo_{sel}", width="stretch", disabled=not f["exists"]):
                        run_action(files.open_in_system, f["path"], rerun=False)
                    if c2.button("打开所在位置", key=f"fr_{sel}", width="stretch", disabled=not f["exists"]):
                        run_action(files.open_in_system, f["path"], reveal=True, rerun=False)
                    with st.form(f"fe_{sel}", border=False):
                        pid = project_selector("项目", key=f"fe_p_{sel}", current=f["project_id"])
                        cat = st.selectbox("类别", FILE_CATEGORIES, index=FILE_CATEGORIES.index(f["category"]) if f["category"] in FILE_CATEGORIES else len(FILE_CATEGORIES) - 1,
                                           key=f"fe_c_{sel}")
                        desc = st.text_input("说明", f["description"] or "", key=f"fe_d_{sel}")
                        if st.form_submit_button("保存"):
                            run_action(files.update_file, sel, pid, cat, desc, success="已保存")
                    with st.popover("移出索引", width="stretch"):
                        st.write("只删除索引记录，**不会删除磁盘上的文件**。")
                        if confirm_button("移出索引", key=f"fdel_{sel}", confirm_text="确认移出"):
                            run_action(files.remove_from_index, sel, success="已移出索引（文件未受影响）")
                with st.expander("只读预览"):
                    pv = files.preview(f["path"])
                    if pv["kind"] == "missing":
                        st.warning("文件不存在。")
                    elif pv["kind"] == "image":
                        st.image(pv["content"])
                    elif pv["kind"] == "table":
                        st.caption(pv.get("meta", ""))
                        st.dataframe(placeholder="—", data=pv["content"], width="stretch")
                    elif pv["kind"] in ("text", "code"):
                        if pv.get("meta"):
                            st.caption(pv["meta"])
                        st.code(pv["content"] or "（无文本内容）", language=pv.get("lang"))
                    elif pv["kind"] == "error":
                        st.error(pv["content"])
                    else:
                        st.caption("该类型暂不支持预览，可使用“打开文件”。")

with t_reg:
    with st.form("freg", clear_on_submit=False, border=False):
        path = st.text_input("文件绝对路径 *", key="freg_path", placeholder=r"D:\Research\POGLUT1\WB\2026-11-01.tif")
        c1, c2 = st.columns(2)
        with c1:
            pid = project_selector("项目", key="freg_p")
        cat = c2.selectbox("类别", [None] + FILE_CATEGORIES, format_func=lambda x: "按扩展名自动识别" if x is None else x, key="freg_c")
        desc = st.text_input("说明", key="freg_d")
        if st.form_submit_button("登记", type="primary"):
            try:
                files.register_file(path, pid, cat, desc)
                st.success("已登记（仅记录路径）。")
            except ValidationError as e:
                show_errors(e)

with t_scan:
    st.caption("只读遍历文件夹，列出文件供您勾选后登记；不会复制或修改任何文件。隐藏文件夹与 .git、虚拟环境等会被跳过。")
    c1, c2 = st.columns([3, 1])
    folder = c1.text_input("文件夹绝对路径", key="fs_dir", placeholder=r"D:\Research\NSCLC")
    rec = c2.checkbox("包含子文件夹", True, key="fs_rec")
    exts = st.multiselect("只包含这些扩展名（留空 = 全部）",
                          [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".csv", ".r", ".rmd", ".py", ".ipynb", ".pptx", ".png",
                           ".jpg", ".tif", ".tiff", ".fastq", ".bam", ".vcf", ".rds", ".pzfx", ".md", ".txt"], key="fs_ext")
    if st.button("扫描", key="fs_go"):
        try:
            st.session_state["fs_result"] = files.scan_folder(folder, exts or None, rec)
        except ValidationError as e:
            show_errors(e)
    res = st.session_state.get("fs_result")
    if res is not None:
        if not res:
            empty_state("没有找到文件。")
        else:
            df = pd.DataFrame([{"登记": not r["indexed"], "文件": r["name"], "类别": r["category"], "大小": human_size(r["size"]),
                                "修改时间": r["mtime"], "已在索引": "是" if r["indexed"] else "", "path": r["path"]} for r in res])
            st.caption(f"找到 {len(res)} 个文件（最多显示 2000 个）")
            ed = st.data_editor(placeholder="—", data=df, hide_index=True, key="fs_editor", width="stretch",
                                disabled=["文件", "类别", "大小", "修改时间", "已在索引", "path"],
                                column_config={"path": st.column_config.TextColumn("路径"),
                                               "修改时间": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm")})
            chosen = [r["path"] for _, r in ed.iterrows() if r["登记"] and not r["已在索引"]]
            c1, c2 = st.columns([2, 3])
            with c1:
                sp = project_selector("登记到项目", key="fs_proj")
            if c2.button(f"登记所选 {len(chosen)} 个文件", type="primary", disabled=not chosen, key="fs_reg"):
                out = files.register_many(chosen, sp)
                st.session_state.pop("fs_result", None)
                run_action(lambda: None, success=f"已登记 {len(out['added'])} 个，跳过 {len(out['skipped'])} 个")
