# 开发日志 — Mini Blog / LAN Content Platform

> 记录按 Base Engineering Protocol v2.2 执行的本项目开发过程。Git 提交历史为权威记录，本文档为演进说明。

## Phase 1 — Requirement Analysis

- 完整解析 `readme.md`：目标（局域网多人内容平台 + AI 工程工作流演示）、技术栈、功能模块（认证 / 文章 / 公开内容 / 评论 / 动态 UI / Markdown 编辑器）、权限矩阵、路由表、测试要求、配置要求、非目标。
- 初始化 `plan.md`，状态 `PLAN_READY`。
- 提交：`docs: add initial plan based on readme analysis`

## Phase 2 — Project Bootstrap

- 创建目录结构（`app/` 分层、`tests/`、`docs/`、`data/`）、入口与配置文件（`pyproject.toml`、`.env.example`、`.gitignore`）。
- 创建 `AGENTS.md`（开发规范，继承 Base Protocol 约束）。
- `git init`；环境：Python 3.11.9（D:\python11）venv，安装依赖（fastapi、uvicorn、jinja2、sqlalchemy、pydantic-settings、python-multipart、itsdangerous；dev：pytest、httpx）。
- 知识索引：MCP Vector Backend 不可用；按最小依赖原则未安装 Python 向量后端，采用 Markdown fallback（状态 degraded，记录于 `plan.md` / `decision.md`）。
- 提交：`chore: initial commit with project scaffold and gitignore`

## Phase 3 — Incremental Development

按逻辑单元开发，每单元验证后提交（详见 Git 提交记录）：

1. **DB 层**：`config.py` / `db.py` / models（User / Post / Comment）/ repositories。
2. **认证**：`security.py`（PBKDF2）、`services/auth.py`、`dependencies.py`（get_current_user / require_login / require_admin / flash）、`routes/auth.py`、登录注册模板。
3. **文章**：`services/post.py`（状态机 / Slug / 权限）、`routes/posts.py`、编辑器与「我的文章」模板、Markdown 实时预览（marked.js + DOMPurify）。
4. **公开页面**：首页文章卡片、文章详情（阅读进度 / 代码复制 / 返回顶部）、`/health`。
5. **评论**：`services/comment.py`、`routes/comments.py`、HTMX 异步提交（OOB 表单重置）与删除。
6. **管理后台**：Dashboard 统计、文章管理（发布 / 驳回 / 取消发布 / 删除，HTMX 行刷新）、评论管理、用户管理（停用 / 角色）。
7. **动态 UI**：Tailwind CDN 设计系统、HTMX 交互、Alpine.js 编辑器状态控制。

## 测试

- `tests/test_auth.py`：注册成功 / 重复用户名 / 登录成功 / 错误密码 / 注销 / 未登录访问受保护页面 / 密码不落明文。
- `tests/test_posts.py`：CRUD / 默认 draft / slug 生成与唯一性 / 提交审核 / 重复提交拦截 / 默认不可自助发布 / 管理员发布 / 取消发布 / 删除 / 草稿与待审核不可经公开路由访问 / 他人不可改删。
- `tests/test_comments.py`：登录可评论 / 游客不可评论 / 关联正确 / 仅可删自己的 / 管理员可删任意 / HTMX 片段 / 缺失文章 404。
- `tests/test_permissions.py`：用户 A 不可改用户 B 文章 / 游客不可访问受保护路由 / 游客可访问公开路由 / 非管理员不可进后台 / 非管理员不可执行后台动作 / 草稿不出现在首页。
- `tests/test_routes.py`：首页仅发布文章 / 详情页 / 健康检查 / 登录注册页 / 后台 Dashboard / 后台文章与评论管理 / 用户管理 / HTMX 行片段 / 我的文章页。

## Phase 4 — Verification

- 全量测试通过；模板 / 路由 / 服务端渲染冒烟验证；`plan.md` / `tree.md` / `AGENTS.md` / `decision.md` 同步至最终状态；最终提交并输出交付报告。

## 演进备注

- `readme.md` 结构树中的 `mini-blog/` 即本项目根目录（见 `decision.md`）。
- 路由表之外新增 `GET /posts/mine` 与用户管理动作端点（见 `decision.md`）。
- 迭代：首个注册用户自动成为管理员（fresh 数据库引导，见 `decision.md`）；新增 `promote_admin.py` / `promote_admin.bat` 一键提升脚本（幂等）。
- 后续演示任务（Phase 2/3/4 场景）可基于本代码库继续演进：草稿预览、定时发布、跨模块状态机变更等。
