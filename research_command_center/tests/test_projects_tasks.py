"""项目增删改查、归档、里程碑、时间线；任务状态流转、逾期、四象限、排序、日期逻辑。"""
from __future__ import annotations

from datetime import date, timedelta

import pytest

from rcc.services import literature, projects, tasks
from rcc.utils import ValidationError, today


# ------------------------------------------------------------------ projects
def test_project_crud(tmp_env):
    pid = projects.create_project({"name": "  POGLUT1 测试  ", "progress": "40", "status": "Active",
                                   "start_date": "2026-01-01", "expected_end_date": date(2026, 12, 31)})
    p = projects.get_project(pid)
    assert p["name"] == "POGLUT1 测试" and p["progress"] == 40 and p["start_date"] == date(2026, 1, 1)
    projects.update_project(pid, {"progress": 55, "next_steps": "完成 WB"})
    p = projects.get_project(pid)
    assert p["progress"] == 55 and p["next_steps"] == "完成 WB" and p["status"] == "Active"
    projects.set_archived(pid, True)
    assert projects.list_projects() == []
    assert len(projects.list_projects(include_archived=True)) == 1
    projects.set_archived(pid, False)
    projects.delete_project(pid)
    assert projects.get_project(pid) is None


@pytest.mark.parametrize("data,msg", [
    ({"name": ""}, "项目名称不能为空"),
    ({"name": "x", "progress": 120}, "完成进度"),
    ({"name": "x", "progress": "abc"}, "完成进度"),
    ({"name": "x", "status": "Unknown"}, "未知的项目状态"),
    ({"name": "x", "start_date": "2026-05-01", "expected_end_date": "2026-01-01"}, "不能早于"),
    ({"name": "x", "start_date": "2026/13/45"}, "格式无效"),
    ({"name": "x", "key_paths": "relative/path.docx"}, "绝对路径"),
])
def test_project_validation(tmp_env, data, msg):
    with pytest.raises(ValidationError) as e:
        projects.create_project(data)
    assert msg in str(e.value)


def test_project_unique_name(tmp_env):
    projects.create_project({"name": "同名"})
    with pytest.raises(ValidationError, match="重复"):
        projects.create_project({"name": "同名"})


def test_delete_blocked_when_related_data(tmp_env):
    pid = projects.create_project({"name": "有任务的项目"})
    tasks.create_task({"title": "t", "project_id": pid})
    with pytest.raises(ValidationError, match="归档"):
        projects.delete_project(pid)
    assert projects.get_project(pid) is not None


def test_milestones_and_timeline(tmp_env):
    pid = projects.create_project({"name": "时间线", "start_date": "2026-01-10"})
    projects.add_milestone(pid, {"title": "无日期里程碑"})
    projects.add_milestone(pid, {"title": "M1", "due_date": "2026-03-01", "status": "Done"})
    tasks.create_task({"title": "截止任务", "project_id": pid, "due_date": "2026-02-01"})
    items = projects.timeline(pid)
    assert [i["title"] for i in items] == ["项目开始", "截止任务", "M1", "无日期里程碑"]
    with pytest.raises(ValidationError):
        projects.add_milestone(pid, {"title": ""})


def test_missing_fields(tmp_env):
    pid = projects.create_project({"name": "缺字段"})
    assert "科学问题" in projects.missing_fields(projects.get_project(pid))


# --------------------------------------------------------------------- tasks
def test_task_status_transitions(tmp_env):
    tid = tasks.create_task({"title": "写引言"})
    t = tasks.get_task(tid)
    assert t["status"] == "Todo" and t["priority"] == "Medium" and t["completed_at"] is None
    tasks.set_status(tid, "In Progress")
    assert tasks.get_task(tid)["started_at"] is not None
    tasks.set_status(tid, "Done")
    done = tasks.get_task(tid)
    assert done["completed_at"] is not None
    tasks.set_status(tid, "Todo")  # 重新打开
    assert tasks.get_task(tid)["completed_at"] is None
    tasks.update_task(tid, {"status": "Done"})
    assert tasks.get_task(tid)["completed_at"] is not None
    with pytest.raises(ValidationError):
        tasks.set_status(tid, "Finished")


