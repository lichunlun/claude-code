"""从备份恢复数据库（请先关闭应用）。

    python scripts/restore_db.py --list
    python scripts/restore_db.py --latest
    python scripts/restore_db.py --file "D:\\...\\backups\\research_20261104_101500_manual.db"

恢复前会自动把当前数据库另存为一份 pre-restore 备份，因此可以撤销。
"""
from __future__ import annotations

import argparse
import socket
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from rcc.config import get_settings  # noqa: E402
from rcc.services import backup  # noqa: E402
from rcc.utils import ValidationError, human_size  # noqa: E402


def _app_running(port: int = 8501) -> bool:
    if (get_settings().data_dir / "rcc.pid").exists():
        return True
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


def main() -> int:
    ap = argparse.ArgumentParser(description="从备份恢复 Research Command Center 数据库")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--list", action="store_true")
    g.add_argument("--latest", action="store_true", help="恢复最近一份备份（不含 pre-restore）")
    g.add_argument("--file", help="备份文件路径")
    ap.add_argument("--yes", action="store_true", help="跳过交互确认")
    ap.add_argument("--force", action="store_true", help="即使检测到应用可能在运行也继续（不推荐）")
    a = ap.parse_args()
    s = get_settings()
    rows = backup.list_backups()
    if a.list:
        for r in rows:
            ok, _ = backup.verify_backup(r["path"])
            print(f"{r['created']:%Y-%m-%d %H:%M:%S}  {r['kind']:<12} {human_size(r['size']):>9}  {'OK ' if ok else 'BAD'}  {r['path']}")
        if not rows:
            print("暂无备份：", s.backup_dir)
        return 0
    if a.latest:
        cands = [r for r in rows if r["kind"] != "pre-restore"]
        if not cands:
            print("没有可用的备份。")
            return 1
        src = cands[0]["path"]
    else:
        src = a.file
    ok, msg = backup.verify_backup(src)
    if not ok:
        print("备份文件不可用：", msg)
        return 1
    if _app_running() and not a.force:
        print("检测到应用可能正在运行。请先运行 stop 脚本关闭应用后再恢复（或使用 --force）。")
        return 1
    print(f"将用以下备份覆盖当前数据库：\n  备份：{src}\n  目标：{s.db_path}")
    if not a.yes and input("输入 yes 确认：").strip().lower() != "yes":
        print("已取消。")
        return 1
    try:
        pre = backup.restore_database(src, db_path=s.db_path)
    except ValidationError as e:
        print("恢复失败：", e)
        return 1
    print(f"恢复完成。恢复前的数据库已另存为：{pre}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
