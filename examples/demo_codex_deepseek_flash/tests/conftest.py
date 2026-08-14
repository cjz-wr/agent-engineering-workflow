"""Shared pytest fixtures.

Strategy: run the real app with uvicorn on a random localhost port against a
temporary SQLite database, then exercise it with a sync httpx client.
(The bundled starlette TestClient is incompatible with httpx 0.28, and a real
server also exercises the full ASGI stack.)
"""

import os
import socket
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

import httpx
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Configure environment BEFORE any app module is imported.
_DB_PATH = Path(tempfile.gettempdir()) / f"mini_blog_test_{uuid.uuid4().hex}.db"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DATABASE_URL"] = f"sqlite:///{_DB_PATH.as_posix()}"
os.environ["ALLOW_USER_PUBLISH"] = "false"


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture(scope="session")
def server():
    """Start the app with uvicorn once per test session; yield its base URL."""
    port = _free_port()
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
            "--log-level",
            "warning",
        ],
        cwd=str(PROJECT_ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creationflags,
    )
    base_url = f"http://127.0.0.1:{port}"
    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            if httpx.get(f"{base_url}/health", timeout=2).status_code == 200:
                break
        except Exception:
            time.sleep(0.3)
    else:
        proc.terminate()
        raise RuntimeError("Test server failed to start")

    yield base_url

    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
    _DB_PATH.unlink(missing_ok=True)


def unique_name(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def register(client: httpx.Client, username: str, password: str = "secret123", display_name: str = ""):
    return client.post(
        "/register",
        data={"username": username, "password": password, "display_name": display_name or username},
    )


def login(client: httpx.Client, username: str, password: str = "secret123"):
    return client.post("/login", data={"username": username, "password": password})


def promote_to_admin(username: str) -> None:
    """Promote a registered user to admin directly in the shared test database."""
    from app.db import SessionLocal
    from app.repositories import user as user_repo

    db = SessionLocal()
    try:
        user = user_repo.get_by_username(db, username)
        assert user is not None
        user.role = "admin"
        db.commit()
    finally:
        db.close()


def new_user_client(server: str, prefix: str = "user", role: str = "user", password: str = "secret123") -> tuple[str, httpx.Client]:
    """Create a fresh user (optionally admin) and return (username, authenticated client)."""
    username = unique_name(prefix)
    client = httpx.Client(base_url=server, follow_redirects=False)
    response = register(client, username, password=password)
    assert response.status_code == 303, response.text
    if role == "admin":
        promote_to_admin(username)
    response = login(client, username, password=password)
    assert response.status_code == 303, response.text
    return username, client


def create_post(client: httpx.Client, title: str, content: str = "# Body") -> int:
    """Create a post via the author client; returns its id."""
    response = client.post("/posts", data={"title": title, "content": content})
    assert response.status_code == 303, response.text
    return int(response.headers["location"].split("/")[2])


def publish_post(author_client: httpx.Client, admin_client: httpx.Client, post_id: int) -> None:
    """Run the full workflow: submit by author, publish by admin."""
    assert author_client.post(f"/posts/{post_id}/submit").status_code == 303
    assert admin_client.post(f"/admin/posts/{post_id}/publish").status_code in (200, 303)


def get_post_slug(post_id: int) -> str:
    from app.db import SessionLocal
    from app.repositories import post as post_repo

    db = SessionLocal()
    try:
        post = post_repo.get_by_id(db, post_id)
        assert post is not None
        return post.slug
    finally:
        db.close()


@pytest.fixture()
def client(server):
    with httpx.Client(base_url=server, follow_redirects=False) as c:
        yield c

