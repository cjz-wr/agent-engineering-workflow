# Architecture

> v2.2.0 — 说明文档，不改变协议。

## Overview

```
project-bootstrap-workflow/SKILL.md        （新项目入口，精简）
        ↓
Base Engineering Protocol                  （references/base-protocol.md，唯一协议来源）
        ↑
        │ inherited by reference
feature-change-workflow/SKILL.md           （已有项目修改入口，精简）
        ↓
Feature-specific Layer                     （references/feature-change.md，差异层）
```

## 协作方式

1. `project-bootstrap-workflow` 承载 **Base Engineering Protocol**（`references/base-protocol.md`），完整定义：
   - Git Workflow
   - Agent State
   - Risk Control
   - Knowledge System / Vector Backend
   - Code Graph
   - Navigation
   - Validation
   - Token Efficiency
   - Delivery

2. `feature-change-workflow` 的 `SKILL.md` 是精简入口，通过相对路径引用 Base Protocol：

   ```
   ../project-bootstrap-workflow/references/base-protocol.md
   ```

   其 `references/feature-change.md` 只定义「已有项目修改」与 Bootstrap 不同的行为：
   - 需求来源（User Request + readme + AGENTS + 现有行为）
   - Existing Workspace Safety
   - Feature 分支
   - Feature-specific Impact Analysis
   - Acceptance Criteria
   - 按影响范围更新文档
   - 交付报告追加 Acceptance Criteria 结果

## 设计原则

- **单一协议来源**：Base Protocol 只定义一次，避免 `Base Protocol A` / `Base Protocol B` 版本漂移。
- **差异层继承**：Feature Skill 只写差异，不复制完整 Base Protocol。
- **版本统一**：所有 SKILL.md 与文档统一 `v2.2.0`。
