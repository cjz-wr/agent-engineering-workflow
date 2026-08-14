# Mini Blog / LAN Content Platform

一个基于 **FastAPI + Jinja2 + SQLite + HTMX + Alpine.js + Tailwind CSS** 构建的轻量级局域网多人内容平台。

本项目用于演示 **AI Software Engineering Workflow / Agent Engineering Workflow** 在真实项目中的完整应用过程：从空仓库开始，经过需求分析、架构设计、分阶段实现、测试、文档同步与 Git 提交，逐步构建并持续演进一个可运行的多人内容平台。

项目坚持 **Server-Side Rendering（SSR）+ Progressive Enhancement** 的设计理念，在不引入 React / Vue / Next.js / Vite / Webpack 等重型前端工程链的情况下，通过 HTMX、Alpine.js 与 Tailwind CSS 实现现代化、流畅的 Web 交互体验。

---

## ✨ Features

### 👤 Multi-user Authentication

* 用户注册
* 用户登录 / 注销
* Session Cookie 会话认证
* 密码安全哈希存储
* 用户个人资料
* 基础角色：

  * `user`
  * `admin`
* 未登录用户只能访问公开内容
* 登录用户可以创建文章、管理自己的文章并发表评论
* 管理员可以管理全部文章、用户与评论

### ✍️ Article Management

支持完整的文章生命周期：

```text
draft
  ↓
submitted
  ↓
published
```

支持：

* 创建文章
* 编辑文章
* 保存草稿
* 提交审核
* 发布文章
* 取消发布
* 删除文章
* Markdown 内容编辑
* Slug 自动生成
* Slug 唯一性校验
* 发布时间记录
* 创建时间 / 更新时间记录

作者只能修改或删除自己的文章，管理员可以管理全部文章。

### 📖 Public Content

读者可以：

* 浏览已发布文章
* 查看文章详情
* 查看作者信息
* 阅读 Markdown 渲染后的正文
* 查看文章发布时间
* 浏览评论

草稿、待审核文章和其他非公开状态文章不能通过公开路由访问。

### 💬 Comments

登录用户可以：

* 发表评论
* 查看文章评论
* 删除自己的评论

管理员可以：

* 删除任意评论
* 管理异常或违规评论

评论通过 **HTMX** 实现异步提交与局部刷新，无需重新加载整个页面。

### ⚡ Dynamic UI

前端采用轻量级现代 Web 技术：

* **Tailwind CSS**

  * 响应式布局
  * 现代化卡片
  * Hover 动效
  * 状态 Badge
  * Modal
  * Dashboard UI

* **HTMX**

  * 无刷新发布 / 取消发布
  * 无刷新删除
  * 评论异步提交
  * 局部列表刷新
  * 动态状态切换

* **Alpine.js**

  * Modal
  * Tabs
  * Dropdown
  * 编辑器状态控制
  * Markdown Preview
  * 客户端微交互

* **Lucide Icons**

  * 轻量 SVG 图标
  * 统一视觉风格

### 📝 Markdown Editor

文章编辑页面支持：

* Markdown 原文编辑
* 实时 Markdown Preview
* 左右分屏预览
* Slug 自动建议
* 发布状态显示
* 保存草稿
* 提交审核

---

## 🖥️ LAN Access

项目支持局域网访问。

启动服务器：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

服务器启动后，局域网其他设备可以通过：

```text
http://<HOST_IP>:8000
```

访问。

例如：

```text
http://192.168.1.100:8000
```

因此可以使用：

```text
电脑
手机
平板
其他局域网设备
```

共同访问同一个内容平台。

---

## 🏗️ Tech Stack

### Backend

* Python 3.11+
* FastAPI
* Jinja2
* SQLAlchemy 2.0+
* SQLite
* Pydantic

### Authentication

* Session Cookie
* Password Hashing
* Server-side Authentication

### Frontend

* Tailwind CSS
* HTMX
* Alpine.js
* Lucide Icons
* marked.js

### Testing

