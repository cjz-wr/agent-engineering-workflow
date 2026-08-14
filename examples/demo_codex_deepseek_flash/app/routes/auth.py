"""Authentication routes: register / login / logout."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..db import get_db
from ..repositories import user as user_repo
from ..services import auth as auth_service
from ..services.session import SessionBox, get_session
from ..templating import render_page

router = APIRouter()


def _next_url(request: Request) -> str:
    target = request.query_params.get("next", "/")
    return target if target.startswith("/") and not target.startswith("//") else "/"


def _redirect_with_session(session: SessionBox, target: str) -> RedirectResponse:
    response = RedirectResponse(target, status_code=303)
    session.apply_to(response)
    return response


@router.get("/register")
def register_page(request: Request, session: SessionBox = Depends(get_session)):
    if session.uid is not None:
        return RedirectResponse("/", status_code=303)
    response = render_page(request, "auth/register.html", flashes=session.pop_flashes())
    session.apply_to(response)
    return response


@router.post("/register")
def register(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
    display_name: str = Form(""),
    session: SessionBox = Depends(get_session),
    db: Session = Depends(get_db),
):
    error = None
    if not username.strip():
        error = "用户名不能为空。"
    elif not password:
        error = "密码不能为空。"
    elif user_repo.get_by_username(db, username.strip()):
        error = "该用户名已被注册。"
    else:
        user = auth_service.register_user(db, username=username, password=password, display_name=display_name)
        db.commit()
        session.login(user.id)
        session.add_flash("注册成功，欢迎加入！")
        return _redirect_with_session(session, _next_url(request))

    response = render_page(
        request,
        "auth/register.html",
        flashes=session.pop_flashes(),
        error=error,
        username=username,
        display_name=display_name,
    )
    session.apply_to(response)
    return response


@router.get("/login")
def login_page(request: Request, session: SessionBox = Depends(get_session)):
    if session.uid is not None:
        return RedirectResponse("/", status_code=303)
    response = render_page(request, "auth/login.html", flashes=session.pop_flashes())
    session.apply_to(response)
    return response


@router.post("/login")
def login(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
    session: SessionBox = Depends(get_session),
    db: Session = Depends(get_db),
):
    user = auth_service.authenticate(db, username=username, password=password)
    if user is None:
        response = render_page(
            request,
            "auth/login.html",
            flashes=session.pop_flashes(),
            error="用户名或密码错误。",
            username=username,
        )
        session.apply_to(response)
        return response
    session.login(user.id)
    session.add_flash(f"欢迎回来，{user.display_name or user.username}！")
    return _redirect_with_session(session, _next_url(request))


@router.post("/logout")
def logout(session: SessionBox = Depends(get_session)):
    session.logout()
    return _redirect_with_session(session, "/")
