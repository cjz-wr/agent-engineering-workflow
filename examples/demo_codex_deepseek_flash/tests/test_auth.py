"""Authentication workflow tests."""

import httpx

from .conftest import login, register, unique_name


def test_register_success(client: httpx.Client):
    username = unique_name("reg")
    response = register(client, username)
    assert response.status_code == 303
    assert response.headers["location"] == "/"
    assert "mini_blog_session" in response.headers.get("set-cookie", "")


def test_register_duplicate_username(client: httpx.Client):
    username = unique_name("dup")
    assert register(client, username).status_code == 303
    response = register(client, username)
    assert response.status_code == 200
    assert "已被注册" in response.text


def test_register_requires_username_and_password(client: httpx.Client):
    response = register(client, unique_name("empty"), password="")
    assert response.status_code == 200
    assert "密码不能为空" in response.text


def test_login_success(client: httpx.Client):
    username = unique_name("login")
    register(client, username)
    client.cookies.clear()
    response = login(client, username)
    assert response.status_code == 303
    assert response.headers["location"] == "/"
    assert "mini_blog_session" in response.headers.get("set-cookie", "")


def test_login_wrong_password(client: httpx.Client):
    username = unique_name("wrong")
    register(client, username)
    client.cookies.clear()
    response = login(client, username, password="nope")
    assert response.status_code == 200
    assert "用户名或密码错误" in response.text


def test_logout(client: httpx.Client):
    username = unique_name("logout")
    register(client, username)
    response = client.post("/logout")
    assert response.status_code == 303
    # After logout, a protected page must redirect to login.
    response = client.get("/posts/new")
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_protected_page_requires_login(client: httpx.Client):
    response = client.get("/posts/new")
    assert response.status_code == 303
    assert response.headers["location"] == "/login"

