# Agent State Machine

> v2.2.0 — 说明文档，不改变协议。

## 正常流程

```
INIT
↓
ANALYZE
↓
PLAN_READY
↓
PREPARE
↓
IMPLEMENTING
↓
VERIFYING
↓
REVIEW
↓
COMMITTING
↓
DONE
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

## 异常状态

```
WAIT_USER
FAILED
```

| 状态 | 含义 | 进入条件 | 恢复方式 |
| --- | --- | --- | --- |
| `WAIT_USER` | 等待用户输入 | 需求模糊、冲突或需确认 | 明确向用户提问后等待 |
| `FAILED` | 失败终止 | 验证无法通过且无法修复 | 输出失败报告，等待用户决策 |

## 转换规则

- 每次进入新状态 MUST 在 `plan.md` 更新当前状态标记。
- 遇到需求模糊点 MUST 转入 `WAIT_USER`，MUST NOT 自行假设后继续。
- 验证失败且无法修复 MUST 转入 `FAILED` 并输出失败报告。
- 任何异常状态下 MUST NOT 执行 `git commit`。
