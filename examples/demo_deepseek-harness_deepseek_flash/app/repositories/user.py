"""Data access for the User model."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import ROLE_USER, User


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalar_one_or_none()


def create(
    db: Session,
    *,
    username: str,
    password_hash: str,
    display_name: str = "",
    role: str = ROLE_USER,
) -> User:
    user = User(
        username=username,
        password_hash=password_hash,
        display_name=display_name,
        role=role,
    )
    db.add(user)
    db.flush()
    return user


def list_all(db: Session) -> list[User]:
    stmt = select(User).order_by(User.created_at.desc())
    return list(db.execute(stmt).scalars())


def count(db: Session) -> int:
    return db.execute(select(func.count()).select_from(User)).scalar_one()


def save(db: Session, user: User) -> User:
    db.add(user)
    db.flush()
    return user
