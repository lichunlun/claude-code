"""界面渲染与基本交互（Streamlit AppTest，无需浏览器）。"""
from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from rcc.services import experiments, literature, projects, publications, tasks
from rcc.utils import today

ROOT = Path(__file__).resolve().parent.parent
PAGES = sorted(str(p) for p in (ROOT / "views").glob("*.py"))


@pytest.fixture()
def populated(seeded):
    pid = projects.list_projects()[0]["id"]
    tasks.create_task({"title": "[Demo] UI 测试任务", "priority": "Critical", "due_date": today(), "project_id": pid})
    experiments.create_experiment({"name": "[Demo] UI 实验", "project_id": pid, "experiment_date": today()})
    literature.create_manual({"title": "[Demo] UI literature", "doi": "10.7777/ui.1"}, project_id=pid)
    return seeded


@pytest.mark.parametrize("page", PAGES, ids=lambda p: Path(p).stem)
def test_page_renders_without_exception(populated, page):
    at = AppTest.from_file(page, default_timeout=60)
    at.run()
    assert not at.exception, [e.value for e in at.exception]


def test_app_entry_renders(populated):
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    at.run()
    assert not at.exception


def test_overview_metrics_match_database(populated):
    at = AppTest.from_file(str(ROOT / "views" / "overview.py"), default_timeout=60)
    at.run()
    m = {x.label: x.value for x in at.metric}
    assert m["进行中的项目"] == "0"  # 预置项目的状态均待填写，不自动推断
    assert m["待处理任务"] == "1" and m["待完成实验"] == "1" and m["投稿中论文"] == "0"


def test_overview_complete_button(populated):
    at = AppTest.from_file(str(ROOT / "views" / "overview.py"), default_timeout=60)
    at.run()
    tid = tasks.list_tasks()[0]["id"]
    at.button(key=f"done_{tid}").click().run()
    assert tasks.get_task(tid)["status"] == "Done"


def test_project_detail_page(populated):
    pid = projects.list_projects()[0]["id"]
    at = AppTest.from_file(str(ROOT / "views" / "projects.py"), default_timeout=60)
    at.query_params["project"] = str(pid)
    at.run()
    assert not at.exception
    assert any("概览" in t.label for t in at.tabs)


def test_publication_unconfirmed_notice(populated):
    at = AppTest.from_file(str(ROOT / "views" / "publications.py"), default_timeout=60)
    at.run()
    assert not at.exception
    assert len(publications.list_publications(statuses=["Unconfirmed"])) == 2
