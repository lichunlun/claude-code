"""离线“科研体检”：不调用任何模型，只根据数据库中的事实给出提醒。"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from ...constants import TASK_OPEN_STATUSES
from ...utils import split_lines, today
from .. import bioinfo, experiments, files, literature, projects, publications, tasks


@dataclass
class Finding:
    level: str  # 高 / 中 / 低
    category: str
    message: str
    ref: str = ""


def run_checks(project_id: Optional[int] = None) -> list[Finding]:
    out: list[Finding] = []
    t = today()
    plist = [projects.get_project(project_id)] if project_id else projects.list_projects()
    plist = [p for p in plist if p]
    pids = [p["id"] for p in plist]

    for p in plist:
        miss = projects.missing_fields(p)
        if miss:
            out.append(Finding("低", "项目信息", f"「{p['name']}」有 {len(miss)} 项待填写：{'、'.join(miss[:6])}"
                               + ("…" if len(miss) > 6 else ""), f"项目 #{p['id']}"))
        if p.get("expected_end_date") and p["expected_end_date"] < t and p.get("status") != "Completed":
            out.append(Finding("中", "项目进度", f"「{p['name']}」已超过预计完成时间（{p['expected_end_date']}）", f"项目 #{p['id']}"))
        for path in split_lines(p.get("key_paths")):
            if not files.file_stat(path)["exists"]:
                out.append(Finding("中", "文件", f"「{p['name']}」的关键文件不存在：{path}", f"项目 #{p['id']}"))

    task_rows = tasks.list_tasks(project_ids=pids if project_id else None, statuses=TASK_OPEN_STATUSES)
    for tk in task_rows:
        if tk["is_overdue"]:
            out.append(Finding("高", "任务", f"任务已逾期 {(t - tk['due_date']).days} 天：{tk['title']}", f"任务 #{tk['id']}"))
        elif tk["priority"] in ("Critical", "High") and not tk["due_date"]:
            out.append(Finding("低", "任务", f"高优先级任务未设置截止日期：{tk['title']}", f"任务 #{tk['id']}"))
        if tk["status"] == "Blocked":
            out.append(Finding("中", "任务", f"任务处于受阻状态：{tk['title']}", f"任务 #{tk['id']}"))

    for e in experiments.list_experiments(project_id=project_id):
        if e["status"] == "Failed" and not e.get("failure_reason"):
            out.append(Finding("中", "实验", f"实验失败但未记录失败原因：{e['name']}", f"实验 #{e['id']}"))
        if e["status"] == "Completed" and not e.get("result_summary"):
            out.append(Finding("中", "实验", f"实验已完成但缺少结果摘要：{e['name']}", f"实验 #{e['id']}"))
        if e["status"] == "Planned" and e.get("experiment_date") and e["experiment_date"] < t:
            out.append(Finding("中", "实验", f"计划日期已过但仍为“待开展”：{e['name']}（{e['experiment_date']}）", f"实验 #{e['id']}"))
        if e.get("raw_data_path") and not files.file_stat(e["raw_data_path"])["exists"]:
            out.append(Finding("高", "实验数据", f"原始数据路径不存在：{e['raw_data_path']}", f"实验 #{e['id']}"))

    for pb in publications.list_publications(project_id=project_id):
        if pb["status"] == "Unconfirmed":
            out.append(Finding("中", "投稿", f"投稿状态待您确认：{pb['title'][:60]}", f"论文 #{pb['id']}"))
        if pb["status"] == "Revision" and pb.get("revision_due_date"):
            left = (pb["revision_due_date"] - t).days
            if left < 0:
                out.append(Finding("高", "投稿", f"修改期限已过 {-left} 天：{pb['title'][:60]}", f"论文 #{pb['id']}"))
            elif left <= 7:
                out.append(Finding("高", "投稿", f"修改期限还剩 {left} 天：{pb['title'][:60]}", f"论文 #{pb['id']}"))
        if pb["status"] == "Revision" and not pb.get("revision_due_date"):
            out.append(Finding("中", "投稿", f"处于修改阶段但未登记修改期限：{pb['title'][:60]}", f"论文 #{pb['id']}"))
        if pb["status"] in ("Draft", "Internal Review") and pb.get("planned_submission_date") and \
                pb["planned_submission_date"] <= t + timedelta(days=14):
            out.append(Finding("中", "投稿", f"计划投稿期限临近（{pb['planned_submission_date']}）：{pb['title'][:60]}",
                               f"论文 #{pb['id']}"))
        if not pb.get("next_action") and pb["status"] not in ("Published", "Withdrawn"):
            out.append(Finding("低", "投稿", f"未填写下一步行动：{pb['title'][:60]}", f"论文 #{pb['id']}"))

    lits = literature.literature_for_project(project_id) if project_id else literature.search_literature()
    unverified = [x for x in lits if x["verification_status"] != "Verified"]
    if unverified:
        out.append(Finding("中", "文献", f"{len(unverified)} 篇文献的著录信息尚未核实（引用前请核对 DOI/PMID）", ""))
    no_id = [x for x in lits if not x.get("doi") and not x.get("pmid")]
    if no_id:
        out.append(Finding("中", "文献", f"{len(no_id)} 篇文献没有 DOI 或 PMID，无法追溯", ""))

    for j in bioinfo.list_jobs(project_id=project_id):
        if j["status"] == "Needs Verification":
            out.append(Finding("中", "分析", f"分析结果待核验：{j['name']}", f"分析 #{j['id']}"))
        if j["status"] == "Failed" and not j.get("error_log"):
            out.append(Finding("低", "分析", f"分析失败但未记录错误日志：{j['name']}", f"分析 #{j['id']}"))
        if j["status"] == "Completed" and not j.get("result_summary"):
            out.append(Finding("低", "分析", f"分析已完成但缺少结果摘要：{j['name']}", f"分析 #{j['id']}"))

    missing_files = files.list_files(project_id=project_id, exists=False)
    if missing_files:
        out.append(Finding("中", "文件", f"文件索引中有 {len(missing_files)} 个文件当前不存在（可能被移动或重命名）", ""))

    order = {"高": 0, "中": 1, "低": 2}
    out.sort(key=lambda f: (order.get(f.level, 3), f.category))
    return out
