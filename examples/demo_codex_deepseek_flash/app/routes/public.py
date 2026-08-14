"""Public routes: home, post detail and health check."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..db import get_db
from ..dependencies import get_current_user
from ..models.user import User
from ..repositories import comment as comment_repo
from ..repositories import post as post_repo
from ..services import post as post_service
from ..templating import render_page

router = APIRouter()


@router.get("/")
def home(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user),
):
    posts = post_repo.list_published(db)
    return render_page(request, "public/home.html", posts=posts, current_user=current_user)


@router.get("/posts/{slug}")
def post_detail(
    request: Request,
    slug: str,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user),
):
    post = post_service.get_public_post(db, slug)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    comments = comment_repo.list_for_post(db, post.id)
    return render_page(
        request,
        "public/post_detail.html",
        post=post,
        comments=comments,
        current_user=current_user,
    )

