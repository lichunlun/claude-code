"""文献库：导入、编辑、检索、全文检索、笔记、项目关联、真实性核实。"""
from __future__ import annotations

import re
import urllib.parse
from pathlib import Path
from typing import Any, Optional

from sqlalchemy import delete as sa_delete
from sqlalchemy import or_, select, text

from ..config import get_settings
from ..constants import (
    LIT_TYPES,
    NOTE_TYPES,
    READING_STATUSES,
    SRC_CROSSREF,
    SRC_MANUAL,
    SRC_PUBMED,
    VERIFICATION_STATUSES,
)
from ..db import FTS_TABLE, session_scope
from ..models import Literature, LiteratureNote, ProjectLiterature, now
from ..utils import (
    ValidationError,
    clean_str,
    dumps,
    join_tags,
    loads,
    normalize_doi,
    normalize_path,
    normalize_pmid,
    parse_int,
    split_tags,
    today,
)
from . import crud
from .pdf_import import PdfExtraction, extract_pdf

IDENTITY_FIELDS = ("title", "authors", "year", "journal", "doi", "pmid")


class DuplicateLiteratureError(ValidationError):
    def __init__(self, message: str, existing_id: int):
        super().__init__(message)
        self.existing_id = existing_id


# ------------------------------------------------------------------ cleaning
def clean_literature(data: dict, partial: bool = False) -> dict:
    out: dict[str, Any] = {}
    errors: list[str] = []

    def want(k: str) -> bool:
        return not partial or k in data

    for k in ("title", "authors", "journal", "abstract", "value_note", "limitation_note", "verification_note"):
        if want(k):
            out[k] = clean_str(data.get(k))
    for k in ("keywords", "research_tags"):
        if want(k):
            out[k] = join_tags(split_tags(data.get(k)))
    try:
        if want("year"):
            out["year"] = parse_int(data.get("year"), "年份", 1800, today().year + 1)
        if want("doi"):
            out["doi"] = normalize_doi(data.get("doi"))
        if want("pmid"):
            out["pmid"] = normalize_pmid(data.get("pmid"))
        if want("file_path"):
            out["file_path"] = normalize_path(data.get("file_path"), "文献文件路径")
    except ValidationError as e:
        errors.extend(e.errors)
    if want("pub_type"):
        t = clean_str(data.get("pub_type"))
        if t is not None and t not in LIT_TYPES:
            errors.append(f"未知的文献类型：{t}")
        out["pub_type"] = t
    if want("reading_status"):
        r = clean_str(data.get("reading_status")) or "Unread"
        if r not in READING_STATUSES:
            errors.append(f"未知的阅读状态：{r}")
        out["reading_status"] = r
    if errors:
        raise ValidationError(errors)
    return out


def _check_duplicates(s, doi: Optional[str], pmid: Optional[str], file_hash: Optional[str],
                      exclude_id: Optional[int] = None) -> None:
    checks = [("DOI", Literature.doi, doi), ("PMID", Literature.pmid, pmid), ("同一 PDF 文件", Literature.file_hash, file_hash)]
    for label, col, val in checks:
        if not val:
            continue
        stmt = select(Literature.id, Literature.title).where(col == val)
        if exclude_id:
            stmt = stmt.where(Literature.id != exclude_id)
        row = s.execute(stmt).first()
        if row:
            raise DuplicateLiteratureError(
                f"文献库中已存在相同{label}的记录（#{row.id} {row.title or '标题待核实'}）", row.id)


def _initial_sources(data: dict, source: str) -> dict:
    return {"fields": {k: source for k in IDENTITY_FIELDS if data.get(k) not in (None, "")}}


