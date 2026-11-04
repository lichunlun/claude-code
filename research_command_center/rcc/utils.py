"""通用工具：输入清洗、校验、日期、路径。"""
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Optional


class ValidationError(ValueError):
    """用户输入校验失败。errors 为可直接展示给用户的中文消息列表。"""

    def __init__(self, errors: str | Iterable[str]):
        self.errors = [errors] if isinstance(errors, str) else list(errors)
        super().__init__("；".join(self.errors))


# ------------------------------------------------------------------ strings
def is_null(value: Any) -> bool:
    """None、NaN、pandas 的 NA/NaT 都视为空（表格编辑器中的空单元格会产生这些值）。"""
    if value is None:
        return True
    if isinstance(value, float) and value != value:
        return True
    return not isinstance(value, str) and str(value) in {"nan", "NaN", "<NA>", "NaT"}


def clean_str(value: Any, max_len: Optional[int] = None) -> Optional[str]:
    if is_null(value):
        return None
    s = str(value).strip()
    if not s:
        return None
    if max_len is not None and len(s) > max_len:
        raise ValidationError(f"内容过长（最多 {max_len} 个字符）")
    return s


def split_lines(value: Optional[str]) -> list[str]:
    if not value:
        return []
    return [ln.strip().strip('"').strip("'") for ln in str(value).splitlines() if ln.strip()]


def split_tags(value: Optional[str]) -> list[str]:
    if not value:
        return []
    parts = re.split(r"[,，;；\n]", str(value))
    seen: list[str] = []
    for p in parts:
        p = p.strip()
        if p and p not in seen:
            seen.append(p)
    return seen


def join_tags(tags: Iterable[str]) -> Optional[str]:
    tags = [t for t in tags if t]
    return ", ".join(tags) if tags else None


# ------------------------------------------------------------------ numbers
def parse_int(value: Any, field: str, lo: Optional[int] = None, hi: Optional[int] = None) -> Optional[int]:
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    try:
        if isinstance(value, float) and not value.is_integer():
            raise ValueError
        n = int(str(value).strip()) if not isinstance(value, (int, float)) else int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field}必须是整数")
    if lo is not None and n < lo or hi is not None and n > hi:
        raise ValidationError(f"{field}应在 {lo}–{hi} 之间")
    return n


def parse_float(value: Any, field: str, lo: Optional[float] = None, hi: Optional[float] = None) -> Optional[float]:
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    try:
        x = float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field}必须是数字")
    if x != x:  # NaN
        return None
    if lo is not None and x < lo or hi is not None and x > hi:
        raise ValidationError(f"{field}应在 {lo}–{hi} 之间")
    return x


# -------------------------------------------------------------------- dates
def parse_date(value: Any, field: str = "日期") -> Optional[date]:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    s = str(value).strip()
    if not s or s.lower() in {"nat", "none", "null"}:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y%m%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    raise ValidationError(f"{field}格式无效（应为 YYYY-MM-DD）：{s}")


def check_date_order(earlier: Optional[date], later: Optional[date], msg: str) -> None:
    if earlier and later and later < earlier:
        raise ValidationError(msg)


def today() -> date:
    return date.today()


def week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())


def days_until(d: Optional[date], ref: Optional[date] = None) -> Optional[int]:
    if d is None:
        return None
    return (d - (ref or today())).days


def humanize_days(n: Optional[int]) -> str:
    if n is None:
        return ""
    if n < 0:
        return f"已逾期 {-n} 天"
    if n == 0:
        return "今天"
    if n == 1:
        return "明天"
    return f"{n} 天后"


# --------------------------------------------------------------- identifiers
DOI_PATTERN = re.compile(r"^10\.\d{4,9}/\S+$")
_DOI_PREFIXES = ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "http://dx.doi.org/", "doi:", "doi ")


def normalize_doi(value: Any) -> Optional[str]:
    """规范化 DOI：去掉 URL 前缀与尾部标点，转小写（DOI 不区分大小写）。不合法则报错。"""
    s = clean_str(value)
    if s is None:
        return None
    low = s.lower()
    for p in _DOI_PREFIXES:
        if low.startswith(p):
            s = s[len(p):].strip()
            low = s.lower()
    s = s.rstrip(".,;:)]}>\"'")
    if not DOI_PATTERN.match(s):
        raise ValidationError(f"DOI 格式无效：{value}（应形如 10.xxxx/xxxxx）")
    return s.lower()


def normalize_pmid(value: Any) -> Optional[str]:
    s = clean_str(value)
    if s is None:
        return None
    s = re.sub(r"^(pmid[:\s]*)", "", s, flags=re.I).strip()
    if not re.fullmatch(r"\d{1,9}", s):
        raise ValidationError(f"PMID 必须为 1–9 位数字：{value}")
    return str(int(s))


def doi_url(doi: Optional[str]) -> Optional[str]:
    return f"https://doi.org/{doi}" if doi else None


def pmid_url(pmid: Optional[str]) -> Optional[str]:
    return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None


# -------------------------------------------------------------------- paths
def normalize_path(value: Any, field: str = "路径", must_be_absolute: bool = True) -> Optional[str]:
    s = clean_str(value)
    if s is None:
        return None
    s = s.strip().strip('"').strip("'")
    p = Path(os.path.expandvars(os.path.expanduser(s)))
    if must_be_absolute and not p.is_absolute():
        raise ValidationError(f"{field}必须是绝对路径（例如 D:\\Research\\data.xlsx 或 /home/me/data.xlsx）：{s}")
    try:
        p = p.resolve(strict=False)
    except OSError:
        pass
    return str(p)


def normalize_path_lines(value: Optional[str], field: str = "路径") -> Optional[str]:
    lines = [normalize_path(ln, field) for ln in split_lines(value)]
    lines = [ln for ln in lines if ln]
    return "\n".join(dict.fromkeys(lines)) if lines else None


def file_stat(path: str) -> dict[str, Any]:
    """只读获取文件状态，从不打开写入。"""
    p = Path(path)
    try:
        st = p.stat()
    except (OSError, ValueError):
        return {"exists": False, "size": None, "mtime": None, "is_dir": False}
    return {
        "exists": True,
        "size": st.st_size if p.is_file() else None,
        "mtime": datetime.fromtimestamp(st.st_mtime).replace(microsecond=0),
        "is_dir": p.is_dir(),
    }


def sha256_file(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:  # 只读
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def human_size(n: Optional[int]) -> str:
    if n is None:
        return ""
    size = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{n} B"


# --------------------------------------------------------------------- json
def dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str)


def loads(s: Optional[str], default: Any = None) -> Any:
    if not s:
        return default
    try:
        return json.loads(s)
    except (TypeError, ValueError):
        return default