* pytest
* HTTPX

### Development

* Git
* Conventional Commits
* `.env` configuration

---

## 📁 Project Structure

```text
mini-blog/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   │
│   ├── repositories/
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   │
│   ├── services/
│   │   ├── auth.py
│   │   ├── post.py
│   │   └── comment.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── public.py
│   │   ├── posts.py
│   │   ├── comments.py
│   │   └── admin.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── public/
│   │   ├── posts/
│   │   ├── components/
│   │   └── admin/
│   │
│   └── static/
│       ├── css/
│       └── js/
│
├── tests/
│   ├── test_auth.py
│   ├── test_posts.py
│   ├── test_comments.py
│   ├── test_permissions.py
│   └── test_routes.py
│
├── docs/
│   ├── architecture.md
│   ├── authentication.md
│   ├── content-workflow.md
│   └── development-log.md
│
├── .env.example
├── pyproject.toml
└── README.md
```

---

## 🗃️ Core Data Model

### User

```text
User
├── id
├── username
├── password_hash
├── display_name
├── avatar
├── role
├── is_active
├── created_at
└── updated_at
```

### Post

```text
Post
├── id
├── author_id
├── title
├── slug
├── content
├── status
├── created_at
├── updated_at
└── published_at
```

### Comment

```text
Comment
├── id
├── post_id
├── author_id
├── content
├── created_at
├── updated_at
└── is_deleted
```

### Relationships

```text
User 1 ─────── N Post
User 1 ─────── N Comment
Post 1 ─────── N Comment
```

---

## 🔐 Permission Model

| Action                 | Guest |         User | Admin |
| ---------------------- | ----: | -----------: | ----: |
| Browse published posts |     ✅ |            ✅ |     ✅ |
| Read published post    |     ✅ |            ✅ |     ✅ |
| Register               |     ✅ |            ✅ |     ✅ |
| Login                  |     ✅ |            ✅ |     ✅ |
| Comment                |     ❌ |            ✅ |     ✅ |
| Create post            |     ❌ |            ✅ |     ✅ |
| Edit own post          |     ❌ |            ✅ |     ✅ |
| Delete own post        |     ❌ |            ✅ |     ✅ |
| Submit own post        |     ❌ |            ✅ |     ✅ |
| Publish own post       |     ❌ | configurable |     ✅ |
| Manage all posts       |     ❌ |            ❌ |     ✅ |
| Manage comments        |     ❌ |     own only |     ✅ |
| Manage users           |     ❌ |            ❌ |     ✅ |

---

## 🌐 Routes

### Public

| Method | Path            | Description              |
| ------ | --------------- | ------------------------ |
| `GET`  | `/`             | Published article list   |
| `GET`  | `/posts/{slug}` | Published article detail |
| `GET`  | `/health`       | Health check             |

### Authentication

| Method | Path        | Description       |
| ------ | ----------- | ----------------- |
| `GET`  | `/login`    | Login page        |
| `POST` | `/login`    | Login             |
| `GET`  | `/register` | Registration page |
| `POST` | `/register` | Registration      |
| `POST` | `/logout`   | Logout            |

### User Content

| Method | Path                 | Description        |
| ------ | -------------------- | ------------------ |
| `GET`  | `/posts/new`         | Create article     |
| `POST` | `/posts`             | Create article     |
| `GET`  | `/posts/{id}/edit`   | Edit own article   |
| `POST` | `/posts/{id}`        | Update own article |
| `POST` | `/posts/{id}/submit` | Submit article     |
| `POST` | `/posts/{id}/delete` | Delete own article |

### Comments

| Method | Path                          | Description          |
| ------ | ----------------------------- | -------------------- |
| `POST` | `/posts/{slug}/comments`      | Create comment       |
| `POST` | `/comments/{id}/delete`       | Delete own comment   |
| `POST` | `/admin/comments/{id}/delete` | Admin delete comment |

### Admin

