"""Data access layer for comments."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models.comment import Comment


def get_by_id(db: Session, comment_id: int) -> Comment | None:
    return db.get(Comment, comment_id)


def create(db: Session, *, post_id: int, author_id: int, content: str) -> Comment:
    comment = Comment(post_id=post_id, author_id=author_id, content=content)
    db.add(comment)
    return comment


def list_for_post(db: Session, post_id: int) -> list[Comment]:
    return list(
        db.scalars(
            select(Comment)
            .where(Comment.post_id == post_id, Comment.is_deleted.is_(False))
            .order_by(Comment.created_at.asc())
        )
    )


def list_all(db: Session) -> list[Comment]:
    return list(db.scalars(select(Comment).order_by(Comment.created_at.desc())))


def list_recent(db: Session, limit: int = 10) -> list[Comment]:
    return list(db.scalars(select(Comment).order_by(Comment.created_at.desc()).limit(limit)))


def count(db: Session) -> int:
    return db.scalar(select(func.count(Comment.id))) or 0


def soft_delete(db: Session, comment: Comment) -> Comment:
    comment.is_deleted = True
    return comment

