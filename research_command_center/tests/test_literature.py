"""文献导入、真实性机制、全文检索、笔记与核实。"""
from __future__ import annotations

import pytest
from sqlalchemy import text

from conftest import XMP_TEMPLATE, make_pdf
from rcc.db import FTS_TABLE, session_scope
from rcc.services import literature
from rcc.services.literature import DuplicateLiteratureError
from rcc.services.pdf_import import extract_pdf
from rcc.utils import ValidationError, normalize_doi, normalize_pmid, sha256_file


@pytest.mark.parametrize("raw,expected", [
    ("10.1038/S41598-025-11368-1", "10.1038/s41598-025-11368-1"),
    ("https://doi.org/10.1371/journal.pone.0337199", "10.1371/journal.pone.0337199"),
    ("doi: 10.1007/s00125-025-06484-6.", "10.1007/s00125-025-06484-6"),
])
def test_normalize_doi(raw, expected):
    assert normalize_doi(raw) == expected


@pytest.mark.parametrize("bad", ["11.1000/abc", "10.12/abc", "not a doi", "10.1000/"])
def test_invalid_doi(bad):
    with pytest.raises(ValidationError):
        normalize_doi(bad)


def test_pmid():
    assert normalize_pmid("PMID: 41252429") == "41252429"
    for bad in ("abc", "1234567890", "12-34"):
        with pytest.raises(ValidationError):
            normalize_pmid(bad)


def test_import_with_xmp_metadata(tmp_env):
    pdf = make_pdf(tmp_env / "a.pdf", ["Some article body text about HDAC6 inhibition.", "Page two mentions HDAC6 again."],
                   xmp=XMP_TEMPLATE.format(title="A Real Embedded Title For Testing", doi="10.1234/demo.5678"))
    before = sha256_file(str(pdf))
    lid = literature.import_pdf(str(pdf))
    lit = literature.get_literature(lid)
    assert lit["title"] == "A Real Embedded Title For Testing"
    assert lit["doi"] == "10.1234/demo.5678" and lit["year"] == 2023 and lit["journal"] == "Demo Journal of Testing"
    assert lit["authors"] == "Alice Zhang; Bob Li"
    assert lit["sources"]["fields"]["doi"] == "pdf_xmp"
    assert lit["verification_status"] == "Unverified"  # 自动提取的信息一律待核实
    assert lit["fulltext_indexed"] and lit["page_count"] == 2
    assert sha256_file(str(pdf)) == before  # 原文件未被修改


def test_doi_from_first_page_text_only(tmp_env):
    pdf = make_pdf(tmp_env / "b.pdf", ["Journal X. https://doi.org/10.5555/first.page.1 Received 2024",
                                       "References: 10.9999/should.not.be.used"])
    ex = extract_pdf(str(pdf))
    assert ex.doi == "10.5555/first.page.1" and ex.sources["doi"] == "pdf_text_page1"
    assert "10.9999/should.not.be.used" not in ex.doi_candidates


def test_pmid_from_text(tmp_env):
    pdf = make_pdf(tmp_env / "pm.pdf", ["Abstract ... PMID: 41252429 ..."])
    assert extract_pdf(str(pdf)).pmid == "41252429"


def test_no_metadata_means_unverified_not_guessed_from_filename(tmp_env):
    pdf = make_pdf(tmp_env / "Smith_2021_Nature_HDAC_inhibitors_in_lung_cancer.pdf", ["plain text without identifiers"])
    lid = literature.import_pdf(str(pdf))
    lit = literature.get_literature(lid)
    assert lit["title"] is None and lit["year"] is None and lit["authors"] is None and lit["doi"] is None
    assert any("不会根据文件名" in w for w in lit["sources"]["warnings"])


