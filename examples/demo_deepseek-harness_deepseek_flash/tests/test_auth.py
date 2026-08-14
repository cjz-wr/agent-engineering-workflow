"""Authentication workflow tests: register, login, logout, sessions."""

from app import repositories as repo
from tests.conftest import SEED_USERNAME, login, register, register_and_login


def test_register_success(client, db):
    resp = register(client, "alice", "secret123", "Alice")
    assert resp.status_code == 303
    assert resp.headers["location"] == "/"

    user = repo.user.get_by_username(db, "alice")
    assert user is not None
    assert user.display_name == "Alice"
    assert user.role == "user"
    assert user.password_hash != "secret123"
    assert user.password_hash.startswith("pbkdf2_sha256$")

    # Register auto-logs the user in.
    home = client.get("/")
    assert home.status_code == 200
    assert "Alice" in home.text


def test_register_duplicate_username(client, db):
    assert register(client, "alice", "secret123").status_code == 303
    resp = register(client, "alice", "other-pass")
    assert resp.status_code == 400
    assert "已被占用" in resp.text


def test_login_success(client, db):
    register(client, "alice", "secret123", "Alice")
    client.post("/logout", follow_redirects=False)

    resp = login(client, "alice", "secret123")
    assert resp.status_code == 303
    assert resp.headers["location"] == "/"

    home = client.get("/")
    assert "Alice" in home.text


def test_login_wrong_password(client, db):
    register(client, "alice", "secret123", "Alice")
    client.post("/logout", follow_redirects=False)

    resp = login(client, "alice", "wrong-pass")
    assert resp.status_code == 400
    assert "用户名或密码错误" in resp.text

    # Not signed in afterwards.
    home = client.get("/")
    assert "Alice" not in home.text


def test_logout(client, db):
    register_and_login(client, "alice", "secret123", "Alice")
    resp = client.post("/logout", follow_redirects=False)
    assert resp.status_code == 303
    assert resp.headers["location"] == "/"

    home = client.get("/")
    assert "Alice" not in home.text
    assert "登录" in home.text


def test_unauthenticated_access_to_protected_page(client, db):
    resp = client.get("/posts/new", follow_redirects=False)
    assert resp.status_code == 303
    assert resp.headers["location"].startswith("/login")


def test_password_not_stored_in_plaintext(client, db):
    register(client, "alice", "secret123")
    user = repo.user.get_by_username(db, "alice")
    assert user is not None
    assert "secret123" not in user.password_hash


def test_first_registered_user_becomes_admin(client, make_client, db):
    # Remove the conftest seed user to simulate a fresh install.
    seed = repo.user.get_by_username(db, SEED_USERNAME)
    db.delete(seed)
    db.commit()

    register(client, "founder", "secret123", "Founder")
    founder = repo.user.get_by_username(db, "founder")
    assert founder.is_admin is True

    # The second registered user stays a regular user.
    second_client = make_client()
    register(second_client, "member2", "secret123", "Member")
    member = repo.user.get_by_username(db, "member2")
    assert member.is_admin is False
    assert member.role == "user"
