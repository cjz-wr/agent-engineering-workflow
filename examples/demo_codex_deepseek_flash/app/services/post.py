"""Post business logic: slug generation, lifecycle and permissions."""

import re
import unicodedata
from datetime import datetime

from sqlalchemy.orm import Session

from ..config import settings
from ..models.post import Post
from ..models.user import User
from ..repositories import post as post_repo

DRAFT = "draft"
SUBMITTED = "submitted"
PUBLISHED = "published"
REJECTED = "rejected"

ALL_STATUSES = (DRAFT, SUBMITTED, PUBLISHED, REJECTED)


def slugify(text: str) -> str:
    """Convert a title into a URL-safe slug (ASCII, lower-case, hyphenated)."""
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^\w\s-]", "", normalized).strip().lower()
    normalized = re.sub(r"[-\s]+", "-", normalized).strip("-")
    return normalized[:180] or "post"


def unique_slug(db: Session, base: str, exclude_id: int | None = None) -> str:
    """Generate a unique slug by appending a numeric suffix when needed."""
    candidate = slugify(base)
    slug = candidate
    n = 2
    while True:
        existing = post_repo.get_by_slug(db, slug)
        if existing is None or (exclude_id is not None and existing.id == exclude_id):
            return slug
        slug = f"{candidate}-{n}"
        n += 1


def create_draft(db: Session, *, author_id: int, title: str, content: str) -> Post:
    return post_repo.create(
        db,
        author_id=author_id,
        title=title.strip(),
        slug=unique_slug(db, title),
        content=content,
        status=DRAFT,
    )


def update_post(
    db: Session, post: Post, *, title: str, content: str, action: str = "save"
) -> Post:
    """Update a post. Editing a rejected post returns it to draft."""
    post.title = title.strip()
    post.content = content
    if post.status == REJECTED:
        post.status = DRAFT
        post.published_at = None
    if action == "submit":
        submit_post(db, post)
    return post


def submit_post(db: Session, post: Post) -> Post:
    """Move a draft/rejected post to submitted (or published when allowed)."""
    if post.status in (DRAFT, REJECTED):
        if settings.allow_user_publish:
            post.status = PUBLISHED
            post.published_at = datetime.utcnow()
        else:
            post.status = SUBMITTED
            post.published_at = None
    return post


def publish_post(db: Session, post: Post) -> Post:
    if post.status != PUBLISHED:
        post.status = PUBLISHED
        post.published_at = datetime.utcnow()
    return post


def reject_post(db: Session, post: Post) -> Post:
    if post.status == SUBMITTED:
        post.status = REJECTED
        post.published_at = None
    return post


def unpublish_post(db: Session, post: Post) -> Post:
    if post.status == PUBLISHED:
        post.status = DRAFT
        post.published_at = None
    return post


def delete_post(db: Session, post: Post) -> None:
    post_repo.delete(db, post)


def get_public_post(db: Session, slug: str) -> Post | None:
    """Return a published post by slug, otherwise None."""
    post = post_repo.get_by_slug(db, slug)
    if post is None or post.status != PUBLISHED:
        return None
    return post


def can_modify(user: User | None, post: Post) -> bool:
    """Author may manage their own post; admins may manage any post."""
    if user is None:
        return False
    return post.author_id == user.id or user.is_admin

