"""日历：独立日程（考试、会议、里程碑、目标等）+ 聚合其他模块中的日期。"""
from __future__ import annotations

from datetime import date, timedelta
from typing import Optional

from sqlalchemy import or_, select

from ..constants import EVENT_TYPES, PUB_PIPELINE
from ..db import session_scope
from ..models import (
    BioinformaticsJob,
    CalendarEvent,
    Experiment,
    Project,
    ProjectMilestone,
    Publication,
    Task,
)
from ..utils import ValidationError, check_date_order, clean_str, parse_date, today
from . import crud


def clean_event(data: dict) -> dict:
    title = clean_str(data.get("title"), 500)
    errors = []
    if not title:
        errors.append("事件名称不能为空")
    et = clean_str(data.get("event_type")) or "other"
    if et not in EVENT_TYPES:
        errors.append(f"未知的事件类型：{et}")
    try:
        start = parse_date(data.get("start_date"), "开始日期")
        end = parse_date(data.get("end_date"), "结束日期")
        if start is None:
            errors.append("请填写开始日期")
        check_date_order(start, end, "结束日期不能早于开始日期")
    except ValidationError as e:
        errors.extend(e.errors)
        start = end = None
    if errors:
        raise ValidationError(errors)
    pid = data.get("project_id")
    return {"title": title, "event_type": et, "start_date": start, "end_date": end,
            "project_id": int(pid) if pid not in (None, "", 0) else None,
            "location": clean_str(data.get("location"), 500), "description": clean_str(data.get("description")),
            "is_done": bool(data.get("is_done", False))}


def create_event(data: dict) -> int:
    clean = clean_event(data)
    return crud.create(CalendarEvent, clean, "calendar_event", f"新建日程：{clean['title']}")


def update_event(event_id: int, data: dict) -> None:
    crud.update(CalendarEvent, event_id, clean_event(data), "calendar_event")


def delete_event(event_id: int) -> None:
    crud.delete(CalendarEvent, event_id, "calendar_event")


def list_events(start: Optional[date] = None, end: Optional[date] = None) -> list[dict]:
    stmt = select(CalendarEvent)
    if start:
        stmt = stmt.where(or_(CalendarEvent.end_date >= start, CalendarEvent.start_date >= start))
    if end:
        stmt = stmt.where(CalendarEvent.start_date <= end)
    return crud.list_dicts(stmt.order_by(CalendarEvent.start_date))


def aggregate(start: date, end: date, project_ids: Optional[list[int]] = None,
              sources: Optional[list[str]] = None, include_done: bool = True) -> list[dict]:
    """返回 [{date, end_date, title, source, kind, project_id, project, ref_id, done}]，按日期排序。"""
    out: list[dict] = []

    def ok(src: str, pid: Optional[int]) -> bool:
        if sources and src not in sources:
            return False
        if project_ids and pid not in project_ids:
            return False
        return True

    with session_scope() as s:
        names = dict(s.execute(select(Project.id, Project.name)).all())

        def add(d, src, kind, title, pid, ref, done, end_d=None):
            if d is None or not ok(src, pid):
                return
            if not include_done and done:
                return
            out.append({"date": d, "end_date": end_d, "title": title, "source": src, "kind": kind,
                        "project_id": pid, "project": names.get(pid), "ref_id": ref, "done": done})

        for e in s.scalars(select(CalendarEvent).where(CalendarEvent.start_date <= end,
                                                       or_(CalendarEvent.start_date >= start,
                                                           CalendarEvent.end_date >= start))):
            add(e.start_date, "event", e.event_type, e.title, e.project_id, e.id, e.is_done, e.end_date)
        for t in s.scalars(select(Task).where(Task.due_date.between(start, end), Task.status != "Cancelled")):
            add(t.due_date, "task", t.priority, t.title, t.project_id, t.id, t.status == "Done")
        for x in s.scalars(select(Experiment).where(Experiment.experiment_date.between(start, end),
                                                    Experiment.status != "Cancelled")):
            add(x.experiment_date, "experiment", x.status, x.name, x.project_id, x.id,
                x.status in ("Completed", "Failed"))
        for p in s.scalars(select(Publication)):
            submitted = p.status not in ("Draft", "Internal Review", "On Hold", "Unconfirmed")
            if p.planned_submission_date and start <= p.planned_submission_date <= end:
                add(p.planned_submission_date, "publication", "planned_submission",
                    f"计划投稿：{p.title[:50]}", p.project_id, p.id, submitted)
            if p.revision_due_date and start <= p.revision_due_date <= end:
                done = p.status != "Revision" and (p.status in PUB_PIPELINE and PUB_PIPELINE.index(p.status) > PUB_PIPELINE.index("Revision"))
                add(p.revision_due_date, "publication", "revision_due", f"修改期限：{p.title[:50]}",
                    p.project_id, p.id, done)
        for pr in s.scalars(select(Project).where(Project.is_archived.is_(False))):
            if pr.start_date and start <= pr.start_date <= end:
                add(pr.start_date, "project", "start", f"项目开始：{pr.name}", pr.id, pr.id, True)
            if pr.expected_end_date and start <= pr.expected_end_date <= end:
                add(pr.expected_end_date, "project", "end", f"项目预计完成：{pr.name}", pr.id, pr.id,
                    pr.status == "Completed")
        for m in s.scalars(select(ProjectMilestone).where(ProjectMilestone.due_date.between(start, end))):
            add(m.due_date, "milestone", m.status, m.title, m.project_id, m.id, m.status == "Done")
        for j in s.scalars(select(BioinformaticsJob).where(BioinformaticsJob.run_started_at.is_not(None))):
            d = j.run_started_at.date()
            if start <= d <= end:
                add(d, "bioinfo", j.status, f"分析运行：{j.name}", j.project_id, j.id, j.status != "Running")
    out.sort(key=lambda e: (e["date"], e["source"], e["title"]))
    return out


def upcoming(days: int = 30, ref: Optional[date] = None, include_overdue_tasks: bool = True) -> list[dict]:
    """未来 N 天未完成的截止事项；可附带已逾期但仍未完成的任务。"""
    ref = ref or today()
    items = aggregate(ref, ref + timedelta(days=days), include_done=False)
    items = [e for e in items if e["source"] != "bioinfo" and not (e["source"] == "project" and e["kind"] == "start")]
    if include_overdue_tasks:
        overdue = [e for e in aggregate(ref - timedelta(days=365), ref - timedelta(days=1), sources=["task", "publication"],
                                        include_done=False)]
        for e in overdue:
            e["overdue"] = True
        items = overdue + items
    return items