# -------------------------------------------------------------------- create
def create_manual(data: dict, project_id: Optional[int] = None) -> int:
    clean = clean_literature(data)
    if not any(clean.get(k) for k in ("title", "doi", "pmid")):
        raise ValidationError("请至少填写标题、DOI 或 PMID 之一")
    verified = data.get("verification_status") in VERIFICATION_STATUSES and data.get("verification_status")
    with session_scope() as s:
        _check_duplicates(s, clean.get("doi"), clean.get("pmid"), None)
        lit = Literature(**clean)
        lit.metadata_sources = dumps(_initial_sources(clean, SRC_MANUAL))
        lit.verification_status = verified or "Unverified"
        if lit.verification_status == "Verified":
            lit.verified_at = now()
        s.add(lit)
        s.flush()
        if project_id:
            s.add(ProjectLiterature(project_id=project_id, literature_id=lit.id))
        crud.log_activity(s, "literature", lit.id, "create", f"手动录入文献：{lit.title or lit.doi or lit.pmid}")
        return lit.id


def preview_pdf(path: str) -> PdfExtraction:
    norm = normalize_path(path, "PDF 路径")
    return extract_pdf(norm, read_text=False)


def import_pdf(path: str, project_id: Optional[int] = None, index_text: bool = True,
               is_uploaded_copy: bool = False) -> int:
    """导入一篇 PDF（只读）：提取元数据 → 查重 → 入库 → 全文索引。原文件不会被修改或移动。"""
    norm = normalize_path(path, "PDF 路径")
    ex = extract_pdf(norm, read_text=True)
    with session_scope() as s:
        _check_duplicates(s, ex.doi, ex.pmid, ex.file_hash)
        lit = Literature(
            title=ex.title, authors=ex.authors, year=ex.year, journal=ex.journal, doi=ex.doi, pmid=ex.pmid,
            file_path=ex.file_path, file_hash=ex.file_hash, file_size=ex.file_size, page_count=ex.page_count,
            is_uploaded_copy=is_uploaded_copy, verification_status="Unverified",
            metadata_sources=dumps({
                "fields": dict(ex.sources),
                "doi_candidates": ex.doi_candidates,
                "warnings": ex.warnings,
                "extracted_at": now().isoformat(),
            }),
        )
        s.add(lit)
        s.flush()
        if project_id:
            s.add(ProjectLiterature(project_id=project_id, literature_id=lit.id))
        if index_text and ex.pages_text:
            _write_fulltext(s, lit.id, ex.pages_text)
            lit.fulltext_indexed = True
        crud.log_activity(s, "literature", lit.id, "import",
                          f"导入 PDF：{ex.file_name}", {"path": ex.file_path, "sources": ex.sources})
        return lit.id


def save_uploaded_copy(file_name: str, content: bytes) -> str:
    """用户通过上传按钮明确要求保存副本时使用；保存到数据目录 library/，不会覆盖已有文件。"""
    safe = re.sub(r"[^\w\-. ()一-鿿]", "_", Path(file_name).name) or "upload.pdf"
    if not safe.lower().endswith(".pdf"):
        raise ValidationError("只支持上传 PDF 文件")
    lib = get_settings().library_dir
    lib.mkdir(parents=True, exist_ok=True)
    target = lib / safe
    i = 1
    while target.exists():
        target = lib / f"{Path(safe).stem}_{i}{Path(safe).suffix}"
        i += 1
    target.write_bytes(content)
    return str(target.resolve())


# -------------------------------------------------------------------- update
def update_literature(lit_id: int, data: dict) -> None:
    clean = clean_literature(data, partial=True)
    with session_scope() as s:
        lit = s.get(Literature, lit_id)
        if lit is None:
            raise ValidationError("文献不存在")
        _check_duplicates(s, clean.get("doi"), clean.get("pmid"), None, exclude_id=lit_id)
        before = lit.to_dict()
        sources = loads(lit.metadata_sources, {}) or {}
        fields = sources.setdefault("fields", {})
        identity_changed = False
        for k, v in clean.items():
            if getattr(lit, k) != v:
                setattr(lit, k, v)
                if k in IDENTITY_FIELDS:
                    identity_changed = True
                    if v in (None, ""):
                        fields.pop(k, None)
                    else:
                        fields[k] = SRC_MANUAL
        lit.metadata_sources = dumps(sources)
        if identity_changed and lit.verification_status == "Verified":
            lit.verification_status = "Partially Verified"
            lit.verification_note = (lit.verification_note or "") + f"\n[{today()}] 核实后手动修改了著录信息，请重新核实。"
        s.flush()
        changes = crud._diff(before, lit.to_dict())
        if changes:
            crud.log_activity(s, "literature", lit_id, "update", f"更新文献 #{lit_id}", changes)


