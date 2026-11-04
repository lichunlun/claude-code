"""模型配置管理。

API Key 存放方式（二选一，均不写入数据库或代码）：
- env：保存在本机环境变量中，这里只记录变量名（例如 RCC_ANTHROPIC_API_KEY）；
- keyring：保存在操作系统凭据管理器（Windows 凭据管理器 / macOS 钥匙串），这里只记录条目名。
本地模型（如 Ollama）可选择 none，不需要密钥。
"""
from __future__ import annotations

import os
import re
from typing import Optional

from sqlalchemy import select, update

from ...db import session_scope
from ...models import AISetting
from ...utils import ValidationError, clean_str, parse_float, parse_int
from .. import crud

KEYRING_SERVICE = "ResearchCommandCenter"
PROVIDER_TYPES = {"anthropic": "Anthropic Claude（官方 SDK）", "openai_compatible": "OpenAI 兼容接口"}
KEY_STORAGES = {"env": "环境变量", "keyring": "系统凭据管理器（keyring）", "none": "无需密钥（本地模型）"}
EFFORT_LEVELS = ["", "low", "medium", "high", "xhigh", "max"]

PRESETS = {
    "Anthropic Claude": {"provider_type": "anthropic", "base_url": "", "model": "claude-opus-5-5",
                         "api_key_env_var": "RCC_ANTHROPIC_API_KEY", "key_storage": "env"},
    "OpenAI GPT": {"provider_type": "openai_compatible", "base_url": "https://api.openai.com/v1", "model": "",
                   "api_key_env_var": "RCC_OPENAI_API_KEY", "key_storage": "env"},
    "Google Gemini（OpenAI 兼容端点）": {"provider_type": "openai_compatible",
                                    "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
                                    "model": "", "api_key_env_var": "RCC_GEMINI_API_KEY", "key_storage": "env"},
    "本地 Ollama": {"provider_type": "openai_compatible", "base_url": "http://localhost:11434/v1", "model": "",
                  "api_key_env_var": "", "key_storage": "none"},
    "自定义": {"provider_type": "openai_compatible", "base_url": "", "model": "", "api_key_env_var": "",
            "key_storage": "env"},
}


def keyring_available() -> bool:
    try:
        import keyring
        from keyring.backends import fail

        return not isinstance(keyring.get_keyring(), fail.Keyring)
    except Exception:  # noqa: BLE001
        return False


def clean_profile(data: dict) -> dict:
    errors = []
    name = clean_str(data.get("profile_name"), 100)
    if not name:
        errors.append("配置名称不能为空")
    ptype = data.get("provider_type")
    if ptype not in PROVIDER_TYPES:
        errors.append("未知的接口类型")
    model = clean_str(data.get("model"), 200)
    if not model:
        errors.append("请填写模型名称")
    base_url = clean_str(data.get("base_url"))
    if ptype == "openai_compatible" and not base_url:
        errors.append("OpenAI 兼容接口需要填写 API Base URL")
    if base_url and not re.match(r"^https?://", base_url):
        errors.append("API Base URL 应以 http:// 或 https:// 开头")
    storage = data.get("key_storage") or "env"
    if storage not in KEY_STORAGES:
        errors.append("未知的密钥存放方式")
    env_var = clean_str(data.get("api_key_env_var"), 100)
    if storage == "env":
        if not env_var:
            errors.append("请填写保存 API Key 的环境变量名")
        elif not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", env_var):
            errors.append("环境变量名只能包含字母、数字和下划线")
        elif env_var.startswith(("sk-", "sk_")) or len(env_var) > 60:
            errors.append("这里应填写“环境变量名”，而不是 API Key 本身")
    try:
        max_tokens = parse_int(data.get("max_tokens") or 8000, "最大输出 tokens", 256, 128000)
        temperature = parse_float(data.get("temperature"), "temperature", 0, 2)
    except ValidationError as e:
        errors.extend(e.errors)
        max_tokens, temperature = 8000, None
    effort = clean_str(data.get("effort"))
    if effort and effort not in EFFORT_LEVELS:
        errors.append("未知的 effort 等级")
    if errors:
        raise ValidationError(errors)
    return {"profile_name": name, "provider_type": ptype, "base_url": base_url, "model": model,
            "key_storage": storage, "api_key_env_var": env_var if storage == "env" else None,
            "max_tokens": max_tokens, "temperature": temperature if ptype == "openai_compatible" else None,
            "effort": effort if ptype == "anthropic" else None,
            "use_fallbacks": bool(data.get("use_fallbacks", True)) if ptype == "anthropic" else False}


def save_profile(data: dict, profile_id: Optional[int] = None, make_active: bool = False) -> int:
    clean = clean_profile(data)
    if profile_id:
        crud.update(AISetting, profile_id, clean, "ai_setting", f"更新模型配置：{clean['profile_name']}")
        pid = profile_id
    else:
        pid = crud.create(AISetting, clean, "ai_setting", f"新建模型配置：{clean['profile_name']}")
    if make_active or len(list_profiles()) == 1:
        set_active(pid)
    return pid


def set_active(profile_id: int) -> None:
    with session_scope() as s:
        s.execute(update(AISetting).values(is_active=False))
        p = s.get(AISetting, profile_id)
        if p is None:
            raise ValidationError("配置不存在")
        p.is_active = True


def delete_profile(profile_id: int) -> None:
    prof = crud.get(AISetting, profile_id)
    if prof and prof["key_storage"] == "keyring":
        try:
            import keyring

            keyring.delete_password(KEYRING_SERVICE, prof["profile_name"])
        except Exception:  # noqa: BLE001
            pass
    crud.delete(AISetting, profile_id, "ai_setting")


def list_profiles() -> list[dict]:
    return crud.list_dicts(select(AISetting).order_by(AISetting.is_active.desc(), AISetting.profile_name))


def get_profile(profile_id: Optional[int]) -> Optional[dict]:
    return crud.get(AISetting, profile_id)


def active_profile() -> Optional[dict]:
    rows = crud.list_dicts(select(AISetting).where(AISetting.is_active.is_(True)))
    return rows[0] if rows else None


# ------------------------------------------------------------------ keys
def store_key_in_keyring(profile_name: str, api_key: str) -> None:
    if not keyring_available():
        raise ValidationError("当前系统没有可用的凭据管理器（keyring），请改用环境变量")
    key = (api_key or "").strip()
    if not key:
        raise ValidationError("API Key 为空")
    import keyring

    keyring.set_password(KEYRING_SERVICE, profile_name, key)


def get_api_key(profile: dict) -> Optional[str]:
    storage = profile.get("key_storage")
    if storage == "none":
        return None
    if storage == "keyring":
        try:
            import keyring

            return keyring.get_password(KEYRING_SERVICE, profile["profile_name"])
        except Exception:  # noqa: BLE001
            return None
    var = profile.get("api_key_env_var")
    return os.environ.get(var) if var else None


def key_status(profile: dict) -> tuple[bool, str]:
    storage = profile.get("key_storage")
    if storage == "none":
        return True, "无需密钥"
    key = get_api_key(profile)
    if storage == "keyring":
        return (bool(key), "已在系统凭据管理器中找到密钥" if key else "凭据管理器中未找到密钥")
    var = profile.get("api_key_env_var")
    return (bool(key), f"环境变量 {var} 已设置" if key else f"环境变量 {var} 未设置（设置后需重启应用）")


def mask(key: Optional[str]) -> str:
    if not key:
        return "（无）"
    return key[:4] + "…" + key[-4:] if len(key) > 10 else "****"
