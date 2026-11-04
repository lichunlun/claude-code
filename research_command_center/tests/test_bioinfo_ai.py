"""生信任务与安全执行；AI 接口层（全部使用模拟，不调用任何收费 API）。"""
from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from rcc.db import current_db_path
from rcc.services import app_settings, bioinfo, experiments, projects, publications, runner, tasks
from rcc.services.ai import assistant, context, offline_checks, profiles, providers
from rcc.utils import ValidationError, sha256_file


# ---------------------------------------------------------------- bioinfo
def test_job_registration_and_logs(tmp_env):
    script = tmp_env / "deg.R"
    script.write_text("cat('hi')")
    jid = bioinfo.create_job({"name": "差异分析", "script_path": str(script), "data_paths": str(tmp_env / "counts.csv"),
                              "data_source": "GSE00000（示例）"})
    j = bioinfo.get_job(jid)
    assert j["language"] == "R" and j["status"] == "Pending"
    rep = bioinfo.path_report(j)
    assert {r["类别"]: r["存在"] for r in rep} == {"脚本": True, "输入数据": False}
    bioinfo.add_manual_log(jid, "Failed", "Error in DESeq: missing counts")
    assert bioinfo.get_job(jid)["status"] == "Failed" and "DESeq" in bioinfo.get_job(jid)["error_log"]
    with pytest.raises(ValidationError):
        bioinfo.add_manual_log(jid, None, "")
    with pytest.raises(ValidationError):
        bioinfo.create_job({"name": "x", "status": "Done"})
    with pytest.raises(ValidationError):
        bioinfo.create_job({"name": "x", "script_path": "rel/script.py"})


def test_runner_disabled_by_default(tmp_env):
    s = tmp_env / "ok.py"
    s.write_text("print('ok')")
    jid = bioinfo.create_job({"name": "py", "script_path": str(s)})
    pv = runner.build_preview(jid)
    assert not pv["ok"] and any("未开启" in e for e in pv["errors"])
    with pytest.raises(ValidationError):
        runner.start_run(jid, True, pv["script_sha256"])


def _enable(monkeypatch):
    app_settings.set_allow_script_execution(True)
    app_settings.set_interpreters(sys.executable, None)


def test_runner_success_needs_verification(tmp_env, monkeypatch):
    _enable(monkeypatch)
    inp = tmp_env / "input.csv"
    inp.write_text("a,b\n1,2\n")
    h_in = sha256_file(str(inp))
    out = tmp_env / "out.txt"
    s = tmp_env / "analysis.py"
    s.write_text(f"import sys\nprint('reading', open(r'{inp}').read().count(chr(10)))\nopen(r'{out}','w').write('done')\n"
                 "print('arg', sys.argv[1])\n")
    jid = bioinfo.create_job({"name": "py", "script_path": str(s), "script_args": "--flag", "data_paths": str(inp),
                              "output_paths": str(out)})
    pv = runner.build_preview(jid)
    assert pv["ok"] and pv["command"] == [str(Path(sys.executable).resolve()), str(s), "--flag"]
    with pytest.raises(ValidationError):
        runner.start_run(jid, False, pv["script_sha256"])  # 未确认
    run_id = runner.start_run(jid, True, pv["script_sha256"])
    runner.wait_for(run_id, 30)
    j = bioinfo.get_job(jid)
    assert j["status"] == "Needs Verification"  # 成功也需人工核验，不自动标记 Completed
    run = bioinfo.list_runs(jid)[0]
    assert run["exit_code"] == 0 and "arg --flag" in run["log_excerpt"] and run["confirmed_by_user"]
    assert out.read_text() == "done" and sha256_file(str(inp)) == h_in


def test_runner_failure_and_tamper(tmp_env, monkeypatch):
    _enable(monkeypatch)
    s = tmp_env / "fail.py"
    s.write_text("raise SystemExit('boom')")
    jid = bioinfo.create_job({"name": "fail", "script_path": str(s)})
    pv = runner.build_preview(jid)
    s.write_text("print('changed after confirmation')")
    with pytest.raises(ValidationError, match="SHA-256"):
        runner.start_run(jid, True, pv["script_sha256"])
    s.write_text("raise SystemExit('boom')")
    pv = runner.build_preview(jid)
    rid = runner.start_run(jid, True, pv["script_sha256"])
    runner.wait_for(rid, 30)
    j = bioinfo.get_job(jid)
    assert j["status"] == "Failed" and "boom" in j["error_log"]


