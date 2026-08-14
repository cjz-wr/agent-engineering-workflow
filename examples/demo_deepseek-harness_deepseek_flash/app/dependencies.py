"""Shared FastAPI dependencies: current user, login/admin guards, flash messages."""

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app import repositories as repo
from app.db import get_db
from app.models import User

LOGIN_URL = "/login"
FLASH_SESSION_KEY = "_flash"


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    """Resolve the signed-in user from the session, or None."""
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    user = repo.user.get_by_id(db, user_id)
    if user is None or not user.is_active:
        return None
    request.state.current_user = user
    return user


def require_login(request: Request, user: User | None = Depends(get_current_user)) -> User:
    """Redirect to the login page when no user is signed in.

    Note: this FastAPI version does not short-circuit on dependency-returned
    Response objects, so the redirect is expressed as a 303 HTTPException with
    a Location header (browsers and HTMX follow it normally).
    """
    if user is None:
        raise HTTPException(
            status_code=303,
            headers={"Location": f"{LOGIN_URL}?next={request.url.path}"},
            detail="login required",
        )
    return user


def require_admin(user: User = Depends(require_login)) -> User:
    """Forbid access unless the signed-in user is an admin."""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="admin privileges required")
    return user


def flash(request: Request, message: str, category: str = "info") -> None:
    """Queue a one-shot flash message for the next rendered page."""
    messages = request.session.setdefault(FLASH_SESSION_KEY, [])
    messages.append({"message": message, "category": category})


def get_flashed_messages(request: Request) -> list[dict]:
    """Pop and return queued flash messages."""
    return request.session.pop(FLASH_SESSION_KEY, [])