def set_reading_status(lit_id: int, status: str) -> None:
    if status not in READING_STATUSES:
        raise ValidationError("未知的阅读状态")
    crud.update(Literature, lit_id, {"reading_status": status}, "literature", f"文献 #{lit_id} 阅读状态 → {status}")


def mark_verified(lit_id: int, note: str, status: str = "Verified") -> None:
    """用户确认已人工核对（例如在出版商页面或 PubMed 上逐项比对）。"""
    if status not in VERIFICATION_STATUSES:
        raise ValidationError("未知的核实状态")
    note = clean_str(note)
    if status == "Verified" and not note:
        raise ValidationError("请填写核实依据（例如：已在 PubMed 页面逐项比对标题、作者、期刊、年份）")
    with session_scope() as s:
        lit = s.get(Literature, lit_id)
        if lit is None:
            raise ValidationError("文献不存在")
        if status == "Verified" and not (lit.doi or lit.pmid):
            raise ValidationError("没有 DOI 或 PMID 的文献无法标记为“已核实”（无法追溯）；可标记为“部分核实”")
        lit.verification_status = status
        lit.verified_at = now() if status != "Unverified" else None
        stamp = f"[{today()}] {note}" if note else f"[{today()}] 状态改为 {status}"
        lit.verification_note = ((lit.verification_note + "\n") if lit.verification_note else "") + stamp
        crud.log_activity(s, "literature", lit_id, "verify", f"文献 #{lit_id} 核实状态 → {status}", {"note": note})


def apply_online_metadata(lit_id: int, online: dict, fields_to_apply: list[str], source: str) -> None:
    """用户在比对界面中勾选后，采用在线数据库返回的字段。"""
    if source not in (SRC_CROSSREF, SRC_PUBMED):
        raise ValidationError("未知的数据来源")
    patch = {k: online.get(k) for k in fields_to_apply if k in IDENTITY_FIELDS}
    clean = clean_literature(patch, partial=True)
    with session_scope() as s:
        lit = s.get(Literature, lit_id)
        if lit is None:
            raise ValidationError("文献不存在")
        _check_duplicates(s, clean.get("doi"), clean.get("pmid"), None, exclude_id=lit_id)
        sources = loads(lit.metadata_sources, {}) or {}
        fields = sources.setdefault("fields", {})
        for k, v in clean.items():
            setattr(lit, k, v)
            if v not in (None, ""):
                fields[k] = source
        lit.metadata_sources = dumps(sources)
        ident = lit.doi if source == SRC_CROSSREF else lit.pmid
        lit.verification_status = "Verified" if ident else "Partially Verified"
        lit.verified_at = now()
        stamp = f"[{today()}] 已与 {'Crossref' if source == SRC_CROSSREF else 'PubMed'} 记录（{ident}）比对，采用字段：{', '.join(fields_to_apply) or '无'}"
        lit.verification_note = ((lit.verification_note + "\n") if lit.verification_note else "") + stamp
        crud.log_activity(s, "literature", lit_id, "verify", stamp)


def delete_literature(lit_id: int) -> None:
    """删除数据库记录及其全文索引；不会删除磁盘上的 PDF 文件。"""
    with session_scope() as s:
        s.execute(text(f"DELETE FROM {FTS_TABLE} WHERE literature_id = :i"), {"i": lit_id})
    crud.delete(Literature, lit_id, "literature", f"删除文献记录 #{lit_id}（未删除磁盘文件）")


