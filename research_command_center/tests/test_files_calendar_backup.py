"""文件索引与路径检测、日历与日期逻辑、备份与恢复。"""
from __future__ import annotations

import time
from datetime import timedelta
from pathlib import Path

import pytest

from rcc.services import backup, calendar, experiments, files, projects, publications, tasks
from rcc.utils import ValidationError, sha256_file, today


# --------------------------------------------------------------------- files
def test_register_and_detect(tmp_env):
    f = tmp_env / "data.xlsx"
    f.write_bytes(b"PK fake")
    fid = files.register_file(str(f))
    row = files.list_files()[0]
    assert row["id"] == fid and row["exists"] and row["category"] == "数据表格" and row["size_bytes"] == 7
    with pytest.raises(ValidationError, match="已在索引"):
        files.register_file(str(f))
    with pytest.raises(ValidationError, match="不存在"):
        files.register_file(str(tmp_env / "missing.docx"))
    files.register_file(str(tmp_env / "later.docx"), allow_missing=True)
    with pytest.raises(ValidationError):
        files.register_file(str(tmp_env))  # 文件夹
    time.sleep(1.1)
    f.write_bytes(b"PK changed content")
    r = files.refresh_status()
    assert r["checked"] == 2 and r["changed"] >= 1 and r["missing"] == 1
    f.unlink()
    files.refresh_status([fid])
    assert files.list_files(exists=False)


def test_remove_from_index_keeps_file(tmp_env):
    f = tmp_env / "script.R"
    f.write_text("print(1)")
    h = sha256_file(str(f))
    fid = files.register_file(str(f))
    files.remove_from_index(fid)
    assert files.list_files() == [] and f.exists() and sha256_file(str(f)) == h


def test_scan_folder(tmp_env):
    root = tmp_env / "proj"
    (root / "sub").mkdir(parents=True)
    (root / ".git").mkdir()
    (root / "a.pdf").write_bytes(b"%PDF")
    (root / "sub" / "b.py").write_text("x=1")
    (root / ".git" / "c.txt").write_text("skip")
    (root / ".hidden.txt").write_text("skip")
    (root / "~$lock.docx").write_text("skip")
    res = files.scan_folder(str(root))
    assert sorted(r["name"] for r in res) == ["a.pdf", "b.py"]
    assert [r["name"] for r in files.scan_folder(str(root), [".py"])] == ["b.py"]
    assert [r["name"] for r in files.scan_folder(str(root), recursive=False)] == ["a.pdf"]
    out = files.register_many([r["path"] for r in res])
    assert len(out["added"]) == 2
    assert all(r["indexed"] for r in files.scan_folder(str(root)))
    with pytest.raises(ValidationError):
        files.scan_folder(str(tmp_env / "nope"))


def test_preview_read_only(tmp_env):
    import docx

    d = docx.Document()
    d.add_paragraph("论文第一段")
    p = tmp_env / "paper.docx"
    d.save(str(p))
    csv = tmp_env / "t.csv"
    csv.write_text("a,b\n1,2\n")
    h1, h2 = sha256_file(str(p)), sha256_file(str(csv))
    assert "论文第一段" in files.preview(str(p))["content"]
    assert files.preview(str(csv))["kind"] == "table"
    assert files.preview(str(tmp_env / "none.txt"))["kind"] == "missing"
    assert (h1, h2) == (sha256_file(str(p)), sha256_file(str(csv)))


def test_categorize():
    assert files.categorize("x.R") == "R 脚本" and files.categorize("x.PPTX") == "演示文稿"
    assert files.categorize("x.tif") == "实验图片" and files.categorize("x.unknown") == "其他"


