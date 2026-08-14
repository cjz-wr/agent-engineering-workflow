# AGENTS.md — Mini Blog / LAN Content Platform

## 项目定位

轻量级局域网多人内容平台（FastAPI + Jinja2 + SQLite + HTMX + Alpine.js + Tailwind CSS），
用于演示 AI Software Engineering Workflow 的完整应用过程。唯一需求来源为根目录 `readme.md`。

## 技术栈与常用命令

- 后端：Python 3.11+ / FastAPI / SQLAlchemy 2.0 / SQLite / Jinja2 / Pydantic
- 前端：Tailwind CSS (CDN) / HTMX / Alpine.js / Lucide Icons / marked.js（无重型构建链）
- 运行：`uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
- 测试：`pytest`
- 语法检查：`python -m compileall app tests scripts`
- 创建管理员：`python scripts/create_admin.py <username>`

## 工程规范

- 遵循 Base Engineering Protocol（由 project-bootstrap-workflow Skill 承载）。
- 提交使用 Conventional Commits（feat / fix / docs / refactor / test / chore）。
- 功能开发 MUST 在 `feature/<功能简称>` 分支上进行，按逻辑单元小步提交。
- 核心业务逻辑 MUST 有自动化测试覆盖。
- 每个逻辑单元完成后同步更新 `plan.md`、`tree.md` 与 `docs/knowledge/` 知识索引。
- 代码发生重大结构变化时同步更新 `docs/` 与 `decision.md`。

## 项目约定

- 数据访问：`app/models`（模型）+ `app/repositories`（仓储）
- 业务逻辑：`app/services`
- HTTP 路由：`app/routes`（auth / public / posts / comments / admin）
- 页面模板：`app/templates`；静态资源：`app/static`
- 配置：`.env`（不入库），模板见 `.env.example`，禁止硬编码密钥
- 文章状态流转：`draft → submitted → published / rejected`
  - 作者：创建 / 编辑 / 提交 / 删除自己的文章
  - 管理员：发布 / 驳回 / 取消发布 / 删除任意文章、管理评论与用户

## 禁止事项

- 不得臆造 `readme.md` 中不存在的需求。
- 不得修改 `readme.md` 或删除用户提供的源材料。
- 不得硬编码密钥、密码、Token；`.env` 不得提交到 Git。
- 不得执行破坏性 Git 操作（`reset --hard` / force push / 非必要 rebase）。
- 不引入无必要依赖；新增依赖须记录名称、版本、用途与理由。