| Method | Path                          | Description       |
| ------ | ----------------------------- | ----------------- |
| `GET`  | `/admin`                      | Admin dashboard   |
| `GET`  | `/admin/posts`                | Manage all posts  |
| `POST` | `/admin/posts/{id}/publish`   | Publish article   |
| `POST` | `/admin/posts/{id}/reject`    | Reject article    |
| `POST` | `/admin/posts/{id}/unpublish` | Unpublish article |
| `POST` | `/admin/posts/{id}/delete`    | Delete article    |
| `GET`  | `/admin/comments`             | Manage comments   |
| `GET`  | `/admin/users`                | Manage users      |

HTMX requests may return HTML fragments rather than complete pages.

---

## 🎨 UI / UX

### Public Home

```text
┌─────────────────────────────────────────────────────┐
│ Mini Blog                              Login / User │
├─────────────────────────────────────────────────────┤
│                                                     │
│                    Latest Posts                     │
│                                                     │
│  ┌────────────────┐  ┌────────────────┐            │
│  │ Article Card   │  │ Article Card   │            │
│  │                │  │                │            │
│  │ Title          │  │ Title          │            │
│  │ Author         │  │ Author         │            │
│  │ Updated        │  │ Updated        │            │
│  └────────────────┘  └────────────────┘            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Article Page

包含：

* 清晰的 Markdown 排版
* 文章标题
* 作者信息
* 发布时间
* 阅读进度条
* 代码块复制
* 返回顶部按钮
* 评论区
* 登录状态提示

### Admin Dashboard

包含：

* 文章数量
* 用户数量
* 评论数量
* 待审核文章
* 最近活动
* 文章状态统计

---

## 🧪 Testing Requirements

核心业务必须具备自动化测试。

至少覆盖：

### Authentication

* 注册成功
* 重复用户名
* 登录成功
* 错误密码
* 注销
* 未登录访问受保护页面

### Posts

* 创建文章
* 编辑文章
* 删除文章
* 默认状态为 `draft`
* 正确生成 slug
* slug 唯一性
* 发布文章
* 取消发布
* 草稿不可通过公开路由访问
* 非法用户不能修改其他用户文章

### Comments

* 登录用户可以发表评论
* 未登录用户不能发表评论
* 评论正确关联文章和用户
* 用户只能删除自己的评论
* 管理员可以删除任意评论

### Permissions

必须重点测试：

```text
User A
  ↓
不能修改
  ↓
User B 的文章
```

以及：

```text
Guest
  ↓
不能访问
  ↓
Authenticated-only routes
```

---

## ⚙️ Configuration

禁止将配置与密钥硬编码到源码中。

使用 `.env`：

```env
APP_NAME=Mini Blog
APP_HOST=0.0.0.0
APP_PORT=8000
DATABASE_URL=sqlite:///./data/blog.db
SECRET_KEY=change-me
```

提供：

```text
.env.example
```

真实 `.env` 不应提交到 Git。

---

## 🚀 Local Development

### 1. Clone

```bash
git clone <repository-url>
cd mini-blog
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Linux / macOS：

```bash
source .venv/bin/activate
```

Windows：

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

### 4. Configure Environment

```bash
cp .env.example .env
```

根据实际环境修改 `.env`。

### 5. Run Tests

```bash
pytest
```

### 6. Start Development Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 7. Open in Browser

本机：

```text
http://127.0.0.1:8000
```

局域网：

```text
http://<HOST_IP>:8000
```

---

## 🔄 Development Workflow

本项目不仅用于展示最终产品，也用于演示 **AI Coding Agent 的软件工程工作流**。

所有开发任务遵循：

```text
Requirement
    ↓
Analysis
    ↓
Impact Analysis
    ↓
Implementation Plan
    ↓
Implementation
    ↓
Testing
    ↓
Verification
    ↓
Documentation
    ↓
Git Diff Review
    ↓
Commit
```

### Development Principles

