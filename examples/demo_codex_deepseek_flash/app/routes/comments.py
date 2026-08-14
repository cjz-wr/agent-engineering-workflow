"""Comment routes: create and delete (with HTMX support)."""

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session

from ..db import get_db
from ..dependencies import require_user
from ..models.user import User
from ..repositories import comment as comment_repo
from ..services import comment as comment_service
from ..services import post as post_service
from ..templating import render_page

router = APIRouter()


@router.post("/posts/{slug}/comments")
def create_comment(
    request: Request,
    slug: str,
    content: str = Form(""),
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    post = post_service.get_public_post(db, slug)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    comment = comment_service.create_comment(db, post=post, author=current_user, content=content)
    if comment is None:
        return Response("评论内容不能为空或过长。", status_code=400, media_type="text/plain")
    db.commit()

    if request.headers.get("hx-request") == "true":
        return render_page(request, "components/comment_item.html", current_user=current_user, comment=comment)
    return RedirectResponse(f"/posts/{slug}#comments", status_code=303)


@router.post("/comments/{comment_id}/delete")
def delete_comment(
    request: Request,
    comment_id: int,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    comment = comment_repo.get_by_id(db, comment_id)
    if comment is None or not comment_service.can_delete(current_user, comment):
        raise HTTPException(status_code=404, detail="Comment not found")

    comment_repo.soft_delete(db, comment)
    db.commit()

    if request.headers.get("hx-request") == "true":
        return Response("", media_type="text/html")
    return RedirectResponse(f"/posts/{comment.post.slug}#comments", status_code=303)

