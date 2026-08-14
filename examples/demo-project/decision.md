# decision.md

## Decision

Date: <YYYY-MM-DD>

Context: 待办数据以内存列表存储，还是持久化到文件。

Decision: 先用内存列表实现，后续按需求持久化。

Reason: 示例项目规模极小，优先验证核心逻辑。

Alternatives: 持久化到 JSON 文件、SQLite。

Rejected: SQLite —— 对当前最小示例引入不必要的存储依赖。
