"""Comment tests: creation, association, ownership and admin deletion."""

from app import repositories as repo
from tests.conftest import make_published_post, register_and_login


def test_logged_in_user_can_comment(alice_client, db, author):
    post = make_published_post(db, author, "Commentable")
    resp = alice_client.post(
        f"/posts/{post.slug}/comments",
        data={"content": "Nice post!"},
        follow_redirects=False,
    )
    assert resp.status_code == 303

    comments = repo.comment.list_for_post(db, post.id)
    assert len(comments) == 1
    assert comments[0].content == "Nice post!"
    assert comments[0].post_id == post.id
    assert comments[0].author.username == "alice"


def test_guest_cannot_comment(client, db, author):
    post = make_published_post(db, author, "Locked")
    resp = client.post(
        f"/posts/{post.slug}/comments",
        data={"content": "hello"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert resp.headers["location"].startswith("/login")
    assert repo.comment.count(db) == 0


def test_user_can_only_delete_own_comment(alice_client, bob_client, db, fresh_session, author):
    post = make_published_post(db, author, "Mine")
    alice_client.post(f"/posts/{post.slug}/comments", data={"content": "alice says"}, follow_redirects=False)
    bob_client.post(f"/posts/{post.slug}/comments", data={"content": "bob says"}, follow_redirects=False)

    alice_comment, bob_comment = repo.comment.list_for_post(db, post.id)

    # Bob cannot delete Alice's comment.
    assert bob_client.post(f"/comments/{alice_comment.id}/delete", follow_redirects=False).status_code == 403
    assert repo.comment.get_by_id(db, alice_comment.id).is_deleted is False

    # Alice can delete her own.
    assert alice_client.post(f"/comments/{alice_comment.id}/delete", follow_redirects=False).status_code == 303
    assert repo.comment.get_by_id(fresh_session, alice_comment.id).is_deleted is True

    # Deleted comments are hidden from the list.
    visible = repo.comment.list_for_post(fresh_session, post.id)
    assert [c.id for c in visible] == [bob_comment.id]


def test_admin_can_delete_any_comment(admin_client, make_client, db, fresh_session, author):
    post = make_published_post(db, author, "Moderated")
    reporter = make_client()
    register_and_login(reporter, "reporter", "secret123", "Reporter")
    reporter.post(f"/posts/{post.slug}/comments", data={"content": "spam"}, follow_redirects=False)

    comment = repo.comment.list_for_post(db, post.id)[0]
    assert admin_client.post(f"/admin/comments/{comment.id}/delete", follow_redirects=False).status_code == 303
    assert repo.comment.get_by_id(fresh_session, comment.id).is_deleted is True


def test_htmx_comment_returns_fragment(alice_client, db, author):
    post = make_published_post(db, author, "Async")
    resp = alice_client.post(
        f"/posts/{post.slug}/comments",
        data={"content": "via htmx"},
        headers={"hx-request": "true"},
    )
    assert resp.status_code == 200
    assert "via htmx" in resp.text
    assert 'id="comment-' in resp.text
    assert "hx-swap-oob" in resp.text  # form reset fragment included


def test_comment_on_missing_post_404(alice_client, db):
    resp = alice_client.post(
        "/posts/no-such-slug/comments",
        data={"content": "hello"},
        follow_redirects=False,
    )
    assert resp.status_code == 404
