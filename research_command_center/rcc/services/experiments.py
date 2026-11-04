"""电子实验记录：实验、批次、附件（只建立引用，不修改原始数据）、参数对比。"""
from __future__ import annotations

from typing import Any, Optional

import pandas as pd
from sqlalchemy import select

from ..constants import (
    ATTACHMENT_KINDS,
    EXPERIMENT_OUTCOMES,
    EXPERIMENT_PENDING_STATUSES,
    EXPERIMENT_STATUSES,
)
from ..db import session_scope
from ..models import Experiment, ExperimentAttachment, ExperimentBatch, now
from ..utils import (
    ValidationError,
    clean_str,
    dumps,
    file_stat,
    is_null,
    loads,
    normalize_path,
    parse_date,
)
from . import crud

TEXT_FIELDS = ["purpose", "groups", "model_system", "reagents", "instruments", "result_summary",
               "failure_reason", "next_experiment", "notes"]


def clean_parameters(params: Any) -> Optional[str]:
    """参数统一保存为 [{name, value, unit}] JSON。接受列表/字典/DataFrame。"""
    if params is None:
        return None
    if isinstance(params, pd.DataFrame):
        params = params.to_dict("records")
    if isinstance(params, dict):
        params = [{"name": k, "value": v, "unit": None} for k, v in params.items()]
    rows = []
    seen = set()
    for p in params or []:
        name = clean_str(p.get("name") if isinstance(p, dict) else None, 200)
        if not name:
            continue
        if name in seen:
            raise ValidationError(f"实验参数名重复：{name}")
        seen.add(name)
        val = p.get("value")
        val = None if is_null(val) else str(val).strip() or None
        unit = clean_str(p.get("unit"), 50)
        rows.append({"name": name, "value": val, "unit": unit})
    return dumps(rows) if rows else None


def clean_experiment(data: dict, partial: bool = False) -> dict:
    out: dict[str, Any] = {}
    errors: list[str] = []

    def want(k: str) -> bool:
        return not partial or k in data

    if want("name"):
        name = clean_str(data.get("name"), 500)
        if not name:
            errors.append("实验名称不能为空")
        out["name"] = name
    for k in ("project_id", "batch_id"):
        if want(k):
            v = data.get(k)
            out[k] = int(v) if v not in (None, "", 0) else None
    for k in TEXT_FIELDS:
        if want(k):
            out[k] = clean_str(data.get(k))
    if want("status"):
        st = clean_str(data.get("status")) or "Planned"
        if st not in EXPERIMENT_STATUSES:
            errors.append(f"未知的实验状态：{st}")
        out["status"] = st
    if want("outcome"):
        oc = clean_str(data.get("outcome"))
        if oc is not None and oc not in EXPERIMENT_OUTCOMES:
            errors.append(f"未知的实验结果判定：{oc}")
        out["outcome"] = oc
    try:
        if want("experiment_date"):
            out["experiment_date"] = parse_date(data.get("experiment_date"), "实验日期")
        if want("raw_data_path"):
            out["raw_data_path"] = normalize_path(data.get("raw_data_path"), "原始数据路径")
        if want("parameters"):
            out["parameters"] = clean_parameters(data.get("parameters"))
    except ValidationError as e:
        errors.extend(e.errors)
    # 一致性：判定为失败时建议记录原因（不强制，但给出提示由界面处理）
    if errors:
        raise ValidationError(errors)
    return out


def create_experiment(data: dict) -> int:
    clean = clean_experiment(data)
    return crud.create(Experiment, clean, "experiment", f"新建实验：{clean['name']}")


def update_experiment(exp_id: int, data: dict) -> None:
    crud.update(Experiment, exp_id, clean_experiment(data, partial=True), "experiment", f"更新实验 #{exp_id}")


def delete_experiment(exp_id: int) -> None:
    """删除实验记录及其附件引用；磁盘上的原始数据文件不受影响。"""
    crud.delete(Experiment, exp_id, "experiment", f"删除实验记录 #{exp_id}（未删除任何原始文件）")


def get_experiment(exp_id: Optional[int]) -> Optional[dict]:
    d = crud.get(Experiment, exp_id)
    if d is not None:
        d["parameters_list"] = loads(d.get("parameters"), []) or []
    return d


def list_experiments(project_id: Optional[int] = None, statuses: Optional[list[str]] = None,
                     batch_id: Optional[int] = None, search: Optional[str] = None) -> list[dict]:
    stmt = select(Experiment)
    if project_id:
        stmt = stmt.where(Experiment.project_id == project_id)
    if statuses:
        stmt = stmt.where(Experiment.status.in_(statuses))
    if batch_id:
        stmt = stmt.where(Experiment.batch_id == batch_id)
    if search:
        like = f"%{search.strip()}%"
        stmt = stmt.where(Experiment.name.ilike(like) | Experiment.purpose.ilike(like)
                          | Experiment.model_system.ilike(like))
    stmt = stmt.order_by(Experiment.experiment_date.is_(None), Experiment.experiment_date.desc(), Experiment.id.desc())
    return crud.list_dicts(stmt)


