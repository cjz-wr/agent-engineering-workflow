"""Comment routes (HTMX-friendly async submission and deletion)."""

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse, Response

from app import repositories as repo
from app.db import get_db
from app.dependencies import flash, require_login
from app.models import User
from app.services import comment as comment_service
from app.templating import is_htmx, render

router = APIRouter()


@router.post("/posts/{slug}/comments")
def create_comment(
    request: Request,
    slug: str,
    content: str = Form(...),
    user: User = Depends(require_login),
    db: Session = Depends(get_db),
):
    post = repo.post.get_by_slug(db, slug)
    if post is None or not post.is_published:
        raise HTTPException(status_code=404, detail="post not found")
    try:
        comment = comment_service.create_comment(db, author=user, post=post, content=content)
        db.commit()
    except ValueError as exc:
        db.rollback()
        flash(request, str(exc), "error")
        if is_htmx(request):
            return render(
                request,
                "components/comment_form_oob.html",
                {"post": post, "error_message": str(exc)},
                status_code=400,
            )
        return RedirectResponse(f"/posts/{post.slug}", status_code=303)
    if is_htmx(request):
        # Main swap: append the new comment; OOB swap: reset the form.
        return render(request, "components/comment_created.html", {"comment": comment, "post": post})
    return RedirectResponse(f"/posts/{post.slug}#comments", status_code=303)


@router.post("/comments/{comment_id}/delete")
def delete_comment(
    request: Request,
    comment_id: int,
    user: User = Depends(require_login),
    db: Session = Depends(get_db),
):
    comment = repo.comment.get_by_id(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="comment not found")
    if not comment_service.can_delete(user, comment):
        raise HTTPException(status_code=403, detail="not allowed to delete this comment")
    comment_service.delete_comment(db, comment=comment)
    db.commit()
    if is_htmx(request):
        return Response(content="", status_code=200)
    flash(request, "评论已删除", "success")
    return RedirectResponse(f"/posts/{comment.post.slug}#comments", status_code=303)