# --------------------------------------------------------------------- query
def get_literature(lit_id: Optional[int]) -> Optional[dict]:
    d = crud.get(Literature, lit_id)
    if d is not None:
        d["sources"] = loads(d.get("metadata_sources"), {}) or {}
    return d


def search_literature(query: Optional[str] = None, reading_statuses: Optional[list[str]] = None,
                      pub_types: Optional[list[str]] = None, project_id: Optional[int] = None,
                      verification: Optional[list[str]] = None) -> list[dict]:
    stmt = select(Literature)
    q = clean_str(query)
    if q:
        like = f"%{q}%"
        conds = [Literature.title.ilike(like), Literature.authors.ilike(like), Literature.keywords.ilike(like),
                 Literature.research_tags.ilike(like), Literature.journal.ilike(like),
                 Literature.doi.ilike(like), Literature.pmid == q.strip()]
        try:
            d = normalize_doi(q)
            if d:
                conds.append(Literature.doi == d)
        except ValidationError:
            pass
        stmt = stmt.where(or_(*conds))
    if reading_statuses:
        stmt = stmt.where(Literature.reading_status.in_(reading_statuses))
    if pub_types:
        stmt = stmt.where(Literature.pub_type.in_(pub_types))
    if verification:
        stmt = stmt.where(Literature.verification_status.in_(verification))
    if project_id:
        stmt = stmt.join(ProjectLiterature, ProjectLiterature.literature_id == Literature.id).where(
            ProjectLiterature.project_id == project_id)
    stmt = stmt.order_by(Literature.created_at.desc(), Literature.id.desc())
    return crud.list_dicts(stmt)


def recent_literature(n: int = 5) -> list[dict]:
    return crud.list_dicts(select(Literature).order_by(Literature.created_at.desc(), Literature.id.desc()).limit(n))


# ----------------------------------------------------------------- full text
def _write_fulltext(s, lit_id: int, pages: list[str]) -> None:
    s.execute(text(f"DELETE FROM {FTS_TABLE} WHERE literature_id = :i"), {"i": lit_id})
    for i, content in enumerate(pages, start=1):
        if content and content.strip():
            s.execute(text(f"INSERT INTO {FTS_TABLE}(content, literature_id, page) VALUES (:c, :i, :p)"),
                      {"c": content, "i": lit_id, "p": i})


def reindex_fulltext(lit_id: int) -> int:
    lit = get_literature(lit_id)
    if not lit or not lit.get("file_path"):
        raise ValidationError("该文献没有关联 PDF 文件")
    if not Path(lit["file_path"]).exists():
        raise ValidationError(f"PDF 文件不存在：{lit['file_path']}")
    ex = extract_pdf(lit["file_path"], read_text=True)
    with session_scope() as s:
        _write_fulltext(s, lit_id, ex.pages_text)
        obj = s.get(Literature, lit_id)
        obj.fulltext_indexed = any(t.strip() for t in ex.pages_text)
        obj.page_count = ex.page_count
        crud.log_activity(s, "literature", lit_id, "reindex", f"重建全文索引 #{lit_id}")
    return sum(1 for t in ex.pages_text if t.strip())


def _snippets(content: str, query: str, width: int = 70, max_n: int = 3) -> tuple[list[str], int]:
    flat = re.sub(r"\s+", " ", content)
    low, q = flat.lower(), query.lower()
    out, pos, count = [], 0, 0
    while True:
        idx = low.find(q, pos)
        if idx < 0:
            break
        count += 1
        if len(out) < max_n:
            a, b = max(0, idx - width), min(len(flat), idx + len(q) + width)
            out.append(("…" if a > 0 else "") + flat[a:idx] + "【" + flat[idx:idx + len(q)] + "】"
                       + flat[idx + len(q):b] + ("…" if b < len(flat) else ""))
        pos = idx + len(q)
    return out, count


