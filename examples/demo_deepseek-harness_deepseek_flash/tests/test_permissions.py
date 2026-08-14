"""Permission tests: cross-user isolation and role-based access."""

from app import repositories as repo
from app.models import STATUS_PUBLISHED
from tests.conftest import make_published_post, register_and_login


def test_user_a_cannot_modify_user_b_post(alice_client, bob_client, db, author):
    # Carol (db-level author) owns the post; Alice must not manage it.
    post = make_published_post(db, author, "Carol's Post")

    assert alice_client.get(f"/posts/{post.id}/edit").status_code == 403
    assert (
        alice_client.post(
            f"/posts/{post.id}",
            data={"title": "Hijacked", "content": "x", "action": "save"},
            follow_redirects=False,
        ).status_code
        == 403
    )
    assert alice_client.post(f"/posts/{post.id}/delete", follow_redirects=False).status_code == 403

    assert repo.post.get_by_id(db, post.id).author.username == "carol"


def test_guest_cannot_access_authenticated_routes(client, db):
    for path in ("/posts/new", "/posts/mine"):
        resp = client.get(path, follow_redirects=False)
        assert resp.status_code == 303
        assert resp.headers["location"].startswith("/login")


def test_guest_can_browse_public_routes(client, db, author):
    post = make_published_post(db, author, "Public")
    assert client.get("/").status_code == 200
    assert client.get(f"/posts/{post.slug}").status_code == 200
    assert client.get("/health").status_code == 200


def test_non_admin_cannot_access_admin_pages(alice_client, db):
    for path in ("/admin", "/admin/posts", "/admin/comments", "/admin/users"):
        assert alice_client.get(path).status_code == 403


def test_non_admin_cannot_run_admin_actions(alice_client, db, author):
    post = make_published_post(db, author, "Guarded")
    assert alice_client.post(f"/admin/posts/{post.id}/publish", follow_redirects=False).status_code == 403
    assert alice_client.post(f"/admin/posts/{post.id}/delete", follow_redirects=False).status_code == 403


def test_guest_cannot_run_admin_actions(client, db, author):
    post = make_published_post(db, author, "Guarded")
    resp = client.post(f"/admin/posts/{post.id}/publish", follow_redirects=False)
    assert resp.status_code == 303
    assert resp.headers["location"].startswith("/login")


def test_draft_never_reachable_via_public_route(alice_client, db):
    resp = alice_client.post(
        "/posts",
        data={"title": "Hidden Draft", "content": "secret", "action": "save"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    post = repo.post.list_all(db)[0]
    assert post.status != STATUS_PUBLISHED
    assert alice_client.get(f"/posts/{post.slug}").status_code == 404
    assert "Hidden Draft" not in alice_client.get("/").text


def test_admin_can_manage_any_post(admin_client, db, fresh_session, author):
    post = make_published_post(db, author, "Admin's Domain")
    post_id = post.id
    assert admin_client.get(f"/posts/{post_id}/edit").status_code == 200
    resp = admin_client.post(
        f"/posts/{post_id}",
        data={"title": "Edited By Admin", "content": "ok", "action": "save"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert repo.post.get_by_id(fresh_session, post_id).title == "Edited By Admin"
