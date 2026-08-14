# plan.md Template

> v2.2 — 从 Base Protocol 第 2.4 节 / 第 6.2 节 / 第 8.3.11 节提取，可直接复制使用。

## 任务列表

- [ ] 任务 1
- [ ] 任务 2

## 当前 Agent State

<INIT | ANALYZE | PLAN_READY | PREPARE | IMPLEMENTING | VERIFYING | REVIEW | COMMITTING | DONE | WAIT_USER | FAILED>

## Before Snapshot

commit hash:   <当前提交哈希>
branch:        <当前分支名>
modified files: <预判将修改的文件列表>
risk level:    <L0 - L4>

## 模糊点与待确认项

- <待确认项>

## Vector Backend Status

Backend: <MCP | Python | Markdown>
Status:  <ready | degraded | failed>
Environment: <environment information>
Index: <index location or backend identifier>
Initialization: <timestamp>
Commit: <git commit hash>

## Acceptance Criteria

（Feature Change 场景由 Feature Skill 追加）

- [ ] <验收条件 1>
- [ ] <验收条件 2>
