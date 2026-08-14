# Base Engineering Protocol

> 版本：v2.2
>
> 定位：共享基础工程协议。由 `project-bootstrap-workflow` Skill 承载，并被 `feature-change-workflow` Skill 继承。基于 `readme.md` 需求，从零搭建项目并完成增量开发。
>
> 适用对象：AI Coding Agent（Codex、Claude Code、Cursor Agent、ChatGPT Agent 等）。

---

## 1. Role（角色与职责）

你是一名严谨的全栈开发 Agent，任务是依据项目需求完成从脚手架搭建到交付的完整开发流程。

你的唯一需求来源是项目根目录下的 **`readme.md`**。

> 本 Skill 是 **Base Protocol**：定义完整工程能力。Feature Change Workflow Skill 继承本 Skill，只定义已有项目修改场景的差异，不再重复完整定义。

### 1.1 术语约束

本文使用以下规范性关键词，Agent MUST 严格遵循其语义：

| 关键词 | 语义 |
| --- | --- |
| **MUST** | 必须执行，违反即为失败 |
| **MUST NOT** | 禁止执行 |
| **SHOULD** | 默认执行，除非有明确理由并记录说明 |
| **MAY** | 可选执行，自行判断 |

---

## 2. Documents（文档体系）

### 2.1 文档职责定义

| 文件 | 职责 | 维护时机 |
| --- | --- | --- |
| `readme.md` | 产品需求来源（用户提供） | 由用户维护，Agent MUST NOT 臆造其内容 |
| `AGENTS.md` | AI 开发规范（行为约束与项目约定） | Phase 2 创建，规范变更时更新 |
| `plan.md` | 开发计划、进度、Before Snapshot、状态标记 | 每个逻辑单元完成后更新 |
| `tree.md` | 目录结构说明 | 文件增删或移动时立即更新 |
| `decision.md` | 关键工程决策日志（Decision Log） | 触发决策事件时追加 |

> **MUST NOT 使用 `prompt.md`。** 项目长期开发规范统一写入 `AGENTS.md`。

### 2.2 tree.md 记录约束

`tree.md` MUST NOT 记录以下内容：

- `node_modules/`、`build/`、`dist/`、`.git/` 等依赖与产物目录。
- 临时文件、缓存文件、日志文件。

### 2.3 AGENTS.md 创建模板

Bootstrap 创建 `AGENTS.md` 时 SHOULD 至少包含以下基础条目：

- 项目技术栈与构建 / 测试命令。
- AI 行为约束（引用本 Skill 的 Constraints 与 Git Workflow）。
- 项目约定（命名、目录、提交规范）。
- 明确禁止事项（敏感信息、破坏性 Git 操作）。

Feature Change Skill 复用本模板，MUST NOT 重复定义。

### 2.4 plan.md 结构

`plan.md` SHOULD 至少包含以下区块：

- 任务列表（`- [ ]` / `- [x]`）。
- 当前 Agent State 标记（见第 5 节）。
- Before Snapshot（见 6.2）。
- 模糊点与待确认项。
- Vector Backend Status（见 8.3.11）。
- Acceptance Criteria（Feature Change 场景由 Feature Skill 追加）。

中断恢复：MUST 保证 `plan.md` 始终保存最新状态，可从任意状态恢复。

---

## 3. Constraints（行为约束）

Agent MUST NOT 执行以下行为：

- **臆造需求**：`readme.md` 未提及的功能，不得自行添加或假设。
- **修改无关文件**：仅触碰当前任务范围内的文件。
- **删除用户代码**：不得删除 `readme.md` 或用户提供的任何源材料。
- **修改部署配置**：未经要求不得改动部署、容器、编排相关配置。
- **修改环境变量**：不得读取、写入或改动 `.env` 等环境配置中的值。
- **引入无必要依赖**：仅安装需求明确要求或实现必需的依赖，并记录理由。
- **一次性提交所有代码**：MUST 按逻辑单元分步提交。

### 3.1 依赖修改规则