def test_filename_like_metadata_title_rejected(tmp_env):
    pdf = make_pdf(tmp_env / "my_paper_v3.pdf", ["text"], title="my_paper_v3")
    assert extract_pdf(str(pdf)).title is None
    pdf2 = make_pdf(tmp_env / "x.pdf", ["text"], title="Microsoft Word - draft.docx")
    assert extract_pdf(str(pdf2)).title is None


def test_multiple_dois_warns(tmp_env):
    pdf = make_pdf(tmp_env / "m.pdf", ["doi:10.1111/aaa.1  and also 10.2222/bbb.2 on first page"])
    ex = extract_pdf(str(pdf))
    assert ex.doi == "10.1111/aaa.1" and len(ex.doi_candidates) == 2
    assert any("多个 DOI" in w for w in ex.warnings)


def test_duplicates_rejected(tmp_env):
    pdf = make_pdf(tmp_env / "d.pdf", ["doi 10.3333/dup.1"])
    lid = literature.import_pdf(str(pdf))
    with pytest.raises(DuplicateLiteratureError) as e:
        literature.import_pdf(str(pdf))
    assert e.value.existing_id == lid
    with pytest.raises(DuplicateLiteratureError):
        literature.create_manual({"title": "same doi", "doi": "https://doi.org/10.3333/DUP.1"})


def test_invalid_pdf_and_missing_file(tmp_env):
    bad = tmp_env / "bad.pdf"
    bad.write_bytes(b"not really a pdf")
    with pytest.raises(ValidationError):
        literature.import_pdf(str(bad))
    with pytest.raises(ValidationError):
        literature.import_pdf(str(tmp_env / "nope.pdf"))
    with pytest.raises(ValidationError, match="绝对路径"):
        literature.import_pdf("relative.pdf")


def test_fulltext_search_pages_and_context(tmp_env):
    pdf = make_pdf(tmp_env / "f.pdf", ["Intro text only.", "Methods: we inhibited HDAC6 with tubacin in A549 cells."])
    cn = make_pdf(tmp_env / "cn.pdf", ["本研究发现组蛋白去乙酰化酶抑制剂可增强放疗敏感性。"], cjk=True)
    lid = literature.import_pdf(str(pdf))
    lid2 = literature.import_pdf(str(cn))
    res = literature.search_fulltext("tubacin")
    assert res and res[0]["literature_id"] == lid and res[0]["page"] == 2
    assert "【tubacin】" in res[0]["snippets"][0]
    res_cn = literature.search_fulltext("去乙酰化")
    assert res_cn and res_cn[0]["literature_id"] == lid2 and res_cn[0]["page"] == 1
    assert literature.search_fulltext("放疗")[0]["literature_id"] == lid2  # 少于 3 字符
    assert literature.search_fulltext('he said "quote') == []  # 特殊字符不报错
    literature.delete_literature(lid)
    with session_scope() as s:
        assert s.execute(text(f"SELECT count(*) FROM {FTS_TABLE} WHERE literature_id=:i"), {"i": lid}).scalar() == 0
    assert pdf.exists()  # 删除记录不会删除 PDF


def test_search_metadata(tmp_env):
    literature.create_manual({"title": "Acetylation in NSCLC", "authors": "Wang X; Li Y", "keywords": "HDAC, BET",
                              "doi": "10.4444/abc.1", "pmid": "123456"})
    assert len(literature.search_literature("nsclc")) == 1
    assert len(literature.search_literature("Li Y")) == 1
    assert len(literature.search_literature("BET")) == 1
    assert len(literature.search_literature("https://doi.org/10.4444/ABC.1")) == 1
    assert len(literature.search_literature("123456")) == 1
    assert literature.search_literature("nothing-here") == []


def test_manual_requires_identifier(tmp_env):
    with pytest.raises(ValidationError):
        literature.create_manual({"authors": "Someone"})
    with pytest.raises(ValidationError):
        literature.create_manual({"title": "x", "year": 1500})


