"""Comment behavior and permission tests."""

import httpx

from .conftest import create_post, get_post_slug, new_user_client, publish_post


def _published_post(server):
    _, author = new_user_client(server, prefix="post_author")
    _, admin = new_user_client(server, prefix="comment_admin", role="admin")
    post_id = create_post(author, "Comment Target")
    publish_post(author, admin, post_id)
    return author, admin, get_post_slug(post_id)


def test_logged_in_user_can_comment(server):
    _, _, slug = _published_post(server)
    _, commenter = new_user_client(server, prefix="commenter")
    response = commenter.post(f"/posts/{slug}/comments", data={"content": "Great article!"})
    assert response.status_code == 303
    assert "Great article!" in httpx.get(f"{server}/posts/{slug}").text


def test_guest_cannot_comment(server, client: httpx.Client):
    _, _, slug = _published_post(server)
    response = client.post(f"/posts/{slug}/comments", data={"content": "nope"})
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_comment_linked_to_post_and_user(server):
    _, _, slug = _published_post(server)
    username, commenter = new_user_client(server, prefix="link")
    commenter.post(f"/posts/{slug}/comments", data={"content": "By linked user"})
    page = httpx.get(f"{server}/posts/{slug}").text
    assert "By linked user" in page
    assert username in page


def test_user_can_delete_own_comment(server):
    _, _, slug = _published_post(server)
    _, commenter = new_user_client(server, prefix="own_delete")
    commenter.post(f"/posts/{slug}/comments", data={"content": "my comment"})
    page = httpx.get(f"{server}/posts/{slug}").text
    assert "comment-1" in page

    response = commenter.post("/comments/1/delete", headers={"HX-Request": "true"})
    assert response.status_code == 200
    assert response.text == ""
    assert "my comment" not in httpx.get(f"{server}/posts/{slug}").text


def test_admin_can_delete_any_comment(server):
    _, admin, slug = _published_post(server)
    _, commenter = new_user_client(server, prefix="victim")
    commenter.post(f"/posts/{slug}/comments", data={"content": "to be moderated"})

    response = admin.post("/admin/comments/1/delete", headers={"HX-Request": "true"})
    assert response.status_code == 200
    assert "to be moderated" not in httpx.get(f"{server}/posts/{slug}").text


def test_comment_requires_nonempty_content(server):
    _, _, slug = _published_post(server)
    _, commenter = new_user_client(server, prefix="empty_comment")
    response = commenter.post(f"/posts/{slug}/comments", data={"content": "   "})
    assert response.status_code == 400