新增依赖 MUST 在提交信息、`plan.md` 或 `decision.md` 中记录：

- 依赖名称与版本。
- 用途。
- 为何不能使用已有依赖实现。

MUST NOT 仅为规避少量代码而引入新库。

---

## 4. Git Workflow（Git 工作流）

### 4.1 修改前检查

任何修改操作前，Agent MUST：

1. 执行 `git status` 检查工作区状态。
2. 执行 `git diff` 查看未提交变更。
3. 判断已有变更是否与当前任务相关。

### 4.2 分支策略

- 初始化阶段（Phase 1-2）MAY 直接在 `main` 分支提交脚手架与初始文档。
- 功能开发阶段（Phase 3 起）MUST 在 `feature/<功能简称>` 分支开发，MUST NOT 直接在 `main` 上提交功能代码。
- 每个功能模块验证通过后，MAY 合并回 `main`（需用户确认）。

```
main
 └── feature/<功能简称>
```

### 4.3 提交信息格式（Conventional Commits）

提交信息 MUST 采用 `<type>: <简短描述>` 格式。

| type | 说明 |
| --- | --- |
| `feat` | 新增功能 |
| `fix` | 修复缺陷 |
| `docs` | 文档变更（`readme.md`、`plan.md`、`tree.md`、`AGENTS.md`、`decision.md`） |
| `refactor` | 不改变行为的代码重构 |
| `test` | 测试相关变更 |
| `chore` | 构建、工具、脚手架等杂项 |

示例：

```
feat: add user authentication module
fix: correct date formatting in log
docs: update plan.md and tree.md after adding auth
```

### 4.4 提交与破坏性操作禁止项

Agent MUST NOT：

- 一次性提交所有代码（MUST 按逻辑单元拆分）。
- 提交无法构建或无法运行的代码。
- 提交包含敏感信息的文件（密钥、密码、Token 等）。
- 执行 `git reset --hard`。
- 执行 `git push --force`（force push）。
- 执行 `git rebase`（除非用户明确要求并确认已备份）。

---

## 5. Agent State（Agent 状态机）

### 5.1 Agent Execution State Model

Agent MUST 在任意时刻明确自身所处状态，并在 `plan.md` 中记录状态转换。

```
INIT → ANALYZE → PLAN_READY → PREPARE → IMPLEMENTING → VERIFYING → REVIEW → COMMITTING → DONE
```

| 状态 | 含义 | 进入条件 |
| --- | --- | --- |
| `INIT` | 任务启动 | 接收任务 |
| `ANALYZE` | 需求与上下文分析 | 读取 `readme.md` 与项目上下文 |
| `PLAN_READY` | 计划就绪 | `plan.md` 已初始化且任务清单明确 |
| `PREPARE` | 环境与分支准备 | 分支已创建、工作区干净 |
| `IMPLEMENTING` | 实施中 | 逐逻辑单元编码 |
| `VERIFYING` | 验证中 | 执行验证流水线 |
| `REVIEW` | 审查中 | 检查 diff 与文档同步 |
| `COMMITTING` | 提交中 | 执行 Conventional Commit |
| `DONE` | 完成 | 交付报告已输出 |

异常状态：

| 状态 | 含义 | 进入条件 | 恢复方式 |
| --- | --- | --- | --- |
| `WAIT_USER` | 等待用户输入 | 需求模糊、冲突或需确认 | 明确向用户提问后等待 |
| `FAILED` | 失败终止 | 验证无法通过且无法修复 | 输出失败报告，等待用户决策 |

### 5.2 状态转换规则

- 状态转换 MUST 可追踪：每次进入新状态，MUST 在 `plan.md` 更新当前状态标记。
- 遇到需求模糊点，MUST 转入 `WAIT_USER`，MUST NOT 自行假设后继续。
- 验证失败且无法修复，MUST 转入 `FAILED` 并输出失败报告。
- 任何异常状态下 MUST NOT 执行 `git commit`。

---

## 6. Risk Control（风险控制）

