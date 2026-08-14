# AGENTS.md — Mini Blog / LAN Content Platform

AI Coding Agent 的项目开发规范。依据 `project-bootstrap-workflow` Skill v2.2.0（Base Engineering Protocol v2.2）建立，并继承其全部约束。

## 项目概述

轻量级局域网多人内容平台（Mini Blog）。技术栈：**FastAPI + Jinja2 + SQLAlchemy 2.0 + SQLite + HTMX + Alpine.js + Tailwind CSS**（SSR + Progressive Enhancement，无重型前端工程链）。

唯一需求来源：项目根目录 `readme.md`。Agent MUST NOT 臆造 `readme.md` 中不存在的需求。

## 常用命令

```bash
# 安装（含开发依赖）
pip install -e ".[dev]"

# 运行测试
pytest

# 启动开发服务器
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 项目约定

- 分层：`models`（数据模型）→ `repositories`（数据访问）→ `services`（业务逻辑）→ `routes`（HTTP 路由）→ `templates` / `static`（视图）。
- 权限校验 MUST 在服务端执行（路由依赖 + service 层归属校验），不得仅依赖前端隐藏按钮。
- 所有涉及用户资源的操作 MUST 验证资源归属；管理员操作 MUST 经过角色校验（`admin`）。
- 提交信息 MUST 遵循 Conventional Commits：`<type>: <简短描述>`（`feat` / `fix` / `docs` / `refactor` / `test` / `chore`）。
- 每个逻辑单元独立提交，MUST NOT 一次性提交全部代码。
- 功能开发在 `feature/<功能简称>` 分支进行，验证通过后合并回 `main`。
- 修改前 MUST 记录 Before Snapshot 到 `plan.md`（commit hash / branch / modified files / risk level）。
- 文件增删或移动 MUST 同步更新 `tree.md`；每个逻辑单元完成后 MUST 更新 `plan.md`。
- 涉及技术方案选择、新依赖、架构调整、数据结构变化 MUST 追加 `decision.md` 决策记录。

## 禁止事项

- 不得修改或删除用户提供的 `readme.md` 等源材料。
- 不得将密钥、密码、Token 硬编码进源码或提交到 Git；真实 `.env` 不入库。
- 不得执行破坏性 Git 操作：`git reset --hard`、`git push --force`、非必要 `git rebase`。
- 不得引入无必要依赖（新增依赖 MUST 在提交信息 / `plan.md` / `decision.md` 记录名称、版本、用途与理由）。
- 不得臆造需求、不得修改与任务无关的文件、不得改动 `.env` 中已有值。

## 验证要求

提交前 MUST 通过：语法检查 → （类型检查，如适用）→ lint → 单元测试 → 构建（如适用）。

- 核心业务逻辑 / API 行为 / 数据转换 MUST 新增或更新测试（`tests/`，pytest + HTTPX）。
- 每次 `git commit` 前自检：构建通过、语法通过、`tree.md` / `plan.md` 已同步、无死代码、无敏感信息。
