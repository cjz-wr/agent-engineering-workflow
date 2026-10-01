# 文档索引

> 本目录存放**说明与业务文档**。工作流文档（需求、计划、AI 规范、目录说明、决策日志）统一位于项目根 `.workflow/`，两者 MUST NOT 混放。
>
> 协议规则的唯一事实来源：[`base-protocol.md`](../skills/project-bootstrap-workflow/references/base-protocol.md)。

---

## 文档

| 文档 | 内容 | 适合场景 |
| --- | --- | --- |
| [为什么选择 Agent Engineering Workflow](why-agent-engineering-workflow.md) | 价值说明与对比分析：市场全景、与 spec-kit / BMAD 等主流方案的逐项对比、真正的差异化、创新性、生态地位、优势、实机验证、适用边界与选型建议 | 选型 / 宣传 / 向团队介绍 |
| [Architecture](architecture.md) | 两个 Skill 与共享 Base Protocol 的协作方式与设计原则 | 想理解设计取舍 |
| [Protocol Overview](protocol-overview.md) | 协议要点速览（Git / State / Risk / Knowledge / Vector / Code Graph / Navigation / Validation） | 快速了解能力 |
| [Agent State Machine](state-machine.md) | 9 个正常状态 + 2 个异常状态及其转换规则 | 想了解流程控制 |
| [Base Engineering Protocol](../skills/project-bootstrap-workflow/references/base-protocol.md) | 完整协议（12 章，约 600 行）—— **唯一事实来源** | 需要权威规则 |

## 相关目录

| 目录 | 内容 |
| --- | --- |
| [`../README.md`](../README.md) / [`../README.zh-CN.md`](../README.zh-CN.md) | 项目总览、安装与快速开始 |
| [`../skills/`](../skills) | 两个可安装 Workflow Skill 及其协议与模板 |
| [`../simplePrompt/`](../simplePrompt) | 轻量提示词版（低上下文开销） |
| [`../examples/`](../examples) | 示例项目，含两个可运行的真实产物 |
| [`../scripts/`](../scripts) | 结构校验与本地安装脚本 |

---

## 建议阅读顺序

1. 读 [`../README.zh-CN.md`](../README.zh-CN.md) 了解项目定位与安装方式；
2. 选型阶段读[为什么选择 Agent Engineering Workflow](why-agent-engineering-workflow.md)；
3. 想理解设计读 [Architecture](architecture.md)；
4. 需要权威规则时直接查 [Base Engineering Protocol](../skills/project-bootstrap-workflow/references/base-protocol.md)。

## 维护约定

- 本索引 MUST 与 `docs/` 实际内容保持同步：新增 / 删除 / 重命名文档时同步更新表格。
- 说明性文档 MUST NOT 复制协议正文；需要引用规则时直接链接 `base-protocol.md`，避免出现第二份会漂移的规则来源。