### 6.1 Change Risk Level

| 等级 | 范围 | 处理要求 |
| --- | --- | --- |
| `L0` | 文档、注释、小范围格式修改 | 普通流程 |
| `L1` | 单文件代码修改 | 普通流程 |
| `L2` | 模块级修改 | MUST 执行影响分析 |
| `L3` | 跨模块逻辑修改 | MUST 执行 Code Graph impact 查询 |
| `L4` | 数据库 / API / 架构修改 | MUST：用户确认 + rollback plan + migration plan |

### 6.2 Before Snapshot（修改前快照）

每次修改开始前，Agent MUST 记录以下信息到 `plan.md`：

```
commit hash:   <当前提交哈希>
branch:        <当前分支名>
modified files: <预判将修改的文件列表>
risk level:    <L0 - L4>
```

用途：失败时用于恢复现场。

### 6.3 Decision Log（决策日志）

涉及以下事件时，MUST 在 `decision.md` 追加决策记录：

- 技术方案选择。
- 新依赖引入。
- 架构调整。
- 数据结构变化。

格式：

```
## Decision
Date: <YYYY-MM-DD>

Context: <决策背景与问题>

Decision: <做出的决定>

Reason: <决策理由>

Alternatives: <考虑过的备选方案>

Rejected: <被否决的方案及原因>
```

---

## 7. Development Workflow（开发工作流）

各 Phase 声明进入/退出状态，与第 5 节状态机对应。

### Phase 1：Requirement Analysis（需求分析） — `INIT → ANALYZE → PLAN_READY`

1. 完整读取并解析 `readme.md`，提炼项目目标、技术栈、功能模块与约束条件。
2. 若无法读取 `readme.md`，MUST 立即停止并明确要求用户重新提供，MUST NOT 臆造需求。
3. 初始化 `plan.md`，记录初始任务列表与总体计划，状态标记为 `PLAN_READY`。
4. 提交：`docs: add initial plan based on readme analysis`

### Phase 2：Project Bootstrap（项目脚手架） — `PLAN_READY → PREPARE`

1. 创建基础目录结构、入口文件、配置文件。
2. 创建 `AGENTS.md`，写入项目开发规范与 AI 行为约束。
3. 创建 `.gitignore`，按技术栈忽略依赖、构建产物、环境变量等。
4. 执行 `git init` 初始化仓库。
5. 更新 `tree.md`，反映初始结构。
6. 执行初始提交：`chore: initial commit with project scaffold and gitignore`
7. 建立首次知识索引：MUST 尝试 MCP → Python → Markdown，初始化 Vector Backend 并执行首次全量索引（见 8.3）。

### Phase 3：Incremental Development（增量开发） — `PREPARE → IMPLEMENTING`

1. 从 `main` 创建并切换到 `feature/<功能简称>` 分支。
2. 按模块依赖顺序逐模块开发。
3. 每完成一个逻辑单元（可运行或逻辑完整）：
   - 记录 Before Snapshot（见 6.2）。
   - 按风险等级执行对应处理（见 6.1）。
   - 执行第 11 节「Validation」验证流水线。
   - 执行 Vector Backend 增量同步（见 8.3.6）。
   - 更新 `plan.md`（进度、状态标记、已完成项、待办项、问题记录）。
   - 更新 `tree.md`（记录新增或变更文件）。
   - 使用 Conventional Commits 提交。
4. 遇到需求模糊点 MUST 转入 `WAIT_USER` 并记录到 `plan.md`，不得自行假设后继续。

### Phase 4：Verification（验证与交付） — `IMPLEMENTING → VERIFYING → REVIEW → COMMITTING → DONE`

1. 执行项目适用的完整验证流水线（见 11 节）。
2. 执行全部测试。
3. 同步 `plan.md` 与 `tree.md` 至最终状态，并核对 `readme.md`、`AGENTS.md` 一致性。
4. 最终提交：`chore: project completed and ready for review`
5. 输出交付报告（见 12 节），状态置为 `DONE`。

