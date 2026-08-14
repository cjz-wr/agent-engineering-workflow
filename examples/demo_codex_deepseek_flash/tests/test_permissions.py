"""Permission model tests: cross-user access and guest/admin guards."""

import httpx

from .conftest import create_post, new_user_client


def test_user_a_cannot_modify_user_b_post(server):
    """The README-required scenario: User A cannot modify User B's article."""
    _, user_a = new_user_client(server, prefix="user_a")
    _, user_b = new_user_client(server, prefix="user_b")
    post_id = create_post(user_b, "User B Post")

    assert user_a.get(f"/posts/{post_id}/edit").status_code == 404
    assert user_a.post(f"/posts/{post_id}", data={"title": "Hijacked", "content": "x"}).status_code == 404
    assert user_a.post(f"/posts/{post_id}/delete").status_code == 404
    assert user_a.post(f"/posts/{post_id}/submit").status_code == 404

    # The owner can still edit it.
    assert user_b.get(f"/posts/{post_id}/edit").status_code == 200


def test_guest_cannot_access_authenticated_routes(server, client: httpx.Client):
    assert client.get("/posts/new").status_code == 303
    assert client.get("/posts/1/edit").status_code == 303
    assert client.post("/posts", data={"title": "x"}).status_code == 303
    assert client.post("/posts/1/delete").status_code == 303
    assert client.post("/posts/1/submit").status_code == 303


def test_non_admin_cannot_access_admin_routes(server):
    _, user = new_user_client(server, prefix="plain_user")
    assert user.get("/admin").status_code == 303
    assert user.get("/admin/posts").status_code == 303
    assert user.get("/admin/comments").status_code == 303
    assert user.get("/admin/users").status_code == 303
    assert user.post("/admin/posts/1/publish").status_code == 303


def test_admin_can_access_admin_routes(server):
    _, admin = new_user_client(server, prefix="boss", role="admin")
    assert admin.get("/admin").status_code == 200
    assert admin.get("/admin/posts").status_code == 200
    assert admin.get("/admin/comments").status_code == 200
    assert admin.get("/admin/users").status_code == 200


def test_deactivated_user_cannot_login(server):
    username, user = new_user_client(server, prefix="soon_disabled")
    _, admin = new_user_client(server, prefix="disabler", role="admin")
    users_page = admin.get("/admin/users").text
    assert username in users_page

    # Find the user id from the page (role form action URL) and disable it.
    import re

    match = re.search(rf"/admin/users/(\d+)/role", users_page)
    assert match is not None
    user_id = int(match.group(1))
    assert admin.post(f"/admin/users/{user_id}/toggle-active").status_code == 303

    user.cookies.clear()
    response = user.post("/login", data={"username": username, "password": "secret123"})
    assert response.status_code == 200
    assert "用户名或密码错误" in response.text


def test_admin_cannot_demote_or_disable_self(server):
    _, admin = new_user_client(server, prefix="self_admin", role="admin")
    users_page = admin.get("/admin/users").text
    import re

    match = re.search(r"/admin/users/(\d+)/role", users_page)
    assert match is not None
    self_id = int(match.group(1))
    assert admin.post(f"/admin/users/{self_id}/role", data={"role": "user"}).status_code == 400
    assert admin.post(f"/admin/users/{self_id}/toggle-active").status_code == 400

