"""初始数据：三个预置科研项目。

原则：只录入能从仓库中现有文件追溯的事实，并在 source_note 中注明出处；
没有可靠来源的字段一律为 NULL（界面显示“待填写”）。不编造进度、实验结果、投稿状态或截止日期。

信息来源（只读取，未修改）：
- 修改说明.md（2026-10-31）—— A/B 两篇 NSCLC 乙酰化姊妹综述的修订记录
- A_revised_clean.docx / B_revised_clean.docx —— 稿件标题与署名
- UG_Research_Topic_Committee/README.md 与 08_Final_Recommendation.md（2026-11-04）—— 本科选题委员会结论
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from sqlalchemy import func, select

from .config import APP_ROOT
from .db import get_meta, session_scope, set_meta
from .models import FileIndex, Project, ProjectMilestone, Publication, PublicationStatusHistory, now
from .services import crud
from .services.files import categorize
from .utils import file_stat

SEED_VERSION = "1"

PROJECT_A = "NSCLC 乙酰化精准治疗综述"
PROJECT_B = "POGLUT1–NOTCH–mTOR 与局灶性癫痫研究"
PROJECT_C = "本科阶段原创研究性论文选题"

A_FILES = ["A_revised_clean.docx", "A_revised_tracked.docx", "B_revised_clean.docx", "B_revised_tracked.docx",
           "修改说明.md"]
C_FILES = ["UG_Research_Topic_Committee/README.md",
           "UG_Research_Topic_Committee/08_Final_Recommendation.md",
           "UG_Research_Topic_Committee/03_Top3_Research_Proposals.md",
           "UG_Research_Topic_Committee/04_Innovation_Audit.md",
           "UG_Research_Topic_Committee/05_Experimental_Roadmap.md",
           "UG_Research_Topic_Committee/07_Reviewer_Critique.md",
           "UG_Research_Topic_Committee/01_Literature_Landscape.md",
           "UG_Research_Topic_Committee/02_15_Candidate_Topics.md",
           "UG_Research_Topic_Committee/06_Reference_List.md",
           "UG_Research_Topic_Committee/_WIP_chair_verified_notes.md",
           "UG_Research_Topic_Committee/code/analyze_assay_matrix.py",
           "UG_Research_Topic_Committee/code/analyze_assay_matrix.R",
           "UG_Research_Topic_Committee/code/score_topics.py",
           "UG_Research_Topic_Committee/code/score_topics.R"]
C_KEY_FILES = C_FILES[:6]

AUTHORS = ("Yu Chai†, Chengzhang Li†, Yuhan Wang, Kairui Zhu, Xinhui Jie, Cheng Wei, Youjie Li*")

TITLE_A = ("Beyond Pan-HDAC Inhibition: Precision Targeting of the Acetylation Writer–Eraser–Reader Network "
           "in Non-Small Cell Lung Cancer")
TITLE_B = ("Biomarker-Guided Combination and Sequencing of Acetylation-Targeted Therapy in Non-Small Cell Lung "
           "Cancer: Lessons from Clinical Trials")


def _existing(root: Optional[Path], rels: list[str]) -> list[str]:
    if root is None:
        return []
    out = []
    for r in rels:
        p = (root / r)
        if p.exists():
            out.append(str(p.resolve()))
    return out


def _projects(root: Optional[Path]) -> list[dict]:
    a_files = _existing(root, A_FILES)
    c_files = _existing(root, C_FILES)
    c_key = _existing(root, C_KEY_FILES)
    return [
        {
            "name": PROJECT_A,
            "research_direction": "非小细胞肺癌（NSCLC）乙酰化 writer–eraser–reader 网络的精准靶向治疗；"
                                  "分为两篇姊妹综述：A 篇（靶点生物学、药物开发与 AI 辅助靶点识别）、"
                                  "B 篇（生物标志物指导的联合治疗与给药顺序、临床试验经验）",
            "participants": f"稿件署名：{AUTHORS}（† 共同第一作者，* 通讯作者；来源：A/B_revised_clean.docx 署名）",
            "current_stage": "A、B 两篇姊妹综述已完成“投稿前定稿”修订（修订模式稿 + 干净稿）。"
                             "（来源：修改说明.md，2026-10-31）",
            "next_steps": "修改说明.md 中记录的作者待办：\n"
                          "1. 确认两篇 AI 使用声明的措辞及其在目标期刊中的位置；\n"
                          "2. 为 B 篇 9 处 [REF?] 补充文献（第 7 条可直接引用原稿已有文献）；\n"
                          "3. 在 ClinicalTrials.gov 核对 B 篇 Table 1 中 8 项试验的最新状态；\n"
                          "4. 绘制 A 篇 Figure 3，或删除其图题、占位行与图注。\n"
                          "目标期刊与投稿时间：待填写。",
            "main_risks": "修改说明.md 记录：修订时执行环境无法访问 PubMed / Crossref / ClinicalTrials.gov，"
                          "新增内容未能联网核对；B 篇 Table 1 的试验状态尚未核实。",
            "key_paths": "\n".join(a_files) or None,
            "source_note": "本项目信息摘自仓库文件 修改说明.md（2026-10-31）与 A/B_revised_clean.docx。"
                           "负责人、起止时间、状态、进度、科学问题与假说未在资料中明确，均为待填写。",
            "_files": a_files,
        },
        {
            "name": PROJECT_B,
            "research_direction": "POGLUT1–NOTCH–mTOR 通路与局灶性癫痫（依据项目名称，细节待填写）",
            "source_note": "当前资料中未找到该项目的任何文件或记录。除项目名称外，所有字段均为待填写；"
                           "系统不会推测其科学问题、假说、实验进展或结果。",
            "_files": [],
        },
        {
            "name": PROJECT_C,
            "research_direction": "为一名临床医学本科生遴选“真正可做、具备独立科学贡献、能经受同行评审”的"
                                  "原创研究课题，最终目标为 1 个推荐课题。（来源：README.md）",
            "current_stage": "选题委员会已完成全部 8 份交付物（01–08），并在四人模拟审稿后修订了最终推荐："
                             "先单独做 C02（还原法活力检测对自由基捕获型神经保护剂的干扰定量），"
                             "C01（HT-22 分化态）作为计划中的第二篇，在 C02 完成后进行。"
                             "（来源：UG_Research_Topic_Committee/README.md 与 08_Final_Recommendation.md，2026-11-04）\n"
                             "课题是否已开始实际执行：待填写。",
            "next_steps": "据 08_Final_Recommendation.md 与 README.md：\n"
                          "1. 第 1 周做无细胞干扰对照（培养基 + 化合物 + 显色剂，不加细胞），以判断第一篇论文是否成立；\n"
                          "2. 执行 C02（文件中的估计：4–6 个月，约 ¥10,000–20,000，无需新购细胞系）；\n"
                          "3. C02 完成后再做 C01；\n"
                          "4. 05_Experimental_Roadmap.md 写于审稿之前、按已否决的合并方案编写，使用前按其开头说明取舍。",
            "main_risks": "README.md 记录：\n"
                          "1. 文献数据库直连被网络策略拦截，文献为“检索可见”而非 API 核验，GEO 编号的样本数与平台需本人复核；\n"
                          "2. 29 个候选课题中只有 7 个完成了独立查新；\n"
                          "3. 两个 R 版分析脚本从未被执行过（以 Python 版为准）；\n"
                          "4. 05_Experimental_Roadmap.md 的部分内容基于已被否决的方案。",
            "key_paths": "\n".join(c_key) or None,
            "source_note": "本项目信息摘自 UG_Research_Topic_Committee/README.md 与 08_Final_Recommendation.md（2026-11-04）。"
                           "当前 README 未写明项目状态，故状态为待填写；负责人、起止时间与完成进度未在资料中明确，均为待填写。"
                           "文件中的周期与成本为该文件自身的估计，不是实际数据。",
            "_files": c_files,
            "_milestones": [
                ("选题委员会：8 份交付物完成（含模拟审稿与修订版最终推荐）", "Done"),
                ("C02：第 1 周无细胞干扰对照", "Planned"),
                ("C02：第一篇论文", "Planned"),
                ("C01：第二篇论文（C02 完成后）", "Planned"),
            ],
        },
    ]


def seed_initial_data(repo_root: Optional[Path] = None, force: bool = False) -> bool:
    """首次启动时写入预置项目。已执行过或数据库中已有项目时跳过。返回是否写入。"""
    if not force and get_meta("seed_version"):
        return False
    root = repo_root if repo_root is not None else APP_ROOT.parent
    with session_scope() as s:
        if s.scalar(select(func.count()).select_from(Project)):
            set_meta("seed_version", SEED_VERSION)
            return False
    with session_scope() as s:
        for spec in _projects(root):
            files = spec.pop("_files", [])
            milestones = spec.pop("_milestones", [])
            p = Project(**spec)
            s.add(p)
            s.flush()
            crud.log_activity(s, "project", p.id, "seed", f"初始化预置项目：{p.name}")
            for i, (title, status) in enumerate(milestones):
                s.add(ProjectMilestone(project_id=p.id, title=title, status=status, sort_order=i,
                                       note="来源：README.md / 08_Final_Recommendation.md（2026-11-04）；日期待填写"))
            for path in files:
                st = file_stat(path)
                s.add(FileIndex(project_id=p.id, path=path, file_name=Path(path).name,
                                extension=Path(path).suffix.lower() or None, category=categorize(path),
                                description="初始化时登记的已有项目文件（仅引用路径，未复制或修改）",
                                exists=st["exists"], size_bytes=st["size"], modified_at=st["mtime"],
                                last_checked_at=now()))
            if spec["name"] == PROJECT_A:
                for title, label, clean, tracked in (
                    (TITLE_A, "A", "A_revised_clean.docx", "A_revised_tracked.docx"),
                    (TITLE_B, "B", "B_revised_clean.docx", "B_revised_tracked.docx"),
                ):
                    paths = _existing(root, [clean, tracked])
                    pub = Publication(
                        project_id=p.id, title=title, author_order=AUTHORS,
                        first_author="Yu Chai；Chengzhang Li（共同第一作者）", corresponding_author="Youjie Li",
                        status="Unconfirmed", file_paths="\n".join(paths) or None,
                        source_note=f"{label} 篇标题与署名来自 {clean}。修改说明.md（2026-10-31）记载该稿处于"
                                    "“投稿前定稿”阶段；此后是否投稿、目标期刊、各节点日期系统均不知晓，请您确认。",
                    )
                    s.add(pub)
                    s.flush()
                    s.add(PublicationStatusHistory(publication_id=pub.id, from_status=None, to_status="Unconfirmed",
                                                   note="初始化：投稿状态待用户确认", confirmed_by_user=False))
    set_meta("seed_version", SEED_VERSION)
    return True