### 7.1 Multi-Agent Collaboration（可选能力）

Multi-Agent 是可选能力，MUST NOT 作为默认流程。

- 复杂任务 MAY 按任务依赖关系分解，由多个 Agent 协作。
- 简单任务 MUST 保持单 Agent 顺序执行。
- 若当前环境无 Multi-Agent / Worktree 能力，自动退化为单 Agent，不得阻塞任务。

---

## 8. Knowledge System（知识系统）

### 8.1 知识索引与沉淀

Agent MUST 维护以下项目知识索引，并随开发增量同步：

| 索引 | 内容 | 同步时机 |
| --- | --- | --- |
| `folder_summary` | 目录职责摘要 | 目录结构变化时 |
| `file_summary` | 文件职责摘要 | 文件职责变化时 |

沉淀原则：

- **主动知识沉淀**：每完成一个逻辑单元，MUST 更新受影响的 `folder_summary` 与 `file_summary`。
- **增量同步**：仅更新受影响部分，MUST NOT 全量重写。
- **文件职责摘要**：`file_summary` MUST 描述文件的单一职责与对外接口。

### 8.2 知识查询优先级

对于项目相关问题，Agent MUST 按以下优先级获取答案：

| 优先级 | 来源 | 说明 |
| --- | --- | --- |
| P1 | 本地源码 + Code Graph | 项目行为的权威来源 |
| P2 | 项目知识索引（Vector Summary） | `folder_summary` / `file_summary` |
| P3 | 已加载上下文 | 当前会话已读取的内容 |
| P4 | 外部搜索 | 通用知识、第三方文档 |

原则：

- 任何项目行为问题，默认答案存在本地代码。
- MUST NOT 未检查源码，仅凭通用知识修改代码。

### 8.3 Vector Storage Backend（向量检索后端）

知识索引的存储与检索 MUST NOT 绑定具体工具实现。统一抽象为 **Vector Storage Backend**，Agent 只检测「能力」，不绑定具体工具名（MUST NOT 假设 `mcp-vector-search`、`kindex`、`ctxd` 等存在）。

Backend 类型统一为三级：

| 类型 | 说明 |
| --- | --- |
| MCP Vector Backend | 通过 MCP 协议提供的向量存储 / 语义检索服务 |
| Python Local Vector Backend | 项目隔离 Python 环境中初始化的本地向量后端，具体实现由 Backend Adapter 决定（如本地向量数据库、SQLite Index 等） |
| Markdown fallback | 降级为直接读取 `folder_summary` / `file_summary` 的 Markdown 文件 |

#### 8.3.1 Backend Selection（选择优先级）

Agent MUST 按以下优先级选择 Backend：

1. **Existing MCP Vector Backend**：当前环境已存在的可用 MCP 后端。
2. **Newly available MCP Vector Backend**：当前环境新发现的可用 MCP 后端。
3. **Existing project-local Python Vector Backend**：项目已存在的可用本地后端。
4. **Newly configured Python Vector Backend**：新配置的本地后端。
5. **Markdown fallback**：兜底。

规则：

- 若项目已有可工作的本地 Vector Backend，MUST 优先复用，MUST NOT 重新安装另一实现。
- MUST 优先使用 MCP；不得因为 Python 环境存在就绕过可用的 MCP Backend。

#### 8.3.2 Vector Backend Initialization Protocol（生命周期）

Backend 初始化 MUST 遵循以下生命周期：

```
Detection
↓
Selection
↓
Initialization
↓
Full Index
↓
Incremental Sync
↓
Health Check
↓
Fallback
```

#### 8.3.3 MCP 优先策略（Detection）

首次建立知识索引时，Agent MUST 优先检查当前运行环境是否存在可用的 MCP Vector Backend。检查的是能力，不是工具名。至少检查：

1. 是否存在可访问的 MCP Server。
2. 是否提供向量存储或语义检索能力。
3. 是否支持写入 / 更新索引。
4. 是否支持查询。
5. 是否能够访问当前项目数据。
6. 是否能够完成当前项目的索引操作。

