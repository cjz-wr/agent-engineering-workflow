# plan.md / plan/ Template（计划文档分层模板）

> v2.3 — 计划文档拆分为「入口文件 + 章节索引 + 章节文件」。依据 Base Protocol 第 2.2 节（章节拆分约定）/ 第 2.5 节（plan 结构与标准章节）/ 第 6.2 节（Before Snapshot）/ 第 8.3.11 节（Vector Backend Status）。

## 目录结构

```text
.workflow/
├── plan.md              # 入口文件：总览 + 当前状态标记
└── plan/
    ├── index.md         # 章节索引（Agent 统一读取入口）
    ├── task-list.md     # 任务列表
    ├── agent-state.md   # Agent State 转换记录
    ├── before-snapshot.md
    ├── open-questions.md
    ├── vector-backend-status.md
    └── acceptance-criteria.md   # Feature Change 场景追加
```

## .workflow/plan.md（入口文件）

```markdown
# <项目> Plan

## 总体目标

<一句话描述开发目标>

## 当前状态

Agent State: <INIT | ANALYZE | PLAN_READY | PREPARE | IMPLEMENTING | VERIFYING | REVIEW | COMMITTING | DONE | WAIT_USER | FAILED>

> 任务清单见 [`plan/task-list.md`](plan/task-list.md)，状态转换记录见 [`plan/agent-state.md`](plan/agent-state.md)，全部章节见 [`plan/index.md`](plan/index.md)。
```

## .workflow/plan/index.md（章节索引）

```markdown
# plan 章节索引

| 章节 | 文件 | 职责 |
| --- | --- | --- |
| 任务列表 | [`task-list.md`](task-list.md) | 任务清单与进度（`- [ ]` / `- [x]`） |
| Agent State | [`agent-state.md`](agent-state.md) | 状态机与状态转换记录 |
| Before Snapshot | [`before-snapshot.md`](before-snapshot.md) | 修改前快照（commit / branch / files / risk） |
| 模糊点与待确认项 | [`open-questions.md`](open-questions.md) | 需求模糊点与待确认项 |
| Vector Backend Status | [`vector-backend-status.md`](vector-backend-status.md) | 向量检索后端配置结果 |
| Acceptance Criteria | [`acceptance-criteria.md`](acceptance-criteria.md) | 验收标准（Feature Change 场景由 Feature Skill 追加） |

> 新增 / 删除 / 重命名章节 MUST 同步更新本索引。
```

## 章节模板

### plan/task-list.md

```markdown
# 任务列表

- [ ] 任务 1
- [ ] 任务 2
```

### plan/agent-state.md

```markdown
# Agent State

Current: <INIT | ANALYZE | PLAN_READY | PREPARE | IMPLEMENTING | VERIFYING | REVIEW | COMMITTING | DONE | WAIT_USER | FAILED>

| 时间 | 状态转换 | 说明 |
| --- | --- | --- |
```

### plan/before-snapshot.md

```markdown
# Before Snapshot

commit hash:   <当前提交哈希>
branch:        <当前分支名>
modified files: <预判将修改的文件列表>
risk level:    <L0 - L4>
```

### plan/open-questions.md

```markdown
# 模糊点与待确认项

- <待确认项>
```

### plan/vector-backend-status.md

```markdown
# Vector Backend Status

Backend: <MCP | Python | Markdown>
Status:  <ready | degraded | failed>
Environment: <environment information>
Index: <index location or backend identifier>
Initialization: <timestamp>
Commit: <git commit hash>
```

### plan/acceptance-criteria.md

```markdown
# Acceptance Criteria

（Feature Change 场景由 Feature Skill 追加）

- [ ] <验收条件 1>
- [ ] <验收条件 2>
```