def search_fulltext(query: str, limit: int = 100) -> list[dict]:
    """返回 [{literature_id, title, page, hits, snippets}]，页码从 1 开始。"""
    q = clean_str(query)
    if not q:
        return []
    with session_scope() as s:
        if len(q) >= 3:
            phrase = '"' + q.replace('"', '""') + '"'
            try:
                rows = s.execute(text(
                    f"SELECT literature_id, page, content FROM {FTS_TABLE} WHERE {FTS_TABLE} MATCH :m LIMIT :l"),
                    {"m": phrase, "l": limit * 3}).all()
            except Exception:  # noqa: BLE001
                rows = []
            if not rows:  # 退回子串扫描（兼容 unicode61 分词与标点）
                rows = s.execute(text(
                    f"SELECT literature_id, page, content FROM {FTS_TABLE} WHERE content LIKE :q LIMIT :l"),
                    {"q": f"%{q}%", "l": limit * 3}).all()
        else:
            rows = s.execute(text(
                f"SELECT literature_id, page, content FROM {FTS_TABLE} WHERE content LIKE :q LIMIT :l"),
                {"q": f"%{q}%", "l": limit * 3}).all()
        titles = dict(s.execute(select(Literature.id, Literature.title)).all())
    results = []
    for lit_id, page, content in rows:
        snippets, hits = _snippets(content or "", q)
        if hits:
            results.append({"literature_id": int(lit_id), "title": titles.get(int(lit_id)), "page": int(page),
                            "hits": hits, "snippets": snippets})
    results.sort(key=lambda r: (-r["hits"], r["literature_id"], r["page"]))
    return results[:limit]


# --------------------------------------------------------------------- notes
def add_note(lit_id: int, content: str, note_type: Optional[str] = None, page_ref: Optional[str] = None,
             project_id: Optional[int] = None) -> int:
    c = clean_str(content)
    if not c:
        raise ValidationError("笔记内容不能为空")
    if note_type and note_type not in NOTE_TYPES:
        raise ValidationError("未知的笔记类型")
    return crud.create(LiteratureNote, {
        "literature_id": lit_id, "content": c, "note_type": note_type,
        "page_ref": clean_str(page_ref, 50), "project_id": project_id or None,
    }, "literature_note", f"文献 #{lit_id} 新增笔记")


def update_note(note_id: int, content: str, note_type: Optional[str], page_ref: Optional[str]) -> None:
    c = clean_str(content)
    if not c:
        raise ValidationError("笔记内容不能为空")
    crud.update(LiteratureNote, note_id, {"content": c, "note_type": note_type, "page_ref": clean_str(page_ref, 50)},
                "literature_note")


def delete_note(note_id: int) -> None:
    crud.delete(LiteratureNote, note_id, "literature_note")


def list_notes(lit_id: Optional[int] = None, project_id: Optional[int] = None) -> list[dict]:
    stmt = select(LiteratureNote)
    if lit_id is not None:
        stmt = stmt.where(LiteratureNote.literature_id == lit_id)
    if project_id is not None:
        stmt = stmt.where(LiteratureNote.project_id == project_id)
    return crud.list_dicts(stmt.order_by(LiteratureNote.created_at.desc()))


# --------------------------------------------------------- project relations
def link_project(lit_id: int, project_id: int, relevance: Optional[str] = None) -> None:
    with session_scope() as s:
        row = s.get(ProjectLiterature, (project_id, lit_id))
        if row is None:
            s.add(ProjectLiterature(project_id=project_id, literature_id=lit_id, relevance=clean_str(relevance)))
        else:
            row.relevance = clean_str(relevance)
        crud.log_activity(s, "literature", lit_id, "link_project", f"文献 #{lit_id} 关联项目 #{project_id}")