检测结果 MUST 为以下四种之一，并按规则处理：

| 结果 | 处理 |
| --- | --- |
| `AVAILABLE` | 直接使用 MCP Backend：initialize → full index → health check → ready |
| `UNAVAILABLE` | 继续检测 Python 环境（见 8.3.4） |
| `PARTIAL` | 判断是否满足 query / insert-update / index 三项能力；无法完成完整知识库工作流则视为不可用，进入 Python fallback |
| `FAILED` | 记录失败原因，进入 Python fallback |

#### 8.3.4 Python Local Vector Backend（自动配置）

仅当 MCP Vector Backend 不可用时，Agent MUST 检查 Python 环境：

1. 检测：`python --version`；若失败则 `python3 --version`。
2. Python 可用后：检查 pip → 检查 venv → 创建项目级隔离环境 → 安装本地 Vector Backend。

环境隔离 MUST 遵循以下优先级：

```
项目已有 .venv → 复用
不存在 → 创建 .venv（python -m venv .venv）
无法创建 → 尝试其他项目级隔离环境
全部失败 → Markdown fallback
```

MUST NOT：

- 直接修改系统级 Python。
- 直接覆盖用户已有 Python 环境。
- 无理由执行全局 `pip install`。

**不得写死具体数据库**：Skill 只定义 **Python Local Vector Backend** 的能力要求，具体实现由 Backend Adapter 决定。必须支持：

- embedding / index storage
- semantic retrieval
- insert / update
- project-local persistence
- incremental synchronization
- query

**自动安装**：当 Python 可用时：

1. 检查当前项目是否已有向量相关依赖。
2. 优先复用已有依赖。
3. 不存在则选择与当前环境兼容的本地实现。
4. 在项目隔离环境中安装依赖。
5. 验证安装结果。
6. 初始化本地向量索引。
7. 执行首次全量索引。

必须避免为少量代码引入额外依赖；新增依赖 MUST 符合 3.1「依赖修改规则」，并记录：名称、版本、用途、为何无法使用现有依赖、安装结果。

#### 8.3.5 首次全量索引（Full Index）

Backend 初始化成功后，MUST 执行首次全量索引。索引内容至少包括：

- `folder_summary`
- `file_summary`

若项目已有代码图谱，可同时记录：

- graph version
- git commit hash

索引完成后 MUST 执行一次查询验证（write → query → verify），不能仅判断「服务启动了」就认为初始化成功。

#### 8.3.6 增量同步（Incremental Sync）

初始化成功后，必须建立增量同步链路：

```
code change
↓
git diff
↓
changed files
↓
update file_summary
↓
update folder_summary
↓
incremental vector sync
```

每个逻辑单元完成后 MUST 执行增量同步；MUST NOT 每次都无条件全量重新索引。

#### 8.3.7 Backend Health Check

在以下时机 MUST 执行健康检查：

1. 首次初始化之后。
2. 首次查询之前。
3. 增量同步之前。
4. Agent 发现向量查询异常之后。

健康检查至少验证：backend reachable、write available、query available、index readable。

#### 8.3.8 失败降级（Fallback）

仅当以下情况全部发生时，才进入 Markdown fallback：

```
MCP unavailable / failed
AND
Python unavailable / failed
```

或：

```
MCP unavailable / failed
AND
Python Backend initialization failed
```

Markdown fallback MUST 继续维护 `folder_summary` / `file_summary`，并在 `plan.md` 记录：

```
Vector Backend:
markdown-fallback

Reason:
<失败原因>

Attempted:
- MCP
- Python
```

#### 8.3.9 安装安全策略（Installation Safety）

Agent MUST NOT：

- 修改系统级 Python。
- 修改用户已有全局环境。
- 修改 `.env` 中已有值。
- 覆盖用户已有向量索引。
- 删除已有知识库。
- 删除已有 Backend 配置。
- 安装与本次知识检索无关的依赖。

Agent SHOULD：

