"""Comment business logic and permission rules."""

from sqlalchemy.orm import Session

from app import repositories as repo
from app.models import Comment, Post, User


class PermissionDeniedError(Exception):
    """Raised when a user is not allowed to delete a comment."""


def create_comment(db: Session, *, author: User, post: Post, content: str) -> Comment:
    """Create a comment on a post; content must be non-empty."""
    content = content.strip()
    if not content:
        raise ValueError("comment must not be empty")
    return repo.comment.create(db, post_id=post.id, author_id=author.id, content=content)


def can_delete(user: User, comment: Comment) -> bool:
    """Admins delete any comment; users delete their own."""
    return user.is_admin or comment.author_id == user.id


def delete_comment(db: Session, *, comment: Comment) -> Comment:
    """Soft-delete a comment (hidden from all listings)."""
    return repo.comment.soft_delete(db, comment)