def unlink_project(lit_id: int, project_id: int) -> None:
    with session_scope() as s:
        s.execute(sa_delete(ProjectLiterature).where(ProjectLiterature.literature_id == lit_id,
                                                     ProjectLiterature.project_id == project_id))
        crud.log_activity(s, "literature", lit_id, "unlink_project", f"文献 #{lit_id} 取消关联项目 #{project_id}")


def project_links(lit_id: int) -> list[dict]:
    with session_scope() as s:
        rows = s.scalars(select(ProjectLiterature).where(ProjectLiterature.literature_id == lit_id)).all()
        return [r.to_dict() for r in rows]


def literature_for_project(project_id: int) -> list[dict]:
    with session_scope() as s:
        stmt = (select(Literature, ProjectLiterature.relevance)
                .join(ProjectLiterature, ProjectLiterature.literature_id == Literature.id)
                .where(ProjectLiterature.project_id == project_id)
                .order_by(Literature.year.desc().nulls_last(), Literature.id.desc()))
        out = []
        for lit, rel in s.execute(stmt):
            d = lit.to_dict()
            d["relevance"] = rel
            out.append(d)
        return out


# --------------------------------------------------------- online lookups
USER_AGENT = "ResearchCommandCenter/1.0 (local desktop research app)"


def lookup_crossref(doi: str, timeout: float = 12.0) -> dict:
    """用户主动点击时才调用；只发送 DOI 字符串，不上传任何文件。"""
    import requests

    d = normalize_doi(doi)
    url = "https://api.crossref.org/works/" + urllib.parse.quote(d, safe="/")
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    except requests.RequestException as e:
        raise ValidationError(f"无法连接 Crossref（网络不可用或被拦截）：{e.__class__.__name__}")
    if r.status_code == 404:
        raise ValidationError(f"Crossref 中未找到该 DOI：{d}（DOI 可能有误，请核实）")
    if r.status_code != 200:
        raise ValidationError(f"Crossref 返回错误：HTTP {r.status_code}")
    m = r.json().get("message", {})
    authors = []
    for a in m.get("author", []) or []:
        name = " ".join(x for x in (a.get("given"), a.get("family")) if x) or a.get("name")
        if name:
            authors.append(name)
    year = None
    for key in ("published-print", "published-online", "issued", "published"):
        parts = (m.get(key) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            year = int(parts[0][0])
            break
    return {
        "title": (m.get("title") or [None])[0],
        "authors": "; ".join(authors) or None,
        "year": year,
        "journal": (m.get("container-title") or [None])[0],
        "doi": (m.get("DOI") or d).lower(),
        "type": m.get("type"),
        "url": f"https://doi.org/{d}",
    }


def lookup_pubmed(pmid: str, timeout: float = 12.0) -> dict:
    import requests

    p = normalize_pmid(pmid)
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    try:
        r = requests.get(url, params={"db": "pubmed", "id": p, "retmode": "json"},
                         headers={"User-Agent": USER_AGENT}, timeout=timeout)
    except requests.RequestException as e:
        raise ValidationError(f"无法连接 PubMed（网络不可用或被拦截）：{e.__class__.__name__}")
    if r.status_code != 200:
        raise ValidationError(f"PubMed 返回错误：HTTP {r.status_code}")
    res = (r.json().get("result") or {}).get(p)
    if not res or res.get("error"):
        raise ValidationError(f"PubMed 中未找到该 PMID：{p}（请核实）")
    doi = None
    for aid in res.get("articleids", []):
        if aid.get("idtype") == "doi":
            doi = aid.get("value")
    year = None
    m = re.search(r"(19|20)\d{2}", res.get("pubdate") or "")
    if m:
        year = int(m.group(0))
    return {
        "title": (res.get("title") or "").rstrip(".") or None,
        "authors": "; ".join(a.get("name") for a in res.get("authors", []) if a.get("name")) or None,
        "year": year,
        "journal": res.get("fulljournalname") or res.get("source"),
        "pmid": p,
        "doi": doi.lower() if doi else None,
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{p}/",
    }
