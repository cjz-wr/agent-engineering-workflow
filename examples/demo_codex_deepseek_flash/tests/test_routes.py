"""Route-level behavior tests."""

import httpx

from .conftest import create_post, get_post_slug, new_user_client, publish_post


def test_health(client: httpx.Client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_login_and_register_pages(client: httpx.Client):
    assert client.get("/login").status_code == 200
    assert "登录" in client.get("/login").text
    assert client.get("/register").status_code == 200
    assert "注册" in client.get("/register").text


def test_home_lists_published_posts(server):
    _, author = new_user_client(server, prefix="home_author")
    _, admin = new_user_client(server, prefix="home_admin", role="admin")
    post_id = create_post(author, "Home Featured", content="# Markdown\n\n**bold**")
    publish_post(author, admin, post_id)

    response = httpx.get(f"{server}/")
    assert response.status_code == 200
    assert "Home Featured" in response.text


def test_published_post_detail_renders_markdown(server):
    _, author = new_user_client(server, prefix="md_author")
    _, admin = new_user_client(server, prefix="md_admin", role="admin")
    post_id = create_post(author, "Markdown Post", content="# Heading\n\n**bold** text")
    publish_post(author, admin, post_id)
    slug = get_post_slug(post_id)

    response = httpx.get(f"{server}/posts/{slug}")
    assert response.status_code == 200
    assert "<h1>Heading</h1>" in response.text
    assert "<strong>bold</strong>" in response.text


def test_unknown_post_returns_404(client: httpx.Client):
    response = client.get("/posts/does-not-exist", headers={"accept": "text/html"})
    assert response.status_code == 404
    assert "页面不存在" in response.text

