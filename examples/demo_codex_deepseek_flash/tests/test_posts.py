"""Article lifecycle tests."""

import httpx

from .conftest import create_post, get_post_slug, new_user_client, publish_post


def _admin_and_author(server):
    _, admin = new_user_client(server, prefix="admin", role="admin")
    _, author = new_user_client(server, prefix="author")
    return author, admin


def test_create_post_defaults_to_draft(server):
    author, _ = _admin_and_author(server)
    post_id = create_post(author, "Draft Check")
    response = author.get(f"/posts/{post_id}/edit")
    assert response.status_code == 200
    assert "草稿" in response.text


def test_edit_post(server):
    author, _ = _admin_and_author(server)
    post_id = create_post(author, "Edit Me", content="original")
    response = author.post(f"/posts/{post_id}", data={"title": "Edit Me", "content": "updated", "action": "save"})
    assert response.status_code == 303
    response = author.get(f"/posts/{post_id}/edit")
    assert "updated" in response.text


def test_delete_post(server):
    author, _ = _admin_and_author(server)
    post_id = create_post(author, "Delete Me")
    assert author.post(f"/posts/{post_id}/delete").status_code == 303
    assert author.get(f"/posts/{post_id}/edit").status_code == 404


def test_slug_generated_and_unique(server):
    author, _ = _admin_and_author(server)
    first = create_post(author, "Same Title")
    second = create_post(author, "Same Title")
    slug_one = get_post_slug(first)
    slug_two = get_post_slug(second)
    assert slug_one == "same-title"
    assert slug_two == "same-title-2"


def test_publish_and_unpublish(server):
    author, admin = _admin_and_author(server)
    post_id = create_post(author, "Publish Flow")
    publish_post(author, admin, post_id)
    slug = get_post_slug(post_id)
    assert httpx.get(f"{server}/posts/{slug}").status_code == 200

    assert admin.post(f"/admin/posts/{post_id}/unpublish").status_code in (200, 303)
    assert httpx.get(f"{server}/posts/{slug}").status_code == 404


def test_draft_not_accessible_via_public_route(server):
    author, _ = _admin_and_author(server)
    post_id = create_post(author, "Hidden Draft")
    slug = get_post_slug(post_id)
    response = httpx.get(f"{server}/posts/{slug}")
    assert response.status_code == 404


def test_submit_workflow(server):
    author, admin = _admin_and_author(server)
    post_id = create_post(author, "Submit Flow")
    assert author.post(f"/posts/{post_id}/submit").status_code == 303
    assert "待审核" in author.get(f"/posts/{post_id}/edit").text
    assert admin.post(f"/admin/posts/{post_id}/publish").status_code in (200, 303)
    slug = get_post_slug(post_id)
    assert httpx.get(f"{server}/posts/{slug}").status_code == 200


def test_other_user_cannot_modify_post(server):
    author, admin = _admin_and_author(server)
    post_id = create_post(author, "Owned Post")

    _, intruder = new_user_client(server, prefix="intruder")
    assert intruder.get(f"/posts/{post_id}/edit").status_code == 404
    assert intruder.post(f"/posts/{post_id}", data={"title": "Hacked", "content": "x"}).status_code == 404
    assert intruder.post(f"/posts/{post_id}/delete").status_code == 404
    assert intruder.post(f"/posts/{post_id}/submit").status_code == 404


def test_home_only_lists_published(server):
    author, admin = _admin_and_author(server)
    create_post(author, "Not Listed Yet")
    response = httpx.get(f"{server}/")
    assert "Not Listed Yet" not in response.text

    post_id = create_post(author, "Listed Post")
    publish_post(author, admin, post_id)
    response = httpx.get(f"{server}/")
    assert "Listed Post" in response.text

