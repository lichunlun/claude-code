"""一次完整的 AI 调用：构建上下文 → （界面展示并由用户确认）→ 发送 → 留痕。"""
from __future__ import annotations

from typing import Optional

from sqlalchemy import select

from ...db import session_scope
from ...models import AIInteraction
from ...utils import ValidationError, clean_str, dumps
from .. import crud
from .context import build_context
from .prompts import REQUEST_TYPES, SYSTEM_PROMPT
from .providers import AIProviderError, ChatResult, chat


def compose_user_message(context: str, request_type: str, question: Optional[str]) -> str:
    if request_type not in REQUEST_TYPES:
        raise ValidationError("未知的请求类型")
    title, instruction = REQUEST_TYPES[request_type]
    q = clean_str(question)
    if request_type == "free" and not q:
        raise ValidationError("请输入您的问题")
    parts = [context.strip(), "", f"# 研究者的请求：{title}"]
    if instruction:
        parts.append(instruction)
    if q:
        parts.append(f"补充说明 / 问题：{q}")
    return "\n".join(parts)


def ask(profile: dict, project_id: int, scopes: list[str], request_type: str, question: Optional[str],
        authorized: bool) -> ChatResult:
    if not authorized:
        raise ValidationError("请先确认授权：允许将上述记录发送给所选模型")
    if not scopes:
        raise ValidationError("请至少授权一类数据")
    context = build_context(project_id, scopes)
    user_msg = compose_user_message(context, request_type, question)
    status, err, result = "ok", None, None
    try:
        result = chat(profile, SYSTEM_PROMPT, user_msg)
        return result
    except AIProviderError as e:
        status, err = "error", str(e)
        raise
    finally:
        with session_scope() as s:
            s.add(AIInteraction(project_id=project_id, profile_name=profile.get("profile_name"),
                                model=(result.model if result else profile.get("model")), request_type=request_type,
                                context_scopes=dumps(scopes), question=clean_str(question),
                                context_chars=len(user_msg), response=result.text if result else None,
                                status=status, error=err))
            crud.log_activity(s, "ai", project_id, "ai_request",
                              f"AI 请求（{REQUEST_TYPES[request_type][0]}，授权范围：{', '.join(scopes)}）：{status}")


def history(n: int = 50) -> list[dict]:
    return crud.list_dicts(select(AIInteraction).order_by(AIInteraction.id.desc()).limit(n))
