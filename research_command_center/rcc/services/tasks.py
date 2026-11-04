"""跨项目任务：增删改查、状态流转、逾期、四象限、重要度排序。"""
from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any, Optional

from sqlalchemy import or_, select

from ..constants import (
    PRIORITY_WEIGHT,
    TASK_OPEN_STATUSES,
    TASK_PRIORITIES,
    TASK_STATUSES,
    URGENT_WITHIN_DAYS,
)
from ..db import session_scope
from ..models import Task, now
from ..utils import ValidationError, clean_str, parse_date, parse_float, today, week_start
from . import crud


def _tri(value: Any) -> Optional[bool]:
    """四象限覆盖值：None/'auto' = 自动。"""
    if value in (None, "", "auto"):
        return None
    if isinstance(value, bool):
        return value
    if str(value).lower() in {"1", "true", "yes", "是"}:
        return True
    if str(value).lower() in {"0", "false", "no", "否"}:
        return False
    raise ValidationError(f"无效的四象限设置：{value}")


def clean_task(data: dict, partial: bool = False) -> dict:
    out: dict[str, Any] = {}
    errors: list[str] = []

    def want(k: str) -> bool:
        return not partial or k in data

    if want("title"):
        title = clean_str(data.get("title"), 500)
        if not title:
            errors.append("任务名称不能为空")
        out["title"] = title
    if want("project_id"):
        pid = data.get("project_id")
        out["project_id"] = int(pid) if pid not in (None, "", 0) else None
    if want("notes"):
        out["notes"] = clean_str(data.get("notes"))
    if want("priority"):
        pr = clean_str(data.get("priority")) or "Medium"
        if pr not in TASK_PRIORITIES:
            errors.append(f"未知的优先级：{pr}")
        out["priority"] = pr
    if want("status"):
        st = clean_str(data.get("status")) or "Todo"
        if st not in TASK_STATUSES:
            errors.append(f"未知的任务状态：{st}")
        out["status"] = st
    try:
        if want("due_date"):
            out["due_date"] = parse_date(data.get("due_date"), "截止日期")
        if want("estimated_hours"):
            out["estimated_hours"] = parse_float(data.get("estimated_hours"), "预计耗时（小时）", 0, 10000)
        if want("is_important"):
            out["is_important"] = _tri(data.get("is_important"))
        if want("is_urgent"):
            out["is_urgent"] = _tri(data.get("is_urgent"))
    except ValidationError as e:
        errors.extend(e.errors)
    if errors:
        raise ValidationError(errors)
    return out


def _apply_status_side_effects(task: Task, new_status: str) -> None:
    if new_status == "Done":
        if task.completed_at is None:
            task.completed_at = now()
    else:
        task.completed_at = None
    if new_status == "In Progress" and task.started_at is None:
        task.started_at = now()


def create_task(data: dict) -> int:
    clean = clean_task(data)
    with session_scope() as s:
        t = Task(**clean)
        _apply_status_side_effects(t, t.status)
        s.add(t)
        s.flush()
        crud.log_activity(s, "task", t.id, "create", f"新建任务：{t.title}")
        return t.id


def update_task(task_id: int, data: dict) -> None:
    clean = clean_task(data, partial=True)
    with session_scope() as s:
        t = s.get(Task, task_id)
        if t is None:
            raise ValidationError("任务不存在")
        before = t.to_dict()
        for k, v in clean.items():
            setattr(t, k, v)
        if "status" in clean:
            _apply_status_side_effects(t, clean["status"])
        s.flush()
        changes = crud._diff(before, t.to_dict())
        if changes:
            crud.log_activity(s, "task", task_id, "update", f"更新任务：{t.title}", changes)


def set_status(task_id: int, status: str) -> None:
    if status not in TASK_STATUSES:
        raise ValidationError(f"未知的任务状态：{status}")
    with session_scope() as s:
        t = s.get(Task, task_id)
        if t is None:
            raise ValidationError("任务不存在")
        old = t.status
        if old == status:
            return
        t.status = status
        _apply_status_side_effects(t, status)
        crud.log_activity(s, "task", task_id, "status_change", f"任务「{t.title}」：{old} → {status}",
                          {"from": old, "to": status})


def delete_task(task_id: int) -> None:
    crud.delete(Task, task_id, "task")


