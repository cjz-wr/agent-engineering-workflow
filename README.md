# Agent Engineering Skills

这是一个用于 AI Coding Agent 的工程工作流 Skills 仓库。

Designed for Agent Skills-compatible coding agents and tools that support the standard `SKILL.md` structure.

版本：**v2.2.0**

## Included Skills

### project-bootstrap-workflow

用于新项目。基于 `readme.md` 从零搭建项目并完成增量开发：脚手架、Git 初始化、`AGENTS.md` / `plan.md` / `tree.md` / `decision.md`、知识索引、验证与交付。

适用场景：new project、greenfield、bootstrap、scaffold、from readme。

### feature-change-workflow

用于已有项目。对已有代码库进行功能、缺陷修复、重构或行为变更，保护用户已有修改与项目边界。

适用场景：existing project、feature、bugfix、refactor、change。

## Architecture

```
Bootstrap Skill（project-bootstrap-workflow/SKILL.md）
      ↓
Base Engineering Protocol（references/base-protocol.md）
      ↑
      │ inherited by reference
Feature Change Skill（feature-change-workflow/SKILL.md）
      ↓
Feature-specific Layer（references/feature-change.md）
```

- Base Protocol 只定义一次，位于 Bootstrap Skill 的 `references/base-protocol.md`。
- Feature Change Skill 通过引用继承 Base Protocol，只定义已有项目修改的差异，不复制整份协议。

## Repository Layout

```
agent-engineering-skills/
├── README.md
├── LICENSE
├── skills/
│   ├── project-bootstrap-workflow/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── base-protocol.md
│   │       ├── plan-template.md
│   │       ├── decision-log-template.md
│   │       └── tree-template.md
│   └── feature-change-workflow/
│       ├── SKILL.md
│       └── references/
│           └── feature-change.md
├── docs/
│   ├── architecture.md
│   ├── protocol-overview.md
│   └── state-machine.md
├── examples/
│   └── demo-project/
│       ├── readme.md
│       ├── AGENTS.md
│       ├── plan.md
│       ├── tree.md
│       └── decision.md
└── scripts/
    ├── validate-skills.py
    └── install-local.sh
```

## Version

当前版本统一为：

```
v2.2.0
```

## Installation

将两个 Skill 目录复制到对应工具的 Skills 搜索路径即可。

> 不同客户端版本的 Skills 搜索路径可能不同，应以对应工具当前官方文档为准。

### Codex CLI

项目级：

```
.agents/skills/
```

用户级：

```
~/.agents/skills/
```

### Claude Code

```
.claude/skills/
```

用户级：

```
~/.claude/skills/
```

### Cursor

```
.cursor/skills/
```

用户级：

```
~/.cursor/skills/
```

### 使用安装脚本

本仓库提供本地安装脚本（不联网、不执行任何包管理器安装）：

```bash
./scripts/install-local.sh codex
./scripts/install-local.sh claude
./scripts/install-local.sh cursor
```

脚本默认安装到项目级目录；使用 `--user` 安装到用户级目录：

```bash
./scripts/install-local.sh codex --user
```

脚本在遇到同名 Skill 目录时不会静默覆盖，而是安全失败并给出提示。

## Usage Examples

Bootstrap：

```
使用 project-bootstrap-workflow，从 readme.md 创建项目。
```

Feature：

```
使用 feature-change-workflow，实现用户登录功能。
```

## Compatibility

- 本仓库面向支持标准 `SKILL.md` 结构的 Agent Skills 工具。
- 不同客户端对安装目录、Skill discovery、reference loading、permissions 的行为可能存在差异。
- 本仓库不声称对任何具体客户端的特定版本 100% 兼容。

## Validation

仓库自带校验脚本（仅使用 Python 标准库）：

```bash
python scripts/validate-skills.py
```

校验内容：目录结构、frontmatter（name / description / version / license / metadata）、name 与目录名一致、references 链接有效、版本统一、Feature Skill 未复制 Base Protocol、Markdown 基础结构。

## License

MIT。版权持有人信息请由发布者自行填写，见 `LICENSE`。
