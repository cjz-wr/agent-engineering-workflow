"""Shared Jinja2 templates instance and render helper."""

from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.dependencies import get_flashed_messages

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def is_htmx(request: Request) -> bool:
    """True when the request was issued by HTMX."""
    return request.headers.get("hx-request") == "true"


templates.env.globals["settings"] = get_settings()
templates.env.globals["is_htmx"] = is_htmx


def render(
    request: Request,
    template_name: str,
    context: dict | None = None,
    *,
    status_code: int = 200,
):
    """Render a template with the standard page context injected."""
    ctx: dict = {"request": request}
    if context:
        ctx.update(context)
    ctx.setdefault("current_user", getattr(request.state, "current_user", None))
    ctx.setdefault("flashed_messages", get_flashed_messages(request))
    return templates.TemplateResponse(request, template_name, ctx, status_code=status_code)