# ------------------------------------------------------------------ calendar
def test_calendar_aggregation(tmp_env):
    t0 = today()
    pid = projects.create_project({"name": "日历项目", "expected_end_date": t0 + timedelta(days=20)})
    projects.add_milestone(pid, {"title": "里程碑", "due_date": t0 + timedelta(days=3)})
    tasks.create_task({"title": "任务截止", "due_date": t0 + timedelta(days=1), "project_id": pid})
    cancelled = tasks.create_task({"title": "取消的任务", "due_date": t0 + timedelta(days=1)})
    tasks.set_status(cancelled, "Cancelled")
    experiments.create_experiment({"name": "实验日", "experiment_date": t0 + timedelta(days=2)})
    pub = publications.create_publication({"title": "修改中论文", "status": "Revision",
                                           "revision_due_date": t0 + timedelta(days=5)})
    calendar.create_event({"title": "期末考试", "event_type": "exam", "start_date": t0 + timedelta(days=10)})
    calendar.create_event({"title": "会议", "event_type": "conference", "start_date": t0 - timedelta(days=1),
                           "end_date": t0 + timedelta(days=1)})
    evs = calendar.aggregate(t0, t0 + timedelta(days=30))
    titles = {e["title"] for e in evs}
    assert {"任务截止", "实验日", "里程碑", "期末考试", "会议"} <= titles
    assert "取消的任务" not in titles
    assert any(e["source"] == "publication" and e["ref_id"] == pub for e in evs)
    assert any(e["source"] == "project" for e in evs)
    assert [e["date"] for e in evs] == sorted(e["date"] for e in evs)
    assert calendar.aggregate(t0, t0 + timedelta(days=30), sources=["event"])[0]["source"] == "event"


def test_upcoming_and_overdue(tmp_env):
    t0 = today()
    tasks.create_task({"title": "逾期任务", "due_date": t0 - timedelta(days=4)})
    done = tasks.create_task({"title": "已完成", "due_date": t0 + timedelta(days=2)})
    tasks.set_status(done, "Done")
    tasks.create_task({"title": "第31天", "due_date": t0 + timedelta(days=31)})
    tasks.create_task({"title": "第30天", "due_date": t0 + timedelta(days=30)})
    up = calendar.upcoming(30)
    titles = [e["title"] for e in up]
    assert titles[0] == "逾期任务" and up[0]["overdue"]
    assert "已完成" not in titles and "第31天" not in titles and "第30天" in titles


def test_event_validation(tmp_env):
    t0 = today()
    with pytest.raises(ValidationError):
        calendar.create_event({"title": "x", "start_date": t0, "end_date": t0 - timedelta(days=1)})
    with pytest.raises(ValidationError):
        calendar.create_event({"title": "", "start_date": t0})
    with pytest.raises(ValidationError):
        calendar.create_event({"title": "x"})
    with pytest.raises(ValidationError):
        calendar.create_event({"title": "x", "start_date": t0, "event_type": "party"})


# -------------------------------------------------------------------- backup
def test_backup_and_restore_roundtrip(tmp_env):
    pid = projects.create_project({"name": "备份前项目"})
    b = backup.backup_database("manual")
    assert b.exists() and backup.verify_backup(b) == (True, "ok")
    projects.update_project(pid, {"name": "备份后改名"})
    projects.create_project({"name": "备份后新增"})
    pre = backup.restore_database(b)
    assert Path(pre).exists() and "pre-restore" in Path(pre).name
    names = [p["name"] for p in projects.list_projects()]
    assert names == ["备份前项目"]
    # 可撤销：从 pre-restore 再恢复
    backup.restore_database(pre)
    assert sorted(p["name"] for p in projects.list_projects()) == ["备份后改名", "备份后新增"]


def test_backup_rotation_and_kinds(tmp_env, monkeypatch):
    from rcc import config

    monkeypatch.setenv("RCC_BACKUP_KEEP", "2")
    config.reset_settings_cache()
    for _ in range(4):
        backup.backup_database("auto")
    m = backup.backup_database("manual")
    kinds = [b["kind"] for b in backup.list_backups()]
    assert kinds.count("auto") == 2 and kinds.count("manual") == 1 and m.exists()


def test_verify_rejects_bad_files(tmp_env):
    bad = tmp_env / "x.db"
    bad.write_bytes(b"garbage")
    assert backup.verify_backup(bad)[0] is False
    assert backup.verify_backup(tmp_env / "missing.db")[0] is False
    with pytest.raises(ValidationError):
        backup.restore_database(bad)


def test_auto_backup_interval(tmp_env, monkeypatch):
    from rcc import config

    monkeypatch.setenv("RCC_AUTO_BACKUP_HOURS", "24")
    config.reset_settings_cache()
    assert backup.maybe_auto_backup() is not None
    assert backup.maybe_auto_backup() is None  # 24 小时内不重复
    monkeypatch.setenv("RCC_AUTO_BACKUP_HOURS", "0")
    config.reset_settings_cache()
    assert backup.maybe_auto_backup() is None


def test_export_excel(tmp_env):
    import openpyxl

    projects.create_project({"name": "导出项目"})
    out = backup.export_excel(tmp_env / "exp.xlsx")
    wb = openpyxl.load_workbook(out)
    assert "projects" in wb.sheetnames and "tasks" in wb.sheetnames
