"""Shared FastAPI dependencies: current user and authentication guards."""

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from .db import get_db
from .models.user import User
from .repositories import user as user_repo
from .services.session import SessionBox, get_session


def get_current_user(
    request: Request,
    session: SessionBox = Depends(get_session),
    db: Session = Depends(get_db),
) -> User | None:
    """Return the authenticated user or None."""
    if session.uid is None:
        return None
    user = user_repo.get_by_id(db, session.uid)
    if user is None or not user.is_active:
        return None
    return user


def _redirect_to_login(request: Request) -> None:
    if request.headers.get("hx-request") == "true":
        raise HTTPException(status_code=401, headers={"HX-Redirect": "/login"})
    raise HTTPException(status_code=303, headers={"Location": "/login"})


def require_user(
    request: Request, current_user: User | None = Depends(get_current_user)
) -> User:
    """Guard: require an authenticated user, otherwise redirect (or HX-Redirect) to /login."""
    if current_user is None:
        _redirect_to_login(request)
    return current_user


def require_admin(
    request: Request, current_user: User = Depends(require_user)
) -> User:
    """Guard: require an admin user."""
    if current_user.role != "admin":
        if request.headers.get("hx-request") == "true":
            raise HTTPException(status_code=403, headers={"HX-Redirect": "/"})
        raise HTTPException(status_code=303, headers={"Location": "/"})
    return current_user
