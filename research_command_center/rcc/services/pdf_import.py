"""PDF 元数据与全文提取（只读）。

真实性规则：
- 只采信 PDF 内嵌元数据（XMP / 文档属性）与首页文本中出现的 DOI/PMID 标识符；
- 绝不根据文件名推断标题、作者、年份；
- 每个字段都记录来源，导入后一律标记为“待核实”；
- 首页出现多个 DOI 时取第一个并提示核实（正文/参考文献中的 DOI 不采用）。
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import pymupdf  # PyMuPDF >= 1.24
except ImportError:  # pragma: no cover
    import fitz as pymupdf  # type: ignore

from ..constants import SRC_PDF_INFO, SRC_PDF_TEXT, SRC_PDF_XMP
from ..utils import ValidationError, file_stat, sha256_file

DOI_TEXT_RE = re.compile(r"\b(10\.\d{4,9}/[^\s\"<>{}|\\^`\[\]]+)", re.I)
PMID_TEXT_RE = re.compile(r"\bPMID\s*[:：]?\s*(\d{4,9})\b", re.I)
YEAR_RE = re.compile(r"(19|20)\d{2}")

_NS = {
    "x": "adobe:ns:meta/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "dc": "http://purl.org/dc/elements/1.1/",
    "prism": "http://prismstandard.org/namespaces/basic/2.0/",
    "prism1": "http://prismstandard.org/namespaces/basic/1.2/",
    "prism3": "http://prismstandard.org/namespaces/basic/3.0/",
    "pdfx": "http://ns.adobe.com/pdfx/1.3/",
}
_JUNK_TITLE_PREFIXES = ("microsoft word", "microsoft powerpoint", "untitled", "无标题", "document", "doi:")
_FILE_EXT_RE = re.compile(r"\.(docx?|pdf|tex|indd|rtf|pptx?)$", re.I)


@dataclass
class PdfExtraction:
    file_path: str
    file_name: str
    file_hash: str
    file_size: Optional[int]
    page_count: int
    title: Optional[str] = None
    authors: Optional[str] = None
    year: Optional[int] = None
    journal: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    sources: dict = field(default_factory=dict)
    doi_candidates: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    pages_text: list = field(default_factory=list)

    def as_record(self) -> dict:
        return {
            "title": self.title, "authors": self.authors, "year": self.year, "journal": self.journal,
            "doi": self.doi, "pmid": self.pmid,
        }


def clean_doi_candidate(raw: str) -> Optional[str]:
    s = raw.strip().rstrip(".,;:)]}>'\"")
    # 去掉粘连在 DOI 后面的常见词
    s = re.split(r"(?i)(?:received|accepted|published|available|copyright|©)", s)[0]
    s = s.rstrip(".,;:)]}>'\"")
    if not re.match(r"^10\.\d{4,9}/\S+$", s):
        return None
    return s.lower()


def _is_junk_title(title: str, file_stem: str) -> bool:
    t = title.strip()
    low = t.lower()
    if len(t) < 8:
        return True
    if low.startswith(_JUNK_TITLE_PREFIXES):
        return True
    if _FILE_EXT_RE.search(t):
        return True
    if t.replace("_", " ").replace("-", " ").strip().lower() == file_stem.replace("_", " ").replace("-", " ").strip().lower():
        return True  # 等同于文件名：不采信（禁止由文件名推断）
    if re.fullmatch(r"[\d\W_]+", t):
        return True
    if DOI_TEXT_RE.fullmatch(t):
        return True
    return False


def _xmp_values(root: ET.Element, tag: str) -> list[str]:
    out: list[str] = []
    for prefix, uri in _NS.items():
        for el in root.iter(f"{{{uri}}}{tag}"):
            items = [li.text for li in el.iter(f"{{{_NS['rdf']}}}li") if li.text]
            if items:
                out.extend(i.strip() for i in items if i.strip())
            elif el.text and el.text.strip():
                out.append(el.text.strip())
        # 属性形式：<rdf:Description prism:doi="...">
        for el in root.iter(f"{{{_NS['rdf']}}}Description"):
            val = el.attrib.get(f"{{{uri}}}{tag}")
            if val and val.strip():
                out.append(val.strip())
    return out


def parse_xmp(xml: str) -> dict:
    result: dict = {}
    if not xml or not xml.strip():
        return result
    try:
        root = ET.fromstring(xml.encode("utf-8") if isinstance(xml, str) else xml)
    except ET.ParseError:
        return result
    for tag in ("doi",):
        for v in _xmp_values(root, tag):
            d = clean_doi_candidate(v.replace("doi:", "").replace("https://doi.org/", ""))
            if d:
                result["doi"] = d
                break
    if "doi" not in result:
        for v in _xmp_values(root, "identifier"):
            m = DOI_TEXT_RE.search(v)
            if m and (d := clean_doi_candidate(m.group(1))):
                result["doi"] = d
                break
    titles = _xmp_values(root, "title")
    if titles:
        result["title"] = titles[0]
    creators = _xmp_values(root, "creator")
    if creators:
        result["authors"] = "; ".join(creators)
    pubs = _xmp_values(root, "publicationName")
    if pubs:
        result["journal"] = pubs[0]
    for tag in ("coverDate", "publicationDate", "coverDisplayDate"):
        for v in _xmp_values(root, tag):
            m = YEAR_RE.search(v)
            if m:
                result["year"] = int(m.group(0))
                break
        if "year" in result:
            break
    return result


def _looks_like_author_list(s: str) -> bool:
    return bool(re.search(r"[,;，；]| and ", s)) or len(s.split()) >= 2


def extract_pdf(path: str, read_text: bool = True, max_pages_text: int = 2000) -> PdfExtraction:
    p = Path(path)
    if not p.exists():
        raise ValidationError(f"文件不存在：{path}")
    if p.suffix.lower() != ".pdf":
        raise ValidationError(f"不是 PDF 文件：{path}")
    st = file_stat(str(p))
    try:
        doc = pymupdf.open(str(p))  # 只读打开，不会写回
    except Exception as e:  # noqa: BLE001
        raise ValidationError(f"无法打开 PDF（可能已损坏或加密）：{p.name}（{e}）")
    try:
        if doc.needs_pass:
            raise ValidationError(f"PDF 已加密，无法读取：{p.name}")
        ex = PdfExtraction(
            file_path=str(p.resolve()), file_name=p.name, file_hash=sha256_file(str(p)),
            file_size=st.get("size"), page_count=doc.page_count,
        )
        stem = p.stem
        info = doc.metadata or {}
        try:
            xmp = parse_xmp(doc.get_xml_metadata() or "")
        except Exception:  # noqa: BLE001
            xmp = {}

        if read_text:
            for i, page in enumerate(doc):
                if i >= max_pages_text:
                    break
                ex.pages_text.append(page.get_text("text") or "")
        first_page = ex.pages_text[0] if ex.pages_text else (doc[0].get_text("text") if doc.page_count else "")

        # ---- DOI：XMP > 首页文本 > 文档属性(subject/keywords)
        page1_dois: list[str] = []
        for m in DOI_TEXT_RE.finditer(first_page or ""):
            d = clean_doi_candidate(m.group(1))
            if d and d not in page1_dois:
                page1_dois.append(d)
        ex.doi_candidates = page1_dois
        if xmp.get("doi"):
            ex.doi, ex.sources["doi"] = xmp["doi"], SRC_PDF_XMP
            if page1_dois and xmp["doi"] not in page1_dois:
                ex.warnings.append(f"内嵌元数据 DOI 与首页文本 DOI 不一致：{xmp['doi']} vs {page1_dois[0]}，请核实")
        elif page1_dois:
            ex.doi, ex.sources["doi"] = page1_dois[0], SRC_PDF_TEXT
            if len(page1_dois) > 1:
                ex.warnings.append("首页识别到多个 DOI：" + "、".join(page1_dois[:5]) + "；已暂取第一个，请核实")
        else:
            for k in ("subject", "keywords"):
                m = DOI_TEXT_RE.search(info.get(k) or "")
                if m and (d := clean_doi_candidate(m.group(1))):
                    ex.doi, ex.sources["doi"] = d, SRC_PDF_INFO
                    break
        if not ex.doi:
            ex.warnings.append("未识别到 DOI（标记为待核实，请手动补充或在线比对）")

        # ---- PMID：仅首页文本中明确的“PMID: 数字”
        m = PMID_TEXT_RE.search(first_page or "")
        if m:
            ex.pmid, ex.sources["pmid"] = str(int(m.group(1))), SRC_PDF_TEXT

        # ---- 标题
        cand = [(xmp.get("title"), SRC_PDF_XMP), (info.get("title"), SRC_PDF_INFO)]
        for t, src in cand:
            if t and not _is_junk_title(t, stem):
                ex.title, ex.sources["title"] = re.sub(r"\s+", " ", t).strip(), src
                break
        if not ex.title:
            ex.warnings.append("未识别到可信标题（系统不会根据文件名推断），请手动填写")

        # ---- 作者
        if xmp.get("authors"):
            ex.authors, ex.sources["authors"] = xmp["authors"], SRC_PDF_XMP
        elif info.get("author") and _looks_like_author_list(info["author"]):
            ex.authors, ex.sources["authors"] = info["author"].strip(), SRC_PDF_INFO

        # ---- 期刊与年份（只采信 XMP 中的出版信息；文件创建日期不是出版年份）
        if xmp.get("journal"):
            ex.journal, ex.sources["journal"] = xmp["journal"], SRC_PDF_XMP
        if xmp.get("year"):
            ex.year, ex.sources["year"] = xmp["year"], SRC_PDF_XMP

        if read_text and not any(t.strip() for t in ex.pages_text):
            ex.warnings.append("PDF 无可提取文本（可能为扫描件），全文检索不可用")
        return ex
    finally:
        doc.close()


def find_pdfs(folder: str, recursive: bool = True, limit: int = 500) -> list[str]:
    root = Path(folder)
    if not root.is_dir():
        raise ValidationError(f"文件夹不存在：{folder}")
    it = root.rglob("*") if recursive else root.glob("*")
    out: list[str] = []
    for p in it:
        if p.is_file() and p.suffix.lower() == ".pdf" and not p.name.startswith("."):
            out.append(str(p.resolve()))
            if len(out) >= limit:
                break
    return sorted(out)
