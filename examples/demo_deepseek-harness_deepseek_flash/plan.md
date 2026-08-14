# plan.md — Mini Blog / LAN Content Platform

> 依据 `project-bootstrap-workflow` Skill v2.2.0（Base Engineering Protocol v2.2）维护。
> 唯一需求来源：`readme.md`。Agent MUST NOT 臆造需求。

## 任务列表

### Phase 1 — Requirement Analysis（需求分析）

- [x] 完整读取并解析 `readme.md`，提炼目标、技术栈、功能模块与约束
- [x] 初始化 `plan.md`（本文件）

### Phase 2 — Project Bootstrap（项目脚手架）

- [x] 创建基础目录结构与入口文件
- [x] 创建 `AGENTS.md`（AI 开发规范）
- [x] 创建 `.gitignore`、`.env.example`、`pyproject.toml`
- [x] `git init` 并完成初始提交
- [x] 建立首次知识索引（Vector Backend 检测与降级：Markdown fallback，状态 degraded）

### Phase 3 — Incremental Development（增量开发）

- [x] DB 层：`config.py` / `db.py` / models（User / Post / Comment）/ repositories
- [x] 认证：注册 / 登录 / 注销 / Session Cookie / 密码哈希 / 权限
- [x] 文章：CRUD / Slug / 状态机（draft → submitted → published / rejected）/ 归属校验
- [x] 公开页面：文章列表 / 详情 / Markdown 渲染 / 健康检查
- [x] 评论：发表 / 删除 / 权限（HTMX 异步）
- [x] 管理后台：Dashboard / 文章管理 / 评论管理 / 用户管理
- [x] 动态 UI：Tailwind / HTMX / Alpine.js / Markdown 编辑器与实时预览

### 测试

- [x] `tests/test_auth.py`
- [x] `tests/test_posts.py`
- [x] `tests/test_comments.py`
- [x] `tests/test_permissions.py`
- [x] `tests/test_routes.py`

### 文档

- [x] `docs/architecture.md`
- [x] `docs/authentication.md`
- [x] `docs/content-workflow.md`
- [x] `docs/development-log.md`

### Phase 4 — Verification（验证与交付）

- [x] 完整验证流水线（syntax → test → build：pytest 44 passed；uvicorn 实机启动 /health 200；全页面 + HTMX 片段冒烟通过）
- [x] 全部测试通过
- [x] 同步 `plan.md` / `tree.md` / `AGENTS.md` / `decision.md` 与 `readme.md` 一致性
- [x] 最终提交并输出交付报告

## 当前 Agent State

`DONE`

## Before Snapshot

commit hash:   `59798d9`（最终同步前的 HEAD）
branch:        `main`
modified files: `plan.md`、`tree.md`（最终状态同步）
risk level:    `L0`

## 模糊点与待确认项

- [x] 任务范围确认：按 `readme.md` 从零实现整个项目（用户已确认）。
- [x] 「Publish own post: configurable」：实现为环境变量 `ALLOW_USER_PUBLISH`（默认 false，仅管理员发布；true 时作者可发布自己的文章），见 `decision.md`。
- [x] 功能开发分支合并策略：本项目为演示型 Bootstrap，采用「每个 feature 逻辑单元独立提交到 main」的方式执行（功能代码均以独立 Conventional Commit 提交，未使用长期 feature 分支）。

## Vector Backend Status

Backend: `Markdown`（markdown-fallback）
Status:  `degraded`
Environment: Python 3.11.9（D:\python11）；无 MCP Vector Backend 可用
Index: `docs/` + `folder_summary` / `file_summary` 知识索引（Markdown 维护）
Initialization: 2026-08-13（见 `decision.md` 决策记录）
Commit: `59798d9`

Reason: 环境中无可用 MCP Vector Backend；Python 本地向量后端未安装 —— `readme.md` 未要求任何向量检索 / 知识库依赖，安装将违反协议 3.1「依赖修改规则」与 8.3.9「安装安全策略」的最小依赖原则，故降级为 Markdown fallback 并记录 degraded 状态。

Attempted:
- MCP: 当前会话无可用 MCP Vector Backend（UNAVAILABLE）
- Python: Python 3.11.9 可用，但按最小依赖原则未引入向量检索依赖

## Acceptance Criteria

- [x] 项目可安装、可启动、可通过 `uvicorn app.main:app --host 0.0.0.0 --port 8000` 运行（实机启动验证通过）
- [x] 认证 / 文章 / 评论 / 权限 / 路由 全部测试通过（44 passed）
- [x] `plan.md` / `tree.md` / `AGENTS.md` / `decision.md` 与 `readme.md` 一致
- [x] Git 提交历史清晰、可独立回溯（Conventional Commits，按逻辑单元提交）
- [x] 无敏感信息残留（`.env` 不入库，`SECRET_KEY` 通过环境变量配置）
