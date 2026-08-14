"""Public routes: home, published post detail, health check."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app import repositories as repo
from app.db import get_db
from app.dependencies import get_current_user
from app.models import User
from app.templating import render

router = APIRouter()


@router.get("/")
def home(request: Request, db: Session = Depends(get_db), _user: User | None = Depends(get_current_user)):
    posts = repo.post.list_published(db)
    return render(request, "public/index.html", {"posts": posts})


@router.get("/posts/{slug}")
def post_detail(
    request: Request,
    slug: str,
    db: Session = Depends(get_db),
    _user: User | None = Depends(get_current_user),
):
    post = repo.post.get_by_slug(db, slug)
    # Non-public statuses must never be reachable through the public route.
    if post is None or not post.is_published:
        raise HTTPException(status_code=404, detail="post not found")
    comments = repo.comment.list_for_post(db, post.id)
    return render(request, "public/post_detail.html", {"post": post, "comments": comments})


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}
