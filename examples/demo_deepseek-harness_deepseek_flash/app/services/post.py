"""Article lifecycle business logic and permission rules."""

import re
import secrets

from sqlalchemy.orm import Session

from app import repositories as repo
from app.config import get_settings
from app.models import (
    STATUS_DRAFT,
    STATUS_PUBLISHED,
    STATUS_REJECTED,
    STATUS_SUBMITTED,
    Post,
    User,
)
from app.utils import utcnow

SLUG_MAX_LENGTH = 200


class PermissionDeniedError(Exception):
    """Raised when a user is not allowed to perform an operation."""


class InvalidTransitionError(Exception):
    """Raised for an illegal article status transition."""


def slugify(title: str) -> str:
    """ASCII slug from a title; falls back to a random slug when empty."""
    text = title.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    slug = text.strip("-")
    if not slug:
        slug = f"post-{secrets.token_hex(4)}"
    return slug[:SLUG_MAX_LENGTH].rstrip("-")


def unique_slug(db: Session, title: str, *, exclude_id: int | None = None) -> str:
    """Slug guaranteed unique across posts (appends -2, -3, ... on conflict)."""
    base = slugify(title)
    slug = base
    counter = 2
    while True:
        existing = repo.post.get_by_slug(db, slug)
        if existing is None or (exclude_id is not None and existing.id == exclude_id):
            return slug
        suffix = f"-{counter}"
        slug = f"{base[: SLUG_MAX_LENGTH - len(suffix)]}{suffix}"
        counter += 1


def can_manage(user: User, post: Post) -> bool:
    """Admins manage any post; authors manage their own."""
    return user.is_admin or post.author_id == user.id


def can_publish(user: User, post: Post) -> bool:
    """Admins always publish; users publish their own only when configured."""
    if user.is_admin:
        return True
    return post.author_id == user.id and get_settings().allow_user_publish


def create_post(db: Session, *, author: User, title: str, content: str = "") -> Post:
    """Create a post in draft status with an auto-generated unique slug."""
    slug = unique_slug(db, title)
    return repo.post.create(db, author_id=author.id, title=title.strip(), slug=slug, content=content)


def update_post(db: Session, *, post: Post, title: str, content: str) -> Post:
    """Update title and content of a post."""
    post.title = title.strip()
    post.content = content
    return repo.post.save(db, post)


def submit_post(db: Session, *, post: Post) -> Post:
    """Move a post to submitted (only from draft or rejected)."""
    if post.status not in (STATUS_DRAFT, STATUS_REJECTED):
        raise InvalidTransitionError(f"cannot submit a post in status '{post.status}'")
    post.status = STATUS_SUBMITTED
    return repo.post.save(db, post)


def publish_post(db: Session, *, post: Post) -> Post:
    """Publish a post (records published_at)."""
    post.status = STATUS_PUBLISHED
    if post.published_at is None:
        post.published_at = utcnow()
    return repo.post.save(db, post)


def reject_post(db: Session, *, post: Post) -> Post:
    """Reject a submitted post."""
    post.status = STATUS_REJECTED
    return repo.post.save(db, post)


def unpublish_post(db: Session, *, post: Post) -> Post:
    """Unpublish a post back to draft."""
    post.status = STATUS_DRAFT
    post.published_at = None
    return repo.post.save(db, post)


def delete_post(db: Session, *, post: Post) -> None:
    """Hard-delete a post (cascades to its comments)."""
    repo.post.delete(db, post)
