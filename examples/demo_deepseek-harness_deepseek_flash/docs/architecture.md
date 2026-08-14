# 架构文档 — Mini Blog / LAN Content Platform

## 1. 项目定位

轻量级局域网多人内容平台。用于演示 **AI Software Engineering Workflow / Agent Engineering Workflow**：SSR + Progressive Enhancement，无 React / Vue / Next.js / Vite / Webpack 等重型前端工程链。

技术栈：**Python 3.11+ / FastAPI / Jinja2 / SQLAlchemy 2.0 / SQLite / Pydantic / Session Cookie；Tailwind CSS / HTMX / Alpine.js / Lucide / marked.js；pytest / HTTPX**。

## 2. 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│ Routes（HTTP 层）  auth / public / posts / comments / admin   │
│   - 参数解析、依赖注入、模板渲染、重定向、HTMX 片段           │
├─────────────────────────────────────────────────────────────┤
│ Services（业务逻辑层） auth / post / comment                  │
│   - 注册登录、状态机转换、权限规则、Slug 生成                 │
├─────────────────────────────────────────────────────────────┤
│ Repositories（数据访问层） user / post / comment              │
│   - 对 Session 的查询 / 写入封装                             │
├─────────────────────────────────────────────────────────────┤
│ Models（数据模型）  User / Post / Comment                    │
├─────────────────────────────────────────────────────────────┤
│ db.py（engine / session / Base） → SQLite                    │
└─────────────────────────────────────────────────────────────┘
```

依赖方向自上而下：Routes → Services → Repositories → Models。跨层横向依赖（如 Routes 直接读取 Repositories）在简单只读场景允许。

## 3. 数据模型

| 模型 | 关键字段 | 说明 |
| --- | --- | --- |
| User | username(唯一)、password_hash、display_name、avatar、role、is_active | 角色：`user` / `admin` |
| Post | author_id、title、slug(唯一)、content(Markdown)、status、published_at | 状态：draft / submitted / published / rejected |
| Comment | post_id、author_id、content、is_deleted | 软删除：删除后从所有列表隐藏 |

关系：`User 1—N Post`、`User 1—N Comment`、`Post 1—N Comment`（Post 删除级联删除其评论）。

## 4. 权限模型

| Action | Guest | User | Admin |
| --- | --- | --- | --- |
| 浏览 / 阅读已发布文章 | ✅ | ✅ | ✅ |
| 注册 / 登录 | ✅ | ✅ | ✅ |
| 发表评论 / 删除自己的评论 | ❌ | ✅ | ✅ |
| 创建 / 编辑 / 删除自己的文章 | ❌ | ✅ | ✅ |
| 提交审核自己的文章 | ❌ | ✅ | ✅ |
| 发布自己的文章 | ❌ | configurable（`ALLOW_USER_PUBLISH`） | ✅ |
| 管理全部文章 / 评论 / 用户 | ❌ | ❌ | ✅ |

服务端校验：登录态经 Session 中间件 + `get_current_user` 依赖解析；归属校验在 service 层（`can_manage` / `can_delete`）；管理员操作经 `require_admin` 依赖（403）。

## 5. 路由概览

- 公开：`GET /`、`GET /posts/{slug}`、`GET /health`
- 认证：`GET|POST /login`、`GET|POST /register`、`POST /logout`
- 用户内容：`GET /posts/mine`、`GET /posts/new`、`POST /posts`、`GET /posts/{id}/edit`、`POST /posts/{id}`、`POST /posts/{id}/submit`、`POST /posts/{id}/delete`
- 评论：`POST /posts/{slug}/comments`、`POST /comments/{id}/delete`
- 管理：`GET /admin`、`GET|POST /admin/posts[...]`、`GET|POST /admin/comments[...]`、`GET|POST /admin/users[...]`

HTMX 请求（`hx-request: true`）返回 HTML 片段：评论异步追加、文章行局部刷新、删除行移除。

## 6. 关键设计决策（详见 decision.md）

- 密码哈希：标准库 PBKDF2-HMAC-SHA256（600k 迭代、每用户盐、`compare_digest`）。
- 会话：Starlette SessionMiddleware（itsdangerous 签名），`SECRET_KEY` 为必填环境变量；Session 仅存 `user_id`，权限每次请求从 DB 重新校验。
- 文章状态机：`draft|rejected → submitted → published`，`published → draft`；非法转换在 service 层拒绝。
- 前端无构建链：Tailwind Play CDN + HTMX / Alpine.js / Lucide / marked.js / DOMPurify（CDN）；Markdown 输出经 DOMPurify 消毒。
- Slug：`slugify(title)` 自动生成，冲突时追加 `-2`、`-3`…；公开路由仅放行 `published` 状态。

## 7. 目录结构

完整结构见 `tree.md`。

## 8. 一致性要求

- `plan.md`：进度与状态标记（Agent State / Before Snapshot / Vector Backend Status）。
- `tree.md`：文件增删或移动立即更新。
- `decision.md`：技术方案 / 依赖 / 架构 / 数据结构变更时追加。
- `AGENTS.md`：AI 开发规范（继承 Base Engineering Protocol v2.2）。
