"""运行配置：数据目录、备份目录等。

优先级（高 → 低）：
1. 环境变量 RCC_DATA_DIR / RCC_BACKUP_DIR / RCC_BACKUP_KEEP / RCC_AUTO_BACKUP_HOURS
2. config/settings.toml（可选，用户自建，不纳入版本库）
3. 默认值：<项目目录>/data 与 <数据目录>/backups

数据库与代码分离：代码在 rcc/，数据在 data/（已被 .gitignore 排除）。
"""
from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = APP_ROOT / "config" / "settings.toml"
DB_FILENAME = "research.db"


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    backup_dir: Path
    backup_keep: int = 30
    auto_backup_hours: float = 24.0

    @property
    def db_path(self) -> Path:
        return self.data_dir / DB_FILENAME

    @property
    def log_dir(self) -> Path:
        return self.data_dir / "logs"

    @property
    def library_dir(self) -> Path:
        """仅存放用户通过“上传”明确要求保存的文献副本。"""
        return self.data_dir / "library"

    def ensure_dirs(self) -> None:
        for d in (self.data_dir, self.backup_dir, self.log_dir, self.library_dir):
            d.mkdir(parents=True, exist_ok=True)


def _resolve(p: str | os.PathLike) -> Path:
    path = Path(os.path.expandvars(os.path.expanduser(str(p))))
    if not path.is_absolute():
        path = APP_ROOT / path
    return path.resolve()


def _read_toml() -> dict:
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("rb") as fh:
            return tomllib.load(fh)
    return {}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    cfg = _read_toml()
    paths = cfg.get("paths", {})
    backup = cfg.get("backup", {})

    data_dir = _resolve(os.environ.get("RCC_DATA_DIR") or paths.get("data_dir") or "data")
    backup_dir_raw = os.environ.get("RCC_BACKUP_DIR") or paths.get("backup_dir")
    backup_dir = _resolve(backup_dir_raw) if backup_dir_raw else data_dir / "backups"

    keep = int(os.environ.get("RCC_BACKUP_KEEP") or backup.get("keep", 30))
    hours = float(os.environ.get("RCC_AUTO_BACKUP_HOURS") or backup.get("interval_hours", 24))
    return Settings(data_dir=data_dir, backup_dir=backup_dir, backup_keep=max(keep, 1),
                    auto_backup_hours=max(hours, 0.0))


def reset_settings_cache() -> None:
    """测试或切换数据目录时使用。"""
    get_settings.cache_clear()
