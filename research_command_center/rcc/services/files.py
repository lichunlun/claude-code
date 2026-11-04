"""文件中心：为原始科研文件建立索引（只记录绝对路径和状态）。

- 从不复制、移动、重命名或删除原始文件；
- “移出索引”只删除数据库中的引用；
- 预览以只读方式读取。
"""
from __future__ import annotations

import os
import platform
import subprocess
from pathlib import Path
from typing import Optional

from sqlalchemy import select

from ..constants import EXTENSION_CATEGORY, FILE_CATEGORIES
from ..db import session_scope
from ..models import FileIndex, now
from ..utils import ValidationError, clean_str, file_stat, normalize_path
from . import crud

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", ".Rproj.user", "$RECYCLE.BIN"}


def categorize(path: str) -> str:
    return EXTENSION_CATEGORY.get(Path(path).suffix.lower(), "其他")


def register_file(path: str, project_id: Optional[int] = None, category: Optional[str] = None,
                  description: Optional[str] = None, allow_missing: bool = False) -> int:
    norm = normalize_path(path, "文件路径")
    if not norm:
        raise ValidationError("文件路径不能为空")
    st = file_stat(norm)
    if not st["exists"] and not allow_missing:
        raise ValidationError(f"文件不存在：{norm}")
    if st.get("is_dir"):
        raise ValidationError("这是一个文件夹；请使用“扫描文件夹”批量登记其中的文件")
    cat = category or categorize(norm)
    if cat not in FILE_CATEGORIES:
        raise ValidationError(f"未知的文件类别：{cat}")
    with session_scope() as s:
        if s.scalar(select(FileIndex.id).where(FileIndex.path == norm)):
            raise ValidationError(f"该文件已在索引中：{norm}")
        f = FileIndex(path=norm, file_name=Path(norm).name, extension=Path(norm).suffix.lower() or None,
                      category=cat, description=clean_str(description), project_id=project_id or None,
                      exists=st["exists"], size_bytes=st["size"], modified_at=st["mtime"], last_checked_at=now())
        s.add(f)
        s.flush()
        crud.log_activity(s, "file", f.id, "register", f"登记文件（仅引用）：{norm}")
        return f.id


def register_many(paths: list[str], project_id: Optional[int] = None, category: Optional[str] = None) -> dict:
    added, skipped = [], []
    for p in paths:
        try:
            added.append(register_file(p, project_id, category))
        except ValidationError as e:
            skipped.append({"path": p, "reason": e.errors[0]})
    return {"added": added, "skipped": skipped}


def update_file(file_id: int, project_id: Optional[int], category: Optional[str], description: Optional[str]) -> None:
    if category and category not in FILE_CATEGORIES:
        raise ValidationError("未知的文件类别")
    crud.update(FileIndex, file_id, {"project_id": project_id or None, "category": category,
                                     "description": clean_str(description)}, "file")


def remove_from_index(file_id: int) -> None:
    """只删除索引记录，不会删除磁盘文件。"""
    crud.delete(FileIndex, file_id, "file", f"文件 #{file_id} 移出索引（磁盘文件未受影响）")


def refresh_status(file_ids: Optional[list[int]] = None) -> dict:
    checked = missing = changed = 0
    with session_scope() as s:
        stmt = select(FileIndex)
        if file_ids:
            stmt = stmt.where(FileIndex.id.in_(file_ids))
        for f in s.scalars(stmt):
            st = file_stat(f.path)
            if st["exists"] != f.exists or st["mtime"] != f.modified_at or st["size"] != f.size_bytes:
                changed += 1
            f.exists, f.size_bytes, f.modified_at, f.last_checked_at = st["exists"], st["size"], st["mtime"], now()
            checked += 1
            if not st["exists"]:
                missing += 1
    return {"checked": checked, "missing": missing, "changed": changed}


def list_files(project_id: Optional[int] = None, categories: Optional[list[str]] = None,
               exists: Optional[bool] = None, search: Optional[str] = None, unassigned: bool = False) -> list[dict]:
    stmt = select(FileIndex)
    if unassigned:
        stmt = stmt.where(FileIndex.project_id.is_(None))
    elif project_id:
        stmt = stmt.where(FileIndex.project_id == project_id)
    if categories:
        stmt = stmt.where(FileIndex.category.in_(categories))
    if exists is not None:
        stmt = stmt.where(FileIndex.exists.is_(exists))
    if search:
        like = f"%{search.strip()}%"
        stmt = stmt.where(FileIndex.path.ilike(like) | FileIndex.description.ilike(like))
    return crud.list_dicts(stmt.order_by(FileIndex.modified_at.desc().nulls_last()))


