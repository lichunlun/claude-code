"""全局样式与图表配色。

颜色基调：灰白背景 + 深蓝强调色（见 .streamlit/config.toml）。
自定义 HTML 使用 CSS light-dark() 跟随 Streamlit 的浅色/深色主题；不支持时退回中性半透明色。
图表配色来自经过色盲安全校验的分类色板（第 1 色为蓝），单系列图表只用一种颜色。
"""
from __future__ import annotations

import streamlit as st

# 分类色板（顺序固定，不循环）：浅色 / 深色
CATEGORICAL_LIGHT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
CATEGORICAL_DARK = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767"]
# 有序（ordinal）蓝色阶：Critical → Low
ORDINAL_LIGHT = ["#184f95", "#256abf", "#3987e5", "#86b6ef"]
ORDINAL_DARK = ["#9ec5f4", "#6da7ec", "#3987e5", "#1c5cab"]
NEUTRAL_LIGHT = "#c3c8d1"
NEUTRAL_DARK = "#4a5468"

CSS = """
<style>
:root {
  --rcc-card: light-dark(#ffffff, #151c2a);
  --rcc-border: light-dark(#e3e7ee, #273145);
  --rcc-muted: light-dark(#5b6576, #9aa5b8);
  --rcc-soft: light-dark(#f2f4f8, #1b2333);
  --rcc-accent: light-dark(#1d4f91, #6ea8fe);
  --rcc-accent-soft: light-dark(rgba(29,79,145,.08), rgba(110,168,254,.12));
  --rcc-warn: light-dark(#a15c00, #f2b75b);
  --rcc-danger: light-dark(#b42318, #f28b82);
}
.block-container { padding-top: 3.6rem; padding-bottom: 3rem; max-width: 1320px; }
h1 { font-size: 1.55rem !important; font-weight: 650 !important; letter-spacing: -0.01em; }
h2 { font-size: 1.2rem !important; font-weight: 620 !important; }
h3 { font-size: 1.02rem !important; font-weight: 620 !important; }
[data-testid="stAppDeployButton"] { display: none; }
[data-testid="stMetricValue"] { font-size: 1.85rem; font-weight: 650; }
[data-testid="stMetricLabel"] p { font-size: .84rem; color: var(--rcc-muted); }
[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] { gap: .6rem; }
div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) { }
section[data-testid="stSidebar"] [data-testid="stSidebarNavSeparator"] { margin: .4rem 0; }
.rcc-sub { color: var(--rcc-muted); font-size: .9rem; margin: -.5rem 0 1.1rem 0; }
.rcc-muted { color: var(--rcc-muted); }
.rcc-pending { color: var(--rcc-muted); opacity: .8; }
.rcc-small { font-size: .82rem; color: var(--rcc-muted); }
.rcc-kv { display: grid; grid-template-columns: 8.5rem 1fr; gap: .45rem 1rem; font-size: .92rem; }
.rcc-kv .k { color: var(--rcc-muted); }
.rcc-kv .v { white-space: pre-wrap; word-break: break-word; }
.rcc-path { margin-bottom: .35rem; line-height: 1.35; }
.rcc-path .dir { font-size: .76rem; color: var(--rcc-muted); word-break: break-all; }
.rcc-item { padding: .55rem 0; border-bottom: 1px solid var(--rcc-border); }
.rcc-item:last-child { border-bottom: none; }
.rcc-item .t { font-weight: 560; }
.rcc-item .m { font-size: .8rem; color: var(--rcc-muted); margin-top: .1rem; }
.rcc-tag { display: inline-block; font-size: .72rem; padding: 0 .45rem; border-radius: 999px;
           border: 1px solid var(--rcc-border); color: var(--rcc-muted); margin-left: .35rem; line-height: 1.35rem; }
.rcc-tag.accent { color: var(--rcc-accent); border-color: var(--rcc-accent); }
.rcc-tag.warn { color: var(--rcc-warn); border-color: var(--rcc-warn); }
.rcc-tag.danger { color: var(--rcc-danger); border-color: var(--rcc-danger); }
.rcc-dot { display: inline-block; width: .5rem; height: .5rem; border-radius: 50%; margin-right: .4rem;
           background: var(--rcc-accent); vertical-align: middle; }
.rcc-dot.warn { background: var(--rcc-warn); } .rcc-dot.danger { background: var(--rcc-danger); }
.rcc-dot.muted { background: var(--rcc-muted); }
/* 日历 */
.rcc-cal { width: 100%; border-collapse: separate; border-spacing: 4px; table-layout: fixed; }
.rcc-cal th { font-size: .75rem; font-weight: 500; color: var(--rcc-muted); text-align: left; padding: 0 .3rem; }
.rcc-cal td { vertical-align: top; height: 5.4rem; padding: .3rem .35rem; border-radius: 6px;
              background: var(--rcc-card); border: 1px solid var(--rcc-border); overflow: hidden; }
.rcc-cal td.out { opacity: .45; }
.rcc-cal td.today { border-color: var(--rcc-accent); box-shadow: inset 0 0 0 1px var(--rcc-accent); }
.rcc-cal .d { font-size: .78rem; color: var(--rcc-muted); margin-bottom: .15rem; }
.rcc-cal td.today .d { color: var(--rcc-accent); font-weight: 650; }
.rcc-cal .e { font-size: .72rem; line-height: 1.15rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.rcc-cal .e.done { text-decoration: line-through; opacity: .55; }
.rcc-cal .more { font-size: .7rem; color: var(--rcc-muted); }
.rcc-cal.compact td { height: 3.1rem; }
.rcc-cal.compact .n { font-size: .95rem; font-weight: 620; color: var(--rcc-accent); }
.rcc-heat-0 { } .rcc-heat-1 { background: var(--rcc-accent-soft) !important; }
.rcc-heat-2 { background: light-dark(rgba(29,79,145,.16), rgba(110,168,254,.22)) !important; }
.rcc-heat-3 { background: light-dark(rgba(29,79,145,.26), rgba(110,168,254,.32)) !important; }
.rcc-week { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 6px; }
.rcc-week .col { border: 1px solid var(--rcc-border); border-radius: 6px; padding: .4rem .45rem; min-height: 9rem;
                 background: var(--rcc-card); }
.rcc-week .col.today { border-color: var(--rcc-accent); }
.rcc-week .h { font-size: .78rem; color: var(--rcc-muted); margin-bottom: .3rem; }
.rcc-week .e { font-size: .78rem; padding: .2rem 0; border-top: 1px solid var(--rcc-border); }
.rcc-week .e:first-of-type { border-top: none; }
.rcc-snip { font-size: .86rem; line-height: 1.45; padding: .35rem .6rem; border-left: 2px solid var(--rcc-accent);
            background: var(--rcc-soft); margin: .3rem 0; border-radius: 0 4px 4px 0; }
.rcc-timeline { border-left: 2px solid var(--rcc-border); margin-left: .4rem; padding-left: 1rem; }
.rcc-timeline .ti { position: relative; padding: .3rem 0 .6rem 0; }
.rcc-timeline .ti::before { content: ""; position: absolute; left: -1.38rem; top: .62rem; width: .6rem; height: .6rem;
                            border-radius: 50%; background: var(--rcc-card); border: 2px solid var(--rcc-accent); }
.rcc-timeline .ti.nodate::before { border-color: var(--rcc-muted); }
.rcc-timeline .dt { font-size: .78rem; color: var(--rcc-muted); }
@media (max-width: 700px) {
  .rcc-kv { grid-template-columns: 1fr; }
  .rcc-week { grid-template-columns: 1fr; }
  .rcc-cal td { height: 3.6rem; }
}
</style>
"""


def inject_css() -> None:
    st.html(CSS)


def is_dark() -> bool:
    try:
        return st.context.theme.type == "dark"
    except Exception:  # noqa: BLE001
        return False


def series_color(i: int = 0) -> str:
    pal = CATEGORICAL_DARK if is_dark() else CATEGORICAL_LIGHT
    return pal[i % len(pal)]


def ordinal_colors() -> list[str]:
    return ORDINAL_DARK if is_dark() else ORDINAL_LIGHT


def neutral_color() -> str:
    return NEUTRAL_DARK if is_dark() else NEUTRAL_LIGHT
