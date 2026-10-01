# 为什么选择 Agent Engineering Workflow

> v2.2.0 — 价值说明与对比分析。本文为宣传 / 选型材料，不改变协议。协议规则以
> [`skills/project-bootstrap-workflow/references/base-protocol.md`](../skills/project-bootstrap-workflow/references/base-protocol.md) 为唯一事实来源。

---

## 1. 一句话定位

**Agent Engineering Workflow 不是一组 Prompt，而是一套可安装的「Coding Agent 工程流程规范」——
把成熟软件工程纪律编译成 Agent 能稳定执行的运行时约束。**

```
需求 → 计划 → 代码定位 → 影响分析 → 实施 → 验证 → 知识沉淀 → Git 提交 → 交付
```

这条链路里，每一步都有明确的**准入条件、产物、校验方式与回退路径**，而不是"请谨慎操作"式的口头建议。

### 核心数据

| 指标 | 数值 |
| --- | --- |
| 交付形态 | 2 个可安装 Skill（新项目 / 已有项目）+ 1 套共享基础协议 |
| 协议规模 | 12 章、约 600 行规范性条款 |
| 状态机 | 9 个正常状态 + 2 个异常状态（`WAIT_USER` / `FAILED`） |
| 风险分级 | L0–L4，逐级附加强制动作 |
| 验证流水线 | 5 级（syntax → type → lint → test → build） |
| 结构校验 | `validate-skills.py`，27 项断言，仅依赖标准库 |
| 实机验证 | 3 个示例项目，10 个测试文件、78 个测试函数 |
| 安装成本 | 复制 2 个目录，**零第三方依赖**（无需 uv / Node） |
| 许可证 | MIT |

