"""生信分析任务：登记、脚本路径管理、日志记录、结果索引。

脚本执行（第二阶段功能）见 runner.py：默认关闭，需在“设置”中显式开启，
且每次运行前都必须展示命令、输入、输出并由用户确认。
"""
from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import select

from ..constants import BIO_LANGUAGES, BIO_STATUSES
from ..db import session_scope
from ..models import BioinformaticsJob, BioinformaticsRun, now
from ..utils import (
    ValidationError,
    clean_str,
    file_stat,
    normalize_path,
    normalize_path_lines,
    split_lines,
)
from . import crud


def clean_job(data: dict, partial: bool = False) -> dict:
    out: dict[str, Any] = {}
    errors: list[str] = []

    def want(k: str) -> bool:
        return not partial or k in data

    if want("name"):
        n = clean_str(data.get("name"), 500)
        if not n:
            errors.append("分析名称不能为空")
        out["name"] = n
    if want("project_id"):
        v = data.get("project_id")
        out["project_id"] = int(v) if v not in (None, "", 0) else None
    for k in ("purpose", "data_source", "error_log", "result_summary", "notes"):
        if want(k):
            out[k] = clean_str(data.get(k))
    if want("script_args"):
        args = split_lines(data.get("script_args"))
        out["script_args"] = "\n".join(args) if args else None
    if want("language"):
        lang = clean_str(data.get("language"))
        if lang is not None and lang not in BIO_LANGUAGES:
            errors.append(f"未知的分析语言：{lang}")
        out["language"] = lang
    if want("status"):
        st = clean_str(data.get("status")) or "Pending"
        if st not in BIO_STATUSES:
            errors.append(f"未知的运行状态：{st}")
        out["status"] = st
    try:
        if want("script_path"):
            out["script_path"] = normalize_path(data.get("script_path"), "脚本路径")
        if want("working_dir"):
            out["working_dir"] = normalize_path(data.get("working_dir"), "工作目录")
        if want("data_paths"):
            out["data_paths"] = normalize_path_lines(data.get("data_paths"), "数据文件路径")
        if want("output_paths"):
            out["output_paths"] = normalize_path_lines(data.get("output_paths"), "输出文件路径")
    except ValidationError as e:
        errors.extend(e.errors)
    if out.get("script_path") and not out.get("language") and want("language"):
        ext = out["script_path"].lower()
        out["language"] = "R" if ext.endswith((".r", ".rmd")) else "Python" if ext.endswith(".py") else None
    if errors:
        raise ValidationError(errors)
    return out


def create_job(data: dict) -> int:
    clean = clean_job(data)
    return crud.create(BioinformaticsJob, clean, "bioinformatics_job", f"登记分析任务：{clean['name']}")


def update_job(job_id: int, data: dict) -> None:
    crud.update(BioinformaticsJob, job_id, clean_job(data, partial=True), "bioinformatics_job", f"更新分析任务 #{job_id}")


def set_status(job_id: int, status: str, note: Optional[str] = None) -> None:
    if status not in BIO_STATUSES:
        raise ValidationError("未知的运行状态")
    with session_scope() as s:
        job = s.get(BioinformaticsJob, job_id)
        if job is None:
            raise ValidationError("分析任务不存在")
        old = job.status
        job.status = status
        crud.log_activity(s, "bioinformatics_job", job_id, "status_change", f"分析任务 #{job_id}：{old} → {status}",
                          {"note": note})


def delete_job(job_id: int) -> None:
    with session_scope() as s:
        job = s.get(BioinformaticsJob, job_id)
        if job is not None and job.status == "Running":
            raise ValidationError("任务正在运行，不能删除")
    crud.delete(BioinformaticsJob, job_id, "bioinformatics_job", f"删除分析任务记录 #{job_id}（未删除脚本或数据）")


def get_job(job_id: Optional[int]) -> Optional[dict]:
    return crud.get(BioinformaticsJob, job_id)


def list_jobs(project_id: Optional[int] = None, statuses: Optional[list[str]] = None) -> list[dict]:
    stmt = select(BioinformaticsJob)
    if project_id:
        stmt = stmt.where(BioinformaticsJob.project_id == project_id)
    if statuses:
        stmt = stmt.where(BioinformaticsJob.status.in_(statuses))
    return crud.list_dicts(stmt.order_by(BioinformaticsJob.updated_at.desc()))


def add_manual_log(job_id: int, status: Optional[str], note: str, started_at=None, finished_at=None,
                   log_path: Optional[str] = None, update_job_status: bool = True) -> int:
    """登记在系统外（RStudio、终端、服务器）运行的结果。"""
    note = clean_str(note)
    if not note:
        raise ValidationError("请填写日志内容")
    if status is not None and status not in BIO_STATUSES:
        raise ValidationError("未知的运行状态")
    lp = normalize_path(log_path, "日志文件路径") if log_path else None
    with session_scope() as s:
        job = s.get(BioinformaticsJob, job_id)
        if job is None:
            raise ValidationError("分析任务不存在")
        run = BioinformaticsRun(job_id=job_id, source="manual", status=status, note=note, log_path=lp,
                                started_at=started_at, finished_at=finished_at, confirmed_by_user=True)
        s.add(run)
        if update_job_status and status:
            job.status = status
            if started_at:
                job.run_started_at = started_at
            if finished_at:
                job.run_finished_at = finished_at
            if status == "Failed":
                job.error_log = note
        s.flush()
        crud.log_activity(s, "bioinformatics_job", job_id, "log", f"分析任务 #{job_id} 登记日志")
        return run.id


def list_runs(job_id: int) -> list[dict]:
    return crud.list_dicts(select(BioinformaticsRun).where(BioinformaticsRun.job_id == job_id)
                           .order_by(BioinformaticsRun.id.desc()))


def path_report(job: dict) -> list[dict]:
    """脚本、数据、输出路径的存在性检测（只读）。"""
    out = []
    groups = [("脚本", [job.get("script_path")] if job.get("script_path") else []),
              ("输入数据", split_lines(job.get("data_paths"))),
              ("输出结果", split_lines(job.get("output_paths")))]
    for role, paths in groups:
        for p in paths:
            st = file_stat(p)
            out.append({"类别": role, "路径": p, "存在": st["exists"], "大小": st["size"],
                        "修改时间": st["mtime"]})
    return out


def reconcile_orphan_runs(alive_pids: Optional[set[int]] = None) -> int:
    """应用重启后，标记那些仍显示 Running 但进程已不存在的运行（无法确认结果 → Needs Verification）。"""
    alive_pids = alive_pids or set()
    n = 0
    with session_scope() as s:
        for job in s.scalars(select(BioinformaticsJob).where(BioinformaticsJob.status == "Running")):
            runs = [r for r in job.runs if r.status == "Running"]
            if any(r.pid in alive_pids for r in runs if r.pid):
                continue
            for r in runs:
                r.status = "Needs Verification"
                r.finished_at = r.finished_at or now()
                r.note = (r.note or "") + "\n应用重启时该运行状态未知，请核对日志与输出文件。"
            job.status = "Needs Verification"
            crud.log_activity(s, "bioinformatics_job", job.id, "reconcile", "重启后运行状态未知，已标记为待核验")
            n += 1
    return n
