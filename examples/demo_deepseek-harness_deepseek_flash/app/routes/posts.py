"""Author routes: create, edit, submit and delete posts."""

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse, Response

from app import repositories as repo
from app.db import get_db
from app.dependencies import flash, require_login
from app.models import Post, User
from app.services import post as post_service
from app.templating import is_htmx, render

router = APIRouter()

VALID_ACTIONS = ("save", "submit", "publish", "unpublish")


def _get_managed_post(db: Session, post_id: int, user: User) -> Post:
    """Fetch a post the user is allowed to manage (author or admin)."""
    post = repo.post.get_by_id(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    if not post_service.can_manage(user, post):
        raise HTTPException(status_code=403, detail="not allowed to manage this post")
    return post


def _apply_action(db: Session, post: Post, user: User, action: str) -> None:
    """Apply the editor action (submit / publish / unpublish) to a post."""
    if action == "submit":
        post_service.submit_post(db, post=post)
    elif action == "publish":
        if not post_service.can_publish(user, post):
            raise post_service.PermissionDeniedError("当前配置不允许作者直接发布，请提交审核")
        post_service.publish_post(db, post=post)
    elif action == "unpublish":
        post_service.unpublish_post(db, post=post)


@router.get("/posts/mine")
def my_posts(request: Request, user: User = Depends(require_login), db: Session = Depends(get_db)):
    """List the signed-in user's own posts (all statuses)."""
    posts = repo.post.list_by_author(db, user.id)
    return render(request, "posts/mine.html", {"posts": posts})


@router.get("/posts/new")
def new_post_page(request: Request, user: User = Depends(require_login)):
    return render(request, "posts/editor.html", {"post": None, "title": "", "content": ""})


@router.post("/posts")
def create_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(""),
    action: str = Form("save"),
    user: User = Depends(require_login),
    db: Session = Depends(get_db),
):
    if not title.strip():
        flash(request, "标题不能为空", "error")
        return render(
            request, "posts/editor.html",
            {"post": None, "title": title, "content": content},
            status_code=400,
        )
    post = post_service.create_post(db, author=user, title=title, content=content)
    db.commit()
    if action in VALID_ACTIONS and action != "save":
        try:
            _apply_action(db, post, user, action)
            db.commit()
        except (post_service.PermissionDeniedError, post_service.InvalidTransitionError) as exc:
            db.rollback()
            flash(request, str(exc), "error")
    return RedirectResponse(f"/posts/{post.id}/edit", status_code=303)


@router.get("/posts/{post_id}/edit")
def edit_post_page(
    request: Request,
    post_id: int,
    user: User = Depends(require_login),
    db: Session = Depends(get_db),
):
    post = _get_managed_post(db, post_id, user)
    return render(
        request, "posts/editor.html",
        {"post": post, "title": post.title, "content": post.content},
    )


@router.post("/posts/{post_id}")
def update_post(
    request: Request,
    post_id: int,
    title: str = Form(...),
    content: str = Form(""),
    action: str = Form("save"),
    user: User = Depends(require_login),
    db: Session = Depends(get_db),
):
    post = _get_managed_post(db, post_id, user)
    if not title.strip():
        flash(request, "标题不能为空", "error")
        return render(
            request, "posts/editor.html",
            {"post": post, "title": title, "content": content},
            status_code=400,
        )
    post_service.update_post(db, post=post, title=title, content=content)
    if action in VALID_ACTIONS and action != "save":
        try:
            _apply_action(db, post, user, action)
            db.commit()
        except (post_service.PermissionDeniedError, post_service.InvalidTransitionError) as exc:
            db.rollback()
            flash(request, str(exc), "error")
            return render(
                request, "posts/editor.html",
                {"post": post, "title": title, "content": content},
                status_code=400,
            )
    else:
        db.commit()
    flash(request, "已保存", "success")
    return RedirectResponse(f"/posts/{post_id}/edit", status_code=303)


@router.post("/posts/{post_id}/submit")
def submit_post(
    request: Request,
    post_id: int,
    user: User = Depends(require_login),
    db: Session = Depends(get_db),
):
    post = _get_managed_post(db, post_id, user)
    try:
        post_service.submit_post(db, post=post)
        db.commit()
        flash(request, "已提交审核", "success")
    except post_service.InvalidTransitionError as exc:
        db.rollback()
        flash(request, str(exc), "error")
    return RedirectResponse(f"/posts/{post_id}/edit", status_code=303)


@router.post("/posts/{post_id}/delete")
def delete_post(
    request: Request,
    post_id: int,
    user: User = Depends(require_login),
    db: Session = Depends(get_db),
):
    post = _get_managed_post(db, post_id, user)
    post_service.delete_post(db, post=post)
    db.commit()
    if is_htmx(request):
        # Replace the row with nothing so HTMX removes it from the list.
        return Response(content="", status_code=200)
    flash(request, "文章已删除", "success")
    return RedirectResponse("/posts/mine", status_code=303)
