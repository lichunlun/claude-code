"""数据库读写、持久化、迁移与初始数据真实性。"""
from __future__ import annotations

import sqlite3

import pytest
from sqlalchemy import inspect, text

from rcc import db, seed
from rcc.services import files, projects, publications, tasks
from rcc.utils import ValidationError

EXPECTED_TABLES = {
    "projects", "project_milestones", "tasks", "literature", "literature_notes", "project_literature",
    "experiments", "experiment_batches", "experiment_attachments", "publications", "publication_status_history",
    "bioinformatics_jobs", "bioinformatics_runs", "calendar_events", "files_index", "ai_settings",
    "ai_interactions", "activity_logs", "app_meta", "literature_fulltext",
}


def test_schema_created(tmp_env):
    names = set(inspect(db.get_engine()).get_table_names())
    assert EXPECTED_TABLES <= names
    assert db.get_meta("schema_version") == str(db.SCHEMA_VERSION)


def test_foreign_keys_enforced(tmp_env):
    with pytest.raises(ValidationError):
        tasks.create_task({"title": "x", "project_id": 99999})


def test_data_persists_after_restart(tmp_env):
    pid = projects.create_project({"name": "持久化测试项目"})
    tid = tasks.create_task({"title": "持久化任务", "project_id": pid})
    path = db.current_db_path()
    db.dispose_engine()  # 模拟应用关闭
    db.init_engine(path)  # 模拟重新启动
    assert projects.get_project(pid)["name"] == "持久化测试项目"
    assert tasks.get_task(tid)["title"] == "持久化任务"


def test_additive_migration_adds_missing_column(tmp_path):
    path = tmp_path / "old.db"
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, project_id INTEGER, title VARCHAR(500) NOT NULL, "
                "priority VARCHAR(20) NOT NULL, status VARCHAR(20) NOT NULL, created_at DATETIME NOT NULL, "
                "updated_at DATETIME NOT NULL)")
    con.execute("INSERT INTO tasks VALUES (1, NULL, '旧任务', 'Medium', 'Todo', '2026-01-01 00:00:00', '2026-01-01 00:00:00')")
    con.commit()
    con.close()
    db.dispose_engine()
    db.init_engine(path)
    cols = {c["name"] for c in inspect(db.get_engine()).get_columns("tasks")}
    assert {"due_date", "estimated_hours", "completed_at", "is_important"} <= cols
    assert tasks.get_task(1)["title"] == "旧任务"
    db.dispose_engine()


def test_seed_only_confirmed_facts(seeded):
    rows = {p["name"]: p for p in projects.list_projects(include_archived=True)}
    assert set(rows) == {seed.PROJECT_A, seed.PROJECT_B, seed.PROJECT_C}
    for p in rows.values():
        # 未确认的信息一律为空（界面显示“待填写”），不得编造
        assert p["progress"] is None
        assert p["start_date"] is None and p["expected_end_date"] is None
        assert p["lead"] is None
        assert p["scientific_question"] is None and p["core_hypothesis"] is None
        assert p["source_note"]
    b = rows[seed.PROJECT_B]
    for f in ("status", "current_stage", "next_steps", "main_risks", "participants", "key_paths"):
        assert b[f] is None, f
    # 资料中均未明确写出项目状态 → 待填写（不根据“文件存在”推断项目在进行中）
    assert all(p["status"] is None for p in rows.values())
    c = rows[seed.PROJECT_C]
    assert "C02" in c["current_stage"] and "08_Final_Recommendation.md" in c["source_note"]
    ms = projects.list_milestones(c["id"])
    assert ms and all(m["due_date"] is None for m in ms)  # 不编造日期
    # 不得编造任务、实验或截止日期
    assert tasks.list_tasks() == []
    pubs = publications.list_publications()
    assert len(pubs) == 2 and all(p["status"] == "Unconfirmed" for p in pubs)
    for p in pubs:
        for f in ("target_journal", "submission_date", "revision_due_date", "decision_date", "planned_submission_date"):
            assert p[f] is None
    # 登记的文件均为仓库中真实存在的文件
    for f in files.list_files():
        assert f["exists"]


def test_seed_idempotent(seeded):
    assert seed.seed_initial_data() is False
    assert len(projects.list_projects(include_archived=True)) == 3


def test_seed_skipped_when_projects_exist(tmp_env):
    projects.create_project({"name": "用户自己的项目"})
    assert seed.seed_initial_data() is False
    assert [p["name"] for p in projects.list_projects()] == ["用户自己的项目"]


def test_activity_log_written(tmp_env):
    pid = projects.create_project({"name": "日志测试"})
    projects.update_project(pid, {"progress": 30})
    with db.session_scope() as s:
        actions = [r[0] for r in s.execute(text("SELECT action FROM activity_logs WHERE entity_type='project' ORDER BY id"))]
    assert actions[:2] == ["create", "update"]
