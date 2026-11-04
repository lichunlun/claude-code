"""生成 Demo 数据库（用于界面演示与测试，绝不写入真实数据库）。

    python scripts/make_demo_db.py                 # 写入 <项目目录>/demo_data/
    RCC_DATA_DIR=demo_data streamlit run app.py    # 用 Demo 数据库启动

所有 Demo 记录的标题都以“[Demo]”开头，并与真实数据库物理隔离（不同目录、不同文件）。
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def build(data_dir: Path) -> Path:
    os.environ["RCC_DATA_DIR"] = str(data_dir)
    from rcc import config

    config.reset_settings_cache()
    real = (ROOT / "data").resolve()
    if config.get_settings().data_dir.resolve() == real:
        raise SystemExit("拒绝写入真实数据目录 data/")
    from rcc import db
    from rcc.models import Task
    from rcc.services import calendar, experiments, files, literature, projects, publications, tasks
    from rcc.services import bioinfo

    db.init_engine()
    t = date.today()
    sample_dir = data_dir / "demo_files"
    sample_dir.mkdir(parents=True, exist_ok=True)

    p1 = projects.create_project({"name": "[Demo] 示例项目：HDAC 抑制剂体外筛选", "status": "Active", "progress": 45,
                                  "research_direction": "Demo 数据：用于展示界面，不代表任何真实研究",
                                  "start_date": t - timedelta(days=60), "expected_end_date": t + timedelta(days=120),
                                  "current_stage": "Demo：细胞实验阶段", "next_steps": "Demo：完成第二批 CCK-8",
                                  "lead": "Demo User", "source_note": "Demo 数据"})
    p2 = projects.create_project({"name": "[Demo] 示例项目：单细胞数据再分析", "status": "Planning", "progress": 10,
                                  "research_direction": "Demo 数据", "source_note": "Demo 数据"})
    projects.add_milestone(p1, {"title": "[Demo] 完成预实验", "due_date": t - timedelta(days=20), "status": "Done"})
    projects.add_milestone(p1, {"title": "[Demo] 提交组会汇报", "due_date": t + timedelta(days=9), "status": "Planned"})

    specs = [("[Demo] 整理 WB 定量结果", "Critical", t + timedelta(days=1), "In Progress"),
             ("[Demo] 回复合作者邮件", "Medium", t + timedelta(days=2), "Todo"),
             ("[Demo] 补充引言段落", "High", t - timedelta(days=2), "Todo"),
             ("[Demo] 订购抗体", "High", t + timedelta(days=12), "Todo"),
             ("[Demo] 归档旧数据", "Low", None, "Todo"),
             ("[Demo] 预约流式", "Medium", t + timedelta(days=5), "Blocked")]
    for title, pr, due, st in specs:
        tasks.create_task({"title": title, "priority": pr, "due_date": due, "status": st, "project_id": p1})
    for i, d in enumerate([3, 9, 16, 24, 30, 38]):
        tid = tasks.create_task({"title": f"[Demo] 已完成任务 {i + 1}", "priority": "Medium", "project_id": p1})
        tasks.set_status(tid, "Done")
        with db.session_scope() as s:
            obj = s.get(Task, tid)
            obj.created_at = datetime.now() - timedelta(days=d + 3)
            obj.completed_at = datetime.now() - timedelta(days=d)

    img = sample_dir / "demo_wb.png"
    img.write_bytes(bytes.fromhex("89504e470d0a1a0a0000000d4948445200000001000000010806000000"
                                  "1f15c4890000000d49444154789c6360000002000154a24f5d0000000049454e44ae426082"))
    e1 = experiments.create_experiment({"name": "[Demo] CCK-8 细胞活力（批次 1）", "project_id": p1, "status": "Completed",
                                        "outcome": "Success", "experiment_date": t - timedelta(days=10),
                                        "parameters": [{"name": "细胞密度", "value": "5000", "unit": "个/孔"},
                                                       {"name": "药物浓度", "value": "1", "unit": "μM"},
                                                       {"name": "处理时间", "value": "48", "unit": "h"}],
                                        "result_summary": "Demo：示例结果摘要", "model_system": "Demo 细胞系"})
    experiments.create_experiment({"name": "[Demo] CCK-8 细胞活力（批次 2）", "project_id": p1, "status": "Planned",
                                   "experiment_date": t + timedelta(days=4),
                                   "parameters": [{"name": "细胞密度", "value": "5000", "unit": "个/孔"},
                                                  {"name": "药物浓度", "value": "2", "unit": "μM"},
                                                  {"name": "处理时间", "value": "48", "unit": "h"}]})
    experiments.create_experiment({"name": "[Demo] Western Blot", "project_id": p1, "status": "Failed", "outcome": "Failure",
                                   "experiment_date": t - timedelta(days=3)})
    experiments.add_attachment(e1, str(img), "WB 图片", "Demo 占位图片")

    pid_pub = publications.create_publication({"title": "[Demo] Example manuscript on acetylation", "project_id": p1,
                                               "status": "Draft", "planned_submission_date": t + timedelta(days=21)})
    publications.change_status(pid_pub, "Internal Review", True, t - timedelta(days=1), "Demo")
    pub2 = publications.create_publication({"title": "[Demo] Example accepted paper", "project_id": p2, "status": "Submitted",
                                            "submission_date": t - timedelta(days=90)})
    publications.change_status(pub2, "Under Review", True, t - timedelta(days=60))
    publications.change_status(pub2, "Revision", True, t - timedelta(days=10))
    with db.session_scope() as s:
        from rcc.models import Publication

        s.get(Publication, pub2).revision_due_date = t + timedelta(days=6)

    literature.create_manual({"title": "[Demo] A placeholder review (not a real citation)", "year": 2024,
                              "journal": "Demo Journal", "pub_type": "Review"}, project_id=p1)
    calendar.create_event({"title": "[Demo] 学术会议", "event_type": "conference", "start_date": t + timedelta(days=14),
                           "end_date": t + timedelta(days=16)})
    calendar.create_event({"title": "[Demo] 期末考试", "event_type": "exam", "start_date": t + timedelta(days=25)})
    bioinfo.create_job({"name": "[Demo] 差异表达分析", "project_id": p2, "language": "R", "status": "Needs Verification",
                        "data_source": "Demo", "result_summary": "Demo 摘要"})
    files.register_file(str(img), p1, None, "Demo 文件")
    db.set_meta("seed_version", "demo")  # Demo 库不写入真实预置项目，保持与真实数据完全隔离
    return config.get_settings().db_path


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=str(ROOT / "demo_data"))
    ap.add_argument("--reset", action="store_true")
    a = ap.parse_args()
    d = Path(a.data_dir).resolve()
    if a.reset and d.exists():
        shutil.rmtree(d)
    print("Demo 数据库：", build(d))
