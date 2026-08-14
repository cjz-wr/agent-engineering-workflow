# tree.md — 目录结构说明

## 目录结构

```
.
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI 入口（中间件、静态资源、路由装配、lifespan）
│   ├── config.py          # 环境配置（pydantic-settings，读取 .env）
│   ├── db.py              # SQLAlchemy engine / session / Base / init_db
│   ├── security.py        # 密码哈希（PBKDF2-HMAC-SHA256）
│   ├── utils.py           # 通用工具（utcnow）
│   ├── dependencies.py    # FastAPI 依赖：current_user / require_login / require_admin / flash
│   ├── templating.py      # Jinja2 实例与 render / is_htmx 帮助函数
│   ├── models/            # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py        # User（username / password_hash / role / is_active）
│   │   ├── post.py        # Post（title / slug / content / status / published_at）
│   │   └── comment.py     # Comment（post_id / author_id / content / is_deleted）
│   ├── repositories/      # 数据访问层（对 Session 的查询 / 写入封装）
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── services/          # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── auth.py        # 注册 / 登录 / 会话
│   │   ├── post.py        # 文章状态机 / Slug / 权限规则
│   │   └── comment.py     # 评论创建 / 删除权限
│   ├── routes/            # HTTP 路由
│   │   ├── __init__.py
│   │   ├── auth.py        # /login /register /logout
│   │   ├── public.py      # / /posts/{slug} /health
│   │   ├── posts.py       # /posts/mine /posts/new /posts/{id}/... 文章 CRUD
│   │   ├── comments.py    # /posts/{slug}/comments /comments/{id}/delete
│   │   └── admin.py       # /admin 后台管理
│   ├── templates/         # Jinja2 模板
│   │   ├── base.html
│   │   ├── auth/          # login.html / register.html
│   │   ├── public/        # index.html / post_detail.html
│   │   ├── posts/         # editor.html（Markdown 编辑器）/ mine.html
│   │   ├── components/    # post_card / comment_form / comment_form_oob / comment_item / comment_created / admin_post_row
│   │   └── admin/         # dashboard.html / posts.html / comments.html / users.html
│   └── static/
│       ├── css/app.css    # 自定义样式（Markdown 排版 / 阅读进度 / 复制按钮）
│       └── js/app.js      # 阅读进度 / 返回顶部 / 代码块复制
├── tests/                 # pytest 测试（pytest + HTTPX TestClient）
│   ├── conftest.py        # 隔离数据库 / 多客户端 / 用户 fixtures
│   ├── test_auth.py
│   ├── test_posts.py
│   ├── test_comments.py
│   ├── test_permissions.py
│   └── test_routes.py
├── docs/                  # 项目文档
│   ├── architecture.md
│   ├── authentication.md
│   ├── content-workflow.md
│   └── development-log.md
├── data/                  # SQLite 运行时数据（.gitignore 排除，不入库）
├── promote_admin.py       # 一键提升用户为管理员（Python 脚本，幂等）
├── promote_admin.bat      # 一键提升入口（Windows 批处理）
├── AGENTS.md              # AI 开发规范
├── plan.md                # 开发计划与进度
├── tree.md                # 目录结构说明（本文件）
├── decision.md            # 关键工程决策日志
├── readme.md              # 产品需求来源（用户提供）
├── .env.example           # 环境变量示例
├── .gitignore
└── pyproject.toml         # 项目元数据与依赖
```

## 记录约束

MUST NOT 记录以下内容：

- `node_modules/`、`build/`、`dist/`、`.git/`、`.venv/` 等依赖与产物目录。
- 临时文件、缓存文件、日志文件、`data/*.db` 等运行时数据。
