"""Article management routes (create / edit / submit / delete)."""

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session

from ..db import get_db
from ..dependencies import require_user
from ..models.post import Post
from ..models.user import User
from ..repositories import post as post_repo
from ..services import post as post_service
from ..services.session import SessionBox, get_session
from ..templating import render_page

router = APIRouter()


def _get_own_post_or_404(db: Session, user: User, post_id: int) -> Post:
    post = post_repo.get_by_id(db, post_id)
    if post is None or not post_service.can_modify(user, post):
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def _editor_response(
    request: Request,
    *,
    post: Post | None,
    error: str | None = None,
    title: str = "",
    content: str = "",
    **extra,
):
    return render_page(
        request,
        "posts/editor.html",
        post=post,
        error=error,
        title=title,
        content=content,
        **extra,
    )


@router.get("/posts/new")
def new_post_page(request: Request, current_user: User = Depends(require_user)):
    return _editor_response(request, post=None)


@router.post("/posts")
def create_post(
    request: Request,
    title: str = Form(""),
    content: str = Form(""),
    action: str = Form("save"),
    current_user: User = Depends(require_user),
    session: SessionBox = Depends(get_session),
    db: Session = Depends(get_db),
):
    if not title.strip():
        response = _editor_response(request, post=None, error="标题不能为空。", title=title, content=content)
        session.apply_to(response)
        return response

    post = post_service.create_draft(db, author_id=current_user.id, title=title, content=content)
    if action == "submit":
        post_service.submit_post(db, post)
    db.commit()

    session.add_flash("文章已创建。")
    response = RedirectResponse(f"/posts/{post.id}/edit", status_code=303)
    session.apply_to(response)
    return response


@router.get("/posts/{post_id}/edit")
def edit_post_page(
    request: Request,
    post_id: int,
    current_user: User = Depends(require_user),
    session: SessionBox = Depends(get_session),
    db: Session = Depends(get_db),
):
    post = _get_own_post_or_404(db, current_user, post_id)
    response = _editor_response(request, post=post, flashes=session.pop_flashes())
    session.apply_to(response)
    return response


@router.post("/posts/{post_id}")
def update_post(
    request: Request,
    post_id: int,
    title: str = Form(""),
    content: str = Form(""),
    action: str = Form("save"),
    current_user: User = Depends(require_user),
    session: SessionBox = Depends(get_session),
    db: Session = Depends(get_db),
):
    post = _get_own_post_or_404(db, current_user, post_id)
    if not title.strip():
        response = _editor_response(request, post=post, error="标题不能为空。")
        session.apply_to(response)
        return response

    post_service.update_post(db, post, title=title, content=content, action=action)
    db.commit()

    session.add_flash("文章已保存。")
    response = RedirectResponse(f"/posts/{post.id}/edit", status_code=303)
    session.apply_to(response)
    return response


@router.post("/posts/{post_id}/submit")
def submit_post(
    request: Request,
    post_id: int,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    post = _get_own_post_or_404(db, current_user, post_id)
    post_service.submit_post(db, post)
    db.commit()
    if request.headers.get("hx-request") == "true":
        return render_page(request, "components/post_actions.html", current_user=current_user, post=post)
    return RedirectResponse(f"/posts/{post.id}/edit", status_code=303)


@router.post("/posts/{post_id}/delete")
def delete_post(
    request: Request,
    post_id: int,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    post = _get_own_post_or_404(db, current_user, post_id)
    post_service.delete_post(db, post)
    db.commit()
    if request.headers.get("hx-request") == "true":
        return Response("", media_type="text/html")
    return RedirectResponse("/", status_code=303)
