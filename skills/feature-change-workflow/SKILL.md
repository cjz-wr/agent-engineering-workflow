---
name: feature-change-workflow
description: >
  Modify an existing software project using the Feature Change Workflow.
  Use when implementing a feature, fixing a bug, refactoring code, changing behavior,
  or making an incremental modification to an existing codebase.
version: "2.2.0"
license: MIT
metadata:
  author: your-name-or-org
  tags:
    - feature
    - bugfix
    - refactor
    - change
    - impact-analysis
---

# Feature Change Workflow

> v2.2.0 — 已有项目修改 Skill。是 Base Engineering Protocol 之上的「差异层」，
> 不是另一份完整协议。完整 Feature-specific 规则见 [`references/feature-change.md`](references/feature-change.md)。

## 1. Role

严格遵循流程的项目修改 Agent，依据用户功能需求，对已有项目进行规划、实施与验证。

需求来源 = 用户功能需求 + `readme.md` + `AGENTS.md` + 现有项目行为。`readme.md` **不是**唯一需求来源。

## 2. When to Use

- feature request（功能需求）
- bug fix（缺陷修复）
- refactor（重构）
- behavior change（行为变更）
- existing project modification（已有项目修改）

## 3. Base Protocol Reference

本 Skill 使用共享的 v2.2 Base Engineering Protocol，定义于：

[`../project-bootstrap-workflow/references/base-protocol.md`](../project-bootstrap-workflow/references/base-protocol.md)

本 Skill 只定义「已有项目修改」与 Bootstrap 不同的行为。以下能力直接遵循 Base Protocol，本文 MUST NOT 重复展开：

- Git Workflow（Conventional Commits、破坏性操作）
- Agent State（状态机与状态转换）
- Risk Control（Risk Level、Before Snapshot）
- Decision Log
- Knowledge System / Vector Backend
- Code Graph（含 Impact Primitives）
- Navigation（Progressive Discovery）
- Token Efficiency
- Validation Protocol
- Delivery Standards

## 4. Core Rules

Agent MUST：

- 修改前执行 `git status`、`git diff`，区分用户已有修改 / 当前任务修改 / 冲突。
- 在 `feature/<功能简称>` 分支开发，不得直接修改 `main` / `master` / `develop`。
- 按逻辑单元：edit → validate → knowledge sync → update plan → commit。
- L2 及以上修改 MUST 执行影响分析。
- 建立 Acceptance Criteria 并在 Finalize 逐项验证。

Agent MUST NOT：

- 自动提交或覆盖用户已有修改。
- 冲突时自行处理（MUST 停止并提示用户处理）。
- 修改与任务无关的模块 / 数据库 / API / CI/CD / 密钥配置。
- 臆造需求或修改需求语义。

## 5. Workflow Summary

```
INIT → ANALYZE → PLAN_READY → PREPARE → IMPLEMENTING → VERIFYING → REVIEW → COMMITTING → DONE
```

| Phase | 说明 |
| --- | --- |
| Analyze | 读取需求与 `AGENTS.md`，拆分任务，建立 `plan.md` 与 Acceptance Criteria，评估风险 |
| Prepare | 工作区保护检查、创建 feature 分支、Before Snapshot、检查已有 Vector Backend |
| Implement | 按逻辑单元修改、验证、增量同步、更新 `plan.md`、小步提交 |
| Validate | Base Validation 流水线 + Acceptance Criteria 逐项检查 |
| Review | `git diff` 审查、敏感信息检查、按影响范围同步文档、提交 |
| Finalize | Acceptance 结果记录、文档同步、交付报告、状态置 `DONE` |

## 6. Protocol References

- 完整 Feature-specific 规则：[`references/feature-change.md`](references/feature-change.md)
- 完整共享基础协议：[`../project-bootstrap-workflow/references/base-protocol.md`](../project-bootstrap-workflow/references/base-protocol.md)
