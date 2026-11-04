"""一键启动 / 关闭 / 状态（只依赖 Python 标准库，可在依赖安装前运行）。

用法：
    python scripts/launcher.py start [--port 8501] [--no-browser]
    python scripts/launcher.py stop
    python scripts/launcher.py status

依赖只在首次运行或 requirements.txt 变化时安装（以文件哈希判断），之后启动不再重复配置环境。
"""
from __future__ import annotations

import argparse
import hashlib
import os
import platform
import signal
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from rcc.config import get_settings  # noqa: E402  (rcc.config 只依赖标准库)

REQ = ROOT / "requirements.txt"
IS_WIN = platform.system() == "Windows"


def _pid_file() -> Path:
    s = get_settings()
    s.data_dir.mkdir(parents=True, exist_ok=True)
    return s.data_dir / "rcc.pid"


def _alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if IS_WIN:
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True)
        return str(pid) in out.stdout
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


def ensure_deps() -> None:
    if sys.version_info < (3, 11):
        sys.exit("[RCC] 需要 Python 3.11 或更高版本，当前为 " + platform.python_version())
    digest = hashlib.sha256(REQ.read_bytes()).hexdigest()
    stamp = Path(sys.prefix) / ".rcc_requirements.sha256"
    if stamp.exists() and stamp.read_text().strip() == digest:
        return
    print("[RCC] 正在安装依赖（仅在首次运行或 requirements.txt 变化时执行）……", flush=True)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "-q", "-r", str(REQ)])
    stamp.write_text(digest)
    print("[RCC] 依赖已就绪。", flush=True)


def start(port: int, open_browser: bool) -> int:
    pf = _pid_file()
    if pf.exists():
        try:
            pid = int(pf.read_text().strip())
        except ValueError:
            pid = -1
        if _alive(pid) and _port_open(port):
            print(f"[RCC] 应用已在运行：http://localhost:{port}")
            if open_browser:
                webbrowser.open(f"http://localhost:{port}")
            return 0
        pf.unlink(missing_ok=True)
    if _port_open(port):
        print(f"[RCC] 端口 {port} 已被其他程序占用，请使用 --port 指定其他端口。")
        return 1
    ensure_deps()
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    cmd = [sys.executable, "-m", "streamlit", "run", str(ROOT / "app.py"),
           "--server.port", str(port), "--server.address", "127.0.0.1",
           "--server.headless", "false" if open_browser else "true",
           "--browser.gatherUsageStats", "false"]
    proc = subprocess.Popen(cmd, cwd=str(ROOT), env=env)
    pf.write_text(str(proc.pid))
    print(f"[RCC] Research Command Center 已启动：http://localhost:{port}", flush=True)
    print("[RCC] 关闭方法：在本窗口按 Ctrl+C，或运行 stop 脚本。", flush=True)
    try:
        return proc.wait()
    except KeyboardInterrupt:
        print("\n[RCC] 正在关闭……", flush=True)
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        return 0
    finally:
        pf.unlink(missing_ok=True)


def stop() -> int:
    pf = _pid_file()
    if not pf.exists():
        print("[RCC] 没有找到正在运行的应用。")
        return 0
    try:
        pid = int(pf.read_text().strip())
    except ValueError:
        pf.unlink(missing_ok=True)
        return 0
    if not _alive(pid):
        print("[RCC] 应用未在运行（已清理过期的 PID 文件）。")
        pf.unlink(missing_ok=True)
        return 0
    if IS_WIN:
        subprocess.call(["taskkill", "/PID", str(pid), "/T", "/F"])
    else:
        os.kill(pid, signal.SIGTERM)
        for _ in range(50):
            if not _alive(pid):
                break
            time.sleep(0.2)
    pf.unlink(missing_ok=True)
    print("[RCC] 应用已关闭。")
    return 0


def status(port: int) -> int:
    pf = _pid_file()
    pid = int(pf.read_text().strip()) if pf.exists() and pf.read_text().strip().isdigit() else None
    running = bool(pid and _alive(pid))
    print(f"[RCC] 运行中：{'是' if running else '否'}；端口 {port}：{'已占用' if _port_open(port) else '空闲'}；"
          f"数据库：{get_settings().db_path}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Research Command Center 启动器")
    ap.add_argument("command", choices=["start", "stop", "status"])
    ap.add_argument("--port", type=int, default=8501)
    ap.add_argument("--no-browser", action="store_true")
    a = ap.parse_args()
    if a.command == "start":
        return start(a.port, not a.no_browser)
    if a.command == "stop":
        return stop()
    return status(a.port)


if __name__ == "__main__":
    sys.exit(main())
