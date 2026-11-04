"""安全执行本机 R / Python 脚本（第二阶段功能，默认关闭）。

安全设计：
1. 设置中未开启“允许执行脚本”时，任何执行请求都会被拒绝；
2. 只执行已登记在分析任务中、扩展名与语言匹配（.R / .py）的脚本；
3. 执行前生成预览：完整命令、工作目录、输入文件（存在性）、输出路径、脚本 SHA-256；
4. 用户必须勾选确认；若确认后脚本内容发生变化（SHA-256 不同）则拒绝执行；
5. 不使用 shell（shell=False），参数逐个传递，避免命令注入；
6. 运行成功也只标记为 Needs Verification（结果需人工核验），不会自动标记 Completed；
7. 日志写入数据目录 logs/，不触碰输入文件。脚本本身的写操作由脚本决定，界面会给出提醒。
"""
from __future__ import annotations

import subprocess
import threading
from pathlib import Path
from typing import Optional

from ..config import get_settings
from ..constants import RUNNABLE_EXTENSIONS
from ..db import session_scope
from ..models import BioinformaticsJob, BioinformaticsRun, now
from ..utils import ValidationError, dumps, file_stat, sha256_file, split_lines
from . import app_settings, crud

_PROCS: dict[int, subprocess.Popen] = {}
_LOCK = threading.Lock()


def running_pids() -> set[int]:
    with _LOCK:
        return {p.pid for p in _PROCS.values() if p.poll() is None}


def build_preview(job_id: int) -> dict:
    with session_scope() as s:
        job = s.get(BioinformaticsJob, job_id)
        if job is None:
            raise ValidationError("分析任务不存在")
        job_d = job.to_dict()
    errors: list[str] = []
    warnings: list[str] = []
    if not app_settings.allow_script_execution():
        errors.append("脚本执行功能未开启（设置 → 脚本执行）。默认关闭以保护您的数据。")
    lang = job_d.get("language")
    script = job_d.get("script_path")
    if lang not in RUNNABLE_EXTENSIONS:
        errors.append("仅支持执行 R 或 Python 脚本（请在任务中设置分析语言）")
    if not script:
        errors.append("未登记脚本路径")
    sha = None
    if script:
        st = file_stat(script)
        if not st["exists"] or st["is_dir"]:
            errors.append(f"脚本文件不存在：{script}")
        else:
            if lang in RUNNABLE_EXTENSIONS and Path(script).suffix.lower() not in RUNNABLE_EXTENSIONS[lang]:
                errors.append(f"脚本扩展名与分析语言（{lang}）不匹配")
            sha = sha256_file(script)
    interp = app_settings.python_interpreter() if lang == "Python" else app_settings.rscript_interpreter() if lang == "R" else None
    if lang in RUNNABLE_EXTENSIONS and not interp:
        errors.append(f"未找到 {'Python' if lang == 'Python' else 'Rscript'} 解释器，请在设置中指定路径")
    args = split_lines(job_d.get("script_args"))
    cwd = job_d.get("working_dir") or (str(Path(script).parent) if script else None)
    if cwd and not Path(cwd).is_dir():
        errors.append(f"工作目录不存在：{cwd}")
    inputs = []
    for p in split_lines(job_d.get("data_paths")):
        st = file_stat(p)
        inputs.append({"path": p, "exists": st["exists"]})
        if not st["exists"]:
            warnings.append(f"输入文件不存在：{p}")
    outputs = []
    for p in split_lines(job_d.get("output_paths")):
        st = file_stat(p)
        outputs.append({"path": p, "exists": st["exists"]})
        if st["exists"]:
            warnings.append(f"输出路径已存在，脚本运行可能覆盖它：{p}")
    warnings.append("本系统不会修改您的输入文件，但脚本自身的读写行为由脚本代码决定，请确认脚本来源可信。")
    cmd = [interp, script, *args] if (interp and script) else []
    log_path = get_settings().log_dir / f"job{job_id}_{now().strftime('%Y%m%d_%H%M%S')}.log"
    return {
        "ok": not errors, "errors": errors, "warnings": warnings, "command": cmd, "cwd": cwd,
        "inputs": inputs, "outputs": outputs, "script_sha256": sha, "log_path": str(log_path),
        "timeout_minutes": app_settings.script_timeout_minutes(), "job": job_d,
    }


def _tail(path: str, n: int = 4000) -> str:
    try:
        data = Path(path).read_bytes()
    except OSError:
        return ""
    return data[-n:].decode("utf-8", errors="replace")


