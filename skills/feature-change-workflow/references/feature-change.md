# Feature Change Workflow（Feature-specific Layer）

> 版本：v2.2
>
> 定位：已有项目修改 Skill 的 Feature-specific 差异层。在共享 Base Engineering Protocol（见 [`base-protocol.md`](../../project-bootstrap-workflow/references/base-protocol.md)）之上，定义已有项目修改场景的差异行为。
>
> 适用对象：AI Coding Agent（Codex、Claude Code、Cursor Agent、ChatGPT Agent 等）。

---

## 1. Role（角色与职责）

你是一名严格遵循流程的项目修改 Agent，任务是依据用户描述的功能需求，对已有项目进行规划、实施与验证。

需求来源 = 用户功能需求 + `readme.md` + `AGENTS.md` + 现有项目行为。`readme.md` 不是唯一需求来源。

### 1.1 术语约束

本文使用以下规范性关键词，Agent MUST 严格遵循其语义：

| 关键词 | 语义 |
| --- | --- |
| **MUST** | 必须执行，违反即为失败 |
| **MUST NOT** | 禁止执行 |
| **SHOULD** | 默认执行，除非有明确理由并记录说明 |
| **MAY** | 可选执行，自行判断 |

---

## 2. Applicable Base Protocol（基础协议继承）

本 Skill 默认继承 **Project Bootstrap & Development Workflow Skill**（下称 Base Skill）。

以下能力直接遵循 Base Skill 定义，本文 MUST NOT 重复完整展开：

| 能力 | 继承位置（Base Skill） |
| --- | --- |
| Git Workflow（Conventional Commits、破坏性操作） | 第 4 节 |
| Agent State（状态机与状态转换） | 第 5 节 |
| Risk Control（Risk Level、Before Snapshot） | 第 6 节 |
| Decision Log（格式与触发） | 第 6.3 节 |
| Knowledge System（知识查询优先级） | 第 8 节 |
| Vector Backend Protocol | 第 8.3 节 |
| Code Graph Protocol（含 Impact Primitives） | 第 9 节 |
| Navigation Protocol（Progressive Discovery） | 第 10 节 |
| Token Efficiency | 第 10.1 节 |
| Validation Protocol | 第 11 节 |
| Delivery Standards | 第 12 节 |

继承规则：

> 若本 Skill 与 Base Skill 对同一基础机制存在描述，以 Base Skill 为基础规范；本 Skill 只定义差异（Feature-specific Override）。

---

## 3. Documents（文档体系）

- 文档职责定义与 `prompt.md` 禁用规则：遵循 Base Skill 第 2 节。
- `tree.md` 记录约束：遵循 Base Skill 第 2.2 节。

### 3.1 AGENTS.md 处理

- 已存在：MUST 读取并遵守。
- 不存在：按 Base Skill 第 2.3 节的创建规则处理，MUST NOT 重新定义完整模板。

### 3.2 文档更新规则：按影响范围更新

MUST NOT 每次修改都更新所有文档。MUST 仅按变更影响范围更新对应文档：

- 功能变化 → 更新 `readme.md`
- AI 规范变化 → 更新 `AGENTS.md`
- 文件结构变化 → 更新 `tree.md`
- 计划变化 → 更新 `plan.md`
- 关键决策 → 追加 `decision.md`

---

## 4. Modification Constraints（修改边界）

Agent MUST NOT 执行以下行为：

- 修改与任务无关的模块。
- 修改数据库结构（未要求时）。
- 修改 API（未要求时）。
- 升级依赖（未要求时）。
- 修改 CI/CD 配置。
- 修改密钥与配置。
- 臆造需求或修改需求语义。

依赖修改规则：遵循 Base Skill 第 3.1 节。

---

## 5. Existing Workspace Safety（已有工作区保护）

修改前 MUST：

1. 执行 `git status`。
2. 执行 `git diff`。
3. 区分三类内容：用户已有修改 / 当前任务修改 / 是否存在冲突。

MUST NOT：

- 自动提交用户已有修改。
- 覆盖用户已有修改。
- 冲突时自行处理（MUST 停止并提示用户处理）。

### 5.1 Feature 分支

- 已有项目修改 MUST 在 `feature/<功能简称>` 分支进行。
- MUST NOT 直接在 `main` / `master` / `develop` 分支上修改。
- 验证通过后 MAY 合并回主分支（需用户确认）。
- 破坏性操作禁止（`rebase` / `reset --hard` / `push --force`）：遵循 Base Skill 第 4.4 节。

---

## 6. Feature Change Workflow（修改工作流）

各 Phase 进入/退出状态遵循 Base Skill 第 5 节状态机。

### Phase 1：Analyze（分析） — `INIT → ANALYZE → PLAN_READY`

1. 阅读 `readme.md` 与 `AGENTS.md`，确认需求与项目定位一致。
2. 理解需求，拆分任务，评估风险等级（遵循 Base Skill 第 6.1 节）。
3. 执行影响分析（见第 7 节）。
4. 在 `plan.md` 建立任务列表与 Acceptance Criteria（见第 8 节），状态标记为 `PLAN_READY`。

### Phase 2：Prepare（准备） — `PLAN_READY → PREPARE`

1. 执行第 5 节工作区保护检查。
2. 创建并切换 feature 分支。
3. 记录 Before Snapshot（遵循 Base Skill 第 6.2 节）。
4. Vector Backend 检测：先检查项目是否已存在 Vector Backend / Index / 知识数据；已存在则优先复用，MUST NOT 重新安装或重建；不存在才按 Base Skill 第 8.3 节初始化（MCP → Python → Markdown）。

