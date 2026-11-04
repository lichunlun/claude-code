"""测试夹具：每个测试使用独立的临时数据库（绝不触碰真实 data/ 目录）。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture()
def tmp_env(tmp_path, monkeypatch):
    monkeypatch.setenv("RCC_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.delenv("RCC_BACKUP_DIR", raising=False)
    monkeypatch.setenv("RCC_AUTO_BACKUP_HOURS", "0")
    from rcc import config, db

    config.reset_settings_cache()
    db.dispose_engine()
    assert config.get_settings().data_dir != (ROOT / "data").resolve(), "测试不得使用真实数据目录"
    db.init_engine()
    yield tmp_path
    db.dispose_engine()
    config.reset_settings_cache()


@pytest.fixture()
def seeded(tmp_env):
    from rcc import seed

    seed.seed_initial_data(repo_root=ROOT.parent)
    return tmp_env


def make_pdf(path: Path, pages: list[str], title: str | None = None, author: str | None = None,
             subject: str | None = None, xmp: str | None = None, cjk: bool = False) -> Path:
    import pymupdf

    doc = pymupdf.open()
    for text in pages:
        page = doc.new_page()
        page.insert_text((60, 72), text, fontsize=10, fontname="china-s" if cjk else "helv")
    meta = {}
    if title is not None:
        meta["title"] = title
    if author is not None:
        meta["author"] = author
    if subject is not None:
        meta["subject"] = subject
    if meta:
        doc.set_metadata(meta)
    if xmp:
        doc.set_xml_metadata(xmp)
    doc.save(str(path))
    doc.close()
    return path


XMP_TEMPLATE = """<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:prism="http://prismstandard.org/namespaces/basic/2.0/">
   <dc:title><rdf:Alt><rdf:li xml:lang="x-default">{title}</rdf:li></rdf:Alt></dc:title>
   <dc:creator><rdf:Seq><rdf:li>Alice Zhang</rdf:li><rdf:li>Bob Li</rdf:li></rdf:Seq></dc:creator>
   <prism:doi>{doi}</prism:doi>
   <prism:publicationName>Demo Journal of Testing</prism:publicationName>
   <prism:coverDate>2023-05-01</prism:coverDate>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>"""
