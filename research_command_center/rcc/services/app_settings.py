"""界面可修改的应用设置（保存在 app_meta 表）。不包含任何密钥。"""
from __future__ import annotations

import shutil
from typing import Optional

from ..db import get_meta, set_meta
from ..utils import ValidationError, normalize_path, parse_int

KEY_ALLOW_EXEC = "allow_script_execution"
KEY_PYTHON = "python_interpreter"
KEY_RSCRIPT = "rscript_interpreter"
KEY_TIMEOUT = "script_timeout_minutes"


def allow_script_execution() -> bool:
    return get_meta(KEY_ALLOW_EXEC, "0") == "1"


def set_allow_script_execution(value: bool) -> None:
    set_meta(KEY_ALLOW_EXEC, "1" if value else "0")


def python_interpreter() -> Optional[str]:
    return get_meta(KEY_PYTHON) or shutil.which("python") or shutil.which("python3")


def rscript_interpreter() -> Optional[str]:
    return get_meta(KEY_RSCRIPT) or shutil.which("Rscript")


def set_interpreters(python_path: Optional[str], rscript_path: Optional[str]) -> None:
    for key, val, label in ((KEY_PYTHON, python_path, "Python 解释器"), (KEY_RSCRIPT, rscript_path, "Rscript")):
        norm = normalize_path(val, label) if val else None
        set_meta(key, norm)


def script_timeout_minutes() -> int:
    try:
        return int(get_meta(KEY_TIMEOUT, "120") or 120)
    except ValueError:
        return 120


def set_script_timeout_minutes(value) -> None:
    n = parse_int(value, "超时时间（分钟）", 1, 7 * 24 * 60)
    if n is None:
        raise ValidationError("请填写超时时间")
    set_meta(KEY_TIMEOUT, str(n))
