"""科研项目：增删改查、归档、里程碑、时间线、项目关联数据统计。"""
from __future__ import annotations

from datetime import date
from typing import Any, Optional

from sqlalchemy import func, select

from ..constants import MILESTONE_STATUSES, PROJECT_STATUSES
from ..db import session_scope
from ..models import (
    BioinformaticsJob,
    CalendarEvent,
    Experiment,
    FileIndex,
    LiteratureNote,
    Project,
    ProjectLiterature,
    ProjectMilestone,
    Publication,
    PublicationStatusHistory,
    Task,
    now,
)
from ..utils import (
    ValidationError,
    check_date_order,
    clean_str,
    normalize_path_lines,
    parse_date,
    parse_int,
)
from . import crud

TEXT_FIELDS = [
    "research_direction",
    "scientific_question",
    "core_hypothesis",
    "participants",
    "current_stage",
    "next_steps",
    "main_risks",
    "notes",
    "source_note",
]


def clean_project(data: dict, partial: bool = False) -> dict:
    out: dict[str, Any] = {}
    errors: list[str] = []
    if not partial or "name" in data:
        name = clean_str(data.get("name"), 300)
        if not name:
            errors.append("项目名称不能为空")
        out["name"] = name
    for f in TEXT_FIELDS:
        if f in data or not partial:
            out[f] = clean_str(data.get(f))
    if "lead" in data or not partial:
        out["lead"] = clean_str(data.get("lead"), 300)
    try:
        if "start_date" in data or not partial:
            out["start_date"] = parse_date(data.get("start_date"), "开始时间")
        if "expected_end_date" in data or not partial:
            out["expected_end_date"] = parse_date(data.get("expected_end_date"), "预计完成时间")
        check_date_order(out.get("start_date"), out.get("expected_end_date"), "预计完成时间不能早于开始时间")
    except ValidationError as e:
        errors.extend(e.errors)
    if "status" in data or not partial:
        status = clean_str(data.get("status"))
        if status is not None and status not in PROJECT_STATUSES:
            errors.append(f"未知的项目状态：{status}")
        out["status"] = status
    if "progress" in data or not partial:
        try:
            out["progress"] = parse_int(data.get("progress"), "完成进度", 0, 100)
        except ValidationError as e:
            errors.extend(e.errors)
    if "key_paths" in data or not partial:
        try:
            out["key_paths"] = normalize_path_lines(data.get("key_paths"), "关键文件路径")
        except ValidationError as e:
            errors.extend(e.errors)
    if errors:
        raise ValidationError(errors)
    return out


def create_project(data: dict) -> int:
    clean = clean_project(data)
    return crud.create(Project, clean, "project", f"新建项目：{clean['name']}")


def update_project(project_id: int, data: dict) -> None:
    clean = clean_project(data, partial=True)
    crud.update(Project, project_id, clean, "project", f"更新项目 #{project_id}")


def set_archived(project_id: int, archived: bool) -> None:
    with session_scope() as s:
        p = s.get(Project, project_id)
        if p is None:
            raise ValidationError("项目不存在")
        p.is_archived = archived
        p.archived_at = now() if archived else None
        crud.log_activity(s, "project", project_id, "archive" if archived else "unarchive",
                          f"{'归档' if archived else '恢复'}项目：{p.name}")


def related_counts(project_id: int) -> dict[str, int]:
    with session_scope() as s:
        def c(model, col=None):
            col = col if col is not None else model.project_id
            return s.scalar(select(func.count()).select_from(model).where(col == project_id)) or 0
        return {
            "tasks": c(Task),
            "experiments": c(Experiment),
            "publications": c(Publication),
            "bioinformatics_jobs": c(BioinformaticsJob),
            "files": c(FileIndex),
            "events": c(CalendarEvent),
            "literature": c(ProjectLiterature),
            "literature_notes": c(LiteratureNote),
        }


def delete_project(project_id: int) -> None:
    """仅允许删除没有任何关联数据的项目；否则请使用归档。不会删除任何磁盘文件。"""
    counts = related_counts(project_id)
    blocking = {k: v for k, v in counts.items() if v}
    if blocking:
        names = {
            "tasks": "任务", "experiments": "实验", "publications": "论文", "bioinformatics_jobs": "分析任务",
            "files": "文件索引", "events": "日程", "literature": "关联文献", "literature_notes": "文献笔记",
        }
        detail = "、".join(f"{names[k]} {v} 条" for k, v in blocking.items())
        raise ValidationError(f"该项目仍有关联数据（{detail}），为防止误删，请改用“归档”。")
    crud.delete(Project, project_id, "project", f"删除项目 #{project_id}")


def get_project(project_id: Optional[int]) -> Optional[dict]:
    return crud.get(Project, project_id)