def test_runner_rejects_wrong_extension(tmp_env, monkeypatch):
    _enable(monkeypatch)
    s = tmp_env / "x.sh"
    s.write_text("echo hi")
    jid = bioinfo.create_job({"name": "sh", "script_path": str(s), "language": "Python"})
    assert any("扩展名" in e for e in runner.build_preview(jid)["errors"])


def test_reconcile_orphans(tmp_env):
    jid = bioinfo.create_job({"name": "orphan"})
    from rcc.db import session_scope
    from rcc.models import BioinformaticsJob, BioinformaticsRun

    with session_scope() as s:
        s.get(BioinformaticsJob, jid).status = "Running"
        s.add(BioinformaticsRun(job_id=jid, source="executed", status="Running", pid=999999))
    assert bioinfo.reconcile_orphan_runs(set()) == 1
    assert bioinfo.get_job(jid)["status"] == "Needs Verification"


# --------------------------------------------------------------------- AI
def _profile(**kw):
    base = {"profile_name": "Claude", "provider_type": "anthropic", "base_url": "", "model": "claude-opus-5-5",
            "key_storage": "env", "api_key_env_var": "RCC_TEST_KEY"}
    base.update(kw)
    return base


def test_profile_validation(tmp_env):
    with pytest.raises(ValidationError, match="环境变量名"):
        profiles.save_profile(_profile(api_key_env_var="sk-ant-REALKEY123"))
    with pytest.raises(ValidationError, match="Base URL"):
        profiles.save_profile(_profile(provider_type="openai_compatible", base_url=""))
    with pytest.raises(ValidationError):
        profiles.save_profile(_profile(model=""))
    pid = profiles.save_profile(_profile())
    assert profiles.active_profile()["id"] == pid  # 第一个配置自动设为当前


def test_api_key_never_stored(tmp_env, monkeypatch):
    secret = "sk-test-SECRET-should-not-be-in-db-123456"
    monkeypatch.setenv("RCC_TEST_KEY", secret)
    pid = profiles.save_profile(_profile())
    prof = profiles.get_profile(pid)
    assert profiles.get_api_key(prof) == secret
    assert profiles.key_status(prof)[0]
    assert secret.encode() not in current_db_path().read_bytes()
    monkeypatch.delenv("RCC_TEST_KEY")
    assert profiles.key_status(prof) == (False, "环境变量 RCC_TEST_KEY 未设置（设置后需重启应用）")


def test_context_respects_scopes(tmp_env):
    pid = projects.create_project({"name": "AI 项目", "scientific_question": "Q?"})
    tasks.create_task({"title": "秘密任务名", "project_id": pid})
    experiments.create_experiment({"name": "实验甲", "project_id": pid, "result_summary": "结果甲"})
    ctx = context.build_context(pid, ["project"])
    assert "AI 项目" in ctx and "秘密任务名" not in ctx and "实验甲" not in ctx
    ctx2 = context.build_context(pid, ["tasks", "experiments"])
    assert "秘密任务名" in ctx2 and "结果甲" in ctx2 and "科学问题" not in ctx2
    assert "待填写" in context.build_context(pid, ["project"])  # 未填字段如实标注


