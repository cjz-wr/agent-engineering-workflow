# Agent Engineering Workflow

[English](./README.md)

面向 AI Coding Agent 的工程化开发工作流 Skills。

**v2.2.0**

将下面这条链路组织成可安装、可复用的 Coding Agent Workflow：

```
需求 → 计划 → 代码定位 → 影响分析 → 实施 → 验证 → 知识沉淀 → Git 提交 → 交付
```

这不是一个普通 Prompt 集合，而是一套可安装的 Coding Agent Workflow Skills。

## 为什么使用

传统 Coding Agent 常见问题：

- 上下文读取过多
- 修改范围失控
- 不知道代码影响范围
- 容易覆盖用户已有修改
- 长期项目缺少知识沉淀
- 跨会话依赖聊天记忆
- 验证和交付流程不稳定

本项目通过以下机制解决：

| 机制 | 解决的问题 |
| --- | --- |
| 状态机 | 明确阶段与可恢复状态，避免流程漂移 |
| 风险控制 | L0–L4 风险分级，控制修改范围 |
| 渐进式发现 | 按需逐层定位，减少上下文读取 |
| 代码图谱 | 理解结构与影响范围 |
| 向量知识库 | 长期知识沉淀，跨会话复用 |
| Git 安全 | 保护用户已有修改，小步提交 |
| 验证 | 稳定的验证流水线 |
| 验收标准 | 交付前逐项验收 |


## 两种使用方式

本项目提供两种使用层级：

### Lightweight Prompt Edition

适合小型项目、个人项目以及希望直接复制提示词使用的场景。

位于：

`simplePrompt/`

主要文件：

- `OptimizeGeneratePromotSkill.md`
  - 用于新项目初始化与增量开发
- `OptimizeEditFunctionSkill.md`
  - 用于已有项目的功能修改、Bug 修复与局部重构

这两个提示词经过实际使用验证，流程更短、上下文开销更低，适合不需要完整 Agent Skills 基础设施的小型项目。

v2.2 在轻量提示词版的基础上增加了状态机、风险控制、代码图谱、向量知识等能力，因此功能更完整，但也需要更多上下文和更复杂的执行流程。

### Agent Skills Edition

适合中大型项目、长期维护项目以及需要持久化知识、代码图谱、状态管理和标准 Skill 安装的场景。

包括：

- `project-bootstrap-workflow`
- `feature-change-workflow`

特点：

- 标准 `SKILL.md` 结构
- 状态机
- 风险分级
- Code Graph
- Vector Backend
- Progressive Discovery
- 跨会话计划状态
- 完整验证与交付流程



## 技能选择

| Skill | 适用场景 | 输入 | 输出 |
| --- | --- | --- | --- |
| `project-bootstrap-workflow` | 新项目 | `readme.md` | 完整项目骨架与开发流程 |
| `feature-change-workflow` | 已有项目 | 用户需求 + 项目上下文 | 安全的增量修改 |

```
新项目 → project-bootstrap-workflow
已有项目修改 → feature-change-workflow
```

## 架构

两个 Skill 共享同一套基础工程协议，功能变更只增加已有项目修改的特定流程，避免维护两份重复规则。

```
        共享工程协议
             │
      ┌──────┴──────┐
      ↓             ↓
  项目引导工作流  功能变更工作流
      ↓             ↓
    新项目        已有项目
```

基础协议只定义一次，位于 `skills/project-bootstrap-workflow/references/base-protocol.md`。

## 核心能力

### 工程控制

- 代理状态机
- L0–L4 风险控制
- 修改前快照
- 决策日志

### 代码智能

- 渐进式发现
- L1/L2/L3 三级导航
- 代码图谱
- 影响范围分析

### 知识

- 向量后端
- MCP → Python → Markdown 降级方案
- 全量索引
- 增量同步
- 健康检查

### 交付

- Git 安全
- 验证流水线
- 验收标准
- 跨会话计划状态

## 知识系统

```
MCP 向量后端
    ↓
Python 本地向量后端
    ↓
Markdown 降级方案
```

- 优先复用现有后端
- 没有 MCP 时，尝试 Python 项目级隔离环境
- 最后才使用 Markdown 摘要
- 不绑定具体向量数据库产品

## 快速开始

### 新项目

```text
使用 `project-bootstrap-workflow`，根据 `readme.md` 初始化并开发新项目。
```

### 已有项目

```text
使用 `feature-change-workflow`，根据以下需求修改现有项目：
<功能需求>
```

### 修复缺陷

```text
使用 `feature-change-workflow`，根据以下问题分析并修复现有项目：
<Bug 描述>
```


## 安装

### Option A — 项目级安装

适合团队项目。克隆仓库后，将对应 Skill 目录复制到目标 Agent 的项目级 Skills 目录。

```
git clone <your-repository-url>
cd <your-repository-name>
```

### Option B — 用户级安装

适合个人在所有项目中复用。将 Skill 目录复制到目标 Agent 的用户级 Skills 目录。

### Option C — 本地安装脚本

本地安装脚本（仅本地复制，不会自动联网安装额外依赖）：

```
./scripts/install-local.sh codex
./scripts/install-local.sh claude
./scripts/install-local.sh cursor
```

安装到用户级目录：

```
./scripts/install-local.sh codex --user
```

脚本遇到同名 Skill 目录时不会静默覆盖，而是安全失败并给出提示。

> 不同客户端的 Skills 搜索路径可能不同，具体以对应工具当前官方文档为准。

## 安装后会发生什么

```
用户需求
    ↓
选择 Skill
    ↓
分析
    ↓
计划
    ↓
代码定位
    ↓
实施
    ↓
验证
    ↓
提交
    ↓
交付
```

## 示例

`examples/demo-project/` 展示一个完整示例及各文件之间的关系：

| 文件 | 职责 |
| --- | --- |
| `readme.md` | 产品需求来源 |
| `AGENTS.md` | AI 开发规范 |
| `plan.md` | 开发计划与进度 |
| `tree.md` | 目录结构说明 |
| `decision.md` | 关键工程决策日志 |

## 目录结构

```
agent-engineering-workflow/
├── README.md
├── skills/      # 两个 Workflow Skill
├── docs/        # 架构与协议说明
├── examples/    # demo-project 示例
└── scripts/     # 校验与安装脚本
```

## 兼容性

面向支持 Agent Skills 的编码智能体设计。

不同客户端及版本的发现路径与安装行为可能存在差异。
请始终以目标客户端当前的官方文档为准进行 Skill 的安装与发现。

## 开发

验证 Skill 结构：

```
python scripts/validate-skills.py
```

校验内容：Skill 结构、frontmatter、引用、版本、重复。

修改协议时建议流程：

```
修改基础协议 → 验证 → 同步两个 Skill → 更新版本
```

## 贡献

如果有更好的建议，或在使用中遇到问题，欢迎提交 [Issue](../../issues) 或 [Pull Request](../../pulls)。

## 版本

当前版本：**v2.2.0**

变更记录请查看 Git 提交历史 / 发布说明。

## 许可证

[MIT](./LICENSE)
