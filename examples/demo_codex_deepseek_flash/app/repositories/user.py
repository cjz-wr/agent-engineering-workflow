"""Data access layer for users."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models.user import User


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_by_username(db: Session, username: str) -> User | None:
    return db.scalar(select(User).where(User.username == username))


def create(
    db: Session,
    *,
    username: str,
    password_hash: str,
    display_name: str = "",
    avatar: str = "",
    role: str = "user",
) -> User:
    user = User(
        username=username,
        password_hash=password_hash,
        display_name=display_name,
        avatar=avatar,
        role=role,
    )
    db.add(user)
    return user


def list_all(db: Session) -> list[User]:
    return list(db.scalars(select(User).order_by(User.created_at.desc())))


def count(db: Session) -> int:
    return db.scalar(select(func.count(User.id))) or 0


def set_role(db: Session, user: User, role: str) -> User:
    user.role = role
    return user


def set_active(db: Session, user: User, is_active: bool) -> User:
    user.is_active = is_active
    return user