def test_ask_requires_authorization_and_logs(tmp_env, monkeypatch):
    pid = projects.create_project({"name": "授权项目"})
    prof = profiles.get_profile(profiles.save_profile(_profile()))
    with pytest.raises(ValidationError, match="授权"):
        assistant.ask(prof, pid, ["project"], "summary", None, authorized=False)
    with pytest.raises(ValidationError):
        assistant.ask(prof, pid, [], "summary", None, authorized=True)
    captured = {}

    def fake_chat(profile, system, user, timeout=180.0):
        captured["system"], captured["user"] = system, user
        return providers.ChatResult(text="【事实】……【推测】……【建议】……", model="fake-model")

    monkeypatch.setattr(assistant, "chat", fake_chat)
    res = assistant.ask(prof, pid, ["project"], "risks", "请关注风险", authorized=True)
    assert "【事实】" in res.text and "严禁编造" in captured["system"] and "授权项目" in captured["user"]
    h = assistant.history()[0]
    assert h["status"] == "ok" and h["request_type"] == "risks" and h["response"].startswith("【事实】")


def test_ask_provider_error_logged(tmp_env, monkeypatch):
    pid = projects.create_project({"name": "错误项目"})
    prof = profiles.get_profile(profiles.save_profile(_profile()))

    def bad(*a, **k):
        raise providers.AIProviderError("API Key 无效（401）")

    monkeypatch.setattr(assistant, "chat", bad)
    with pytest.raises(providers.AIProviderError):
        assistant.ask(prof, pid, ["project"], "summary", None, authorized=True)
    assert assistant.history()[0]["status"] == "error"


def test_openai_compatible_provider(monkeypatch):
    calls = {}

    class R:
        status_code = 200
        text = ""

        def json(self):
            return {"model": "local-llm", "choices": [{"message": {"content": "OK"}, "finish_reason": "stop"}]}

    import requests

    def post(url, json=None, headers=None, timeout=None):
        calls.update(url=url, json=json, headers=headers)
        return R()

    monkeypatch.setattr(requests, "post", post)
    prof = {"provider_type": "openai_compatible", "base_url": "http://localhost:11434/v1/", "model": "llama",
            "key_storage": "none", "max_tokens": 100, "temperature": 0.2}
    res = providers.chat(prof, "sys", "hello")
    assert res.text == "OK" and calls["url"] == "http://localhost:11434/v1/chat/completions"
    assert "Authorization" not in calls["headers"] and calls["json"]["temperature"] == 0.2


def test_anthropic_provider_uses_sdk(monkeypatch):
    import anthropic

    seen = {}

    def create(**kw):
        seen.update(kw)
        return SimpleNamespace(content=[SimpleNamespace(type="text", text="回答")], model="claude-opus-5-5",
                               stop_reason="end_turn", usage=SimpleNamespace(input_tokens=10, output_tokens=5))

    class FakeClient:
        def __init__(self, **kw):
            seen["client"] = kw
            self.messages = SimpleNamespace(create=create)
            self.beta = SimpleNamespace(messages=SimpleNamespace(create=create))

    monkeypatch.setattr(anthropic, "Anthropic", FakeClient)
    monkeypatch.setenv("RCC_TEST_KEY", "k")
    res = providers.chat({**_profile(), "max_tokens": 500, "use_fallbacks": True}, "sys", "user")
    assert res.text == "回答" and seen["fallbacks"] == "default" and seen["betas"] == [providers.FALLBACK_BETA]
    assert seen["system"] == "sys" and "temperature" not in seen and seen["client"]["api_key"] == "k"
    monkeypatch.delenv("RCC_TEST_KEY")
    with pytest.raises(providers.AIProviderError, match="API Key"):
        providers.chat(_profile(), "s", "u")


def test_offline_checks(tmp_env):
    from datetime import timedelta

    from rcc.utils import today

    pid = projects.create_project({"name": "体检项目"})
    tasks.create_task({"title": "逾期的", "project_id": pid, "due_date": today() - timedelta(days=2)})
    experiments.create_experiment({"name": "失败无原因", "project_id": pid, "status": "Failed"})
    publications.create_publication({"title": "待确认论文", "project_id": pid, "status": "Unconfirmed"})
    msgs = [f.message for f in offline_checks.run_checks(pid)]
    assert any("逾期" in m for m in msgs) and any("失败原因" in m for m in msgs) and any("待您确认" in m for m in msgs)
    levels = [f.level for f in offline_checks.run_checks(pid)]
    assert levels == sorted(levels, key=lambda x: {"高": 0, "中": 1, "低": 2}[x])