> 与市面主流方案的逐项对比见 **[§3 竞争格局与对比](#3-竞争格局与对比)**。
> 最直接的参照是 [spec-kit](https://github.com/github/spec-kit)（规范驱动开发）与 [BMAD](https://github.com/bmad-code-org/BMAD-METHOD)（敏捷 AiDD）。

---

## 2. 它解决什么问题

传统 Coding Agent 的失败模式，几乎都能归到"上下文"和"纪律"两件事上：

| 常见失败模式 | 根因 | 本项目的机制 |
| --- | --- | --- |
| 读取过多上下文、越读越糊涂 | 缺少分层定位 | **Progressive Discovery**（L1 目录 → L2 文件 → L3 源码） |
| 修改范围失控、牵一发动全身 | 缺少影响分析 | **Risk L0–L4** + Code Graph **Blast Radius** |
| 覆盖用户已有的未提交修改 | 缺少修改前检查 | `git status` / `git diff` 前置 + **Before Snapshot** |
| 跨会话失忆，重复交代背景 | 依赖聊天记忆 | 计划与知识**落盘** `.workflow/`，跨会话可恢复 |
| 交付过程不可复现、不可审计 | 缺少过程记录 | **Decision Log** + **交付报告** + Conventional Commits |
| 一次提交全部代码，出问题无法回退 | 缺少提交纪律 | 按逻辑单元小步提交，禁止破坏性 Git 操作 |

---

## 3. 竞争格局与对比

> 以下星标数、依赖要求与命令名核对于 2026-10，取自各项目官方仓库与文档（见 [§12 数据来源](#12-数据来源与时效)）。

### 3.1 市场全景：四类玩家

| 类别 | 代表项目 | 规模 | 定位 | 安装依赖 |
| --- | --- | --- | --- | --- |
| **工程流程类**（直接同类） | github/spec-kit | 139.7k ★ | 规范驱动开发（SDD）：constitution → specify → plan → tasks → implement → converge | Python 3.11+、uv |
| | BMAD-METHOD | 53.7k ★ | 敏捷 AI 驱动开发，多智能体专家分工 | Node.js + npm + uv |
| | obra/superpowers | — | TDD、调试、协作模式技能库 | 插件市场 |
| | Claude CodePro、RIPER Workflow、AB Method、Claude Code PM | — | 各自的 SDD / 阶段化流程变体 | 各自不同 |
| **领域能力类**（互补） | anthropics/skills | 179.3k ★ | docx / pdf / pptx / xlsx 等**垂直能力**；官方明确标注 *"for demonstration and educational purposes only"* | 复制目录 / 插件 |
| **单点基础设施类**（可叠加） | Claude Code Safety Net、TDD Guard、Dippy | — | hook 层拦截破坏性命令 / 强制 TDD | 各自不同 |
| | agnix、Schliff、Ctxlint、BlockWatch、Upkeep、SkilLock | — | 指令文件 lint、评分、文档-代码-配置漂移检测 | 各自不同 |
| | NVIDIA SkillSpector | — | Agent Skill 安全扫描 | 各自不同 |
| | Selvedge、faf-cli、presence、Context Engineering Kit | — | 长期记忆、上下文文件单一来源、置信度门禁 | 各自不同 |
| **聚合索引** | awesome-claude-code / awesome-claude-skills | 54.9k / 15.2k ★ | 资源目录，不提供流程 | — |

> **本项目的生态位**：工程流程类中的一员，但**不提供 CLI、不依赖 uv / Node**，以「复制两个目录即可用」的形态交付。

### 3.2 与最直接的两个同类逐项对比

#### vs github/spec-kit（最接近的同类）

spec-kit 是 GitHub 官方的规范驱动开发工具包，方法论成熟、生态庞大（227 个 release、集成目录覆盖 Copilot / MiniMax / Grok 等多种客户端）。

| 维度 | spec-kit | 本项目 |
| --- | --- | --- |
| 核心主张 | 先定义 **what / why**，再决定 **how** | 在 what/why 之外，额外约束**改动本身的危险度** |
| 制品位置 | `.specify/`（spec、plan、tasks、assessment） | `.workflow/`（readme、plan、AGENTS、tree、decision） |
| 流程入口 | 三个独立入口：SDD、bug fixing、idea assessment | 两个：新项目、已有项目修改 |
| 质量门 | clarification、checklists、consistency analysis、converge | 风险分级、影响分析、验收标准、提交前自检 |
| 前置依赖 | **Python 3.11+ 与 uv**，需执行 `specify init` | **无**，复制目录即可 |
| 扩展体系 | extensions / presets / workflows / bundles | 无（协议单文件，改动即生效） |
| 文档职责分离 | 未强制工作流文档与业务文档分离 | **强制** `.workflow/` 与 `docs/` 分离，并禁用 `prompt.md` |
| 风险机制 | bug 评 **severity**（critical / high / medium / low，理由含 "blast radius, data risk"）；idea 评 **risk posture**；converge 产出分 severity 的差异项 | 按**改动范围**分级（L0–L4），并**绑定强制动作**（见下行） |
| 变更安全纪律 | 无「改动范围 → 强制动作」绑定；无面向用户代码改动的 Git 前快照（其快照用于 CLI / 扩展自升级回滚） | 模块级起必须影响分析；跨模块必须图谱查询；数据库 / API / 架构必须用户确认 + 回滚方案 + 迁移方案 |
| 提交纪律 | 提供 **git 扩展**（`speckit.git.commit`），支持**可选**的 Conventional Commits 生成与按阶段自动提交 | 强制小步提交与 Conventional Commits，且**明令禁止**自动提交用户已有改动 |

**一句话**：spec-kit 解决"**写对东西**"，本项目额外解决"**别把东西弄坏**"。两者可叠用。

#### vs BMAD-METHOD（方法论最完整）

BMAD 是敏捷 AI 驱动开发框架，强项在**按规模调节流程**（小改动直接构建，复杂工作才展开规划）与**多智能体专家视角**（产品 / 架构 / UX / 开发 / 测试）。

| 维度 | BMAD | 本项目 |
| --- | --- | --- |
| 核心主张 | 把"思考"显式化并跨会话保留，可扩展到完整敏捷体系 | 把"工程纪律"显式化并**可机器校验** |
| 交付循环 | Clarify → Plan → Build & verify → Learn and adjust | INIT → ANALYZE → PLAN_READY → PREPARE → IMPLEMENTING → VERIFYING → REVIEW → COMMITTING → DONE |
| 多智能体 | **核心能力**，含 Builder / Test Architect / Loop 等模块 | 可选能力，环境不支持时自动退化为单 Agent |
| 流程调节 | 按改动规模自动选择规划深度 | 通过**双形态交付**调节：轻量提示词版 ↔ Skills 版 |
| 安装成本 | `npx skills add`（Node + npm + Git + uv）或插件市场，需选择模块 | 复制两个目录，或用 POSIX 脚本 |
| 生态 | Claude Code 与 Codex 双插件市场、官方 modules、Web bundles | 暂无插件市场集成（提供 Codex / Claude / Cursor 安装脚本） |
| 风险机制 | **风险标注为核心机制**：每张 ticket（story / spike / epic / initiative / bug）都带 `risk: low\|medium\|high`，bug 额外带 `severity: P0–P3`；风险驱动规划深度（高风险工作上调一档） | 按改动范围分级并绑定强制动作；风险不决定"要不要多做规划"，而决定"**必须额外执行哪些验证与确认**" |
| 影响分析 | `bmad-correct-course` 跨 PRD / epics / architecture / UX 做**文档级影响评估**；代码审查要求点名 "impacted consumer … `file:line`" | 代码级影响分析：图谱原语 `callers` / `callees` / `deps` / `impact`，并计算 Blast Radius |
| 变更安全纪律 | 无改动范围 → 强制动作绑定；无面向用户代码改动的 Git 前快照 | **完整具备** |

**一句话**：BMAD 在**方法论广度、风险标注体系与生态集成**上明显强于本项目；本项目在**改动风险驱动的强制动作与代码级影响分析**上更强，且安装成本更低。

#### vs 单点基础设施工具（互补）

| 能力 | 常见做法 | 本项目的差异 |
| --- | --- | --- |
| 防破坏性命令 | `claude-code-safety-net` 等 hook 在**运行时拦截** | 在**流程层前置**：`git status` / `git diff` / Before Snapshot / L0–L4 风险分级 |
| 强制 TDD | `tdd-guard` 用 hook 阻止违反 TDD 的写入 | 覆盖语法 → 类型 → lint → 测试 → 构建的**完整验证流水线**，并按修改类型规定测试义务 |
| 指令文件质量 | `agnix`、`Schliff`、`Ctxlint` 做 lint 与评分 | 校验**协议是否被重复定义**（防规则漂移），而非文件格式 |
| 长期记忆 | `Selvedge`、`faf-cli`、`presence` 提供记忆与漂移治理 | 记忆落在**项目内** `.workflow/plan/`，与 Git 一同版本化，不依赖外部服务 |

> 这一类工具可以**直接叠加**在本项目之上：hook 负责"物理拦截"，本协议负责"流程纪律"。

### 3.3 能力矩阵

图例：✅ 完整支持　🟡 部分支持 / 需自行实现　❌ 不具备

| 能力 | 本项目 | spec-kit | BMAD | 单点工具组合¹ |
| --- | :---: | :---: | :---: | :---: |
| 明确阶段与状态推进 | ✅ | ✅ | ✅ | ❌ |
| 跨会话状态恢复 | ✅ | ✅ | ✅ | 🟡 |
| **改动范围风险分级（范围 → 强制动作）** | ✅ | ❌ | ❌ | ❌ |
| 风险 / 严重度标注（条目级） | ✅ | ✅ | ✅ | ❌ |
| **代码图谱影响分析（callers / callees / deps / Blast Radius）** | ✅ | ❌ | ❌ | ❌ |
| 影响分析（LLM 估算受影响文件 / 消费者） | ✅ | 🟡 | ✅ | ❌ |
| 分层代码定位（控制上下文读取） | ✅ | 🟡 | 🟡 | ❌ |
| 保护用户未提交修改（前快照 + 不自动提交） | ✅ | 🟡 | 🟡 | 🟡 |
| 提交纪律（Conventional Commits / 小步提交） | ✅ | 🟡 | 🟡 | 🟡 |
| 标准化验证流水线 | ✅ | ✅ | ✅ | 🟡 |
| 知识沉淀与语义检索 | ✅ | 🟡 | 🟡 | 🟡 |
| 过程可审计（决策日志 / 交付报告） | ✅ | 🟡 | 🟡 | ❌ |
| 单一协议来源 + 防复制门禁 | ✅ | ❌ | ❌ | ❌ |
| 零第三方依赖即可安装 | ✅ | ❌ | ❌ | ✅ |
| 多智能体编排 | 🟡 | 🟡 | ✅ | ❌ |
| 官方插件市场集成 | ❌ | ✅ | ✅ | ✅ |

¹ 「单点工具组合」指把 safety-net / tdd-guard / agnix / Selvedge 等各自独立的工具拼起来使用。
² 两者的"风险标注"是**给条目打分**（bug severity / ticket risk 标签），不是**按改动范围强制动作**。

### 3.4 三条经得起查证的差异化

以下三项是**逐条比照 spec-kit 与 BMAD 源码**后确认的差异。注意表述的边界——同类方案**并非完全没有相关机制**，差在**绑定强度**：

| 差异化 | 事实说明 | 查证后的市场现状 |
| --- | --- | --- |
| **改动范围 → 强制动作的绑定** | L0–L4 不只给改动打标签，而是规定**必须额外执行什么**：模块级起必须影响分析，跨模块必须图谱查询，数据库 / API / 架构必须用户确认 + 回滚方案 + 迁移方案 | 两者**都有风险标注**（spec-kit 的 bug severity / risk posture；BMAD 的 `risk: low\|medium\|high` 标签与 severity），但标签只用于**评估与选规划深度**，**不产生强制动作义务**。差异在"绑定强度"，不在"有没有风险概念" |
| **代码级影响分析原语** | 5 类节点、6 类关系、7 个影响原语（`callers` / `callees` / `deps` / `impact` / `flow` / `neighbors` / Blast Radius），含四级构建降级策略，**不需任何第三方解析器**即可起步 | 两者**都有影响分析**，但是**LLM 判断而非图谱查询**：spec-kit 在 bug 评估里输出 "Files likely to change"；BMAD 要求审查时点名 "impacted consumer … `file:line`"、并用 `bmad-correct-course` 做**文档级**影响评估。差异在"图谱原语 + 可降级构建"，不在"有没有影响分析" |
| **防规则漂移的机器门禁** | 单一协议来源 + 差异层继承，并用脚本哨兵**在 CI 中拦截"复制协议内容"** | spec-kit 社区生态中**已意识到漂移问题**（其 constitution-sync preset 明确写 "Materialized copies can drift"，并用"每轮读实时 constitution"规避），但**靠约定与架构规避，无 CI 门禁**。差异在"是否有可执行拦截" |

同时诚实地说明：**其余能力普遍存在行业同类做法**——spec-kit 的 `constitution` 对应项目宪法、BMAD 的 durable context 对应状态外置、两者的 progressive disclosure 对应分层定位。

本项目的价值不在于发明概念，而在于**把它们固化成一套零依赖、可机器校验、跨客户端的协议**。

### 3.5 什么时候应该选别的方案

| 你的诉求 | 建议 |
| --- | --- |
| 需要成熟的**规范编写方法论**与大规模社区生态 | 选 **spec-kit** |
| 需要**风险标注与严重度体系**贯穿需求与缺陷管理 | 选 **BMAD**（每张 ticket 带 `risk` / `severity`，风险驱动规划深度） |
| 需要**多智能体专家分工**、完整敏捷流程、官方插件市场 | 选 **BMAD** |
| 需要**按阶段自动提交**（含 Conventional Commits 生成） | 选 **spec-kit** 的 git 扩展 |
| 需要**处理 docx / pdf / xlsx 等文档** | 选 **anthropics/skills**（与本项目可叠加） |
| 需要**运行时物理隔离**（沙箱 / 容器 / 微虚拟机） | 选专门的沙箱方案（Cleat、Container Use、Brood Box 等） |
| 需要**对话历史语义检索** | 选 Callimachus、Selvedge 等记忆方案（可与本项目的 `.workflow/` 并存） |
| 只想**一次性改个脚本** | 用本项目的轻量提示词版，或不必引入 |

> 明确划出"不适用边界"比宣称"全都适用"更有参考价值。本项目**不与上述方案竞争**，其中多数可直接叠加。

---

## 4. 创新性

> 判定标准：**"市场上是否有同类做法"**，以及**"同类做法绑定了多强的强制力"**。只有在这两个维度上都站得住的主张才计入创新性（对照见 [§3.4](#34-三条经得起查证的差异化)）。

### 4.1 协议即基础设施：单一协议来源 + 差异层继承

多数 Prompt / Skill 项目的演进方式是**复制粘贴**——`v2` 目录、`v2.2` 目录各存一份，规则逐步漂移。

本项目把协议当作代码来管：

```
        共享 Base Engineering Protocol（定义一次）
                 │
          ┌──────┴──────┐
          ↓             ↓
   Project Bootstrap  Feature Change
      Workflow           Workflow
```

- 完整协议只定义一次，位于 `references/base-protocol.md`；
- 已有项目修改 Skill **只写差异**（Feature-specific Override），不重复展开；
- 更关键的是——`validate-skills.py` 内置**重复内容哨兵检查**（`BASE_ONLY_SENTINELS`）与**标题重叠检查**，一旦 Feature Skill 开始复制 Base Protocol 内容，脚本直接 FAIL。

> 把"不要重复"从口头约定变成**可执行的门禁**，这是同类项目里罕见的做法。

### 4.2 把工程纪律写成运行时约束，而非建议

协议采用四级规范关键词，语义接近 RFC 2119：

| 关键词 | 语义 |
| --- | --- |
| **MUST** | 必须执行，违反即为失败 |
| **MUST NOT** | 禁止执行 |
| **SHOULD** | 默认执行，除非有明确理由并记录说明 |
| **MAY** | 可选执行，自行判断 |

配合 9 状态状态机与 L0–L4 风险分级，形成"**可判定的对错**"而非"尽量小心"。

### 4.3 状态外置：跨会话、跨客户端、可中断恢复

这是与"把一切交给上下文"最本质的差别：

```
.workflow/
├── readme.md / readme/   需求（用户维护，Agent MUST NOT 臆造）
├── plan.md   / plan/     计划、任务清单、状态、快照、待确认项
├── AGENTS.md             项目级 AI 规范
├── tree.md               目录结构说明
└── decision.md           决策日志
```

- 任意时刻中断，Agent 都能通过「入口文件 + `index.md` 索引」定位并恢复；
- 换一个 Agent 客户端、换一个会话，状态依然存在；
- 配套**章节拆分约定**（入口 + `index.md` + kebab-case 章节文件）防止单文件无限膨胀；
- 强制**工作流文档（`.workflow/`）与业务文档（`docs/`）分离**，并禁用 `prompt.md`，避免事实来源分裂。

### 4.4 知识能力抽象，而非工具绑定

协议刻意**不绑定任何具体向量数据库产品**：

```
MCP Vector Backend → Python Local Vector Backend → Markdown fallback
```

- Agent 只检测**能力**（能否写入 / 查询 / 索引），不检测工具名；
- 已有知识库优先复用，明令禁止覆盖或重建；
- 全部失败时降级为直接读取 Markdown 摘要，且必须记录 `degraded` 状态；
- 安装侧有独立安全策略（不改系统 Python、不动 `.env`、不装无关依赖）。

### 4.5 双重交付形态：按项目规模选型

同一套工程思想，提供两个成本档位：

| 形态 | 位置 | 适用 |
| --- | --- | --- |
| **轻量提示词版** | `simplePrompt/` | 小项目、个人项目，直接复制即用，上下文开销低 |
| **Agent Skills 版** | `skills/` | 中大型、长期维护项目，需要状态管理、影响分析、知识沉淀 |

这避免了"要么太轻（不够用）、要么太重（划不来）"的二选一。

### 4.6 每条规则都能被机器校验

`validate-skills.py` 仅依赖 Python 标准库，执行 8 类检查、27 项断言：

- Skill 目录与 `SKILL.md` 结构完整性
- frontmatter 字段齐备、`name` 与目录名一致、多 Skill 版本统一
- **全部相对 Markdown 链接可解析**（死链检查）
- **孤儿引用文件检测**（存在但从未被引用）
- **Base Protocol 重复定义检测**（标题重叠 + 内容哨兵）
- Markdown 基础结构合法性

> 协议文档里的规则，不再只是"希望 Agent 遵守"，而是**CI 里可以拦住的东西**。

---

## 5. 生态地位

### 5.1 在分层中的位置

```
┌────────────────────────────────────────────────────────────┐
│  运行时宿主  Claude Code / Codex / Cursor / Gemini CLI …    │  ← Agent 跑在哪里
├────────────────────────────────────────────────────────────┤
│  工程流程   spec-kit（SDD）  BMAD（敏捷 AiDD）  superpowers  │  ← 怎么组织开发
├────────────────────────────────────────────────────────────┤
│  ★ 本项目的生态位 ★                                        │
│  变更安全纪律（风险分级 / 影响分析 / 快照 / 可审计）          │  ← 本项目
├────────────────────────────────────────────────────────────┤
│  领域能力   anthropics/skills（docx / pdf / xlsx …）        │  ← Agent 能做什么
├────────────────────────────────────────────────────────────┤
│  单点基础设施  沙箱 / hook 拦截 / TDD 强制 / 指令 lint / 记忆 │  ← 怎么加硬约束
└────────────────────────────────────────────────────────────┘
```

本项目落在**流程层的下沿**：不与 spec-kit、BMAD 争夺"如何写好规范"，而是在它们与代码之间补上"**每次改动有多危险、改了会波及什么**"这一层，且可以叠加在它们之上。

### 5.2 三个关键站位

| 站位 | 含义 |
| --- | --- |
| **技术栈无关** | 协议不含任何脚手架、框架或语言模板，Node / Python / Java / Go 项目同样适用 |
| **客户端中立** | 遵循 Agent Skills 开放标准（同一份 `SKILL.md` 可被 Claude Code / Codex / Cursor / Gemini CLI 等加载），提供三种安装目标，不锁定单一厂商 |
| **零依赖** | 与 spec-kit（需 uv）、BMAD（需 Node + npm + uv）不同，安装只需**复制两个目录**；规模校验脚本仅用 Python 标准库 |
| **渐进增强** | 向量检索、代码图谱、多 Agent 协作全部是**可选能力**，环境不支持时自动降级，绝不阻塞任务 |

---

## 6. 优势

### 6.1 对手写代码的开发者

- **不再被 Agent 覆盖本地未提交修改**：修改前强制检查工作区，冲突时停止并交还人工处理。
- **每次改动都可回溯**：小步提交 + 决策日志，出问题能精确定位到某个逻辑单元。
- **跨会话不用重复交代背景**：`.workflow/` 里存的是状态，不是聊天记录。

### 6.2 对团队

- **新人 / Agent 上手成本低**：规范写一次进 `.workflow/AGENTS.md`，全队与全部 Agent 共用。
- **评审有据可依**：交付报告固定包含修改摘要、文件清单、提交记录、验证结果、风险决策、未完成事项。
- **规则不漂移**：单一协议来源 + 脚本门禁，避免"三个人维护三份规范"。

### 6.3 对长期项目

- **知识持续沉淀**：`folder_summary` / `file_summary` 随开发增量同步，不依赖任何一次会话的记忆。
- **文档不会烂掉**：`tree.md` 在文件增删时强制更新，且被包含在提交前自检清单中。
- **协议可演进而不破版**：差异层继承让新增场景（例如新的修改类型）只需追加差异，不必重写协议。

---

## 7. 实机验证

### 7.1 示例项目

仓库内提供 3 个示例，其中 2 个是**完整可运行的真实产物**：

| 示例 | 说明 | 测试规模 |
| --- | --- | --- |
| `examples/demo-project/` | 最小结构示例，展示各文档之间关系 | — |
| `examples/demo_codex_deepseek_flash/` | FastAPI + Jinja2 + SQLite + HTMX + Alpine.js + Tailwind 局域网多人内容平台 | 5 个文件 / 33 个测试函数 |
| `examples/demo_deepseek-harness_deepseek_flash/` | 同一需求、另一 Agent 运行时下的产物 | 5 个文件 / 45 个测试函数 |

两个平台示例展示了完整链路：需求分析 → 架构设计 → 分阶段实现 → 测试 → 文档同步 → Git 提交，并包含多用户认证、文章生命周期（`draft → submitted → published`）、评论与权限体系。

### 7.2 一个值得注意的信号

示例目录以 `demo_codex_deepseek_flash`、`demo_deepseek-harness_deepseek_flash` 命名，指向 **两套不同 Agent 运行时 + DeepSeek Flash 级别模型**的实际产物。

这意味着：**收益来自流程结构本身，而不是模型强度。** 流程把"该怎么走"固定下来之后，即使是轻量模型也能稳定产出可测试、可交付的工程结果。

### 7.3 仓库自身受同一套规则管理

本仓库的协议文档、示例与脚本之间的一致性，由 `validate-skills.py` 持续校验，当前状态：

```
Summary: 27 PASS, 0 WARNING, 0 FAIL
RESULT: PASS
```

---

## 8. 适用边界（诚实说明）

明确说清**不做什么**，比夸大能力更可信：

| 不适用场景 | 原因 |
| --- | --- |
| 替代 CI/CD | 本项目规范"开发过程"，不负责构建、发布、部署流水线 |
| 团队权限与审批流 | 不涉及账号、审批、合规策略 |
| 提供脚手架 / 代码模板 | 刻意保持技术栈无关，不产出任何框架样板 |
| 一次性脚本任务 | 引入完整流程不划算，建议用轻量提示词版或不引入 |
| 无 Git 的项目 | 修改前检查、快照、小步提交等核心能力依赖 Git |

---

## 9. 快速开始

### 新项目

```text
使用 `project-bootstrap-workflow`，根据 `readme.md` 初始化并开发新项目。
```

### 已有项目修改

```text
使用 `feature-change-workflow`，根据以下需求修改现有项目：
<功能需求>
```

### 修复缺陷

```text
使用 `feature-change-workflow`，根据以下问题分析并修复现有项目：
<Bug 描述>
```

### 安装

```bash
git clone https://github.com/cjz-wr/agent-engineering-workflow.git
cd agent-engineering-workflow

# 项目级安装（适合团队，随仓库共享）
./scripts/install-local.sh claude

# 用户级安装（适合个人，所有项目复用）
./scripts/install-local.sh claude --user
```

目标客户端支持 `codex` / `claude` / `cursor`。安装脚本仅做本地复制，不联网安装依赖；遇到同名 Skill 目录会安全失败而非静默覆盖。

---

## 10. 后续规划

| 方向 | 说明 |
| --- | --- |
| 行为评估集（evals） | 从"结构校验"扩展到"触发时机与输出质量校验"，含应触发 / 不应触发负例 |
| 文档同步校验脚本 | 把提交前自检清单（`tree.md` 一致性、版本一致性、frontmatter 合规）自动化 |
| 跨平台安装 | 为 Windows 环境提供与 POSIX 脚本等价的一键安装 |
| 变更记录 | 增加 `CHANGELOG.md`，便于脱离 Git 历史的使用者追踪演进 |

---

## 11. 相关文档

| 文档 | 内容 |
| --- | --- |
| [`../README.zh-CN.md`](../README.zh-CN.md) | 项目总览与快速开始 |
| [`architecture.md`](architecture.md) | 两个 Skill 与共享协议的协作方式 |
| [`protocol-overview.md`](protocol-overview.md) | 协议要点速览 |
| [`state-machine.md`](state-machine.md) | 状态机与转换规则 |
| [`../skills/project-bootstrap-workflow/references/base-protocol.md`](../skills/project-bootstrap-workflow/references/base-protocol.md) | 完整协议（唯一事实来源） |

---

## 12. 数据来源与时效

本文中涉及第三方项目的星标数、依赖要求、命令名与能力描述，核对于 **2026-10**，来源如下：

| 项目 / 资料 | 来源 |
| --- | --- |
| Spec Kit | [github/spec-kit](https://github.com/github/spec-kit) 官方仓库与文档 |
| BMAD-METHOD | [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) 官方仓库与文档 |
| Anthropic 官方 Skills | [anthropics/skills](https://github.com/anthropics/skills) 官方仓库 |
| Agent Skills 开放标准 | [agentskills.io](https://agentskills.io/) 规范与客户端列表 |
| Claude Code Skills 机制 | [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) |
| Skill 编写最佳实践 | [platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |
| 上下文工程方法论 | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) |
| 生态工具清单 | [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)、[awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) |

> 第三方项目演进较快，具体功能与依赖请以其**当前官方文档**为准。

### 核实方法

对比章节中的第三方能力描述，均经过**两层核实**，而非仅读 README：

1. **官方文档层**：阅读各自仓库 README、官方文档站点与命令参考；
2. **源码层**：在源码中检索关键机制的实际存在情况，例如：
   - 在 `github/spec-kit` 中检索 `risk`、`snapshot`、`Files likely to change`、`git status`，命中其 `extensions/bug/commands/speckit.bug.assess.md`（severity 与 "blast radius, data risk"）、`extensions/git/commands/speckit.git.commit.md`（Conventional Commits 与自动提交）；
   - 在 `bmad-code-org/BMAD-METHOD` 中检索 `risk`、`impact`、`snapshot`，命中其 `skills/bmad-ticket/assets/*-template.md`（`risk: low|medium|high`、`severity: P0–P3`）、`skills/bmad-correct-course/`（文档级影响评估）等。

### 更正记录

本文档首版曾声称 "两者均无风险分级、无影响分析"，**该断言不正确**，已依据上述源码抽查更正：

| 原断言 | 更正为 |
| --- | --- |
| spec-kit 无风险分级 | 有 bug severity（`critical/high/medium/low`，理由含 blast radius）与 idea risk posture；但**无"改动范围 → 强制动作"绑定** |
| spec-kit 无 Git / 提交纪律 | 有 **git 扩展**，支持可选的 Conventional Commits 与按阶段自动提交；但**不保护用户未提交改动，反而会自动提交** |
| BMAD 无风险分级 | **每个 ticket 都带 `risk: low\|medium\|high`**，bug 另带 severity，且风险驱动规划深度；但同样是**标注而非强制动作** |
| 两者无影响分析 | spec-kit 有 AI 估算的 "Files likely to change"；BMAD 有文档级影响评估与受影响消费者点名；但**均无图谱查询原语** |

保留这三项作为差异化的理由，已从"对方完全没有"下调为"对方有但绑定强度不同"（见 [§3.4](#34-三条经得起查证的差异化)）。

---

## 许可证

[MIT](../LICENSE)