* 不直接跳过需求分析进入编码
* 修改前识别受影响文件与模块
* 优先进行小范围、可验证的修改
* 核心逻辑必须有测试
* 功能修改必须同步检查相关文档
* 不进行未经需求要求的大规模重构
* 不引入无必要依赖
* 不破坏已有功能
* 每个逻辑单元使用独立 Git Commit

---

## 🧩 Suggested Commit Structure

遵循 Conventional Commits。

示例：

```text
feat(db): initialize database models
feat(auth): add user registration and login
feat(posts): implement article CRUD
feat(posts): add article publishing workflow
feat(comments): add article comments
feat(views): integrate public article pages
style(ui): introduce tailwind-based design
feat(dynamic): add htmx interactions
test(auth): cover authentication workflow
test(posts): cover article lifecycle
test(comments): cover comment permissions
docs(architecture): document application structure
fix(posts): prevent drafts from public access
```

推荐保持较小的提交粒度，使每个 Commit 都代表一个清晰的逻辑单元。

---

## 🎯 Demo Scenarios

本项目作为 AI Engineering Workflow Demo 时，推荐使用以下演进任务进行展示。

### Phase 1 — Build From Scratch

```text
Empty Repository
    ↓
Project Initialization
    ↓
Database
    ↓
Authentication
    ↓
Post Management
    ↓
Public Pages
    ↓
Comments
    ↓
Admin Dashboard
```

### Phase 2 — Feature Evolution

示例任务：

```text
Add article preview for drafts.

Add article submission and review workflow.

Add scheduled publishing.

Add Markdown live preview.

Add admin comment moderation.

Add user profile pages.
```

### Phase 3 — Bug Fixing

示例：

```text
Draft posts are visible from a public route.

Users can modify another user's article.

Users can submit duplicate comments.

Deleted comments remain visible after HTMX updates.
```

### Phase 4 — Cross-module Change

示例：

```text
Change article publishing from:

draft → published

to:

draft → submitted → published / rejected
```

此类需求需要同时分析：

```text
Database
Model
Service
Routes
Authorization
Templates
HTMX interactions
Tests
Documentation
```

用于验证 AI Coding Agent 是否能够正确处理真实的软件变更，而不是只生成局部代码。

---

## 🚫 Non-goals

本期明确不实现：

* OAuth / 第三方登录
* 邮箱验证
* 找回密码
* 双因素认证
* 细粒度 RBAC
* 无限级评论回复
* 私信
* 图片文件上传
* 视频上传
* 站内搜索
* RSS
* 推荐算法
* WebSocket 实时通信
* CI/CD
* 自动部署
* 微服务架构
* Redis / Message Queue
* 独立 SPA 前端
* React / Vue / Next.js
* Vite / Webpack 等重型前端构建链

---

## 🔒 Security Notes

尽管这是一个轻量级局域网项目，仍需遵循基本安全要求：

* 密码不得明文存储
* Session Secret 必须通过环境变量配置
* 不得将真实密钥提交到 Git
* 用户提交内容必须进行合理校验
* 服务端必须执行权限检查
* 不能仅依赖前端隐藏按钮实现权限控制
* 草稿和待审核文章必须在服务端阻止公开访问
* 所有涉及用户资源的操作必须验证资源归属
* 管理员操作必须经过服务端角色校验

---

## 📚 Documentation

项目文档位于：

```text
docs/
├── architecture.md
├── authentication.md
├── content-workflow.md
└── development-log.md
```

代码发生重大结构变化时，应同步更新对应文档。

---

## 📌 Project Status

当前项目定位：

> **AI Engineering Workflow Demonstration Project**

重点不是构建功能无限复杂的商业 CMS，而是在一个规模适中的真实 Web 应用中验证：

* AI Agent 是否能够从零建立项目
* AI Agent 是否能够遵循既定工程规范
* AI Agent 是否能够正确分析影响范围
* AI Agent 是否能够进行跨模块修改
* AI Agent 是否能够补充和维护测试
* AI Agent 是否能够保持代码与文档同步
* AI Agent 是否能够通过 Git 形成可追踪的工程历史

---

## License

待定。