def list_projects(include_archived: bool = False, statuses: Optional[list[str]] = None) -> list[dict]:
    stmt = select(Project)
    if not include_archived:
        stmt = stmt.where(Project.is_archived.is_(False))
    if statuses:
        stmt = stmt.where(Project.status.in_(statuses))
    stmt = stmt.order_by(Project.is_archived, Project.updated_at.desc())
    return crud.list_dicts(stmt)


def project_name_map(include_archived: bool = True) -> dict[int, str]:
    with session_scope() as s:
        stmt = select(Project.id, Project.name, Project.is_archived).order_by(Project.name)
        rows = s.execute(stmt).all()
        return {r.id: (r.name + ("（已归档）" if r.is_archived else "")) for r in rows
                if include_archived or not r.is_archived}


def missing_fields(project: dict) -> list[str]:
    labels = {
        "research_direction": "研究方向", "scientific_question": "科学问题", "core_hypothesis": "核心假说",
        "lead": "负责人", "participants": "参与者", "start_date": "开始时间", "expected_end_date": "预计完成时间",
        "status": "当前状态", "progress": "完成进度", "current_stage": "当前研究阶段",
        "next_steps": "下一步计划", "main_risks": "主要风险",
    }
    return [lbl for k, lbl in labels.items() if project.get(k) in (None, "")]


# ------------------------------------------------------------------ milestones
def clean_milestone(data: dict) -> dict:
    title = clean_str(data.get("title"), 300)
    if not title:
        raise ValidationError("里程碑名称不能为空")
    status = clean_str(data.get("status")) or "Planned"
    if status not in MILESTONE_STATUSES:
        raise ValidationError(f"未知的里程碑状态：{status}")
    return {
        "title": title,
        "due_date": parse_date(data.get("due_date"), "里程碑日期"),
        "status": status,
        "note": clean_str(data.get("note")),
        "sort_order": parse_int(data.get("sort_order"), "排序", 0, 10000) or 0,
    }


def add_milestone(project_id: int, data: dict) -> int:
    clean = clean_milestone(data)
    clean["project_id"] = project_id
    return crud.create(ProjectMilestone, clean, "milestone", f"项目 #{project_id} 新增里程碑：{clean['title']}")


def update_milestone(milestone_id: int, data: dict) -> None:
    crud.update(ProjectMilestone, milestone_id, clean_milestone(data), "milestone")


def delete_milestone(milestone_id: int) -> None:
    crud.delete(ProjectMilestone, milestone_id, "milestone")


def list_milestones(project_id: Optional[int] = None) -> list[dict]:
    stmt = select(ProjectMilestone)
    if project_id is not None:
        stmt = stmt.where(ProjectMilestone.project_id == project_id)
    stmt = stmt.order_by(ProjectMilestone.sort_order, ProjectMilestone.due_date.is_(None),
                         ProjectMilestone.due_date, ProjectMilestone.id)
    return crud.list_dicts(stmt)


# -------------------------------------------------------------------- timeline
def timeline(project_id: int) -> list[dict]:
    """合并项目节点、里程碑、任务、实验、投稿状态历史，按日期排序。无日期的条目排在最后。"""
    items: list[dict] = []
    p = get_project(project_id)
    if p is None:
        return items
    if p.get("start_date"):
        items.append({"date": p["start_date"], "kind": "项目", "title": "项目开始", "status": ""})
    if p.get("expected_end_date"):
        items.append({"date": p["expected_end_date"], "kind": "项目", "title": "预计完成", "status": ""})
    for m in list_milestones(project_id):
        items.append({"date": m["due_date"], "kind": "里程碑", "title": m["title"], "status": m["status"]})
    with session_scope() as s:
        for t in s.scalars(select(Task).where(Task.project_id == project_id)):
            if t.completed_at:
                items.append({"date": t.completed_at.date(), "kind": "任务完成", "title": t.title, "status": t.status})
            elif t.due_date:
                items.append({"date": t.due_date, "kind": "任务截止", "title": t.title, "status": t.status})
        for e in s.scalars(select(Experiment).where(Experiment.project_id == project_id)):
            items.append({"date": e.experiment_date, "kind": "实验", "title": e.name, "status": e.status})
        stmt = (select(PublicationStatusHistory, Publication.title)
                .join(Publication, Publication.id == PublicationStatusHistory.publication_id)
                .where(Publication.project_id == project_id))
        for h, title in s.execute(stmt):
            items.append({"date": h.event_date or h.recorded_at.date(), "kind": "投稿",
                          "title": f"{title[:60]} → {h.to_status}", "status": h.to_status})
    items.sort(key=lambda x: (x["date"] is None, x["date"] or date.max))
    return items