def get_task(task_id: Optional[int]) -> Optional[dict]:
    return crud.get(Task, task_id)


def list_tasks(project_ids: Optional[list[Optional[int]]] = None, statuses: Optional[list[str]] = None,
               priorities: Optional[list[str]] = None, due_from: Optional[date] = None,
               due_to: Optional[date] = None, search: Optional[str] = None) -> list[dict]:
    stmt = select(Task)
    if project_ids:
        conds = [Task.project_id.in_([p for p in project_ids if p is not None])]
        if None in project_ids:
            conds.append(Task.project_id.is_(None))
        stmt = stmt.where(or_(*conds))
    if statuses:
        stmt = stmt.where(Task.status.in_(statuses))
    if priorities:
        stmt = stmt.where(Task.priority.in_(priorities))
    if due_from:
        stmt = stmt.where(Task.due_date >= due_from)
    if due_to:
        stmt = stmt.where(Task.due_date <= due_to)
    if search:
        like = f"%{search.strip()}%"
        stmt = stmt.where(Task.title.ilike(like) | Task.notes.ilike(like))
    stmt = stmt.order_by(Task.due_date.is_(None), Task.due_date, Task.id)
    rows = crud.list_dicts(stmt)
    for r in rows:
        r["quadrant"] = quadrant(r)
        r["is_overdue"] = is_overdue(r)
        r["score"] = importance_score(r)
    return rows


def is_open(task: dict) -> bool:
    return task.get("status") in TASK_OPEN_STATUSES


def is_overdue(task: dict, ref: Optional[date] = None) -> bool:
    d = task.get("due_date")
    return bool(is_open(task) and d is not None and d < (ref or today()))


def is_important(task: dict) -> bool:
    if task.get("is_important") is not None:
        return bool(task["is_important"])
    return task.get("priority") in ("Critical", "High")


def is_urgent(task: dict, ref: Optional[date] = None) -> bool:
    if task.get("is_urgent") is not None:
        return bool(task["is_urgent"])
    d = task.get("due_date")
    return d is not None and d <= (ref or today()) + timedelta(days=URGENT_WITHIN_DAYS)


def quadrant(task: dict, ref: Optional[date] = None) -> str:
    imp, urg = is_important(task), is_urgent(task, ref)
    if imp and urg:
        return "Q1"
    if imp:
        return "Q2"
    if urg:
        return "Q3"
    return "Q4"


def importance_score(task: dict, ref: Optional[date] = None) -> float:
    """排序规则（公开透明）：优先级权重×10 + 截止紧迫度（逾期 +15，今天 +12，3 天内 +8，7 天内 +4）。
    已完成/已取消任务为 0。"""
    if not is_open(task):
        return 0.0
    score = PRIORITY_WEIGHT.get(task.get("priority") or "Medium", 2) * 10.0
    d = task.get("due_date")
    if d is not None:
        delta = (d - (ref or today())).days
        if delta < 0:
            score += 15
        elif delta == 0:
            score += 12
        elif delta <= 3:
            score += 8
        elif delta <= 7:
            score += 4
    if task.get("status") == "Blocked":
        score -= 1  # 受阻任务略降，提示先解决阻塞
    return score


def top_tasks(n: int = 3) -> list[dict]:
    rows = [t for t in list_tasks(statuses=TASK_OPEN_STATUSES)]
    rows.sort(key=lambda t: (-t["score"], t["due_date"] or date.max, t["id"]))
    return rows[:n]


def weekly_completion(weeks: int = 8, ref: Optional[date] = None) -> list[dict]:
    """最近 N 周每周新建与完成的任务数（按周一为一周起点）。"""
    ref = ref or today()
    start = week_start(ref) - timedelta(weeks=weeks - 1)
    buckets = {start + timedelta(weeks=i): {"created": 0, "completed": 0} for i in range(weeks)}
    with session_scope() as s:
        start_dt = datetime.combine(start, datetime.min.time())
        for (created,) in s.execute(select(Task.created_at).where(Task.created_at >= start_dt)):
            w = week_start(created.date())
            if w in buckets:
                buckets[w]["created"] += 1
        for (done,) in s.execute(select(Task.completed_at).where(Task.completed_at >= start_dt)):
            w = week_start(done.date())
            if w in buckets:
                buckets[w]["completed"] += 1
    return [{"week": w, **v} for w, v in sorted(buckets.items())]
