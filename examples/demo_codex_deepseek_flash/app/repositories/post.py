"""Data access layer for posts."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models.post import Post

PUBLISHED = "published"


def get_by_id(db: Session, post_id: int) -> Post | None:
    return db.get(Post, post_id)


def get_by_slug(db: Session, slug: str) -> Post | None:
    return db.scalar(select(Post).where(Post.slug == slug))


def create(
    db: Session,
    *,
    author_id: int,
    title: str,
    slug: str,
    content: str = "",
    status: str = "draft",
) -> Post:
    post = Post(author_id=author_id, title=title, slug=slug, content=content, status=status)
    db.add(post)
    return post


def list_published(db: Session) -> list[Post]:
    return list(
        db.scalars(
            select(Post)
            .where(Post.status == PUBLISHED)
            .order_by(Post.published_at.desc(), Post.created_at.desc())
        )
    )


def list_by_author(db: Session, author_id: int) -> list[Post]:
    return list(
        db.scalars(select(Post).where(Post.author_id == author_id).order_by(Post.updated_at.desc()))
    )


def list_all(db: Session) -> list[Post]:
    return list(db.scalars(select(Post).order_by(Post.updated_at.desc())))


def list_by_status(db: Session, status: str) -> list[Post]:
    return list(
        db.scalars(select(Post).where(Post.status == status).order_by(Post.updated_at.desc()))
    )


def count(db: Session) -> int:
    return db.scalar(select(func.count(Post.id))) or 0


def count_by_status(db: Session) -> dict[str, int]:
    rows = db.execute(select(Post.status, func.count(Post.id)).group_by(Post.status)).all()
    return {status: total for status, total in rows}


def delete(db: Session, post: Post) -> None:
    db.delete(post)

