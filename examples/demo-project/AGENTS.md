# AGENTS.md

## 技术栈与命令

- 语言：Python 3
- 运行：`python main.py`
- 测试：`python -m pytest`（如启用）

## AI 行为约束

- 遵循 `project-bootstrap-workflow` / `feature-change-workflow` Skill。
- 修改前执行 `git status`、`git diff`。
- 使用 Conventional Commits。
- 不得修改环境变量、不得提交敏感信息。
- 不得执行破坏性 Git 操作（`reset --hard` / `push --force` / 非必要 `rebase`）。

## 项目约定

- 命名：小写下划线（snake_case）。
- 目录：源码放 `src/`，测试放 `tests/`。
