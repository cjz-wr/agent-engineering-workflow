"""Jinja2 templates plus template helpers and filters."""

import math
import re
from pathlib import Path

import markdown as md
from fastapi import Request
from fastapi.templating import Jinja2Templates

from .config import settings

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

STATUS_LABELS = {
    "draft": "草稿",
    "submitted": "待审核",
    "published": "已发布",
    "rejected": "已驳回",
}

STATUS_COLORS = {
    "draft": "bg-slate-200 text-slate-700",
    "submitted": "bg-amber-100 text-amber-700",
    "published": "bg-emerald-100 text-emerald-700",
    "rejected": "bg-rose-100 text-rose-700",
}


def render_markdown(text: str | None) -> str:
    return md.markdown(text or "", extensions=["fenced_code", "tables", "sane_lists"])


def format_dt(value) -> str:
    return value.strftime("%Y-%m-%d %H:%M") if value else ""


def plain_text(text: str | None) -> str:
    """Approximately strip Markdown syntax for excerpts and reading time."""
    if not text:
        return ""
    value = text
    value = re.sub(r"```.*?```", " ", value, flags=re.DOTALL)
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"^\s*#{1,6}\s*", "", value, flags=re.MULTILINE)
    value = re.sub(r"^\s*([-*+]|\d+\.)\s+", "", value, flags=re.MULTILINE)
    value = re.sub(r"^\s*>\s?", "", value, flags=re.MULTILINE)
    value = re.sub(r"[*_~|]", "", value)
    return re.sub(r"\s+", " ", value).strip()


def excerpt(text: str | None, length: int = 120) -> str:
    """Return a truncated plain-text excerpt ending with an ellipsis."""
    value = plain_text(text)
    if len(value) <= length:
        return value
    return value[:length].rstrip() + "…"


def reading_time(text: str | None) -> str:
    """Estimate reading time (minutes) from plain-text length."""
    minutes = max(1, math.ceil(len(plain_text(text)) / 300))
    return f"约 {minutes} 分钟"


templates.env.filters["markdown"] = render_markdown
templates.env.filters["format_dt"] = format_dt
templates.env.filters["plain_text"] = plain_text
templates.env.filters["excerpt"] = excerpt
templates.env.filters["reading_time"] = reading_time
templates.env.globals["app_name"] = settings.app_name
templates.env.globals["allow_user_publish"] = settings.allow_user_publish
templates.env.globals["status_label"] = lambda s: STATUS_LABELS.get(s, s)
templates.env.globals["status_color"] = lambda s: STATUS_COLORS.get(s, "bg-slate-200 text-slate-700")


def render_page(request: Request, template_name: str, status_code: int = 200, **context):
    """Render a page template with a normalized context."""
    context.setdefault("current_user", None)
    context.setdefault("flashes", [])
    return templates.TemplateResponse(
        template_name, {"request": request, **context}, status_code=status_code
    )
