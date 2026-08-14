"""Authentication routes: register, login, logout."""

from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.db import get_db
from app.dependencies import flash, get_current_user, require_login
from app.models import User
from app.services import auth as auth_service
from app.templating import render

router = APIRouter()


def _safe_next(next_url: str) -> str:
    """Only allow local paths as post-login redirect targets."""
    if next_url.startswith("/") and not next_url.startswith("//"):
        return next_url
    return "/"


@router.get("/register")
def register_page(request: Request, user: User | None = Depends(get_current_user)):
    if user is not None:
        return RedirectResponse("/", status_code=303)
    return render(request, "auth/register.html")


@router.post("/register")
def register_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    display_name: str = Form(""),
    db: Session = Depends(get_db),
):
    try:
        user = auth_service.register(
            db, username=username, password=password, display_name=display_name
        )
    except auth_service.DuplicateUsernameError:
        flash(request, "用户名已被占用", "error")
        return render(
            request, "auth/register.html",
            {"username": username, "display_name": display_name},
            status_code=400,
        )
    except ValueError as exc:
        flash(request, str(exc), "error")
        return render(
            request, "auth/register.html",
            {"username": username, "display_name": display_name},
            status_code=400,
        )
    db.commit()
    auth_service.login_user(request, user)
    flash(request, "注册成功，欢迎！", "success")
    return RedirectResponse("/", status_code=303)


@router.get("/login")
def login_page(request: Request, user: User | None = Depends(get_current_user)):
    if user is not None:
        return RedirectResponse("/", status_code=303)
    return render(request, "auth/login.html", {"next": request.query_params.get("next", "/")})


@router.post("/login")
def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    next: str = Form("/"),
    db: Session = Depends(get_db),
):
    user = auth_service.authenticate(db, username=username, password=password)
    if user is None:
        flash(request, "用户名或密码错误", "error")
        return render(request, "auth/login.html", {"username": username, "next": next}, status_code=400)
    auth_service.login_user(request, user)
    flash(request, "登录成功", "success")
    return RedirectResponse(_safe_next(next), status_code=303)


@router.post("/logout")
def logout(request: Request, _user: User = Depends(require_login)):
    auth_service.logout_user(request)
    flash(request, "已注销", "info")
    return RedirectResponse("/", status_code=303)