def pending_experiments() -> list[dict]:
    rows = list_experiments(statuses=EXPERIMENT_PENDING_STATUSES)
    rows.sort(key=lambda r: (r["experiment_date"] is None, r["experiment_date"] or pd.Timestamp.max.date()))
    return rows


def parameter_comparison(exp_ids: list[int]) -> pd.DataFrame:
    """行 = 参数，列 = 实验；附加“是否一致”列，方便快速看出批次间差异。"""
    cols: dict[str, dict[str, str]] = {}
    with session_scope() as s:
        exps = s.scalars(select(Experiment).where(Experiment.id.in_(exp_ids))).all()
        order = {eid: i for i, eid in enumerate(exp_ids)}
        exps = sorted(exps, key=lambda e: order.get(e.id, 0))
        for e in exps:
            label = f"#{e.id} {e.name[:24]}" + (f"（{e.experiment_date}）" if e.experiment_date else "")
            vals = {}
            for p in loads(e.parameters, []) or []:
                v = p.get("value")
                vals[p["name"]] = f"{v} {p['unit']}".strip() if (v is not None and p.get("unit")) else (v if v is not None else "")
            cols[label] = vals
    if not cols:
        return pd.DataFrame()
    df = pd.DataFrame(cols)
    df.index.name = "参数"
    df = df.fillna("—")
    df["是否一致"] = df.apply(lambda r: "一致" if len(set(r.values)) == 1 else "不同", axis=1)
    return df.sort_values(["是否一致", "参数"], ascending=[False, True]) if len(cols) > 1 else df


# ------------------------------------------------------------------- batches
def create_batch(data: dict) -> int:
    code = clean_str(data.get("code"), 100)
    if not code:
        raise ValidationError("批次编号不能为空")
    return crud.create(ExperimentBatch, {
        "code": code, "project_id": data.get("project_id") or None,
        "description": clean_str(data.get("description")),
        "start_date": parse_date(data.get("start_date"), "批次开始日期"),
        "notes": clean_str(data.get("notes")),
    }, "experiment_batch", f"新建实验批次：{code}")


def update_batch(batch_id: int, data: dict) -> None:
    code = clean_str(data.get("code"), 100)
    if not code:
        raise ValidationError("批次编号不能为空")
    crud.update(ExperimentBatch, batch_id, {
        "code": code, "project_id": data.get("project_id") or None,
        "description": clean_str(data.get("description")),
        "start_date": parse_date(data.get("start_date"), "批次开始日期"),
        "notes": clean_str(data.get("notes")),
    }, "experiment_batch")


def delete_batch(batch_id: int) -> None:
    crud.delete(ExperimentBatch, batch_id, "experiment_batch", "删除批次（批次内实验保留，批次字段置空）")


def list_batches(project_id: Optional[int] = None) -> list[dict]:
    stmt = select(ExperimentBatch)
    if project_id:
        stmt = stmt.where(ExperimentBatch.project_id == project_id)
    return crud.list_dicts(stmt.order_by(ExperimentBatch.start_date.desc().nulls_last(), ExperimentBatch.code))


# --------------------------------------------------------------- attachments
def add_attachment(exp_id: int, path: str, kind: Optional[str] = None, description: Optional[str] = None) -> int:
    norm = normalize_path(path, "附件路径")
    if not norm:
        raise ValidationError("附件路径不能为空")
    if kind and kind not in ATTACHMENT_KINDS:
        raise ValidationError("未知的附件类型")
    st = file_stat(norm)
    return crud.create(ExperimentAttachment, {
        "experiment_id": exp_id, "path": norm, "kind": kind, "description": clean_str(description),
        "exists_last_check": st["exists"], "file_size": st["size"], "file_mtime": st["mtime"],
        "last_checked_at": now(),
    }, "experiment_attachment", f"实验 #{exp_id} 关联附件（仅引用路径）：{norm}")


def delete_attachment(att_id: int) -> None:
    crud.delete(ExperimentAttachment, att_id, "experiment_attachment", "移除附件引用（未删除原文件）")


def refresh_attachments(exp_id: Optional[int] = None) -> int:
    with session_scope() as s:
        stmt = select(ExperimentAttachment)
        if exp_id is not None:
            stmt = stmt.where(ExperimentAttachment.experiment_id == exp_id)
        n = 0
        for a in s.scalars(stmt):
            st = file_stat(a.path)
            a.exists_last_check, a.file_size, a.file_mtime, a.last_checked_at = st["exists"], st["size"], st["mtime"], now()
            n += 1
        return n


def list_attachments(exp_id: int) -> list[dict]:
    return crud.list_dicts(select(ExperimentAttachment).where(ExperimentAttachment.experiment_id == exp_id)
                           .order_by(ExperimentAttachment.id))
