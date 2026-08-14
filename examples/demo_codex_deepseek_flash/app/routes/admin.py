"""Admin routes: dashboard, post management, comment moderation and user management."""

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session

from ..db import get_db
from ..dependencies import require_admin
from ..models.post import Post
from ..models.user import User
from ..repositories import comment as comment_repo
from ..repositories import post as post_repo
from ..repositories import user as user_repo
from ..services import post as post_service
from ..templating import render_page

router = APIRouter()


def _get_post_or_404(db: Session, post_id: int) -> Post:
    post = post_repo.get_by_id(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def _get_user_or_404(db: Session, user_id: int) -> User:
    user = user_repo.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def _post_row_or_redirect(request: Request, post: Post):
    if request.headers.get("hx-request") == "true":
        return render_page(request, "components/admin_post_row.html", post=post)
    return RedirectResponse("/admin/posts", status_code=303)


@router.get("/admin")
def dashboard(
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return render_page(
        request,
        "admin/dashboard.html",
        current_user=current_user,
        total_posts=post_repo.count(db),
        total_users=user_repo.count(db),
        total_comments=comment_repo.count(db),
        status_counts=post_repo.count_by_status(db),
        recent_comments=comment_repo.list_recent(db, 8),
    )


@router.get("/admin/posts")
def admin_posts(
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    posts = post_repo.list_all(db)
    return render_page(request, "admin/posts.html", current_user=current_user, posts=posts)


@router.post("/admin/posts/{post_id}/publish")
def publish_post(
    request: Request,
    post_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    post = _get_post_or_404(db, post_id)
    post_service.publish_post(db, post)
    db.commit()
    return _post_row_or_redirect(request, post)


@router.post("/admin/posts/{post_id}/reject")
def reject_post(
    request: Request,
    post_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    post = _get_post_or_404(db, post_id)
    post_service.reject_post(db, post)
    db.commit()
    return _post_row_or_redirect(request, post)


@router.post("/admin/posts/{post_id}/unpublish")
def unpublish_post(
    request: Request,
    post_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    post = _get_post_or_404(db, post_id)
    post_service.unpublish_post(db, post)
    db.commit()
    return _post_row_or_redirect(request, post)


@router.post("/admin/posts/{post_id}/delete")
def delete_post(
    request: Request,
    post_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    post = _get_post_or_404(db, post_id)
    post_service.delete_post(db, post)
    db.commit()
    if request.headers.get("hx-request") == "true":
        return Response("", media_type="text/html")
    return RedirectResponse("/admin/posts", status_code=303)


@router.get("/admin/comments")
def admin_comments(
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    comments = comment_repo.list_all(db)
    return render_page(request, "admin/comments.html", current_user=current_user, comments=comments)


@router.post("/admin/comments/{comment_id}/delete")
def admin_delete_comment(
    request: Request,
    comment_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    comment = comment_repo.get_by_id(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment_repo.soft_delete(db, comment)
    db.commit()
    if request.headers.get("hx-request") == "true":
        return Response("", media_type="text/html")
    return RedirectResponse("/admin/comments", status_code=303)


@router.get("/admin/users")
def admin_users(
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    users = user_repo.list_all(db)
    return render_page(request, "admin/users.html", current_user=current_user, users=users)


@router.post("/admin/users/{user_id}/role")
def set_user_role(
    request: Request,
    user_id: int,
    role: str = Form("user"),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = _get_user_or_404(db, user_id)
    if role not in ("user", "admin"):
        raise HTTPException(status_code=400, detail="Invalid role")
    if user.id == current_user.id and role != "admin":
        raise HTTPException(status_code=400, detail="Cannot demote yourself")
    user_repo.set_role(db, user, role)
    db.commit()
    return RedirectResponse("/admin/users", status_code=303)


@router.post("/admin/users/{user_id}/toggle-active")
def toggle_user_active(
    request: Request,
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = _get_user_or_404(db, user_id)
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate yourself")
    user_repo.set_active(db, user, not user.is_active)
    db.commit()
    return RedirectResponse("/admin/users", status_code=303)

