# plan.md

## 任务列表

- [x] 初始化项目脚手架
- [x] 创建 `AGENTS.md` 与 `.gitignore`
- [x] 建立首次知识索引（Markdown fallback）
- [ ] 实现 todo 核心逻辑
- [ ] 补充测试

## 当前 Agent State

IMPLEMENTING

## Before Snapshot

commit hash:   <当前提交哈希>
branch:        feature/todo-core
modified files: src/todo.py
risk level:    L2

## 模糊点与待确认项

- 无

## Vector Backend Status

Backend: Markdown
Status:  degraded
Environment: 无可用 MCP / Python 环境
Index: docs 摘要（folder_summary / file_summary）
Initialization: <timestamp>
Commit: <git commit hash>

## Acceptance Criteria

- [ ] `add` 命令能新增一条待办
- [ ] `list` 命令能列出全部待办
- [ ] `done` 命令能标记完成
