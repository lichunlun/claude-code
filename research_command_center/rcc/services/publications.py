"""论文投稿全生命周期。

关键原则：状态只能由用户手动确认变更（confirmed=True），系统绝不根据日期推断
“已送外审”“已接收”等状态。每次变更写入 publication_status_history。
"""
from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import func, select

from ..constants import PUB_IN_SUBMISSION, PUB_PIPELINE, PUB_SIDE_STATUSES, PUB_STATUSES, PUB_UNCONFIRMED
from ..db import session_scope
from ..models import Publication, PublicationStatusHistory
from ..utils import (
    ValidationError,
    check_date_order,
    clean_str,
    normalize_path_lines,
    parse_date,
)
from . import crud

DATE_FIELDS = {
    "planned_submission_date": "计划投稿期限",
    "submission_date": "投稿日期",
    "editor_assigned_date": "编辑分配日期",
    "under_review_date": "外审日期",
    "revision_due_date": "修改期限",
    "decision_date": "拒稿或接收日期",
    "published_date": "发表日期",
}
# 状态 → 建议同步填写的日期字段（仅在用户确认变更时、且该字段为空时填入用户给出的事件日期）
STATUS_DATE_FIELD = {
    "Submitted": "submission_date",
    "Editor Assigned": "editor_assigned_date",
    "Under Review": "under_review_date",
    "Accepted": "decision_date",
    "Rejected": "decision_date",
    "Published": "published_date",
}


def clean_publication(data: dict, partial: bool = False) -> dict:
    out: dict[str, Any] = {}
    errors: list[str] = []

    def want(k: str) -> bool:
        return not partial or k in data

    if want("title"):
        t = clean_str(data.get("title"))
        if not t:
            errors.append("论文标题不能为空")
        out["title"] = t
    if want("project_id"):
        v = data.get("project_id")
        out["project_id"] = int(v) if v not in (None, "", 0) else None
    for k in ("author_order", "next_action", "notes", "source_note", "submission_url"):
        if want(k):
            out[k] = clean_str(data.get(k))
    for k in ("first_author", "corresponding_author"):
        if want(k):
            out[k] = clean_str(data.get(k), 300)
    if want("target_journal"):
        out["target_journal"] = clean_str(data.get("target_journal"), 500)
    if want("submission_url") and out.get("submission_url"):
        if not out["submission_url"].lower().startswith(("http://", "https://")):
            errors.append("投稿系统链接应以 http:// 或 https:// 开头")
    try:
        for k, lbl in DATE_FIELDS.items():
            if want(k):
                out[k] = parse_date(data.get(k), lbl)
        if want("file_paths"):
            out["file_paths"] = normalize_path_lines(data.get("file_paths"), "相关文件路径")
    except ValidationError as e:
        errors.extend(e.errors)
    if not partial:
        st = clean_str(data.get("status")) or "Draft"
        if st not in PUB_STATUSES:
            errors.append(f"未知的投稿状态：{st}")
        out["status"] = st
    if errors:
        raise ValidationError(errors)
    return out


def _check_dates(p: dict) -> None:
    check_date_order(p.get("submission_date"), p.get("editor_assigned_date"), "编辑分配日期不能早于投稿日期")
    check_date_order(p.get("submission_date"), p.get("under_review_date"), "外审日期不能早于投稿日期")
    check_date_order(p.get("submission_date"), p.get("decision_date"), "拒稿/接收日期不能早于投稿日期")
    check_date_order(p.get("decision_date"), p.get("published_date"), "发表日期不能早于接收日期")


def create_publication(data: dict, initial_note: Optional[str] = None) -> int:
    clean = clean_publication(data)
    _check_dates(clean)
    with session_scope() as s:
        pub = Publication(**clean)
        s.add(pub)
        s.flush()
        s.add(PublicationStatusHistory(publication_id=pub.id, from_status=None, to_status=pub.status,
                                       note=initial_note or "创建记录时的初始状态", confirmed_by_user=True))
        crud.log_activity(s, "publication", pub.id, "create", f"新建论文：{pub.title[:80]}")
        return pub.id


