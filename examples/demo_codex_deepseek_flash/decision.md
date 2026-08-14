# Decision Log

## Decision: 独立 Git 仓库

Date: 2026-08-14

Context: demo2 位于既有外层仓库 `agent-engineering-workflow` 的 examples 目录下，而 readme.md 定位为“从空仓库开始、形成可独立回溯的 Git 工程历史”。

Decision: 在 demo2 目录内执行 `git init`，建立独立仓库与提交历史。

Reason: 满足 readme.md 对独立工程历史的演示要求，避免污染外层仓库；外层仓库将 demo2 视为独立嵌入目录。

Alternatives: 直接使用外层仓库提交。

Rejected: 会与外层仓库历史混杂，无法体现“从空仓库开始”的演进过程。

---

## Decision: Session Cookie 会话实现

Date: 2026-08-14

Context: readme 要求 Session Cookie 会话认证，且明确“不引入无必要依赖”。

Decision: 使用标准库 `hmac` + `base64` + `json` 实现 HMAC-SHA256 签名的会话 Cookie（含过期时间），不引入 itsdangerous 等额外依赖。

Reason: 依赖最小化；HMAC-SHA256 签名 + 过期校验满足局域网项目安全要求。

Alternatives: Starlette SessionMiddleware / itsdangerous 签名库。

Rejected: 需要额外依赖（itsdangerous），且本项目无需服务端会话存储。

---

## Decision: 密码哈希方案

Date: 2026-08-14

Context: readme 要求“密码安全哈希存储”。

Decision: 使用标准库 `hashlib.pbkdf2_hmac("sha256", …, 120000)` + 每用户随机盐，存储格式 `pbkdf2_sha256$<iterations>$<salt>$<hash>`。

Reason: 不引入 passlib/bcrypt 等额外依赖，PBKDF2 是 NIST 认可的 KDF。

Alternatives: bcrypt / argon2。

Rejected: 需要额外原生依赖，增加安装成本；对局域网轻量项目收益有限。

---

## Decision: 管理员引导方式

Date: 2026-08-14

Context: readme 定义了 admin 角色的管理能力，但未说明首个管理员如何产生。

Decision: 提供 `scripts/create_admin.py`（可创建或提升管理员），并在 development-log.md 中说明用法。

Reason: 演示流程需要可用的管理员账号，且不改变既有路由与配置。

Alternatives: 首次注册用户自动成为管理员 / 通过 .env 配置种子管理员。

Rejected: 前者改变公开注册语义，后者引入 readme 未声明的配置项。

---

## Decision: 用户发布权限可配置

Date: 2026-08-14

Context: readme 权限表将“Publish own post”标记为 User 列 `configurable`，且未提供用户发布路由。

Decision: 新增 `ALLOW_USER_PUBLISH` 配置（默认 `false`）；为 `true` 时，作者“提交”操作直接将文章发布，否则提交后由管理员发布。

Reason: 覆盖 configurable 语义且无需新增路由。

Alternatives: 为普通用户新增发布路由。

Rejected: 与 readme 路由表不一致。

---

## Decision: 知识索引后端

Date: 2026-08-14

Context: Base Protocol 要求建立 Vector Storage Backend；当前环境无 MCP 资源，Python 本地向量后端需要安装重型依赖。

Decision: 采用 Markdown fallback，维护 `docs/knowledge/folder_summary.md` 与 `docs/knowledge/file_summary.md`。

Reason: readme 与协议均要求最小依赖；项目无语义检索场景。

Alternatives: 安装 chromadb 等本地向量库。

Rejected: 引入与项目无关的重依赖，违背最小依赖原则。

