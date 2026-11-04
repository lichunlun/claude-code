"""一键备份数据库。

    python scripts/backup_db.py            # 立即创建一份手动备份
    python scripts/backup_db.py --list     # 列出所有备份
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from rcc import db  # noqa: E402
from rcc.config import get_settings  # noqa: E402
from rcc.services import backup  # noqa: E402
from rcc.utils import ValidationError, human_size  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="备份 Research Command Center 数据库")
    ap.add_argument("--list", action="store_true", help="列出已有备份")
    a = ap.parse_args()
    s = get_settings()
    if a.list:
        rows = backup.list_backups()
        if not rows:
            print("暂无备份。备份目录：", s.backup_dir)
        for r in rows:
            print(f"{r['created']:%Y-%m-%d %H:%M:%S}  {r['kind']:<12} {human_size(r['size']):>9}  {r['path']}")
        return 0
    if not s.db_path.exists():
        print("数据库不存在：", s.db_path)
        return 1
    db.init_engine()
    try:
        p = backup.backup_database("manual")
    except ValidationError as e:
        print("备份失败：", e)
        return 1
    ok, msg = backup.verify_backup(p)
    print(f"备份完成：{p}\n完整性检查：{'通过' if ok else msg}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
