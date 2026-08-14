# Tree — 目录结构

## 目录结构

```text
.
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── session.py
│   │   ├── auth.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── public.py
│   │   ├── posts.py
│   │   ├── comments.py
│   │   └── admin.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── 404.html
│   │   ├── auth/
│   │   ├── public/
│   │   ├── posts/
│   │   ├── components/
│   │   └── admin/
│   └── static/
│       ├── css/
│       └── js/
├── scripts/
│   └── create_admin.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_posts.py
│   ├── test_comments.py
│   ├── test_permissions.py
│   └── test_routes.py
├── docs/
│   ├── architecture.md
│   ├── authentication.md
│   ├── content-workflow.md
│   ├── development-log.md
│   └── knowledge/
│       ├── folder_summary.md
│       └── file_summary.md
├── .env.example
├── AGENTS.md
├── decision.md
├── plan.md
├── pyproject.toml
└── readme.md
```

## 记录约束

不记录以下内容：`node_modules/`、`build/`、`dist/`、`.git/`、`.venv/`、`__pycache__/`、`.pytest_cache/`、`data/` 等依赖与产物目录，以及临时 / 缓存 / 日志文件。

