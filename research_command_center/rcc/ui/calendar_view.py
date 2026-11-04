"""日历渲染（纯 HTML，离线可用）。"""
from __future__ import annotations

import calendar as pycal
from collections import defaultdict
from datetime import date, timedelta
from typing import Iterable

import streamlit as st

from ..constants import CAL_SOURCE_LABELS
from ..utils import today
from .common import esc

WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
SOURCE_DOT = {"task": "", "publication": "warn", "event": "", "experiment": "", "project": "muted",
              "milestone": "", "bioinfo": "muted"}


OVERDUE_SOURCES = {"task", "publication", "milestone"}


def _mark_overdue(e: dict) -> dict:
    """截止类事项（任务、投稿/修改期限、里程碑）未完成且日期已过 → 标记为逾期（红点）。"""
    if not e.get("done") and e["source"] in OVERDUE_SOURCES and e["date"] < today():
        e = {**e, "overdue": True}
    return e


def _by_day(events: Iterable[dict]) -> dict[date, list[dict]]:
    out: dict[date, list[dict]] = defaultdict(list)
    for e in map(_mark_overdue, events):
        start = e["date"]
        end = e.get("end_date") or start
        d = start
        n = 0
        while d <= end and n < 62:
            out[d].append(e)
            d += timedelta(days=1)
            n += 1
    return out


def _title(e: dict) -> str:
    src = CAL_SOURCE_LABELS.get(e["source"], e["source"])
    proj = f" · {e['project']}" if e.get("project") else ""
    return f"[{src}] {e['title']}{proj}"


def month_view(year: int, month: int, events: list[dict], max_per_day: int = 3) -> None:
    days = _by_day(events)
    cal = pycal.Calendar(firstweekday=0)
    t = today()
    rows = ['<table class="rcc-cal"><thead><tr>' + "".join(f"<th>{w}</th>" for w in WEEKDAYS) + "</tr></thead><tbody>"]
    for week in cal.monthdatescalendar(year, month):
        rows.append("<tr>")
        for d in week:
            cls = []
            if d.month != month:
                cls.append("out")
            if d == t:
                cls.append("today")
            evs = days.get(d, [])
            items = []
            for e in evs[:max_per_day]:
                dot = SOURCE_DOT.get(e["source"], "")
                if e.get("overdue"):
                    dot = "danger"
                items.append(f'<div class="e{" done" if e.get("done") else ""}" title="{esc(_title(e))}">'
                             f'<span class="rcc-dot {dot}"></span>{esc(e["title"])}</div>')
            if len(evs) > max_per_day:
                more = "&#10;".join(esc(_title(e)) for e in evs[max_per_day:])
                items.append(f'<div class="more" title="{more}">另有 {len(evs) - max_per_day} 项</div>')
            rows.append(f'<td class="{" ".join(cls)}"><div class="d">{d.day}</div>{"".join(items)}</td>')
        rows.append("</tr>")
    rows.append("</tbody></table>")
    st.html("".join(rows))


def week_view(start: date, events: list[dict]) -> None:
    days = _by_day(events)
    t = today()
    cols = []
    for i in range(7):
        d = start + timedelta(days=i)
        evs = days.get(d, [])
        items = "".join(
            f'<div class="e" title="{esc(_title(e))}"><span class="rcc-dot {"danger" if e.get("overdue") else SOURCE_DOT.get(e["source"], "")}"></span>'
            f'{"<s>" if e.get("done") else ""}{esc(e["title"])}{"</s>" if e.get("done") else ""}'
            f'<div class="rcc-small">{esc(CAL_SOURCE_LABELS.get(e["source"], ""))}{(" · " + esc(e["project"])) if e.get("project") else ""}</div></div>'
            for e in evs) or '<div class="rcc-small">—</div>'
        cols.append(f'<div class="col{" today" if d == t else ""}"><div class="h">{WEEKDAYS[i]} · {d.month}/{d.day}</div>{items}</div>')
    st.html('<div class="rcc-week">' + "".join(cols) + "</div>")


def compact_window(start: date, days: int, events: list[dict]) -> None:
    """首页：未来 N 天的紧凑日历（每格显示当天事项数，颜色深浅表示数量）。"""
    by_day = _by_day(events)
    first = start - timedelta(days=start.weekday())
    end = start + timedelta(days=days - 1)
    last = end + timedelta(days=6 - end.weekday())
    rows = ['<table class="rcc-cal compact"><thead><tr>' + "".join(f"<th>{w}</th>" for w in WEEKDAYS) + "</tr></thead><tbody>"]
    d = first
    while d <= last:
        rows.append("<tr>")
        for _ in range(7):
            in_window = start <= d <= end
            evs = by_day.get(d, []) if in_window else []
            n = len(evs)
            heat = 0 if n == 0 else 1 if n == 1 else 2 if n <= 3 else 3
            cls = [f"rcc-heat-{heat}"]
            if not in_window:
                cls.append("out")
            if d == today():
                cls.append("today")
            tip = "&#10;".join(esc(_title(e)) for e in evs) or "无事项"
            label = f"{d.month}/{d.day}" if d.day == 1 or d == first else str(d.day)
            rows.append(f'<td class="{" ".join(cls)}" title="{tip}"><div class="d">{label}</div>'
                        + (f'<div class="n">{n}</div>' if n else "") + "</td>")
            d += timedelta(days=1)
        rows.append("</tr>")
    rows.append("</tbody></table>")
    st.html("".join(rows))
