"""Authentication business logic: registration, login, logout, session."""

from fastapi import Request
from sqlalchemy.orm import Session

from app import repositories as repo
from app.config import get_settings
from app.models import ROLE_ADMIN, ROLE_USER, User
from app.security import hash_password, verify_password

SESSION_USER_ID = "user_id"


class DuplicateUsernameError(Exception):
    """Raised when trying to register an existing username."""


class InvalidCredentialsError(Exception):
    """Raised when username or password do not match."""


def register(db: Session, *, username: str, password: str, display_name: str = "") -> User:
    """Create a new user account; raises DuplicateUsernameError if taken.

    The very first account registered on an empty database becomes an admin
    (bootstrap convenience, recorded in decision.md); subsequent accounts are
    regular users.
    """
    username = username.strip()
    if not username:
        raise ValueError("username must not be empty")
    if not password:
        raise ValueError("password must not be empty")
    if repo.user.get_by_username(db, username) is not None:
        raise DuplicateUsernameError(username)
    settings = get_settings()
    password_hash = hash_password(password, iterations=settings.password_iterations)
    role = ROLE_ADMIN if repo.user.count(db) == 0 else ROLE_USER
    return repo.user.create(
        db,
        username=username,
        password_hash=password_hash,
        display_name=display_name.strip(),
        role=role,
    )


def authenticate(db: Session, *, username: str, password: str) -> User | None:
    """Return the user when credentials are valid and the account is active."""
    user = repo.user.get_by_username(db, username.strip())
    if user is None or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def login_user(request: Request, user: User) -> None:
    """Store the signed-in user id in the session cookie."""
    request.session[SESSION_USER_ID] = user.id


def logout_user(request: Request) -> None:
    """Clear the session cookie."""
    request.session.clear()


def current_user_id(request: Request) -> int | None:
    """Id of the signed-in user, if any."""
    return request.session.get(SESSION_USER_ID)
