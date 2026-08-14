"""Data access for the Post model."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import STATUS_DRAFT, Post


def create(
    db: Session,
    *,
    author_id: int,
    title: str,
    slug: str,
    content: str = "",
    status: str = STATUS_DRAFT,
) -> Post:
    post = Post(author_id=author_id, title=title, slug=slug, content=content, status=status)
    db.add(post)
    db.flush()
    return post


def get_by_id(db: Session, post_id: int) -> Post | None:
    return db.get(Post, post_id)


def get_by_slug(db: Session, slug: str) -> Post | None:
    stmt = select(Post).where(Post.slug == slug)
    return db.execute(stmt).scalar_one_or_none()


def list_published(db: Session) -> list[Post]:
    from app.models import STATUS_PUBLISHED

    stmt = (
        select(Post)
        .where(Post.status == STATUS_PUBLISHED)
        .order_by(Post.published_at.desc(), Post.id.desc())
    )
    return list(db.execute(stmt).scalars())


def list_by_author(db: Session, author_id: int) -> list[Post]:
    stmt = select(Post).where(Post.author_id == author_id).order_by(Post.updated_at.desc(), Post.id.desc())
    return list(db.execute(stmt).scalars())


def list_all(db: Session) -> list[Post]:
    stmt = select(Post).order_by(Post.updated_at.desc(), Post.id.desc())
    return list(db.execute(stmt).scalars())


def list_by_status(db: Session, status: str) -> list[Post]:
    stmt = select(Post).where(Post.status == status).order_by(Post.updated_at.desc(), Post.id.desc())
    return list(db.execute(stmt).scalars())


def count(db: Session) -> int:
    return db.execute(select(func.count()).select_from(Post)).scalar_one()


def count_by_status(db: Session, status: str) -> int:
    stmt = select(func.count()).select_from(Post).where(Post.status == status)
    return db.execute(stmt).scalar_one()


def save(db: Session, post: Post) -> Post:
    db.add(post)
    db.flush()
    return post


def delete(db: Session, post: Post) -> None:
    db.delete(post)
    db.flush()
