"""Plotly 图表（统一风格）：细线条、浅网格、单系列单色、悬停提示。"""
from __future__ import annotations

from typing import Optional

import plotly.graph_objects as go

from ..constants import PUB_STATUS_LABELS, TASK_PRIORITIES
from .theme import neutral_color, ordinal_colors, series_color

FONT = "system-ui, -apple-system, 'Segoe UI', 'Microsoft YaHei', 'PingFang SC', sans-serif"


def _style(fig: go.Figure, height: int = 300, legend: bool = False) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=16, t=12, b=8),
        font=dict(family=FONT, size=12),
        showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=None),
        hoverlabel=dict(font=dict(family=FONT, size=12)),
        bargap=0.35,
    )
    fig.update_xaxes(showline=False, zeroline=False, ticks="", title=None)
    fig.update_yaxes(showline=False, zeroline=False, ticks="", title=None)
    return fig


def project_progress(rows: list[dict]) -> go.Figure:
    """横向进度条：灰色轨道 + 蓝色进度；进度未填写的项目显示“待填写”。"""
    names = [r["name"] if len(r["name"]) <= 22 else r["name"][:21] + "…" for r in rows][::-1]
    vals = [r["progress"] for r in rows][::-1]
    fig = go.Figure()
    fig.add_bar(y=names, x=[100] * len(rows), orientation="h", marker=dict(color=neutral_color(), opacity=0.35),
                hoverinfo="skip", showlegend=False)
    fig.add_bar(y=names, x=[v or 0 for v in vals], orientation="h", marker=dict(color=series_color(0)),
                text=[f"{v}%" if v is not None else "进度待填写" for v in vals], textposition="outside",
                cliponaxis=False, hovertemplate="%{y}<br>完成进度 %{x}%<extra></extra>", showlegend=False)
    fig.update_layout(barmode="overlay")
    fig.update_xaxes(range=[0, 118], showgrid=False, showticklabels=False)
    fig.update_yaxes(showgrid=False)
    return _style(fig, height=max(140, 52 * len(rows) + 30))


def weekly_tasks(rows: list[dict]) -> go.Figure:
    labels = [r["week"].strftime("%m-%d") for r in rows]
    fig = go.Figure()
    fig.add_bar(x=labels, y=[r["created"] for r in rows], name="新建", marker=dict(color=neutral_color()),
                hovertemplate="%{x} 当周<br>新建 %{y} 项<extra></extra>")
    fig.add_bar(x=labels, y=[r["completed"] for r in rows], name="完成", marker=dict(color=series_color(0)),
                hovertemplate="%{x} 当周<br>完成 %{y} 项<extra></extra>")
    fig.update_layout(barmode="group", bargroupgap=0.08)
    fig.update_yaxes(rangemode="tozero", dtick=1 if max([r["created"] for r in rows] + [r["completed"] for r in rows] + [0]) < 8 else None)
    fig.update_xaxes(showgrid=False, title=None)
    return _style(fig, height=280, legend=True)


def publication_status(counts: dict[str, int], order: list[str]) -> go.Figure:
    items = [(s, counts.get(s, 0)) for s in order if counts.get(s, 0) > 0]
    labels = [PUB_STATUS_LABELS.get(s, s) for s, _ in items][::-1]
    vals = [n for _, n in items][::-1]
    fig = go.Figure(go.Bar(y=labels, x=vals, orientation="h", marker=dict(color=series_color(0)),
                           text=vals, textposition="outside", cliponaxis=False,
                           hovertemplate="%{y}：%{x} 篇<extra></extra>"))
    fig.update_xaxes(showticklabels=False, showgrid=False, range=[0, max(vals + [1]) * 1.25])
    fig.update_yaxes(showgrid=False)
    return _style(fig, height=max(140, 40 * len(items) + 40))


def priority_distribution(dist: dict[str, int]) -> go.Figure:
    labels = TASK_PRIORITIES
    vals = [dist.get(p, 0) for p in labels]
    fig = go.Figure(go.Bar(x=labels, y=vals, marker=dict(color=ordinal_colors()), text=vals,
                           textposition="outside", cliponaxis=False,
                           hovertemplate="%{x}：%{y} 项未完成任务<extra></extra>"))
    fig.update_yaxes(showgrid=True, rangemode="tozero", range=[0, max(vals + [1]) * 1.25],
                     dtick=1 if max(vals + [0]) < 8 else None)
    fig.update_xaxes(showgrid=False)
    return _style(fig, height=260)


def gantt(rows: list[dict], height: Optional[int] = None) -> go.Figure:
    """项目起止时间线（仅有开始与预计完成日期的项目）。"""
    import plotly.express as px
    import pandas as pd

    df = pd.DataFrame(rows)
    fig = px.timeline(df, x_start="start", x_end="end", y="name", hover_data={"start": True, "end": True, "name": False})
    fig.update_traces(marker=dict(color=series_color(0)))
    fig.update_yaxes(autorange="reversed")
    return _style(fig, height=height or max(160, 46 * len(rows) + 40))
