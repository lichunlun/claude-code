"""在用户授权范围内构建发送给模型的“系统记录”。

只包含数据库中的结构化记录与用户自己写的笔记/摘要，不读取、不上传任何原始文件内容。
"""
from __future__ import annotations

from datetime import date
from typing import Iterable

from ...constants import PENDING, label
from ...utils import loads, split_lines
from .. import bioinfo, experiments, literature, projects, publications, tasks

SCOPES = {
    "project": "项目简介",
    "tasks": "任务列表",
    "literature": "文献与阅读笔记",
    "experiments": "实验记录",
    "bioinfo": "分析结果摘要",
    "publications": "投稿记录",
}


def _v(x) -> str:
    if x is None or x == "":
        return PENDING
    return str(x)


def _clip(s, n: int = 600) -> str:
    s = _v(s)
    return s if len(s) <= n else s[:n] + "…（截断）"


def build_context(project_id: int, scopes: Iterable[str]) -> str:
    scopes = [s for s in scopes if s in SCOPES]
    p = projects.get_project(project_id)
    if p is None:
        return ""
    lines = [f"# 系统记录（项目 #{p['id']}）", f"导出时间：{date.today()}", ""]
    if "project" in scopes:
        lines += [
            "## 项目简介",
            f"- 项目名称：{p['name']}",
            f"- 研究方向：{_v(p['research_direction'])}",
            f"- 科学问题：{_v(p['scientific_question'])}",
            f"- 核心假说：{_v(p['core_hypothesis'])}",
            f"- 负责人：{_v(p['lead'])}；参与者：{_clip(p['participants'], 300)}",
            f"- 时间：{_v(p['start_date'])} 至 {_v(p['expected_end_date'])}（预计）",
            f"- 状态：{label('project_status', p['status'])}；完成进度：{_v(p['progress']) + '%' if p['progress'] is not None else PENDING}",
            f"- 当前研究阶段：{_clip(p['current_stage'])}",
            f"- 下一步计划：{_clip(p['next_steps'])}",
            f"- 主要风险：{_clip(p['main_risks'])}",
            f"- 信息来源说明：{_clip(p['source_note'], 300)}",
        ]
        ms = projects.list_milestones(project_id)
        if ms:
            lines.append("- 里程碑：")
            for m in ms:
                lines.append(f"  - {m['title']}（{label('milestone_status', m['status'])}，日期：{_v(m['due_date'])}）")
        lines.append("")
    if "tasks" in scopes:
        rows = tasks.list_tasks(project_ids=[project_id])
        lines.append(f"## 任务列表（共 {len(rows)} 条）")
        for t in rows[:60]:
            lines.append(f"- 任务 #{t['id']}：{t['title']} | 状态：{label('task_status', t['status'])} | 优先级：{t['priority']}"
                         f" | 截止：{_v(t['due_date'])}{' | 已逾期' if t['is_overdue'] else ''}"
                         + (f" | 备注：{_clip(t['notes'], 200)}" if t.get("notes") else ""))
        if not rows:
            lines.append("- （无任务记录）")
        lines.append("")
    if "literature" in scopes:
        lits = literature.literature_for_project(project_id)
        lines.append(f"## 关联文献（共 {len(lits)} 篇；核实状态如实标注）")
        for lit in lits[:40]:
            lines.append(f"- 文献 #{lit['id']}：{_v(lit['title'])} | {_v(lit['journal'])} {_v(lit['year'])} | DOI：{_v(lit['doi'])}"
                         f" | PMID：{_v(lit['pmid'])} | 核实：{label('verification', lit['verification_status'])}"
                         f" | 阅读：{label('reading_status', lit['reading_status'])}")
            if lit.get("relevance"):
                lines.append(f"  - 与项目关系：{_clip(lit['relevance'], 300)}")
            if lit.get("value_note"):
                lines.append(f"  - 价值：{_clip(lit['value_note'], 300)}")
            if lit.get("limitation_note"):
                lines.append(f"  - 局限：{_clip(lit['limitation_note'], 300)}")
            for n in literature.list_notes(lit_id=lit["id"])[:5]:
                lines.append(f"  - 笔记（{_v(n['note_type'])}，页 {_v(n['page_ref'])}）：{_clip(n['content'], 400)}")
        if not lits:
            lines.append("- （无关联文献）")
        lines.append("")
    if "experiments" in scopes:
        exps = experiments.list_experiments(project_id=project_id)
        lines.append(f"## 实验记录（共 {len(exps)} 条）")
        for e in exps[:40]:
            params = loads(e.get("parameters"), []) or []
            ptxt = "；".join(f"{x['name']}={x.get('value') or ''}{x.get('unit') or ''}" for x in params[:10])
            lines.append(f"- 实验 #{e['id']}：{e['name']} | 日期：{_v(e['experiment_date'])} | 状态：{label('experiment_status', e['status'])}"
                         f" | 判定：{label('experiment_outcome', e['outcome'])}")
            for k, lbl in (("purpose", "目的"), ("model_system", "模型"), ("groups", "分组"), ("result_summary", "结果摘要"),
                           ("failure_reason", "失败原因"), ("next_experiment", "下一步")):
                if e.get(k):
                    lines.append(f"  - {lbl}：{_clip(e[k], 400)}")
            if ptxt:
                lines.append(f"  - 参数：{ptxt}")
        if not exps:
            lines.append("- （无实验记录）")
        lines.append("")
    if "bioinfo" in scopes:
        jobs = bioinfo.list_jobs(project_id=project_id)
        lines.append(f"## 分析任务（共 {len(jobs)} 条）")
        for j in jobs[:30]:
            lines.append(f"- 分析 #{j['id']}：{j['name']} | 语言：{_v(j['language'])} | 状态：{j['status']} | 数据来源：{_clip(j['data_source'], 200)}")
            if j.get("purpose"):
                lines.append(f"  - 目的：{_clip(j['purpose'], 300)}")
            if j.get("result_summary"):
                lines.append(f"  - 结果摘要：{_clip(j['result_summary'], 500)}")
            if j.get("status") == "Failed" and j.get("error_log"):
                lines.append(f"  - 错误日志（末尾）：{_clip(j['error_log'][-400:], 400)}")
            if split_lines(j.get("output_paths")):
                lines.append(f"  - 已登记输出文件 {len(split_lines(j['output_paths']))} 个（未发送文件内容）")
        if not jobs:
            lines.append("- （无分析任务）")
        lines.append("")
    if "publications" in scopes:
        pubs = publications.list_publications(project_id=project_id)
        lines.append(f"## 投稿记录（共 {len(pubs)} 条；状态均为研究者手动确认，‘状态待确认’表示尚未确认）")
        for pb in pubs:
            lines.append(f"- 论文 #{pb['id']}：{_clip(pb['title'], 200)} | 状态：{label('pub_status', pb['status'])}"
                         f" | 目标期刊：{_v(pb['target_journal'])} | 投稿日期：{_v(pb['submission_date'])}"
                         f" | 修改期限：{_v(pb['revision_due_date'])}")
            if pb.get("next_action"):
                lines.append(f"  - 下一步行动：{_clip(pb['next_action'], 300)}")
            if pb.get("source_note"):
                lines.append(f"  - 来源说明：{_clip(pb['source_note'], 300)}")
        if not pubs:
            lines.append("- （无投稿记录）")
        lines.append("")
    return "\n".join(lines).strip() + "\n"
