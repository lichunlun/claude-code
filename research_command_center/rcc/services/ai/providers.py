"""模型调用。

- Anthropic：使用官方 anthropic Python SDK（messages.create）；默认开启服务端拒答回退（fallbacks），
  可在配置中关闭。
- OpenAI 兼容：使用 HTTP 调用 /chat/completions，适配 OpenAI、Gemini 的 OpenAI 兼容端点、Ollama 等。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .profiles import get_api_key

FALLBACK_BETA = "server-side-fallback-2026-07-01"


class AIProviderError(RuntimeError):
    pass


@dataclass
class ChatResult:
    text: str
    model: str
    stop_reason: Optional[str] = None
    usage: dict = field(default_factory=dict)
    notice: Optional[str] = None


def _anthropic_chat(profile: dict, system: str, user: str, timeout: float) -> ChatResult:
    try:
        import anthropic
    except ImportError as e:  # pragma: no cover
        raise AIProviderError("未安装 anthropic SDK：请运行 pip install -r requirements.txt") from e
    key = get_api_key(profile)
    if not key:
        raise AIProviderError("未找到 API Key，请在“模型配置”中检查密钥设置")
    client = anthropic.Anthropic(api_key=key, base_url=profile.get("base_url") or None, timeout=timeout,
                                 max_retries=2)
    kwargs = {
        "model": profile["model"],
        "max_tokens": int(profile.get("max_tokens") or 8000),
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    if profile.get("effort"):
        kwargs["output_config"] = {"effort": profile["effort"]}
    try:
        if profile.get("use_fallbacks"):
            try:
                resp = client.beta.messages.create(**kwargs, betas=[FALLBACK_BETA], fallbacks="default")
            except anthropic.BadRequestError as e:
                # 某些代理/网关或模型不支持 fallbacks 参数时，退回普通调用
                if "fallback" not in str(e).lower():
                    raise
                resp = client.messages.create(**kwargs)
        else:
            resp = client.messages.create(**kwargs)
    except anthropic.AuthenticationError as e:
        raise AIProviderError("API Key 无效或已过期（401）") from e
    except anthropic.PermissionDeniedError as e:
        raise AIProviderError("API Key 没有访问该模型的权限（403）") from e
    except anthropic.NotFoundError as e:
        raise AIProviderError(f"模型或接口不存在（404）：{profile['model']}") from e
    except anthropic.RateLimitError as e:
        raise AIProviderError("请求过于频繁或额度不足（429），请稍后再试") from e
    except anthropic.BadRequestError as e:
        raise AIProviderError(f"请求参数错误（400）：{getattr(e, 'message', e)}") from e
    except anthropic.APIStatusError as e:
        raise AIProviderError(f"服务端错误（{e.status_code}）：{getattr(e, 'message', e)}") from e
    except anthropic.APIConnectionError as e:
        raise AIProviderError("无法连接到 Anthropic API（网络不可用或被拦截）") from e
    text = "".join(getattr(b, "text", "") for b in resp.content if getattr(b, "type", None) == "text")
    notice = None
    if resp.stop_reason == "refusal":
        details = getattr(resp, "stop_details", None)
        notice = "模型拒绝回答该请求" + (f"（类别：{details.category}）" if details and getattr(details, "category", None) else "")
    elif resp.stop_reason == "max_tokens":
        notice = "回答因达到最大输出长度而被截断，可在配置中调大 max_tokens"
    usage = {}
    if getattr(resp, "usage", None) is not None:
        usage = {"input_tokens": getattr(resp.usage, "input_tokens", None),
                 "output_tokens": getattr(resp.usage, "output_tokens", None)}
    return ChatResult(text=text, model=getattr(resp, "model", profile["model"]), stop_reason=resp.stop_reason,
                      usage=usage, notice=notice)


def _openai_compatible_chat(profile: dict, system: str, user: str, timeout: float) -> ChatResult:
    import requests

    base = (profile.get("base_url") or "").rstrip("/")
    if not base:
        raise AIProviderError("未配置 API Base URL")
    headers = {"Content-Type": "application/json"}
    key = get_api_key(profile)
    if profile.get("key_storage") != "none":
        if not key:
            raise AIProviderError("未找到 API Key，请在“模型配置”中检查密钥设置")
        headers["Authorization"] = f"Bearer {key}"
    body = {"model": profile["model"],
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "max_tokens": int(profile.get("max_tokens") or 8000)}
    if profile.get("temperature") is not None:
        body["temperature"] = float(profile["temperature"])
    try:
        r = requests.post(f"{base}/chat/completions", json=body, headers=headers, timeout=timeout)
        if r.status_code == 400 and "max_completion_tokens" in r.text:
            body["max_completion_tokens"] = body.pop("max_tokens")
            r = requests.post(f"{base}/chat/completions", json=body, headers=headers, timeout=timeout)
    except requests.RequestException as e:
        raise AIProviderError(f"无法连接到 {base}（{e.__class__.__name__}）") from e
    if r.status_code == 401:
        raise AIProviderError("API Key 无效（401）")
    if r.status_code == 404:
        raise AIProviderError(f"接口或模型不存在（404）：{profile['model']}")
    if r.status_code == 429:
        raise AIProviderError("请求过于频繁或额度不足（429）")
    if r.status_code >= 400:
        raise AIProviderError(f"接口返回错误 HTTP {r.status_code}：{r.text[:300]}")
    try:
        data = r.json()
        choice = data["choices"][0]
        text = choice["message"].get("content") or ""
    except (ValueError, KeyError, IndexError) as e:
        raise AIProviderError("接口返回格式无法解析（不是 OpenAI 兼容格式？）") from e
    notice = "回答因达到最大输出长度而被截断" if choice.get("finish_reason") == "length" else None
    return ChatResult(text=text, model=data.get("model", profile["model"]), stop_reason=choice.get("finish_reason"),
                      usage=data.get("usage") or {}, notice=notice)


def chat(profile: dict, system: str, user: str, timeout: float = 180.0) -> ChatResult:
    if profile.get("provider_type") == "anthropic":
        return _anthropic_chat(profile, system, user, timeout)
    if profile.get("provider_type") == "openai_compatible":
        return _openai_compatible_chat(profile, system, user, timeout)
    raise AIProviderError(f"未知的接口类型：{profile.get('provider_type')}")