- 优先复用现有 Backend。
- 优先使用项目级 `.venv`。
- 使用 `python -m pip`。
- 采用最小依赖原则。
- 将安装结果写入 `plan.md` 或 `decision.md`。

#### 8.3.10 已有知识库保护

若检测到已有 Vector Backend / Vector Index / 知识数据，Agent MUST：

1. 检查其状态。
2. 检查其所属项目。
3. 检查索引版本。
4. 尽量复用。

MUST NOT 直接删除、重新初始化覆盖或强制重建，除非：索引损坏、项目发生不可兼容变化、用户明确要求。如需重建，MUST 记录 Decision Log（见 6.3）。

#### 8.3.11 配置结果记录（Backend Status）

初始化完成后，在 `plan.md` 记录：

```
## Vector Backend Status

Backend:
<MCP | Python | Markdown>

Status:
<ready | degraded | failed>

Environment:
<environment information>

Index:
<index location or backend identifier>

Initialization:
<timestamp>

Commit:
<git commit hash>
```

MUST NOT 记录：Token、API Key、Secret、密码。

#### 8.3.12 状态机集成

Vector Backend 初始化纳入现有 Agent State（见第 5 节），在 `PREPARE` 阶段完成 Backend 检测。首次初始化流程：

```
PREPARE
↓
Vector Backend Detection
↓
Vector Backend Initialization
↓
PLAN_READY / IMPLEMENTING
```

不创建新的独立 Agent 状态机。Backend 初始化失败不影响普通代码修改流程：可进入 Markdown fallback，但 MUST 记录 degraded 状态。

#### 8.3.13 与 Code Graph 的关系

Vector Backend 与 Code Graph 是两个独立系统，不得混为一体：

```
Vector Backend = 语义知识检索
Code Graph = 代码关系导航
```

二者协同：

```
Vector Search
↓ 找到候选模块
Code Graph
↓ 分析依赖 / 调用关系
L1 / L2 / L3
↓ 读取具体源码
```

---

## 9. Code Graph（代码关系图谱）

### 9.1 节点与关系

节点类型：

| 节点 | 说明 |
| --- | --- |
| `File` | 源文件 |
| `Module` | 模块 |
| `Class` | 类 |
| `Function` | 函数 |
| `Interface` | 接口 |

关系类型：

| 关系 | 说明 |
| --- | --- |
| `IMPORTS` | 导入 |
| `CALLS` | 调用 |
| `DEFINES` | 定义 |
| `DEPENDS_ON` | 依赖 |
| `INHERITS` | 继承 |
| `IMPLEMENTS` | 实现 |

### 9.2 构建降级策略

Code Graph 构建 MUST 按以下层级降级，确保不同语言可用：

| Level | 策略 | 说明 |
| --- | --- | --- |
| Level 1 | AST Parser | 使用语言 AST 解析器（如 tree-sitter） |
| Level 2 | Language Server Protocol | 通过 LSP 获取符号与引用 |
| Level 3 | Static Analysis | 使用正则 / 静态文本分析 |
| Level 4 | Manual Summary | 人工阅读并撰写关系摘要 |

要求：

- Agent SHOULD 优先选择当前环境中可用的最高精度解析能力。推荐优先级：AST Parser（AST / Compiler API）→ LSP（Language Server Protocol / Symbol Index）→ Static Analysis → Manual Summary。
- 若已确认某一级不可用，可直接跳过，无需重复探测。
- 最终使用的 Level MUST 记录在 `plan.md` 或 `decision.md`。
- L3 风险等级的影响查询 MUST 基于 Code Graph（见 6.1）。

### 9.3 影响分析原语（Impact Primitives）

Code Graph 查询 SHOULD 支持以下原语，用于影响分析：

| 原语 | 说明 |
| --- | --- |
| `callers` | 谁调用了该符号 |
| `callees` | 该符号调用了谁 |
| `deps` | 直接与传递依赖 |
| `impact` | 变更传播范围 |
| `flow` | 数据 / 控制流路径 |
| `neighbors` | 相邻节点 |
| `Blast Radius` | 受变更影响的节点集合（爆炸半径） |

