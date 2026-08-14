"""Admin routes: dashboard and management pages for posts, comments and users."""

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse, Response

from app import repositories as repo
from app.db import get_db
from app.dependencies import flash, require_admin
from app.models import (
    ROLE_ADMIN,
    ROLE_USER,
    STATUS_DRAFT,
    STATUS_PUBLISHED,
    STATUS_REJECTED,
    STATUS_SUBMITTED,
    User,
)
from app.services import comment as comment_service
from app.services import post as post_service
from app.templating import is_htmx, render

router = APIRouter()

STATUS_LABELS = {
    STATUS_DRAFT: "草稿",
    STATUS_SUBMITTED: "待审核",
    STATUS_PUBLISHED: "已发布",
    STATUS_REJECTED: "已驳回",
}


@router.get("/admin")
def dashboard(request: Request, _user: User = Depends(require_admin), db: Session = Depends(get_db)):
    stats = {
        "posts": repo.post.count(db),
        "users": repo.user.count(db),
        "comments": repo.comment.count(db),
        "pending": repo.post.count_by_status(db, STATUS_SUBMITTED),
    }
    by_status = {
        status: repo.post.count_by_status(db, status)
        for status in (STATUS_DRAFT, STATUS_SUBMITTED, STATUS_PUBLISHED, STATUS_REJECTED)
    }
    recent_posts = repo.post.list_all(db)[:5]
    return render(
        request, "admin/dashboard.html",
        {"stats": stats, "by_status": by_status, "recent_posts": recent_posts, "status_labels": STATUS_LABELS},
    )


@router.get("/admin/posts")
def manage_posts(request: Request, _user: User = Depends(require_admin), db: Session = Depends(get_db)):
    posts = repo.post.list_all(db)
    return render(request, "admin/posts.html", {"posts": posts, "status_labels": STATUS_LABELS})


def _admin_post(db: Session, post_id: int) -> object:
    post = repo.post.get_by_id(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    return post


def _post_row_or_redirect(request: Request, db: Session, post_id: int):
    """HTMX requests get the refreshed post row; others redirect back."""
    if is_htmx(request):
        post = _admin_post(db, post_id)
        return render(request, "components/admin_post_row.html", {"post": post, "status_labels": STATUS_LABELS})
    return RedirectResponse("/admin/posts", status_code=303)


@router.post("/admin/posts/{post_id}/publish")
def admin_publish(request: Request, post_id: int, _user: User = Depends(require_admin), db: Session = Depends(get_db)):
    post = _admin_post(db, post_id)
    post_service.publish_post(db, post=post)
    db.commit()
    return _post_row_or_redirect(request, db, post_id)


@router.post("/admin/posts/{post_id}/reject")
def admin_reject(request: Request, post_id: int, _user: User = Depends(require_admin), db: Session = Depends(get_db)):
    post = _admin_post(db, post_id)
    post_service.reject_post(db, post=post)
    db.commit()
    return _post_row_or_redirect(request, db, post_id)


@router.post("/admin/posts/{post_id}/unpublish")
def admin_unpublish(request: Request, post_id: int, _user: User = Depends(require_admin), db: Session = Depends(get_db)):
    post = _admin_post(db, post_id)
    post_service.unpublish_post(db, post=post)
    db.commit()
    return _post_row_or_redirect(request, db, post_id)


@router.post("/admin/posts/{post_id}/delete")
def admin_delete(request: Request, post_id: int, _user: User = Depends(require_admin), db: Session = Depends(get_db)):
    post = _admin_post(db, post_id)
    post_service.delete_post(db, post=post)
    db.commit()
    if is_htmx(request):
        return Response(content="", status_code=200)
    return RedirectResponse("/admin/posts", status_code=303)


@router.get("/admin/comments")
def manage_comments(request: Request, _user: User = Depends(require_admin), db: Session = Depends(get_db)):
    comments = repo.comment.list_all(db)
    return render(request, "admin/comments.html", {"comments": comments})


@router.post("/admin/comments/{comment_id}/delete")
def admin_delete_comment(
    request: Request,
    comment_id: int,
    _user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    comment = repo.comment.get_by_id(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="comment not found")
    comment_service.delete_comment(db, comment=comment)
    db.commit()
    if is_htmx(request):
        return Response(content="", status_code=200)
    return RedirectResponse("/admin/comments", status_code=303)


@router.get("/admin/users")
def manage_users(request: Request, _user: User = Depends(require_admin), db: Session = Depends(get_db)):
    users = repo.user.list_all(db)
    return render(request, "admin/users.html", {"users": users})


@router.post("/admin/users/{user_id}/toggle-active")
def toggle_user_active(
    request: Request,
    user_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = repo.user.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    if user.id == admin.id:
        flash(request, "不能停用自己的账号", "error")
        return RedirectResponse("/admin/users", status_code=303)
    user.is_active = not user.is_active
    repo.user.save(db, user)
    db.commit()
    return RedirectResponse("/admin/users", status_code=303)


@router.post("/admin/users/{user_id}/role")
def change_user_role(
    request: Request,
    user_id: int,
    role: str = Form(...),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = repo.user.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    if role not in (ROLE_USER, ROLE_ADMIN):
        raise HTTPException(status_code=400, detail="invalid role")
    if user.id == admin.id and role != ROLE_ADMIN:
        flash(request, "不能取消自己的管理员角色", "error")
        return RedirectResponse("/admin/users", status_code=303)
    user.role = role
    repo.user.save(db, user)
    db.commit()
    return RedirectResponse("/admin/users", status_code=303)
