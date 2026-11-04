"""文献库：检索、详情与笔记、PDF 导入（只读）、全文检索、手动录入、真实性核实。"""
from __future__ import annotations

import html as _html
from pathlib import Path
import pandas as pd
import streamlit as st

from rcc.constants import (
    LIT_TYPES,
    NOTE_TYPES,
    READING_STATUSES,
    SOURCE_LABELS,
    SRC_CROSSREF,
    SRC_PUBMED,
    VERIFICATION_STATUSES,
    label,
)
from rcc.services import files, literature, projects
from rcc.services.literature import DuplicateLiteratureError
from rcc.ui.common import (
    is_repeat_submit,
    mark_submit_done,
    bootstrap,
    code_select,
    confirm_button,
    empty_state,
    esc,
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
from rcc.utils import ValidationError, doi_url, human_size, pmid_url

bootstrap()
show_flash()

names = projects.project_name_map()
FIELD_LABELS = {"title": "标题", "authors": "作者", "year": "年份", "journal": "期刊", "doi": "DOI", "pmid": "PMID"}


def _src(sources: dict, field: str) -> str:
    s = (sources.get("fields") or {}).get(field)
    return f'<span class="rcc-small">（来源：{esc(SOURCE_LABELS.get(s, s))}）</span>' if s else ""


def _val(lit: dict, field: str) -> str:
    v = lit.get(field)
    if v in (None, ""):
        return '<span class="rcc-pending">待核实</span>'
    if field == "doi":
        return f'<a href="{esc(doi_url(v))}" target="_blank">{esc(v)}</a>'
    if field == "pmid":
        return f'<a href="{esc(pmid_url(v))}" target="_blank">{esc(v)}</a>'
    return esc(v)


@st.dialog("编辑著录信息", width="large")
def edit_dialog(lit_id: int) -> None:
    x = literature.get_literature(lit_id) or {}
    k = f"le{lit_id}_"
    st.caption("手动修改的字段会记录来源为“手动录入”。若文献已核实，修改标题/作者/期刊/年份/DOI/PMID 后会降为“部分核实”。")
    with st.form(k + "form", border=False):
        title = st.text_area("标题", x.get("title") or "", height=68, key=k + "title")
        authors = st.text_area("作者（用分号分隔）", x.get("authors") or "", height=68, key=k + "authors")
        c1, c2, c3 = st.columns([1, 2, 2])
        year = c1.text_input("年份", str(x.get("year") or ""), key=k + "year")
        journal = c2.text_input("期刊", x.get("journal") or "", key=k + "journal")
        with c3:
            ptype = code_select("文献类型", "lit_type", LIT_TYPES, key=k + "type", current=x.get("pub_type"),
                                allow_empty=True, empty_label="待核实")
        c4, c5 = st.columns(2)
        doi = c4.text_input("DOI", x.get("doi") or "", key=k + "doi", placeholder="10.xxxx/xxxxx")
        pmid = c5.text_input("PMID", x.get("pmid") or "", key=k + "pmid")
        kw = st.text_input("关键词（逗号分隔）", x.get("keywords") or "", key=k + "kw")
        tags_ = st.text_input("研究方向标签（逗号分隔）", x.get("research_tags") or "", key=k + "tags")
        abstract = st.text_area("摘要（可选）", x.get("abstract") or "", height=100, key=k + "abs")
        path = st.text_input("PDF 文件路径", x.get("file_path") or "", key=k + "path")
        if st.form_submit_button("保存", type="primary"):
            try:
                literature.update_literature(lit_id, {
                    "title": title, "authors": authors, "year": year, "journal": journal, "pub_type": ptype,
                    "doi": doi, "pmid": pmid, "keywords": kw, "research_tags": tags_, "abstract": abstract,
                    "file_path": path})
                st.session_state.setdefault("_rcc_flash", []).append(("著录信息已保存", "✅"))
                st.rerun()
            except ValidationError as e:
                show_errors(e)


def online_compare(lit: dict) -> None:
    key = f"online_{lit['id']}"
    c1, c2 = st.columns(2)
    if c1.button("与 Crossref 比对（DOI）", key=f"cr_{lit['id']}", disabled=not lit.get("doi"), width="stretch",
                 help="只发送 DOI 字符串到 api.crossref.org，不上传任何文件"):
        try:
            st.session_state[key] = (SRC_CROSSREF, literature.lookup_crossref(lit["doi"]))
        except ValidationError as e:
            show_errors(e)
    if c2.button("与 PubMed 比对（PMID）", key=f"pm_{lit['id']}", disabled=not lit.get("pmid"), width="stretch",
                 help="只发送 PMID 到 NCBI E-utilities，不上传任何文件"):
        try:
            st.session_state[key] = (SRC_PUBMED, literature.lookup_pubmed(lit["pmid"]))
        except ValidationError as e:
            show_errors(e)
    if key in st.session_state:
        src, online = st.session_state[key]
        st.markdown(f"**{'Crossref' if src == SRC_CROSSREF else 'PubMed'} 返回结果**（[打开来源]({online.get('url')})）")
        rows = []
        for f, lbl in FIELD_LABELS.items():
            if f in online:
                cur, new = lit.get(f), online.get(f)
                same = (str(cur or "").strip().lower() == str(new or "").strip().lower())
                rows.append({"字段": lbl, "key": f, "当前": cur, "在线": new, "一致": "是" if same else "否", "采用": (not same) and bool(new)})
        df = pd.DataFrame(rows)
        edited = st.data_editor(placeholder="—", data=df, hide_index=True, key=f"cmp_{lit['id']}", disabled=["字段", "当前", "在线", "一致"],
                                column_order=["字段", "当前", "在线", "一致", "采用"], width="stretch")
        chosen = [r["key"] for _, r in edited.iterrows() if r["采用"]]
        st.caption("勾选“采用”的字段会以在线记录覆盖；点击后文献标记为“已核实”，并记录比对依据。")
        if st.button("采用所选字段并标记为已核实", key=f"apply_{lit['id']}", type="primary"):
            try:
                literature.apply_online_metadata(lit["id"], online, chosen, src)
                st.session_state.pop(key, None)
                st.session_state.setdefault("_rcc_flash", []).append(("已采用在线记录并标记为已核实", "✅"))
                st.rerun()
            except ValidationError as e:
                show_errors(e)


def render_detail(lit_id: int) -> None:
    lit = literature.get_literature(lit_id)
    if not lit:
        return
    sources = lit.get("sources") or {}
    with st.container(border=True):
        st.subheader(lit.get("title") or "（标题待核实）")
        vkind = "accent" if lit["verification_status"] == "Verified" else "warn"
        st.html(f'<div style="margin:-.4rem 0 .4rem -.35rem">{tag(label("verification", lit["verification_status"]), vkind)}'
                f'{tag(label("reading_status", lit["reading_status"]))}{tag(label("lit_type", lit["pub_type"], empty="类型待核实"))}'
                f'{tag("已建立全文索引") if lit["fulltext_indexed"] else ""}</div>')
        for w in sources.get("warnings") or []:
            st.warning(w, icon="⚠️")
        left, right = st.columns([3, 2], gap="large")
        with left:
            kv_block([(FIELD_LABELS[f], raw(_val(lit, f) + _src(sources, f))) for f in FIELD_LABELS] + [
                ("关键词", lit.get("keywords")),
                ("研究方向标签", lit.get("research_tags")),
                ("PDF 文件", raw(render_paths(lit.get("file_path"), empty="未关联")
                                 + (tag("上传副本（保存在数据目录 library/）") if lit.get("is_uploaded_copy") else ""))),
                ("页数 / 大小", f"{lit['page_count'] or '—'} 页 · {human_size(lit['file_size'])}" if lit.get("page_count") else None),
                ("核实记录", lit.get("verification_note")),
                ("添加时间", fmt_dt(lit["created_at"])),
            ])
            if sources.get("doi_candidates") and len(sources["doi_candidates"]) > 1:
                st.caption("首页识别到的候选 DOI：" + "、".join(sources["doi_candidates"]))
        with right:
            st.markdown("**阅读状态**")
            rs = st.segmented_control("阅读状态", READING_STATUSES, default=lit["reading_status"],
                                      format_func=lambda x: label("reading_status", x), key=f"rs_{lit_id}",
                                      label_visibility="collapsed")
            if rs and rs != lit["reading_status"]:
                run_action(literature.set_reading_status, lit_id, rs, success="阅读状态已更新")
            b1, b2 = st.columns(2)
            if b1.button("编辑著录", key=f"edit_{lit_id}", width="stretch", icon=":material/edit:"):
                edit_dialog(lit_id)
            if b2.button("打开 PDF", key=f"open_{lit_id}", width="stretch",
                         disabled=not (lit.get("file_path") and Path(lit["file_path"]).exists())):
                run_action(files.open_in_system, lit["file_path"], rerun=False)
            b3, b4 = st.columns(2)
            if b3.button("重建全文索引", key=f"reidx_{lit_id}", width="stretch",
                         disabled=not lit.get("file_path")):
                try:
                    n = literature.reindex_fulltext(lit_id)
                    run_action(lambda: None, success=f"已索引 {n} 页文本")
                except ValidationError as e:
                    show_errors(e)
            with b4.popover("删除记录", width="stretch"):
                st.write("只删除数据库中的文献记录、笔记与全文索引；磁盘上的 PDF 不会被删除。")
                if confirm_button("删除", key=f"ldel_{lit_id}", confirm_text="确认删除该文献记录"):
                    run_action(literature.delete_literature, lit_id, success="文献记录已删除")
            with st.popover("手动标记核实状态", width="stretch"):
                with st.form(f"verify_{lit_id}", border=False):
                    vs = st.selectbox("核实状态", VERIFICATION_STATUSES, index=VERIFICATION_STATUSES.index(lit["verification_status"]),
                                      format_func=lambda x: label("verification", x), key=f"vs_{lit_id}")
                    note = st.text_area("核实依据（必填）", placeholder="例如：已在出版商页面逐项比对标题、作者、期刊、年份、DOI",
                                        key=f"vn_{lit_id}")
                    if st.form_submit_button("保存"):
                        run_action(literature.mark_verified, lit_id, note, vs, success="核实状态已更新")
        t_notes, t_proj, t_online = st.tabs(["阅读笔记", "项目关联 · 价值与局限", "在线核实"])
        with t_notes:
            notes = literature.list_notes(lit_id=lit_id)
            for n in notes:
                with st.container(border=True):
                    a, b = st.columns([6, 1])
                    meta = " · ".join(x for x in [n.get("note_type"), f"页 {n['page_ref']}" if n.get("page_ref") else None,
                                                   names.get(n["project_id"]) if n.get("project_id") else None,
                                                   fmt_dt(n["created_at"])] if x)
                    a.html(f'<div class="rcc-small">{esc(meta)}</div><div style="white-space:pre-wrap">{esc(n["content"])}</div>')
                    if b.button("删除", key=f"nd_{n['id']}"):
                        run_action(literature.delete_note, n["id"], success="笔记已删除")
            with st.form(f"note_add_{lit_id}", clear_on_submit=True, border=False):
                content = st.text_area("新增笔记", height=100, key=f"nc_{lit_id}")
                c1, c2, c3 = st.columns(3)
                ntype = c1.selectbox("类型", [None] + NOTE_TYPES, format_func=lambda x: "（不分类）" if x is None else x,
                                     key=f"nt_{lit_id}")
                page = c2.text_input("页码", key=f"np_{lit_id}")
                with c3:
                    pid = project_selector("关联项目", key=f"npj_{lit_id}")
                if st.form_submit_button("保存笔记", type="primary"):
                    ndata = {"c": content, "t": ntype, "p": page, "pid": pid}
                    if not is_repeat_submit(f"note_{lit_id}", ndata):
                        if run_action(literature.add_note, lit_id, content, ntype, page, pid, rerun=False) is not None:
                            mark_submit_done(f"note_{lit_id}", ndata)
                            run_action(lambda: None, success="笔记已保存")
        with t_proj:
            links = literature.project_links(lit_id)
            if links:
                for l_ in links:
                    a, b = st.columns([6, 1])
                    a.html(f'<div class="rcc-item"><div class="t">{esc(names.get(l_["project_id"], l_["project_id"]))}</div>'
                           f'<div class="m">{esc(l_.get("relevance") or "未填写与项目的关系")}</div></div>')
                    if b.button("取消", key=f"ul_{lit_id}_{l_['project_id']}"):
                        run_action(literature.unlink_project, lit_id, l_["project_id"], success="已取消关联")
            else:
                st.caption("尚未关联项目。")
            with st.form(f"link_{lit_id}", clear_on_submit=True, border=False):
                c1, c2 = st.columns([1, 2])
                with c1:
                    pid = project_selector("关联到项目", key=f"lk_{lit_id}", include_none=False)
                rel = c2.text_input("与项目的关系", key=f"lkr_{lit_id}")
                if st.form_submit_button("关联"):
                    if pid:
                        run_action(literature.link_project, lit_id, pid, rel, success="已关联")
            with st.form(f"val_{lit_id}", border=False):
                v = st.text_area("对项目的价值", lit.get("value_note") or "", height=80, key=f"vv_{lit_id}")
                lm = st.text_area("局限性", lit.get("limitation_note") or "", height=80, key=f"vl_{lit_id}")
                if st.form_submit_button("保存价值与局限"):
                    run_action(literature.update_literature, lit_id, {"value_note": v, "limitation_note": lm},
                               success="已保存")
        with t_online:
            st.caption("在线比对需要联网，且只在您点击时执行。系统不会自动修改著录信息，需您勾选确认。")
            online_compare(lit)


# ===================================================================== page
page_header("文献库", "本地文献数据库 · DOI/PMID 可追溯 · 无法识别的信息一律标记为“待核实”。")
tab_lib, tab_import, tab_fts, tab_manual = st.tabs(["文献库", "导入 PDF", "全文检索", "手动录入"])

with tab_lib:
    c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
    q = c1.text_input("检索（标题 / 作者 / 关键词 / DOI / PMID / 期刊）", key="lq")
    rs_f = c2.multiselect("阅读状态", READING_STATUSES, format_func=lambda x: label("reading_status", x), key="lrs",
                          placeholder="全部")
    ty_f = c3.multiselect("文献类型", LIT_TYPES, format_func=lambda x: label("lit_type", x), key="lty", placeholder="全部")
    vf = c4.multiselect("核实状态", VERIFICATION_STATUSES, format_func=lambda x: label("verification", x), key="lvf",
                        placeholder="全部")
    with st.columns([2, 6])[0]:
        pf = project_selector("按项目", key="lpf", none_label="全部项目")
    rows = literature.search_literature(q, rs_f or None, ty_f or None, pf, vf or None)
    st.caption(f"共 {len(rows)} 篇")
    if not rows:
        empty_state("文献库中没有符合条件的文献。", "可在“导入 PDF”中从本地文件导入，或在“手动录入”中添加。")
    else:
        df = pd.DataFrame([{
            "id": r["id"], "标题": r["title"] or "（标题待核实）",
            "作者": (r["authors"] or "")[:40] + ("…" if r["authors"] and len(r["authors"]) > 40 else ""),
            "年份": r["year"], "期刊": r["journal"], "DOI": r["doi"], "PMID": r["pmid"],
            "类型": label("lit_type", r["pub_type"], empty="待核实"), "阅读": label("reading_status", r["reading_status"]),
            "核实": label("verification", r["verification_status"]),
        } for r in rows])
        sel = select_row(df, "lit_table", column_config={"年份": st.column_config.NumberColumn(format="%d")})
        if sel:
            render_detail(sel)
        else:
            st.caption("选择一行以查看详情、笔记与核实信息。")

with tab_import:
    st.markdown("**从本地路径导入**（推荐：只读取文件、记录路径，不复制、不移动、不修改原文件）")
    c1, c2 = st.columns([3, 1])
    path = c1.text_input("PDF 文件或文件夹的绝对路径", key="imp_path", placeholder=r"D:\Literature\NSCLC  或  D:\Literature\paper.pdf")
    recursive = c2.checkbox("包含子文件夹", value=True, key="imp_rec")
    c3, c4 = st.columns([2, 2])
    with c3:
        imp_proj = project_selector("导入后关联到项目", key="imp_proj")
    index_text = c4.checkbox("同时建立全文索引（支持页码检索）", value=True, key="imp_idx")
    if st.button("扫描并预览元数据", key="imp_scan"):
        try:
            from rcc.services.pdf_import import find_pdfs
            from rcc.utils import normalize_path

            p_norm = normalize_path(path, "路径")
            pdfs = find_pdfs(p_norm, recursive) if p_norm and Path(p_norm).is_dir() else [p_norm]
            previews = []
            for pth in pdfs[:300]:
                try:
                    ex = literature.preview_pdf(pth)
                    previews.append({"导入": True, "文件": Path(pth).name, "标题": ex.title or "（待核实）", "DOI": ex.doi,
                                     "PMID": ex.pmid, "年份": ex.year, "来源": "、".join(f"{FIELD_LABELS[k]}:{SOURCE_LABELS.get(v, v)}"
                                                                                       for k, v in ex.sources.items()),
                                     "提示": "；".join(ex.warnings), "path": pth})
                except ValidationError as e:
                    previews.append({"导入": False, "文件": Path(pth).name, "标题": None, "DOI": None, "PMID": None,
                                     "年份": None, "来源": "", "提示": e.errors[0], "path": pth})
            st.session_state["imp_previews"] = previews
        except ValidationError as e:
            show_errors(e)
    previews = st.session_state.get("imp_previews")
    if previews:
        st.caption(f"识别到 {len(previews)} 个 PDF。元数据仅来自 PDF 内嵌信息与首页文本，导入后均标记为“待核实”。")
        edited = st.data_editor(placeholder="—", data=pd.DataFrame(previews), hide_index=True, key="imp_editor", width="stretch",
                                disabled=["文件", "标题", "DOI", "PMID", "年份", "来源", "提示"],
                                column_order=["导入", "文件", "标题", "DOI", "PMID", "年份", "来源", "提示"])
        chosen = [r["path"] for _, r in edited.iterrows() if r["导入"]]
        if st.button(f"导入所选 {len(chosen)} 篇", type="primary", disabled=not chosen, key="imp_go"):
            ok, dup, fail = 0, [], []
            bar = st.progress(0.0)
            for i, pth in enumerate(chosen):
                try:
                    literature.import_pdf(pth, imp_proj, index_text)
                    ok += 1
                except DuplicateLiteratureError as e:
                    dup.append(f"{Path(pth).name}：{e.errors[0]}")
                except ValidationError as e:
                    fail.append(f"{Path(pth).name}：{e.errors[0]}")
                bar.progress((i + 1) / len(chosen))
            st.session_state.pop("imp_previews", None)
            st.session_state["imp_result"] = (ok, dup, fail)
            st.rerun()
    if "imp_result" in st.session_state:
        ok, dup, fail = st.session_state.pop("imp_result")
        st.success(f"成功导入 {ok} 篇。")
        for d in dup:
            st.info("已存在，跳过：" + d)
        for f in fail:
            st.error("失败：" + f)

    st.divider()
    st.markdown("**上传 PDF**（会在数据目录 `library/` 中保存一份副本，适合不在本机固定位置的文件）")
    ups = st.file_uploader("选择 PDF", type=["pdf"], accept_multiple_files=True, key="imp_up")
    if ups and st.button("保存副本并导入", key="imp_up_go"):
        msgs = []
        for up in ups:
            try:
                saved = literature.save_uploaded_copy(up.name, up.getvalue())
                literature.import_pdf(saved, imp_proj, index_text, is_uploaded_copy=True)
                msgs.append(("ok", up.name))
            except ValidationError as e:
                msgs.append(("err", f"{up.name}：{e.errors[0]}"))
        for kind, m in msgs:
            (st.success if kind == "ok" else st.error)(("已导入：" if kind == "ok" else "") + m)

with tab_fts:
    st.caption("在已建立全文索引的本地 PDF 中检索关键词，返回页码与上下文。支持中英文；少于 3 个字符时使用逐页扫描。")
    q2 = st.text_input("关键词或短语", key="fts_q", placeholder="例如：HDAC6 或 去乙酰化")
    if q2:
        res = literature.search_fulltext(q2)
        if not res:
            empty_state("没有找到匹配内容。", "请确认文献已建立全文索引（导入时勾选，或在文献详情中“重建全文索引”）。")
        else:
            grouped: dict[int, list[dict]] = {}
            for r in res:
                grouped.setdefault(r["literature_id"], []).append(r)
            st.caption(f"{len(grouped)} 篇文献 · {len(res)} 页命中")
            for lid, hits in grouped.items():
                total = sum(h["hits"] for h in hits)
                with st.expander(f"#{lid} {hits[0]['title'] or '（标题待核实）'} — {total} 处命中", expanded=len(grouped) <= 3):
                    for h in sorted(hits, key=lambda h: h["page"]):
                        snips = "".join(
                            '<div class="rcc-snip">' + _html.escape(sn).replace("【", "<mark>").replace("】", "</mark>") + "</div>"
                            for sn in h["snippets"])
                        st.html(f'<div class="rcc-small">第 {h["page"]} 页 · {h["hits"]} 处</div>{snips}')

with tab_manual:
    st.caption("请至少填写标题、DOI 或 PMID 之一。手动录入的文献默认标记为“待核实”，核对后可在详情中标记。")
    with st.form("manual_lit", border=False):
        title = st.text_area("标题", height=68, key="m_title")
        authors = st.text_input("作者（分号分隔）", key="m_auth")
        c1, c2, c3 = st.columns([1, 2, 2])
        year = c1.text_input("年份", key="m_year")
        journal = c2.text_input("期刊", key="m_journal")
        with c3:
            ptype = code_select("文献类型", "lit_type", LIT_TYPES, key="m_type", allow_empty=True, empty_label="待核实")
        c4, c5 = st.columns(2)
        doi = c4.text_input("DOI", key="m_doi", placeholder="10.xxxx/xxxxx")
        pmid = c5.text_input("PMID", key="m_pmid")
        kw = st.text_input("关键词（逗号分隔）", key="m_kw")
        tg = st.text_input("研究方向标签（逗号分隔）", key="m_tags")
        fp = st.text_input("PDF 文件路径（可选）", key="m_path")
        with st.columns(2)[0]:
            pid = project_selector("关联项目", key="m_proj")
        if st.form_submit_button("保存", type="primary"):
            mdata = {"title": title, "authors": authors, "year": year, "journal": journal, "pub_type": ptype, "doi": doi,
                     "pmid": pmid, "keywords": kw, "research_tags": tg, "file_path": fp}
            if is_repeat_submit("manual_lit", {**mdata, "project": pid}):
                st.info("该文献刚刚已保存，已忽略重复提交。")
            else:
                try:
                    literature.create_manual(mdata, project_id=pid)
                    mark_submit_done("manual_lit", {**mdata, "project": pid})
                    st.success("已保存（状态：待核实）")
                except ValidationError as e:
                    show_errors(e)