tail_log = _tail


def _watch(run_id: int, job_id: int, proc: subprocess.Popen, log_fh, timeout_s: int) -> None:
    status, exit_code, note = "Needs Verification", None, None
    try:
        exit_code = proc.wait(timeout=timeout_s)
        if exit_code != 0:
            status, note = "Failed", f"进程退出码 {exit_code}"
        else:
            note = "进程正常结束（退出码 0）。请核验输出文件与结果后再标记为 Completed。"
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        exit_code, status, note = -1, "Failed", f"运行超时（{timeout_s // 60} 分钟）已终止"
    except Exception as e:  # noqa: BLE001
        status, note = "Failed", f"监控进程出错：{e}"
    finally:
        try:
            log_fh.close()
        except Exception:  # noqa: BLE001
            pass
        with _LOCK:
            _PROCS.pop(run_id, None)
    with session_scope() as s:
        run = s.get(BioinformaticsRun, run_id)
        job = s.get(BioinformaticsJob, job_id)
        tail = _tail(run.log_path) if run and run.log_path else ""
        if run is not None:
            if run.status == "Cancelled":
                status = "Failed"
                note = "用户已取消运行"
            run.status, run.exit_code, run.finished_at, run.log_excerpt = status, exit_code, now(), tail
            run.note = note
        if job is not None:
            job.status = status
            job.run_finished_at = now()
            if status == "Failed":
                job.error_log = (note or "") + "\n---- 日志末尾 ----\n" + tail
        crud.log_activity(s, "bioinformatics_job", job_id, "run_finished", f"分析任务 #{job_id} 运行结束：{status}",
                          {"exit_code": exit_code})


def start_run(job_id: int, confirmed: bool, expected_sha256: Optional[str]) -> int:
    if not confirmed:
        raise ValidationError("执行脚本前必须确认命令、输入文件和输出路径")
    pv = build_preview(job_id)
    if not pv["ok"]:
        raise ValidationError(pv["errors"])
    if not expected_sha256 or expected_sha256 != pv["script_sha256"]:
        raise ValidationError("脚本内容在您确认之后发生了变化（SHA-256 不一致），请重新查看并确认")
    if pv["job"]["status"] == "Running":
        raise ValidationError("该任务正在运行")
    log_path = Path(pv["log_path"])
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_fh = open(log_path, "w", encoding="utf-8", errors="replace")
    log_fh.write(f"# Research Command Center 运行日志\n# 命令: {pv['command']}\n# 工作目录: {pv['cwd']}\n"
                 f"# 脚本 SHA-256: {pv['script_sha256']}\n# 开始: {now()}\n\n")
    log_fh.flush()
    try:
        proc = subprocess.Popen(pv["command"], cwd=pv["cwd"], stdout=log_fh, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL, shell=False)
    except OSError as e:
        log_fh.close()
        raise ValidationError(f"无法启动进程：{e}")
    with session_scope() as s:
        run = BioinformaticsRun(job_id=job_id, source="executed", command=dumps(pv["command"]),
                                script_sha256=pv["script_sha256"], started_at=now(), status="Running",
                                log_path=str(log_path), pid=proc.pid, confirmed_by_user=True)
        s.add(run)
        job = s.get(BioinformaticsJob, job_id)
        job.status, job.run_started_at, job.run_finished_at = "Running", now(), None
        s.flush()
        run_id = run.id
        crud.log_activity(s, "bioinformatics_job", job_id, "run_started", f"用户确认后执行分析任务 #{job_id}",
                          {"command": pv["command"], "sha256": pv["script_sha256"]})
    with _LOCK:
        _PROCS[run_id] = proc
    t = threading.Thread(target=_watch, args=(run_id, job_id, proc, log_fh, pv["timeout_minutes"] * 60), daemon=True)
    t.start()
    return run_id


def cancel_run(run_id: int) -> bool:
    with _LOCK:
        proc = _PROCS.get(run_id)
    if proc is None or proc.poll() is not None:
        return False
    with session_scope() as s:
        run = s.get(BioinformaticsRun, run_id)
        if run is not None:
            run.status = "Cancelled"
    proc.terminate()
    return True


def wait_for(run_id: int, timeout: float = 30.0) -> None:
    """测试辅助：等待运行线程结束。"""
    import time

    deadline = time.time() + timeout
    while time.time() < deadline:
        with _LOCK:
            if run_id not in _PROCS:
                return
        time.sleep(0.1)