def update_publication(pub_id: int, data: dict) -> None:
    """编辑除状态以外的字段。状态请使用 change_status。"""
    if "status" in data:
        raise ValidationError("状态变更请使用“确认状态变更”功能")
    clean = clean_publication(data, partial=True)
    current = get_publication(pub_id)
    if current is None:
        raise ValidationError("论文记录不存在")
    merged = {**current, **clean}
    _check_dates(merged)
    crud.update(Publication, pub_id, clean, "publication", f"更新论文 #{pub_id}")


def change_status(pub_id: int, new_status: str, confirmed: bool, event_date=None, note: Optional[str] = None,
                  journal: Optional[str] = None) -> None:
    if not confirmed:
        raise ValidationError("投稿状态必须由您手动确认后才能变更（请勾选确认项）")
    if new_status not in PUB_STATUSES:
        raise ValidationError(f"未知的投稿状态：{new_status}")
    if new_status == PUB_UNCONFIRMED:
        raise ValidationError("不能把状态改回“待确认”")
    ev = parse_date(event_date, "事件日期")
    with session_scope() as s:
        pub = s.get(Publication, pub_id)
        if pub is None:
            raise ValidationError("论文记录不存在")
        old = pub.status
        if old == new_status:
            raise ValidationError("新状态与当前状态相同")
        journal = clean_str(journal, 500)
        if new_status == "Transferred" and not journal:
            raise ValidationError("转投时请填写新的目标期刊")
        pub.status = new_status
        date_field = STATUS_DATE_FIELD.get(new_status)
        if date_field and ev and getattr(pub, date_field) is None:
            setattr(pub, date_field, ev)
        if new_status == "Transferred" and journal:
            pub.target_journal = journal
        _check_dates(pub.to_dict())
        s.add(PublicationStatusHistory(publication_id=pub_id, from_status=old, to_status=new_status, event_date=ev,
                                       journal=journal or pub.target_journal, note=clean_str(note),
                                       confirmed_by_user=True))
        crud.log_activity(s, "publication", pub_id, "status_change", f"论文 #{pub_id}：{old} → {new_status}（用户确认）",
                          {"from": old, "to": new_status, "event_date": ev})


def transition_warning(old: str, new: str) -> Optional[str]:
    """跨越多个阶段的变更给出提示（仍允许，但需用户再次确认）。"""
    if old in PUB_PIPELINE and new in PUB_PIPELINE:
        gap = PUB_PIPELINE.index(new) - PUB_PIPELINE.index(old)
        if gap > 1:
            skipped = PUB_PIPELINE[PUB_PIPELINE.index(old) + 1:PUB_PIPELINE.index(new)]
            return "该变更跳过了以下阶段：" + " → ".join(skipped) + "。请确认这确实是真实发生的状态。"
        if gap < 0:
            return "该变更使状态回退到更早阶段，请确认。"
    if old in ("Rejected", "Withdrawn") and new in PUB_PIPELINE[3:]:
        return "被拒/撤稿后通常需要先“转投”或重新“投稿”，请确认。"
    return None


def history(pub_id: int) -> list[dict]:
    return crud.list_dicts(select(PublicationStatusHistory).where(PublicationStatusHistory.publication_id == pub_id)
                           .order_by(PublicationStatusHistory.id))


def delete_publication(pub_id: int) -> None:
    crud.delete(Publication, pub_id, "publication", f"删除论文记录 #{pub_id}（未删除任何文件）")


def get_publication(pub_id: Optional[int]) -> Optional[dict]:
    return crud.get(Publication, pub_id)


def list_publications(project_id: Optional[int] = None, statuses: Optional[list[str]] = None) -> list[dict]:
    stmt = select(Publication)
    if project_id:
        stmt = stmt.where(Publication.project_id == project_id)
    if statuses:
        stmt = stmt.where(Publication.status.in_(statuses))
    return crud.list_dicts(stmt.order_by(Publication.updated_at.desc()))


def status_counts() -> dict[str, int]:
    with session_scope() as s:
        rows = s.execute(select(Publication.status, func.count()).group_by(Publication.status)).all()
    counts = {k: 0 for k in PUB_STATUSES}
    for st, n in rows:
        counts[st] = n
    return counts


def count_in_submission() -> int:
    c = status_counts()
    return sum(c.get(s, 0) for s in PUB_IN_SUBMISSION)


ALL_ORDER = PUB_PIPELINE + PUB_SIDE_STATUSES + [PUB_UNCONFIRMED]
