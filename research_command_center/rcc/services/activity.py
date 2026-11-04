"""操作日志查询。"""
from __future__ import annotations

from typing import Optional

from sqlalchemy import select

from ..models import ActivityLog
from . import crud


def recent(n: int = 200, entity_type: Optional[str] = None, entity_id: Optional[int] = None) -> list[dict]:
    stmt = select(ActivityLog)
    if entity_type:
        stmt = stmt.where(ActivityLog.entity_type == entity_type)
    if entity_id is not None:
        stmt = stmt.where(ActivityLog.entity_id == entity_id)
    return crud.list_dicts(stmt.order_by(ActivityLog.id.desc()).limit(n))
