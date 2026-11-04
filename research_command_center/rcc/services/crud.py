"""通用增删改查 + 操作日志。各领域模块负责校验，再调用这里落库。"""
from __future__ import annotations

from typing import Any, Optional, Type

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..db import integrity_message, session_scope
from ..models import ActivityLog, Base
from ..utils import ValidationError, dumps


def log_activity(session: Session, entity_type: str, entity_id: Optional[int], action: str,
                 summary: str = "", details: Any = None) -> None:
    session.add(ActivityLog(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        summary=summary[:1000] if summary else None,
        details=dumps(details) if details is not None else None,
    ))


def _diff(before: dict, after: dict) -> dict:
    out = {}
    for k, v in after.items():
        if k in ("updated_at", "created_at"):
            continue
        if before.get(k) != v:
            out[k] = {"from": before.get(k), "to": v}
    return out


def _integrity_message(exc: IntegrityError) -> str:
    return integrity_message(exc)


def create(model: Type[Base], data: dict, entity_type: str, summary: str = "") -> int:
    try:
        with session_scope() as s:
            obj = model(**data)
            s.add(obj)
            s.flush()
            log_activity(s, entity_type, obj.id, "create", summary or f"新建 {entity_type}")
            return obj.id
    except IntegrityError as e:
        raise ValidationError(_integrity_message(e)) from e


def update(model: Type[Base], obj_id: int, data: dict, entity_type: str, summary: str = "") -> None:
    try:
        with session_scope() as s:
            obj = s.get(model, obj_id)
            if obj is None:
                raise ValidationError(f"记录不存在（{entity_type} #{obj_id}）")
            before = obj.to_dict()
            for k, v in data.items():
                setattr(obj, k, v)
            s.flush()
            changes = _diff(before, obj.to_dict())
            if changes:
                log_activity(s, entity_type, obj_id, "update", summary or f"更新 {entity_type}", changes)
    except IntegrityError as e:
        raise ValidationError(_integrity_message(e)) from e


def delete(model: Type[Base], obj_id: int, entity_type: str, summary: str = "") -> None:
    with session_scope() as s:
        obj = s.get(model, obj_id)
        if obj is None:
            return
        snapshot = obj.to_dict()
        s.delete(obj)
        log_activity(s, entity_type, obj_id, "delete", summary or f"删除 {entity_type}", snapshot)


def get(model: Type[Base], obj_id: Optional[int]) -> Optional[dict]:
    if obj_id is None:
        return None
    with session_scope() as s:
        obj = s.get(model, obj_id)
        return obj.to_dict() if obj is not None else None


def list_dicts(stmt) -> list[dict]:
    with session_scope() as s:
        return [r.to_dict() for r in s.scalars(stmt).all()]


def all_rows(model: Type[Base], order_by=None) -> list[dict]:
    stmt = select(model)
    if order_by is not None:
        stmt = stmt.order_by(order_by)
    return list_dicts(stmt)
