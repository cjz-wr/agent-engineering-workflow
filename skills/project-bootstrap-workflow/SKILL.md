---
name: project-bootstrap-workflow
description: >
  Bootstrap a new software project from readme.md using the project's strict engineering workflow.
  Use when starting a greenfield project, scaffolding from requirements, initializing project documents,
  Git workflow, AGENTS.md, plan.md, tree.md, knowledge indexing, validation, or delivery.
version: "2.2.0"
license: MIT
metadata:
  author: your-name-or-org
  tags:
    - bootstrap
    - scaffold
    - engineering-workflow
    - git
    - agents-md
---

# Project Bootstrap Workflow

> v2.2.0 — 新项目 Bootstrap Skill，同时是 **Base Engineering Protocol** 的宿主。
> 完整协议见 [`references/base-protocol.md`](references/base-protocol.md)。

## 1. Role

严谨的全栈开发 Agent 工作流，依据项目需求完成从脚手架搭建到交付的完整流程。

唯一需求来源：项目根目录下的 **`readme.md`**。Agent MUST NOT 臆造 `readme.md` 中不存在的需求。

## 2. When to Use

- new project（新项目）
- greenfield（从零开始）
- bootstrap / scaffold（脚手架）
- 从 `readme.md` 初始化项目
- project initialization（项目初始化）

## 3. Core Rules

Agent MUST：

- 以 `readme.md` 为唯一需求来源，不得臆造需求。
- 遵循 Git Workflow 与 Conventional Commits。
- 维护 `plan.md` 最新状态，任意时刻可中断恢复。
- 按逻辑单元小步提交，不得一次性提交全部代码。
- 按适用性执行 Validation 流水线。
- 遵循知识索引与 Vector Backend 生命周期（MCP → Python → Markdown）。

Agent MUST NOT：

- 修改与任务无关的文件。
- 删除用户提供的任何源材料（`readme.md` 等）。
- 执行破坏性 Git 操作（`reset --hard` / `push --force` / 非必要 `rebase`）。
- 修改环境变量或读取敏感信息。
- 引入无必要依赖。

## 4. Workflow Summary

```
INIT → ANALYZE → PLAN_READY → PREPARE → IMPLEMENTING → VERIFYING → REVIEW → COMMITTING → DONE
```

异常状态：`WAIT_USER`（等待用户）、`FAILED`（失败终止）。

| Phase | 状态 | 说明 |
| --- | --- | --- |
| 1. Requirement Analysis | INIT → ANALYZE → PLAN_READY | 读取并解析 `readme.md`，初始化 `plan.md` |
| 2. Project Bootstrap | PLAN_READY → PREPARE | 脚手架、`AGENTS.md`、`.gitignore`、`git init`、首次全量索引 |
| 3. Incremental Development | PREPARE → IMPLEMENTING | feature 分支、按逻辑单元开发、增量同步 |
| 4. Verification | IMPLEMENTING → VERIFYING → REVIEW → COMMITTING → DONE | 验证、同步文档、最终提交、交付报告 |

## 5. Required Documents

| 文件 | 职责 |
| --- | --- |
| `readme.md` | 产品需求来源（用户提供） |
| `AGENTS.md` | AI 开发规范 |
| `plan.md` | 开发计划、进度、Before Snapshot、状态标记 |
| `tree.md` | 目录结构说明 |
| `decision.md` | 关键工程决策日志 |

MUST NOT 使用 `prompt.md`。

## 6. Protocol References

完整协议位于 [`references/base-protocol.md`](references/base-protocol.md)，包含：

- Git Workflow（Conventional Commits、分支、破坏性操作）
- Agent State Machine（状态机与状态转换）
- Risk Control（L0–L4、Before Snapshot、Decision Log）
- Knowledge System（`folder_summary` / `file_summary`、Progressive Discovery）
- Vector Backend（MCP → Python → Markdown、Full Index、Incremental Sync、Health Check）
- Code Graph（节点/关系、Impact Primitives、构建降级）
- Navigation（L1 → L2 → L3、直接进入 L3 例外）
- Validation（syntax → type → lint → test → build）
- Token Efficiency
- Delivery Report

模板：

- [`references/plan-template.md`](references/plan-template.md)
- [`references/decision-log-template.md`](references/decision-log-template.md)
- [`references/tree-template.md`](references/tree-template.md)
