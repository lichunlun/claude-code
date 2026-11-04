"""初始化数据库（建表 + 预置三个项目）。通常无需手动运行：首次启动应用时会自动执行。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from rcc import db, seed  # noqa: E402
from rcc.config import get_settings  # noqa: E402

if __name__ == "__main__":
    s = get_settings()
    s.ensure_dirs()
    db.init_engine()
    created = seed.seed_initial_data()
    print(f"数据库：{s.db_path}\n预置项目：{'已写入' if created else '已存在，跳过'}")