def test_verification_rules(tmp_env):
    no_id = literature.create_manual({"title": "No identifiers here"})
    with pytest.raises(ValidationError, match="无法追溯"):
        literature.mark_verified(no_id, "checked", "Verified")
    lid = literature.create_manual({"title": "Has DOI", "doi": "10.5555/ver.1"})
    with pytest.raises(ValidationError, match="核实依据"):
        literature.mark_verified(lid, "", "Verified")
    literature.mark_verified(lid, "已在出版商页面逐项比对", "Verified")
    assert literature.get_literature(lid)["verification_status"] == "Verified"
    literature.update_literature(lid, {"title": "Has DOI (edited)"})
    lit = literature.get_literature(lid)
    assert lit["verification_status"] == "Partially Verified"
    assert lit["sources"]["fields"]["title"] == "manual"


def test_apply_online_metadata_with_mock(tmp_env, monkeypatch):
    lid = literature.create_manual({"doi": "10.1371/journal.pone.0337199"})

    class FakeResp:
        status_code = 200

        def json(self):
            return {"message": {"title": ["Editorial on MR studies"], "container-title": ["PLOS ONE"],
                                "author": [{"given": "A", "family": "Editor"}],
                                "issued": {"date-parts": [[2025, 11]]}, "DOI": "10.1371/journal.pone.0337199",
                                "type": "journal-article"}}

    import requests

    monkeypatch.setattr(requests, "get", lambda *a, **k: FakeResp())
    online = literature.lookup_crossref("10.1371/journal.pone.0337199")
    assert online["year"] == 2025 and online["journal"] == "PLOS ONE"
    literature.apply_online_metadata(lid, online, ["title", "journal", "year", "authors"], "crossref")
    lit = literature.get_literature(lid)
    assert lit["title"] == "Editorial on MR studies" and lit["verification_status"] == "Verified"
    assert lit["sources"]["fields"]["title"] == "crossref"


def test_online_lookup_network_failure(tmp_env, monkeypatch):
    import requests

    def boom(*a, **k):
        raise requests.ConnectionError("blocked")

    monkeypatch.setattr(requests, "get", boom)
    with pytest.raises(ValidationError, match="无法连接 Crossref"):
        literature.lookup_crossref("10.1000/abc")
    with pytest.raises(ValidationError, match="无法连接 PubMed"):
        literature.lookup_pubmed("123")


def test_notes_and_links(tmp_env):
    from rcc.services import projects

    pid = projects.create_project({"name": "笔记项目"})
    lid = literature.create_manual({"title": "Notes paper", "doi": "10.6666/n.1"})
    nid = literature.add_note(lid, "关键结果：xxx", "关键结果", "5", pid)
    assert literature.list_notes(lit_id=lid)[0]["page_ref"] == "5"
    literature.update_note(nid, "改写后的笔记", "评论与质疑", None)
    assert literature.list_notes(project_id=pid)[0]["content"] == "改写后的笔记"
    with pytest.raises(ValidationError):
        literature.add_note(lid, "   ")
    literature.link_project(lid, pid, "提供机制证据")
    literature.link_project(lid, pid, "更新后的关系")  # 重复关联 = 更新
    assert literature.project_links(lid)[0]["relevance"] == "更新后的关系"
    literature.unlink_project(lid, pid)
    assert literature.project_links(lid) == []
    literature.delete_note(nid)
    assert literature.list_notes(lit_id=lid) == []


def test_uploaded_copy_saved_in_library(tmp_env):
    p = literature.save_uploaded_copy("../../evil name.pdf", b"%PDF-1.4 test")
    from rcc.config import get_settings

    assert str(get_settings().library_dir) in p and p.endswith(".pdf")
    p2 = literature.save_uploaded_copy("../../evil name.pdf", b"%PDF-1.4 test")
    assert p2 != p  # 不覆盖已有文件
    with pytest.raises(ValidationError):
        literature.save_uploaded_copy("x.exe", b"MZ")