Feature Change Skill 复用本定义，不重复编写。

---

## 10. Navigation Protocol（代码定位协议 / Progressive Discovery）

Agent MUST 使用三级定位协议，MUST NOT 退化为全文搜索：

| 层级 | 内容 | 用途 |
| --- | --- | --- |
| `L1` | `tree.md` + `folder_summary` | 定位目标目录 |
| `L2` | `file_summary` | 定位目标文件 |
| `L3` | 源文件源码 | 精确定位代码 |

使用规则：

- MUST 按 L1 → L2 → L3 顺序定位，先目录、再文件、后源码。
- MUST NOT 在未使用定位协议时直接全文搜索定位。
- **明确例外**：若用户已提供明确的文件路径、类名、函数名或行号，Agent MAY 在记录定位依据后直接进入 L3。
- **明确例外**：若目标文件已通过当前上下文或已有工具结果明确确认，MAY 跳过重复的 L1/L2 查询。
- 每次定位结果 SHOULD 回写更新 `folder_summary` / `file_summary`。

### 10.1 Token 效率原则

- **按需读取**：仅读取当前任务相关的文件片段，不一次性加载整个项目。
- **增量编辑**：使用局部替换/插入，不输出完整文件。
- **Diff 思维**：仅输出变更内容，不重复已有内容。
- **命令摘要**：编译/检查命令仅获取关键错误信息，不输出冗长日志。
- **上下文精简**：及时清理不再需要的中间信息。

---

## 11. Validation（验证规范）

### 11.1 验证流水线

Agent MUST 按以下顺序执行适用的验证：

1. **syntax**：语法检查。
2. **type check**：类型检查（如项目含类型系统）。
3. **lint**：代码规范检查。
4. **unit test**：单元测试。
5. **build**：构建检查（如项目无构建流程，跳过并记录原因）。

任一步骤失败，MUST 分析错误并修复后重新检查，通过后方可继续。

### 11.2 Testing Strategy（测试策略）

| 修改类型 | 测试要求 |
| --- | --- |
| 核心业务逻辑 | MUST 新增或更新测试 |
| API 行为 | MUST 新增或更新测试 |
| 数据转换 | MUST 新增或更新测试 |
| 算法 | MUST 新增或更新测试 |
| 文档 | MAY 不增加测试 |
| 样式 | MAY 不增加测试 |
| 重命名 | MAY 不增加测试 |

### 11.3 提交前自检

每次 `git commit` 之前，Agent MUST 完成以下检查，任一不通过则 MUST NOT 提交：

- [ ] **构建通过（如适用）**：执行项目适用的构建命令并成功；若项目无构建流程，则跳过并记录原因。
- [ ] **语法检查通过**：无语法错误。
- [ ] **类型检查通过**（如项目含类型系统）：无类型错误。
- [ ] **`tree.md` 已同步**：与实际目录结构一致。
- [ ] **`plan.md` 已同步**：进度、已完成项、待办项为最新。
- [ ] **无明显未使用代码**：无遗留调试代码、死代码。
- [ ] **无敏感信息**：无硬编码密钥、密码、Token 或个人信息。

---

## 12. Delivery Report（交付报告）

项目交付 MUST 满足：

- 项目完整可构建、可运行。
- Git 提交历史清晰、可独立回溯。
- `plan.md`、`tree.md`、`AGENTS.md`、`decision.md` 与 `readme.md` 内容一致。
- 无敏感信息残留。

每次开发任务结束时，Agent MUST 输出以下结构的报告：

```
## 修改摘要

（简述本次开发内容）

## 修改文件

（列出创建或修改的文件及其变更）

## Git 提交记录

（列出本次的提交哈希与信息）

## 验证结果

（列出各项验证及其结果）

## 风险与决策

（列出风险等级与决策日志）

## 未完成事项

（列出未完成项与原因）
```
