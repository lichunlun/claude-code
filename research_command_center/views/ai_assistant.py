"""AI 科研助手：授权上下文 → 预览 → 确认发送；离线体检；模型配置；调用记录。"""
from __future__ import annotations

from typing import Optional

import streamlit as st

from rcc.services import projects
from rcc.services.ai import assistant, offline_checks, profiles
from rcc.services.ai.context import SCOPES, build_context
from rcc.services.ai.prompts import REQUEST_TYPES, SYSTEM_PROMPT
from rcc.services.ai.providers import AIProviderError
from rcc.ui.common import (
    bootstrap,
    confirm_button,
    empty_state,
    esc,
    fmt_dt,
    html_block,
    page_header,
    project_selector,
    run_action,
    show_errors,
    show_flash,
    tag,
)
from rcc.utils import ValidationError, loads

bootstrap()
show_flash()
names = projects.project_name_map()

page_header("AI 科研助手", "可选功能：未配置模型时其他所有功能照常使用。AI 只能读取您逐项授权的记录，且必须区分事实、推测与建议。")
t_ask, t_check, t_cfg, t_hist = st.tabs(["科研助手", "离线科研体检", "模型配置", "调用记录"])

# ------------------------------------------------------------------- ask
with t_ask:
    plist = profiles.list_profiles()
    if not plist:
        st.info("尚未配置任何模型。请先在“模型配置”中添加（支持 Anthropic Claude、OpenAI GPT、Google Gemini、本地 Ollama 等）。"
                "不配置也可以使用“离线科研体检”。", icon="ℹ️")
    else:
        c1, c2, c3 = st.columns([2, 2, 2])
        pmap = {p["id"]: p for p in plist}
        active = profiles.active_profile()
        prof_id = c1.selectbox("使用的模型配置", list(pmap.keys()),
                               index=list(pmap.keys()).index(active["id"]) if active else 0,
                               format_func=lambda i: f"{pmap[i]['profile_name']} · {pmap[i]['model']}", key="ai_prof")
        prof = pmap[prof_id]
        ok_key, key_msg = profiles.key_status(prof)
        with c2:
            pid = project_selector("项目", key="ai_proj", include_none=False)
        rtype = c3.selectbox("请求类型", list(REQUEST_TYPES.keys()), format_func=lambda k: REQUEST_TYPES[k][0], key="ai_rt")
        if not ok_key:
            st.warning(f"密钥不可用：{key_msg}", icon="🔑")
        st.markdown("**授权 AI 读取的数据**（默认不勾选；只发送数据库中的结构化记录与您写的笔记/摘要，不发送任何原始文件）")
        sc = st.columns(len(SCOPES))
        scopes = [k for i, (k, lbl) in enumerate(SCOPES.items()) if sc[i].checkbox(lbl, key=f"ai_scope_{k}")]
        question = st.text_area("补充说明或问题" + ("（必填）" if rtype == "free" else "（可选）"), height=80, key="ai_q")
        if pid and scopes:
            ctx = build_context(pid, scopes)
            with st.expander(f"预览将要发送的内容（约 {len(ctx)} 字符）", expanded=False):
                st.markdown("系统提示词：")
                st.code(SYSTEM_PROMPT, language=None)
                st.markdown("系统记录：")
                st.code(ctx, language="markdown")
            dest = prof.get("base_url") or ("Anthropic API（api.anthropic.com）" if prof["provider_type"] == "anthropic" else "")
            agree = st.checkbox(f"我授权将上述记录发送至 {dest}（模型 {prof['model']}）。调用可能产生费用。", key="ai_agree")
            if st.button("发送", type="primary", disabled=not (agree and ok_key), key="ai_send"):
                with st.spinner("模型思考中…"):
                    try:
                        res = assistant.ask(prof, pid, scopes, rtype, question, agree)
                        st.session_state["ai_last"] = {"text": res.text, "model": res.model, "notice": res.notice,
                                                       "usage": res.usage}
                    except (ValidationError,) as e:
                        show_errors(e)
                    except AIProviderError as e:
                        st.error(f"调用失败：{e}")
        elif pid:
            st.caption("请至少勾选一类授权数据。")
        last = st.session_state.get("ai_last")
        if last:
            with st.container(border=True):
                st.caption(f"模型：{last['model']}" + (f" · tokens：{last['usage']}" if last.get("usage") else ""))
                if last.get("notice"):
                    st.warning(last["notice"])
                st.markdown(last["text"] or "（空回答）")
                st.caption("AI 回答仅供参考。涉及删除/覆盖文件、执行代码、修改实验数据的任何建议，都需要您本人确认后再操作；本系统不会自动执行。")

