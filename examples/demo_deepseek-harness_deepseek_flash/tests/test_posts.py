"""Article lifecycle tests: CRUD, slug, status workflow, ownership."""

from app import repositories as repo
from app.models import STATUS_DRAFT, STATUS_PUBLISHED, STATUS_SUBMITTED
from app.services import post as post_service
from tests.conftest import make_published_post, register_and_login


def _create_post(client, title="Hello World", content="# Hi", action="save"):
    return client.post(
        "/posts",
        data={"title": title, "content": content, "action": action},
        follow_redirects=False,
    )


def test_create_post_defaults_to_draft(alice_client, db):
    resp = _create_post(alice_client, "Hello World")
    assert resp.status_code == 303
    assert resp.headers["location"].startswith("/posts/")

    post = repo.post.list_all(db)[0]
    assert post.title == "Hello World"
    assert post.status == STATUS_DRAFT
    assert post.author.username == "alice"


def test_slug_is_generated_and_unique(alice_client, db):
    _create_post(alice_client, "Hello World")
    _create_post(alice_client, "Hello World")

    posts = repo.post.list_all(db)
    slugs = [p.slug for p in posts]
    assert "hello-world" in slugs
    assert len(slugs) == len(set(slugs)), f"slugs not unique: {slugs}"


def test_edit_post(alice_client, db):
    post_id = int(_create_post(alice_client, "Old Title").headers["location"].split("/")[2])
    resp = alice_client.post(
        f"/posts/{post_id}",
        data={"title": "New Title", "content": "Updated body", "action": "save"},
        follow_redirects=False,
    )
    assert resp.status_code == 303

    post = repo.post.get_by_id(db, post_id)
    assert post.title == "New Title"
    assert post.content == "Updated body"
    assert post.status == STATUS_DRAFT


def test_submit_post(alice_client, db):
    post_id = int(_create_post(alice_client, "Ready").headers["location"].split("/")[2])
    resp = alice_client.post(f"/posts/{post_id}/submit", follow_redirects=False)
    assert resp.status_code == 303

    post = repo.post.get_by_id(db, post_id)
    assert post.status == STATUS_SUBMITTED


def test_submit_twice_is_rejected(alice_client, db):
    post_id = int(_create_post(alice_client, "Ready").headers["location"].split("/")[2])
    alice_client.post(f"/posts/{post_id}/submit", follow_redirects=False)
    resp = alice_client.post(f"/posts/{post_id}/submit", follow_redirects=False)
    assert resp.status_code == 303  # error is surfaced as a flash, not a crash
    post = repo.post.get_by_id(db, post_id)
    assert post.status == STATUS_SUBMITTED


def test_user_cannot_publish_own_post_by_default(alice_client, db):
    # ALLOW_USER_PUBLISH is false in the test environment.
    post_id = int(_create_post(alice_client, "Mine", action="publish").headers["location"].split("/")[2])
    post = repo.post.get_by_id(db, post_id)
    assert post.status == STATUS_DRAFT


def test_admin_can_publish(admin_client, db, fresh_session, author):
    post = post_service.create_post(db, author=author, title="By Carol", content="body")
    db.commit()
    post_id = post.id

    resp = admin_client.post(f"/admin/posts/{post_id}/publish", follow_redirects=False)
    assert resp.status_code == 303

    post = repo.post.get_by_id(fresh_session, post_id)
    assert post.status == STATUS_PUBLISHED
    assert post.published_at is not None


def test_unpublish_returns_to_draft(admin_client, db, fresh_session, author):
    post = make_published_post(db, author, "Shiny")
    post_id = post.id
    admin_client.post(f"/admin/posts/{post_id}/unpublish", follow_redirects=False)

    post = repo.post.get_by_id(fresh_session, post_id)
    assert post.status == STATUS_DRAFT
    assert post.published_at is None


def test_delete_post(alice_client, db):
    post_id = int(_create_post(alice_client, "Bye").headers["location"].split("/")[2])
    resp = alice_client.post(f"/posts/{post_id}/delete", follow_redirects=False)
    assert resp.status_code == 303

    assert repo.post.get_by_id(db, post_id) is None


def test_draft_not_accessible_via_public_route(alice_client, db):
    _create_post(alice_client, "Secret Draft")
    post = repo.post.list_all(db)[0]

    resp = alice_client.get(f"/posts/{post.slug}")
    assert resp.status_code == 404


def test_submitted_not_accessible_via_public_route(alice_client, db):
    post_id = int(_create_post(alice_client, "Pending").headers["location"].split("/")[2])
    alice_client.post(f"/posts/{post_id}/submit", follow_redirects=False)
    post = repo.post.get_by_id(db, post_id)

    resp = alice_client.get(f"/posts/{post.slug}")
    assert resp.status_code == 404


def test_other_user_cannot_edit_or_delete_post(alice_client, bob_client, db):
    post_id = int(_create_post(alice_client, "Alice's Post").headers["location"].split("/")[2])

    assert bob_client.get(f"/posts/{post_id}/edit").status_code == 403
    assert (
        bob_client.post(
            f"/posts/{post_id}",
            data={"title": "Hijacked", "content": "nope", "action": "save"},
            follow_redirects=False,
        ).status_code
        == 403
    )
    assert bob_client.post(f"/posts/{post_id}/delete", follow_redirects=False).status_code == 403

    post = repo.post.get_by_id(db, post_id)
    assert post.title == "Alice's Post"
