"""AI 科研助手接口层。

- profiles.py      模型配置（不保存 API Key 明文）
- providers.py     Anthropic（官方 SDK）与 OpenAI 兼容接口（GPT / Gemini / 本地 Ollama 等）
- context.py       在用户授权范围内，从数据库构建事实上下文
- prompts.py       系统提示词：区分事实 / 推测 / 建议，禁止编造
- offline_checks.py 不需要任何 API 的规则化“科研体检”
- assistant.py     一次完整调用：预览 → 用户确认 → 发送 → 留痕
"""
