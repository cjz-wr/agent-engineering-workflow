# Protocol Overview

> v2.2.0 — 简要说明，不改变协议。完整规则见 `skills/project-bootstrap-workflow/references/base-protocol.md`。

## Git

- 修改前 `git status` / `git diff`。
- 功能开发在 `feature/<功能简称>` 分支。
- Conventional Commits（`feat` / `fix` / `docs` / `refactor` / `test` / `chore`）。
- 禁止：一次性提交全部代码、提交无法构建的代码、提交敏感信息、`reset --hard`、`push --force`、非必要 `rebase`。

## State

```
INIT → ANALYZE → PLAN_READY → PREPARE → IMPLEMENTING → VERIFYING → REVIEW → COMMITTING → DONE
```

异常状态：`WAIT_USER`、`FAILED`。

## Risk

- `L0` 文档/注释/格式；`L1` 单文件；`L2` 模块级（MUST 影响分析）；`L3` 跨模块（MUST Code Graph impact）；`L4` 数据库/API/架构（MUST 用户确认 + rollback + migration）。
- 修改前 MUST 记录 Before Snapshot。

## Knowledge

- `folder_summary` / `file_summary` 索引，增量同步。
- 知识查询优先级：P1 本地源码 + Code Graph → P2 知识索引 → P3 已加载上下文 → P4 外部搜索。
- Progressive Discovery：summary → candidate → details → source。

## Vector

- 三级 Backend：MCP Vector Backend → Python Local Vector Backend → Markdown fallback。
- 生命周期：Detection → Selection → Initialization → Full Index → Incremental Sync → Health Check → Fallback。
- 已有知识库优先复用，MUST NOT 覆盖。

## Code Graph

- 节点：File / Module / Class / Function / Interface。
- 关系：IMPORTS / CALLS / DEFINES / DEPENDS_ON / INHERITS / IMPLEMENTS。
- 构建降级：AST / Compiler API → LSP → Static Analysis → Manual Summary。
- Impact Primitives：callers / callees / deps / impact / flow / neighbors / Blast Radius。

## Navigation

- L1（`tree.md` + `folder_summary`）→ L2（`file_summary`）→ L3（源码）。
- 例外：用户已提供明确文件 / 类 / 函数 / 行号，可直接进入 L3。

## Validation

- 流水线：syntax → type check → lint → unit test → build。
- Testing Strategy：核心逻辑 / API / 数据转换 / 算法 MUST 新增或更新测试；文档 / 样式 / 重命名 MAY 不增加。
- 提交前自检清单。