def scan_folder(folder: str, extensions: Optional[list[str]] = None, recursive: bool = True,
                limit: int = 2000) -> list[dict]:
    """列出文件夹中的文件（只读遍历），供用户勾选后登记。"""
    root_s = normalize_path(folder, "文件夹路径")
    root = Path(root_s)
    if not root.is_dir():
        raise ValidationError(f"文件夹不存在：{root_s}")
    exts = {e.lower() if e.startswith(".") else "." + e.lower() for e in (extensions or [])}
    with session_scope() as s:
        indexed = set(s.scalars(select(FileIndex.path)).all())
    out: list[dict] = []
    walker = os.walk(root) if recursive else [(str(root), [], os.listdir(root))]
    for dirpath, dirnames, filenames in walker:
        if recursive:
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in sorted(filenames):
            if fn.startswith(".") or fn.startswith("~$"):
                continue
            p = Path(dirpath) / fn
            if not p.is_file():
                continue
            if exts and p.suffix.lower() not in exts:
                continue
            st = file_stat(str(p))
            ps = str(p.resolve())
            out.append({"path": ps, "name": fn, "category": categorize(ps), "size": st["size"],
                        "mtime": st["mtime"], "indexed": ps in indexed})
            if len(out) >= limit:
                return out
    return out


def open_in_system(path: str, reveal: bool = False) -> None:
    """用系统默认程序打开文件或所在文件夹（只读动作；仅限本机运行时有效）。"""
    p = Path(path)
    if not p.exists():
        raise ValidationError(f"文件不存在：{path}")
    target = str(p.parent if reveal else p)
    system = platform.system()
    try:
        if system == "Windows":
            if reveal:
                subprocess.Popen(["explorer", "/select,", str(p)])
            else:
                os.startfile(target)  # type: ignore[attr-defined]
        elif system == "Darwin":
            subprocess.Popen(["open", "-R", str(p)] if reveal else ["open", target])
        else:
            subprocess.Popen(["xdg-open", target])
    except Exception as e:  # noqa: BLE001
        raise ValidationError(f"无法打开：{e}")


def preview(path: str, max_chars: int = 4000) -> dict:
    """只读预览：Word / PDF / 表格 / 文本 / 图片。"""
    p = Path(path)
    if not p.exists():
        return {"kind": "missing", "content": None}
    ext = p.suffix.lower()
    try:
        if ext == ".docx":
            import docx  # python-docx

            d = docx.Document(str(p))
            paras = [para.text for para in d.paragraphs if para.text.strip()]
            words = sum(len(x.split()) for x in paras)
            return {"kind": "text", "content": "\n\n".join(paras)[:max_chars],
                    "meta": f"{len(paras)} 段 · 约 {words} 个英文词/词组 · {len(d.tables)} 个表格"}
        if ext == ".pdf":
            from .pdf_import import pymupdf

            with pymupdf.open(str(p)) as doc:
                txt = doc[0].get_text("text") if doc.page_count else ""
                return {"kind": "text", "content": txt[:max_chars], "meta": f"共 {doc.page_count} 页（显示第 1 页文本）"}
        if ext in (".csv", ".tsv", ".xlsx", ".xls"):
            import pandas as pd

            if ext in (".csv", ".tsv"):
                df = pd.read_csv(str(p), sep="\t" if ext == ".tsv" else ",", nrows=50, encoding_errors="replace")
            else:
                df = pd.read_excel(str(p), nrows=50)
            return {"kind": "table", "content": df, "meta": "显示前 50 行（只读）"}
        if ext in (".png", ".jpg", ".jpeg", ".gif", ".bmp"):
            return {"kind": "image", "content": str(p)}
        if ext in (".txt", ".md", ".r", ".py", ".rmd", ".qmd", ".log", ".json", ".yaml", ".yml", ".sh", ".tex"):
            with open(p, "r", encoding="utf-8", errors="replace") as fh:
                return {"kind": "code" if ext in (".r", ".py", ".sh") else "text", "content": fh.read(max_chars),
                        "lang": {".r": "r", ".py": "python", ".sh": "bash"}.get(ext)}
    except Exception as e:  # noqa: BLE001
        return {"kind": "error", "content": f"预览失败：{e}"}
    return {"kind": "unsupported", "content": None}
