"""Route tests: pages render, admin actions work, HTMX fragments return."""

from app import repositories as repo
from app.models import STATUS_DRAFT, STATUS_PUBLISHED, STATUS_REJECTED, STATUS_SUBMITTED
from app.services import post as post_service
from tests.conftest import make_published_post, register_and_login


def test_home_lists_only_published_posts(client, db, author):
    published = make_published_post(db, author, "Published One")
    draft = post_service.create_post(db, author=author, title="Draft One", content="x")
    db.commit()

    resp = client.get("/")
    assert resp.status_code == 200
    assert "Published One" in resp.text
    assert "Draft One" not in resp.text
    assert "Published One" in resp.text


def test_post_detail_page(client, db, author):
    post = make_published_post(db, author, "Detail Page", "# Heading\n\nSome text")
    resp = client.get(f"/posts/{post.slug}")
    assert resp.status_code == 200
    assert "Detail Page" in resp.text
    assert "Carol" in resp.text  # author display name


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_login_and_register_pages_render(client):
    assert client.get("/login").status_code == 200
    assert client.get("/register").status_code == 200


def test_admin_dashboard_shows_stats(admin_client, db, author):
    make_published_post(db, author, "One")
    resp = admin_client.get("/admin")
    assert resp.status_code == 200
    assert "管理后台" in resp.text
    assert "文章总数" in resp.text


def test_admin_posts_page_and_htmx_publish(admin_client, db, fresh_session, author):
    post = post_service.create_post(db, author=author, title="To Publish", content="x")
    db.commit()
    post_id = post.id

    page = admin_client.get("/admin/posts")
    assert page.status_code == 200
    assert "To Publish" in page.text

    # HTMX publish returns the refreshed row fragment.
    resp = admin_client.post(
        f"/admin/posts/{post_id}/publish",
        headers={"hx-request": "true"},
    )
    assert resp.status_code == 200
    assert f'id="post-row-{post_id}"' in resp.text
    assert "已发布" in resp.text
    assert repo.post.get_by_id(fresh_session, post_id).status == STATUS_PUBLISHED


def test_admin_reject_and_unpublish_flow(admin_client, db, fresh_session, author):
    post = make_published_post(db, author, "Rejected Then Unpublished")
    post_id = post.id

    admin_client.post(f"/admin/posts/{post_id}/reject", follow_redirects=False)
    assert repo.post.get_by_id(fresh_session, post_id).status == STATUS_REJECTED

    admin_client.post(f"/admin/posts/{post_id}/publish", follow_redirects=False)
    assert repo.post.get_by_id(fresh_session, post_id).status == STATUS_PUBLISHED

    admin_client.post(f"/admin/posts/{post_id}/unpublish", follow_redirects=False)
    post = repo.post.get_by_id(fresh_session, post_id)
    assert post.status == STATUS_DRAFT
    assert post.published_at is None


def test_admin_comments_page(admin_client, make_client, db, author):
    post = make_published_post(db, author, "Commented")
    commenter = make_client()
    register_and_login(commenter, "commenter", "secret123", "Commenter")
    commenter.post(f"/posts/{post.slug}/comments", data={"content": "a comment"}, follow_redirects=False)

    page = admin_client.get("/admin/comments")
    assert page.status_code == 200
    assert "a comment" in page.text


def test_admin_users_page_and_actions(admin_client, make_client, db, fresh_session):
    member_client = make_client()
    register_and_login(member_client, "member", "secret123", "Member")
    user = repo.user.get_by_username(db, "member")
    user_id = user.id

    page = admin_client.get("/admin/users")
    assert page.status_code == 200
    assert "member" in page.text

    admin_client.post(f"/admin/users/{user_id}/toggle-active", follow_redirects=False)
    assert repo.user.get_by_id(fresh_session, user_id).is_active is False

    admin_client.post(f"/admin/users/{user_id}/role", data={"role": "admin"}, follow_redirects=False)
    assert repo.user.get_by_id(fresh_session, user_id).is_admin is True


def test_admin_htmx_delete_post_removes_row(admin_client, db, fresh_session, author):
    post = make_published_post(db, author, "Doomed")
    post_id = post.id
    resp = admin_client.post(f"/admin/posts/{post_id}/delete", headers={"hx-request": "true"})
    assert resp.status_code == 200
    assert repo.post.get_by_id(fresh_session, post_id) is None


def test_my_posts_page(alice_client, db):
    register_and_login(alice_client, "alice", "secret123", "Alice")
    alice_client.post(
        "/posts",
        data={"title": "Mine Only", "content": "x", "action": "save"},
        follow_redirects=False,
    )
    resp = alice_client.get("/posts/mine")
    assert resp.status_code == 200
    assert "Mine Only" in resp.text
