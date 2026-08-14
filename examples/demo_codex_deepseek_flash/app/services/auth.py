"""Authentication business logic: password hashing, registration and login."""

import hashlib
import hmac
import secrets

from sqlalchemy.orm import Session

from ..models.user import User
from ..repositories import user as user_repo

_ALGO = "pbkdf2_sha256"
_ITERATIONS = 120_000


def hash_password(password: str) -> str:
    """Hash a password with PBKDF2-HMAC-SHA256 and a per-user random salt."""
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), _ITERATIONS
    )
    return f"{_ALGO}${_ITERATIONS}${salt}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algo, iterations, salt, expected = stored.split("$")
        if algo != _ALGO:
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt), int(iterations)
        )
        return hmac.compare_digest(digest.hex(), expected)
    except (ValueError, TypeError):
        return False


def register_user(
    db: Session, *, username: str, password: str, display_name: str = ""
) -> User | None:
    """Create a new regular user. Returns None when the username is taken or input is invalid."""
    username = username.strip()
    if not username or len(username) > 50 or not password:
        return None
    if user_repo.get_by_username(db, username):
        return None
    display_name = display_name.strip() or username
    return user_repo.create(
        db,
        username=username,
        password_hash=hash_password(password),
        display_name=display_name,
        role="user",
    )


def authenticate(db: Session, *, username: str, password: str) -> User | None:
    """Return the user on valid credentials, otherwise None."""
    user = user_repo.get_by_username(db, username.strip())
    if user is None or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

