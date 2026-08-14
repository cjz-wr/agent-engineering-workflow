"""Shared pytest fixtures.

Environment variables must be set before the app is imported, so this module
configures them at import time (no app imports above this block).
"""

import os
import tempfile

_TEST_DIR = tempfile.mkdtemp(prefix="mini_blog_test_")
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DATABASE_URL"] = f"sqlite:///{os.path.join(_TEST_DIR, 'test.db')}"
os.environ["ALLOW_USER_PUBLISH"] = "false"
# Speed up PBKDF2 hashing in tests (600k iterations is for production).
os.environ["PASSWORD_ITERATIONS"] = "1000"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app import repositories as repo  # noqa: E402
from app.db import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.services import auth as auth_service  # noqa: E402
from app.services import post as post_service  # noqa: E402

SEED_USERNAME = "seed_user"


def _seed_user(session) -> None:
    """Insert one regular user so test-registered users are never the first
    account (which would otherwise auto-become admin)."""
    if repo.user.count(session) == 0:
        auth_service.register(session, username=SEED_USERNAME, password="seed-pass-1")
        session.commit()


@pytest.fixture()
def db():
    """Isolated database session with tables created/dropped per test."""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    _seed_user(session)
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def fresh_session():
    """A brand-new session for assertions after HTTP mutations (avoids the
    identity-map staleness of the long-lived `db` fixture)."""
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture()
def client(db):
    """TestClient bound to the isolated database."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def make_client(db):
    """Factory for independent TestClients (isolated session cookies)."""
    created: list[TestClient] = []

    def _make() -> TestClient:
        test_client = TestClient(app)
        created.append(test_client)
        return test_client

    yield _make
    for test_client in created:
        test_client.close()


def register(client, username="alice", password="secret123", display_name="Alice"):
    return client.post(
        "/register",
        data={"username": username, "password": password, "display_name": display_name},
        follow_redirects=False,
    )


def login(client, username="alice", password="secret123"):
    return client.post(
        "/login",
        data={"username": username, "password": password, "next": "/"},
        follow_redirects=False,
    )


def register_and_login(client, username="alice", password="secret123", display_name="Alice"):
    register(client, username, password, display_name)
    return login(client, username, password)


def make_published_post(db, author, title="Hello World", content="# Hi\n\nBody text"):
    """Create a post owned by `author` and publish it directly in the DB."""
    post = post_service.create_post(db, author=author, title=title, content=content)
    post_service.publish_post(db, post=post)
    db.commit()
    return post


@pytest.fixture()
def alice_client(db, make_client):
    """Signed-in non-admin user on a dedicated client."""
    test_client = make_client()
    register_and_login(test_client, "alice", "secret123", "Alice")
    return test_client


@pytest.fixture()
def bob_client(db, make_client):
    """A second signed-in non-admin user on a dedicated client."""
    test_client = make_client()
    register_and_login(test_client, "bob", "secret123", "Bob")
    return test_client


@pytest.fixture()
def admin_client(db, make_client):
    """Signed-in admin user on a dedicated client."""
    user = auth_service.register(db, username="boss", password="secret123", display_name="Boss")
    user.role = "admin"
    db.commit()
    test_client = make_client()
    login(test_client, "boss", "secret123")
    return test_client


@pytest.fixture()
def author(db):
    """A registered user (not signed in) used to own posts in the DB."""
    user = auth_service.register(db, username="carol", password="secret123", display_name="Carol")
    db.commit()  # Commit so no transaction holds the SQLite file lock.
    return user


__all__ = [
    "db",
    "fresh_session",
    "client",
    "make_client",
    "register",
    "login",
    "register_and_login",
    "make_published_post",
    "alice_client",
    "bob_client",
    "admin_client",
    "author",
]