# ----------------------------------------------------------------- checks
with t_check:
    st.caption("不调用任何模型，仅根据本地数据库中的事实检查：逾期任务、待填写的关键信息、缺失的失败原因与结果摘要、"
               "待确认的投稿状态、未核实的文献、不存在的文件等。")
    with st.columns([2, 4])[0]:
        cp = project_selector("范围", key="chk_proj", none_label="全部项目")
    findings = offline_checks.run_checks(cp)
    if not findings:
        st.success("没有发现需要处理的问题。")
    else:
        lvl_kind = {"高": "danger", "中": "warn", "低": ""}
        st.caption(f"共 {len(findings)} 条：高 {sum(f.level == '高' for f in findings)} · 中 {sum(f.level == '中' for f in findings)}"
                   f" · 低 {sum(f.level == '低' for f in findings)}")
        html_block("".join(
            f'<div class="rcc-item"><div class="t">{tag(f.level, lvl_kind.get(f.level, ""))}{tag(f.category)} {esc(f.message)}</div>'
            f'<div class="m">{esc(f.ref)}</div></div>' for f in findings))

# ----------------------------------------------------------------- config
with t_cfg:
    st.caption("API Key 不会保存在代码或数据库中：可存放在本机环境变量（数据库只记录变量名），或系统凭据管理器（keyring）。")
    plist = profiles.list_profiles()
    for p in plist:
        ok_key, msg = profiles.key_status(p)
        with st.container(border=True):
            a, b = st.columns([4, 2])
            a.html(f'<div class="t" style="font-weight:600">{esc(p["profile_name"])}{tag("当前使用", "accent") if p["is_active"] else ""}</div>'
                   f'<div class="rcc-small">{esc(profiles.PROVIDER_TYPES[p["provider_type"]])} · 模型 {esc(p["model"])}'
                   f' · {esc(p["base_url"] or "默认端点")}</div>'
                   f'<div class="rcc-small">密钥：{esc(profiles.KEY_STORAGES[p["key_storage"]])} — '
                   f'{tag(msg, "accent" if ok_key else "warn")}</div>')
            with b:
                if not p["is_active"] and st.button("设为当前", key=f"act_{p['id']}", width="stretch"):
                    run_action(profiles.set_active, p["id"], success="已切换")
                if st.button("编辑", key=f"ped_{p['id']}", width="stretch"):
                    st.session_state["ai_edit"] = p["id"]
                with st.popover("删除", width="stretch"):
                    if confirm_button("删除配置", key=f"pdl_{p['id']}", confirm_text="确认删除"):
                        run_action(profiles.delete_profile, p["id"], success="已删除")
            if p["key_storage"] == "keyring":
                with st.expander("在系统凭据管理器中保存 / 更新密钥"):
                    with st.form(f"kr_{p['id']}", clear_on_submit=True, border=False):
                        k_ = st.text_input("API Key", type="password", key=f"krk_{p['id']}")
                        if st.form_submit_button("保存到凭据管理器"):
                            run_action(profiles.store_key_in_keyring, p["profile_name"], k_, success="密钥已保存到系统凭据管理器")
            if st.button("测试连接（发送一条极短消息，可能产生少量费用）", key=f"test_{p['id']}", disabled=not ok_key):
                from rcc.services.ai.providers import chat

                try:
                    r = chat({**p, "max_tokens": 64}, "You are a connectivity check.", "Reply with the single word: OK")
                    st.success(f"连接成功：{r.model} 回复「{(r.text or '').strip()[:40]}」")
                except AIProviderError as e:
                    st.error(f"连接失败：{e}")

    edit_id: Optional[int] = st.session_state.get("ai_edit")
    cur = profiles.get_profile(edit_id) if edit_id else None
    st.markdown("**编辑配置**" if cur else "**新增模型配置**")
    preset_name = None
    if not cur:
        preset_name = st.selectbox("预设", list(profiles.PRESETS.keys()), key="ai_preset")
    base = cur or {**profiles.PRESETS[preset_name], "profile_name": preset_name if preset_name != "自定义" else ""}
    k = f"pf_{cur['id'] if cur else preset_name}_"
    with st.form(k + "form", border=False):
        c1, c2 = st.columns(2)
        name = c1.text_input("配置名称 *", base.get("profile_name") or "", key=k + "name")
        ptype = c2.selectbox("接口类型", list(profiles.PROVIDER_TYPES.keys()), format_func=lambda x: profiles.PROVIDER_TYPES[x],
                             index=list(profiles.PROVIDER_TYPES.keys()).index(base.get("provider_type", "openai_compatible")),
                             key=k + "type")
        c3, c4 = st.columns(2)
        url = c3.text_input("API Base URL", base.get("base_url") or "", key=k + "url",
                            help="Anthropic 可留空（使用官方端点）；OpenAI 兼容接口必填")
        model = c4.text_input("模型名称 *", base.get("model") or "", key=k + "model",
                              help="例如 claude-opus-5-5；其他厂商请填写其官方模型名")
        c5, c6 = st.columns(2)
        storage = c5.selectbox("API Key 存放方式", list(profiles.KEY_STORAGES.keys()), format_func=lambda x: profiles.KEY_STORAGES[x],
                               index=list(profiles.KEY_STORAGES.keys()).index(base.get("key_storage", "env")), key=k + "storage",
                               help=None if profiles.keyring_available() else "当前系统未检测到可用的 keyring 后端")
        env_var = c6.text_input("环境变量名（存放方式为“环境变量”时）", base.get("api_key_env_var") or "", key=k + "env",
                                placeholder="RCC_ANTHROPIC_API_KEY")
        c7, c8, c9 = st.columns(3)
        max_tokens = c7.number_input("最大输出 tokens", 256, 128000, int(base.get("max_tokens") or 8000), step=256, key=k + "mt")
        temp = c8.number_input("temperature（仅 OpenAI 兼容）", 0.0, 2.0, value=base.get("temperature"), step=0.1,
                               placeholder="默认", key=k + "temp")
        effort = c9.selectbox("effort（仅 Anthropic，可空）", profiles.EFFORT_LEVELS,
                              index=profiles.EFFORT_LEVELS.index(base.get("effort") or ""),
                              format_func=lambda x: x or "默认", key=k + "effort")
        fb = st.checkbox("Anthropic：模型拒答时启用服务端自动回退（fallbacks）", value=bool(base.get("use_fallbacks", True)),
                         key=k + "fb")
        make_active = st.checkbox("保存后设为当前使用的配置", value=not plist, key=k + "active")
        if st.form_submit_button("保存配置", type="primary"):
            try:
                profiles.save_profile({"profile_name": name, "provider_type": ptype, "base_url": url, "model": model,
                                       "key_storage": storage, "api_key_env_var": env_var, "max_tokens": max_tokens,
                                       "temperature": temp, "effort": effort, "use_fallbacks": fb},
                                      profile_id=cur["id"] if cur else None, make_active=make_active)
                st.session_state.pop("ai_edit", None)
                st.session_state.setdefault("_rcc_flash", []).append(("模型配置已保存", "✅"))
                st.rerun()
            except ValidationError as e:
                show_errors(e)
    if cur and st.button("取消编辑"):
        st.session_state.pop("ai_edit", None)
        st.rerun()
    with st.expander("如何设置环境变量"):
        st.markdown(
            "**Windows**（在“命令提示符”中执行，然后关闭并重新启动本应用）：\n"
            "```bat\nsetx RCC_ANTHROPIC_API_KEY \"你的密钥\"\n```\n"
            "**macOS / Linux**（写入 `~/.zshrc` 或 `~/.bashrc` 后重新打开终端）：\n"
            "```bash\nexport RCC_ANTHROPIC_API_KEY=\"你的密钥\"\n```\n"
            "密钥只在发送请求时从环境变量读取，不会写入数据库、日志或备份。")

# ----------------------------------------------------------------- history
with t_hist:
    hist = assistant.history(100)
    if not hist:
        empty_state("暂无调用记录。")
    for h in hist:
        with st.expander(f"{fmt_dt(h['created_at'])} · {REQUEST_TYPES.get(h['request_type'], ('?',))[0]} · "
                         f"{names.get(h['project_id'], '—') if h['project_id'] else '—'} · {h['status']}"):
            st.caption(f"配置：{h['profile_name']} · 模型：{h['model']} · 授权范围："
                       f"{'、'.join(SCOPES.get(s, s) for s in (loads(h['context_scopes'], []) or []))} · 发送约 {h['context_chars']} 字符")
            if h.get("question"):
                st.markdown(f"**问题**：{h['question']}")
            if h.get("error"):
                st.error(h["error"])
            if h.get("response"):
                st.markdown(h["response"])
