"""实验记录（原始文件只读）与投稿状态（必须用户确认）。"""
from __future__ import annotations

from datetime import date

import pandas as pd
import pytest

from rcc.services import experiments, projects, publications
from rcc.utils import ValidationError, sha256_file


def test_experiment_crud_and_parameters(tmp_env):
    pid = projects.create_project({"name": "实验项目"})
    eid = experiments.create_experiment({
        "name": "WB 验证", "project_id": pid, "experiment_date": "2026-11-01", "status": "Completed",
        "outcome": "Success",
        "parameters": pd.DataFrame([{"name": "一抗稀释", "value": "1:1000", "unit": None},
                                    {"name": "曝光", "value": 30, "unit": "s"}, {"name": None, "value": "忽略空行"}]),
    })
    e = experiments.get_experiment(eid)
    assert [p["name"] for p in e["parameters_list"]] == ["一抗稀释", "曝光"]
    assert e["parameters_list"][1]["value"] == "30"
    experiments.update_experiment(eid, {"status": "Failed", "failure_reason": "条带模糊"})
    assert experiments.get_experiment(eid)["status"] == "Failed"
    assert experiments.get_experiment(eid)["outcome"] == "Success"  # 部分更新不影响其他字段
    with pytest.raises(ValidationError, match="重复"):
        experiments.update_experiment(eid, {"parameters": [{"name": "a"}, {"name": "a"}]})
    with pytest.raises(ValidationError):
        experiments.create_experiment({"name": ""})
    with pytest.raises(ValidationError):
        experiments.create_experiment({"name": "x", "status": "Done"})


def test_parameter_comparison(tmp_env):
    a = experiments.create_experiment({"name": "A", "parameters": [{"name": "浓度", "value": "1", "unit": "μM"},
                                                                  {"name": "时间", "value": "48", "unit": "h"}]})
    b = experiments.create_experiment({"name": "B", "parameters": [{"name": "浓度", "value": "2", "unit": "μM"},
                                                                  {"name": "时间", "value": "48", "unit": "h"},
                                                                  {"name": "温度", "value": "37"}]})
    df = experiments.parameter_comparison([a, b])
    assert df.loc["浓度", "是否一致"] == "不同" and df.loc["时间", "是否一致"] == "一致"
    assert df.loc["温度"].iloc[0] == "—"


def test_attachments_are_references_only(tmp_env):
    raw = tmp_env / "WB_raw.tif"
    raw.write_bytes(b"\x49\x49\x2a\x00 fake tiff")
    before = sha256_file(str(raw))
    eid = experiments.create_experiment({"name": "WB", "raw_data_path": str(raw)})
    aid = experiments.add_attachment(eid, str(raw), "WB 图片", "原始曝光")
    att = experiments.list_attachments(eid)[0]
    assert att["exists_last_check"] and att["file_size"] == raw.stat().st_size
    with pytest.raises(ValidationError):
        experiments.add_attachment(eid, str(raw))  # 重复引用
    with pytest.raises(ValidationError):
        experiments.add_attachment(eid, "relative/file.tif")
    experiments.delete_attachment(aid)
    experiments.delete_experiment(eid)
    assert raw.exists() and sha256_file(str(raw)) == before  # 原始文件未被修改或删除


def test_attachment_missing_detection(tmp_env):
    f = tmp_env / "seq.fastq"
    f.write_text("@r1\nACGT\n+\n!!!!\n")
    eid = experiments.create_experiment({"name": "测序"})
    experiments.add_attachment(eid, str(f), "测序文件")
    f.rename(tmp_env / "moved.fastq")
    experiments.refresh_attachments(eid)
    assert experiments.list_attachments(eid)[0]["exists_last_check"] is False


def test_batches(tmp_env):
    pid = projects.create_project({"name": "批次项目"})
    bid = experiments.create_batch({"code": "B-2026-01", "project_id": pid})
    eid = experiments.create_experiment({"name": "x", "batch_id": bid})
    assert experiments.list_experiments(batch_id=bid)[0]["id"] == eid
    with pytest.raises(ValidationError):
        experiments.create_batch({"code": "B-2026-01", "project_id": pid})
    experiments.delete_batch(bid)
    assert experiments.get_experiment(eid)["batch_id"] is None


def test_pending_experiments(tmp_env):
    experiments.create_experiment({"name": "计划", "status": "Planned", "experiment_date": "2026-12-01"})
    experiments.create_experiment({"name": "完成", "status": "Completed"})
    assert [e["name"] for e in experiments.pending_experiments()] == ["计划"]


# -------------------------------------------------------------- publications
def test_status_change_requires_confirmation(tmp_env):
    pid = publications.create_publication({"title": "Paper A", "status": "Draft"})
    with pytest.raises(ValidationError, match="手动确认"):
        publications.change_status(pid, "Submitted", confirmed=False)
    assert publications.get_publication(pid)["status"] == "Draft"
    publications.change_status(pid, "Submitted", True, "2026-11-01", "稿件号 ABC-123")
    p = publications.get_publication(pid)
    assert p["status"] == "Submitted" and p["submission_date"] == date(2026, 11, 1)
    hist = publications.history(pid)
    assert [h["to_status"] for h in hist] == ["Draft", "Submitted"] and all(h["confirmed_by_user"] for h in hist)


def test_no_status_inference_from_dates(tmp_env):
    pid = publications.create_publication({"title": "Paper B", "status": "Submitted", "submission_date": "2026-09-01"})
    publications.update_publication(pid, {"under_review_date": "2026-10-01", "decision_date": "2026-10-20"})
    assert publications.get_publication(pid)["status"] == "Submitted"  # 填写日期不会改变状态
    with pytest.raises(ValidationError):
        publications.update_publication(pid, {"status": "Accepted"})


def test_transfer_and_side_statuses(tmp_env):
    pid = publications.create_publication({"title": "Paper C", "status": "Under Review", "target_journal": "J1"})
    publications.change_status(pid, "Rejected", True, "2026-10-01")
    with pytest.raises(ValidationError, match="目标期刊"):
        publications.change_status(pid, "Transferred", True)
    publications.change_status(pid, "Transferred", True, None, None, "J2")
    assert publications.get_publication(pid)["target_journal"] == "J2"
    with pytest.raises(ValidationError):
        publications.change_status(pid, "Transferred", True, None, None, "J3")  # 与当前相同
    with pytest.raises(ValidationError):
        publications.change_status(pid, "Unconfirmed", True)
    for s in ("Withdrawn", "On Hold"):
        publications.change_status(pid, s, True)
    assert publications.get_publication(pid)["status"] == "On Hold"


def test_publication_date_validation(tmp_env):
    with pytest.raises(ValidationError, match="不能早于"):
        publications.create_publication({"title": "x", "submission_date": "2026-10-01", "decision_date": "2026-09-01"})
    with pytest.raises(ValidationError):
        publications.create_publication({"title": "x", "submission_url": "ftp://bad"})
    with pytest.raises(ValidationError):
        publications.create_publication({"title": ""})


def test_counts_and_warnings(tmp_env):
    publications.create_publication({"title": "a", "status": "Under Review"})
    publications.create_publication({"title": "b", "status": "Published"})
    publications.create_publication({"title": "c", "status": "Revision"})
    assert publications.count_in_submission() == 2
    assert publications.status_counts()["Published"] == 1
    assert "跳过" in publications.transition_warning("Draft", "Accepted")
    assert publications.transition_warning("Submitted", "Editor Assigned") is None
