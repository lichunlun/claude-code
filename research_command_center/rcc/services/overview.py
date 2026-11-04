"""首页统计（全部来自数据库实时查询，无任何静态演示数据）。"""
from __future__ import annotations

from sqlalchemy import func, select

from ..constants import EXPERIMENT_PENDING_STATUSES, PUB_IN_SUBMISSION, TASK_OPEN_STATUSES
from ..db import session_scope
from ..models import Experiment, Literature, Project, Publication, Task
from ..utils import today
from . import crud


def summary_counts() -> dict:
    t = today()
    with session_scope() as s:
        def count(stmt) -> int:
            return s.scalar(stmt) or 0

        return {
            "active_projects": count(select(func.count()).select_from(Project).where(
                Project.status == "Active", Project.is_archived.is_(False))),
            "projects_total": count(select(func.count()).select_from(Project).where(Project.is_archived.is_(False))),
            "projects_status_unknown": count(select(func.count()).select_from(Project).where(
                Project.status.is_(None), Project.is_archived.is_(False))),
            "published": count(select(func.count()).select_from(Publication).where(Publication.status == "Published")),
            "in_submission": count(select(func.count()).select_from(Publication).where(
                Publication.status.in_(PUB_IN_SUBMISSION))),
            "pubs_unconfirmed": count(select(func.count()).select_from(Publication).where(
                Publication.status == "Unconfirmed")),
            "pending_experiments": count(select(func.count()).select_from(Experiment).where(
                Experiment.status.in_(EXPERIMENT_PENDING_STATUSES))),
            "open_tasks": count(select(func.count()).select_from(Task).where(Task.status.in_(TASK_OPEN_STATUSES))),
            "overdue_tasks": count(select(func.count()).select_from(Task).where(
                Task.status.in_(TASK_OPEN_STATUSES), Task.due_date < t)),
            "literature": count(select(func.count()).select_from(Literature)),
        }


def recent_projects(n: int = 5) -> list[dict]:
    return crud.list_dicts(select(Project).where(Project.is_archived.is_(False))
                           .order_by(Project.updated_at.desc()).limit(n))


def project_progress() -> list[dict]:
    return [{"id": p["id"], "name": p["name"], "progress": p["progress"], "status": p["status"]}
            for p in crud.list_dicts(select(Project).where(Project.is_archived.is_(False)).order_by(Project.name))]


def task_priority_distribution() -> dict[str, int]:
    with session_scope() as s:
        rows = s.execute(select(Task.priority, func.count()).where(Task.status.in_(TASK_OPEN_STATUSES))
                         .group_by(Task.priority)).all()
    return {p: n for p, n in rows}