@pytest.mark.parametrize("data", [
    {"title": ""}, {"title": "x", "priority": "Urgent"}, {"title": "x", "estimated_hours": -1},
    {"title": "x", "estimated_hours": "两小时"}, {"title": "x", "due_date": "明天"}, {"title": "x" * 501},
])
def test_task_invalid_input(tmp_env, data):
    with pytest.raises(ValidationError):
        tasks.create_task(data)


def test_overdue_and_quadrants(tmp_env):
    t0 = today()
    a = tasks.create_task({"title": "逾期", "priority": "High", "due_date": t0 - timedelta(days=1)})
    b = tasks.create_task({"title": "重要不紧急", "priority": "Critical", "due_date": t0 + timedelta(days=30)})
    c = tasks.create_task({"title": "紧急不重要", "priority": "Low", "due_date": t0 + timedelta(days=2)})
    d = tasks.create_task({"title": "都不", "priority": "Medium"})
    e = tasks.create_task({"title": "手动覆盖", "priority": "Low", "is_important": True, "is_urgent": True})
    f = tasks.create_task({"title": "已完成的逾期", "priority": "High", "due_date": t0 - timedelta(days=5), "status": "Done"})
    rows = {r["id"]: r for r in tasks.list_tasks()}
    assert rows[a]["is_overdue"] and not rows[f]["is_overdue"]
    assert rows[a]["quadrant"] == "Q1" and rows[b]["quadrant"] == "Q2"
    assert rows[c]["quadrant"] == "Q3" and rows[d]["quadrant"] == "Q4" and rows[e]["quadrant"] == "Q1"
    # 边界：今天到期不算逾期
    g = tasks.create_task({"title": "今天到期", "due_date": t0})
    assert not tasks.list_tasks(search="今天到期")[0]["is_overdue"]
    assert tasks.get_task(g)


def test_top_tasks_ordering(tmp_env):
    t0 = today()
    tasks.create_task({"title": "低优先级", "priority": "Low", "due_date": t0})
    tasks.create_task({"title": "关键逾期", "priority": "Critical", "due_date": t0 - timedelta(days=3)})
    tasks.create_task({"title": "高 一周后", "priority": "High", "due_date": t0 + timedelta(days=6)})
    tasks.create_task({"title": "中 无截止", "priority": "Medium"})
    done = tasks.create_task({"title": "已完成关键", "priority": "Critical"})
    tasks.set_status(done, "Done")
    top = [t["title"] for t in tasks.top_tasks(3)]
    assert top == ["关键逾期", "高 一周后", "低优先级"]


def test_task_filters(tmp_env):
    pid = projects.create_project({"name": "P"})
    tasks.create_task({"title": "项目内", "project_id": pid, "priority": "High", "due_date": "2026-11-10"})
    tasks.create_task({"title": "无项目 搜索词", "priority": "Low", "due_date": "2026-12-10"})
    assert [t["title"] for t in tasks.list_tasks(project_ids=[pid])] == ["项目内"]
    assert [t["title"] for t in tasks.list_tasks(project_ids=[None])] == ["无项目 搜索词"]
    assert len(tasks.list_tasks(project_ids=[pid, None])) == 2
    assert [t["title"] for t in tasks.list_tasks(priorities=["Low"])] == ["无项目 搜索词"]
    assert [t["title"] for t in tasks.list_tasks(search="搜索词")] == ["无项目 搜索词"]
    assert [t["title"] for t in tasks.list_tasks(due_from=date(2026, 11, 1), due_to=date(2026, 11, 30))] == ["项目内"]
    # 类 SQL 注入字符串只是普通文本
    assert tasks.list_tasks(search="' OR 1=1 --") == []


def test_weekly_completion(tmp_env):
    tid = tasks.create_task({"title": "本周完成"})
    tasks.set_status(tid, "Done")
    weeks = tasks.weekly_completion(8)
    assert len(weeks) == 8 and weeks[-1]["completed"] == 1 and weeks[-1]["created"] == 1
    assert weeks[0]["week"].weekday() == 0


def test_project_literature_link_counts(tmp_env):
    pid = projects.create_project({"name": "文献关联"})
    lid = literature.create_manual({"title": "Manual paper title", "doi": "10.1000/xyz123"}, project_id=pid)
    assert projects.related_counts(pid)["literature"] == 1
    assert literature.literature_for_project(pid)[0]["id"] == lid