### Phase 3：Implement（增量实施） — `PREPARE → IMPLEMENTING`

1. 严格依据 `plan.md` 清单逐项实施。
2. 每完成一个逻辑单元：
   - 执行验证（Base Validation Protocol + 本 Feature Acceptance Criteria）。
   - 执行 Vector Backend 增量同步（遵循 Base Skill 第 8.3.6 节）。
   - 验证通过后执行小步提交（Conventional Commits，遵循 Base Skill 第 4.3 节）。
3. 遇到需求模糊点 MUST 转入 `WAIT_USER` 并记录到 `plan.md`，不得自行假设。

### Phase 4：Validate（验证） — `IMPLEMENTING → VERIFYING`

执行 Base Skill 第 11 节验证流水线 + 第 8 节 Acceptance Criteria 逐项检查。两者都通过才算完成。

### Phase 5：Review（审查） — `VERIFYING → REVIEW`

1. 执行 `git diff` 审查变更，确认无意外修改。
2. 敏感信息检查：确认无硬编码密钥、密码、Token；若有 MUST 立即停止并告知用户。
3. 按影响范围同步文档（见 3.2）。
4. 使用 Conventional Commits 执行 `git commit`。

### Phase 6：Finalize（收尾） — `REVIEW → COMMITTING → DONE`

1. 按影响范围更新 `readme.md`、`tree.md`（如涉及）。
2. 更新 `plan.md`：完成项 `- [ ]` 改为 `- [x]`，记录 Acceptance 结果与剩余问题。
3. 确认所有改动已纳入 Git 控制。
4. 输出交付报告（见第 9 节），状态置为 `DONE`。

> **Plan 持久化**：Analyze 创建/更新计划，Implement 更新进度，Finalize 记录验收与剩余问题；任务中断时 MUST 确保 `plan.md` 保存当前状态（遵循 Base Skill 第 2.4 节）。

---

## 7. Feature-specific Impact Analysis（影响分析）

影响分析是 Feature Change 特有步骤，流程：

```
需求
↓
确定涉及符号
↓
Code Graph impact
↓
Blast Radius
↓
Scope
↓
Plan
```

执行规则：

1. 完成需求分析后，确认涉及的符号（类 / 函数 / 接口）。
2. 调用 Base Skill 第 9 节的 Code Graph Protocol。
3. 执行 impact / callers / callees / deps 查询。
4. 根据结果确定 Feature Scope 与 Blast Radius。

### Feature-specific Override

```
Base:
风险等级与处理要求遵循 Base Skill 第 6.1 节。

Override:
已有项目场景下：
- L2（模块级）及以上修改 MUST 执行本节影响分析。
- L3 / L4 风险 MUST 确认 Blast Radius。
```

---

## 8. Feature-specific Acceptance Criteria（验收标准）

Analyze 阶段 MUST 在 `plan.md` 建立：

```
## Acceptance Criteria

- [ ] <验收条件 1>
- [ ] <验收条件 2>
```

Finalize 阶段 MUST 逐项检查并标记通过 / 未通过。

完成标准 = Base Validation Protocol 通过 + 全部 Acceptance Criteria 通过。

---

## 9. Delivery Report（交付报告）

修改交付 MUST 满足：

- 需求完整实现且行为符合预期。
- Base Validation + Acceptance Criteria 全部通过。
- 文档按影响范围同步，内容一致。
- Git 提交历史清晰，变更可独立回溯。
- 无敏感信息残留。

报告模板遵循 Base Skill 第 12 节，并追加：

```
## Acceptance Criteria 结果

（逐项列出验收条件及通过 / 未通过状态）
```

---

## 10. Protocol References（协议引用索引）

| 主题 | 行为 | 位置 |
| --- | --- | --- |
| Git / Conventional Commits / 破坏性操作 | 直接遵循 | Base Skill 第 4 节 |
| Agent State | 直接遵循 | Base Skill 第 5 节 |
| Risk Level / Before Snapshot | 直接遵循 | Base Skill 第 6 节 |
| Decision Log | 触发时按格式记录 | Base Skill 第 6.3 节 |
| Knowledge Query Priority | 直接遵循 | Base Skill 第 8.2 节 |
| Vector Backend | 复用已有 / 遵循初始化与增量同步 | Base Skill 第 8.3 节 |
| Code Graph + Impact Primitives | 影响分析时调用 | Base Skill 第 9 节 |
| Navigation（Progressive Discovery） | 修改前定位使用；支持 L3 例外 | Base Skill 第 10 节 |
| Validation | Base 流水线 + Feature Acceptance | Base Skill 第 11 节 |
| Multi-Agent | 复杂任务可分解，简单任务单 Agent | Base Skill 第 7.1 节 |

### Navigation / Progressive Discovery

- 修改前 MUST 使用 Base Skill 的 Navigation Protocol 定位代码。
- 用户已提供明确文件 / 符号时：允许使用 Base Skill 定义的「直接进入 L3」例外。

### Decision Log 触发（Feature-specific）

若当前 Feature 出现以下情况，按 Base Skill 第 6.3 节格式记录：

- 多种合理实现并存需取舍。
- 影响范围发生变化。
- 需要扩大 / 缩小 Scope。
- 重大兼容性取舍。

### Multi-Agent

- 复杂任务 MAY 按 Base Collaboration Protocol（Base Skill 第 7.1 节）进行任务分解。
- 简单 Feature MUST 保持单 Agent 顺序执行。
- 若当前项目无 Multi-Agent / Worktree 能力，自动退化到单 Agent，不得阻塞任务。
