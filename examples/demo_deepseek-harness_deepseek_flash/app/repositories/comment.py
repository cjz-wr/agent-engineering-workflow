"""Data access for the Comment model."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Comment


def create(db: Session, *, post_id: int, author_id: int, content: str) -> Comment:
    comment = Comment(post_id=post_id, author_id=author_id, content=content)
    db.add(comment)
    db.flush()
    return comment


def get_by_id(db: Session, comment_id: int) -> Comment | None:
    return db.get(Comment, comment_id)


def list_for_post(db: Session, post_id: int) -> list[Comment]:
    """Visible (non-deleted) comments for a post, oldest first."""
    stmt = (
        select(Comment)
        .where(Comment.post_id == post_id, Comment.is_deleted.is_(False))
        .order_by(Comment.created_at.asc(), Comment.id.asc())
    )
    return list(db.execute(stmt).scalars())


def list_all(db: Session) -> list[Comment]:
    """Visible (non-deleted) comments across all posts, newest first."""
    stmt = (
        select(Comment)
        .where(Comment.is_deleted.is_(False))
        .order_by(Comment.created_at.desc(), Comment.id.desc())
    )
    return list(db.execute(stmt).scalars())


def count(db: Session) -> int:
    stmt = select(func.count()).select_from(Comment).where(Comment.is_deleted.is_(False))
    return db.execute(stmt).scalar_one()


def soft_delete(db: Session, comment: Comment) -> Comment:
    comment.is_deleted = True
    db.add(comment)
    db.flush()
    return comment
