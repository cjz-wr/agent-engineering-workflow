# decision.md — 关键工程决策日志

> 依据 Base Engineering Protocol v2.2 第 6.3 节维护。涉及技术方案选择、新依赖引入、架构调整、数据结构变化时追加。

---

## Decision

Date: 2026-08-13

Context: 项目根目录与目录结构的确定。`readme.md` 中给出的结构树以 `mini-blog/` 为项目根，但工作区根目录（`D:\code\deepseek_H\demo`）即存放 `readme.md`。

Decision: 将工作区根目录视为项目根目录，全部工程文件（`app/`、`tests/`、`docs/`、`plan.md`、`tree.md`、`AGENTS.md`、`decision.md` 等）直接建于工作区根下；`readme.md` 中的 `mini-blog/` 即指本项目根。

Reason: 技能协议要求「唯一需求来源：项目根目录下的 readme.md」，readme.md 位于工作区根；再嵌套一层 `mini-blog/` 会让需求文档脱离项目根，且无必要。

Alternatives: 在 `demo/mini-blog/` 下创建完整子项目。

Rejected: 嵌套目录使 readme.md 与项目分离，增加一层无意义路径；被否决。

---

## Decision

Date: 2026-08-13

Context: 知识索引 Backend 选型（协议 8.3）。项目为演示型内容平台，`readme.md` 未要求任何向量检索 / 知识库能力。

Decision: 采用 Markdown fallback 维护 `folder_summary` / `file_summary` 知识索引，Vector Backend 状态记录为 `degraded`。

Reason: 当前会话无可用 MCP Vector Backend（UNAVAILABLE）；Python 本地向量后端虽可行（Python 3.11.9 可用），但安装向量检索依赖将违反协议 3.1「依赖修改规则」（仅安装需求明确要求或实现必需的依赖）与 8.3.9「安装安全策略」的最小依赖原则——知识索引是 Agent 工具，不是产品需求。

Alternatives: MCP Vector Backend（不可用）；Python Local Vector Backend（chromadb 等，需引入与产品无关的依赖）。

Rejected: Python 向量后端 —— 为 Agent 知识检索引入非产品依赖，与「不得为少量代码引入额外依赖」冲突，且本任务为文档型索引，Markdown fallback 足够。

---

## Decision

Date: 2026-08-13

Context: 密码安全哈希方案（`readme.md` 要求「密码安全哈希存储」）。

Decision: 使用标准库 `hashlib.pbkdf2_hmac` 实现 PBKDF2-HMAC-SHA256（每用户随机盐 + 可配置迭代次数，默认 600,000；`hmac.compare_digest` 防时序攻击），不引入 passlib / bcrypt。

Reason: 零额外依赖即满足安全哈希要求；passlib 已停止维护且与新版 bcrypt 存在兼容问题，bcrypt 为原生扩展依赖。

Alternatives: passlib[bcrypt]、argon2-cffi。

Rejected: passlib —— 未维护，引入额外风险；argon2 —— 原生扩展依赖，演示项目无必要。

---

## Decision

Date: 2026-08-13

Context: 会话认证实现方式（`readme.md` 要求 Session Cookie 会话认证，且「Session Secret 必须通过环境变量配置」）。

Decision: 使用 Starlette `SessionMiddleware`（其签名机制依赖 `itsdangerous`），`SECRET_KEY` 为必填环境变量（缺失则应用启动失败），Session 仅存 `user_id`，每次请求由服务端重新加载用户并校验 `is_active`。

Reason: 会话签名由成熟中间件承载，避免手写 HMAC 方案的边界问题；不存用户名/角色于 Cookie，角色变更即时生效。

Alternatives: 自研 HMAC 签名 Cookie；JWT。

Rejected: JWT —— 无状态但吊销困难，与「服务端必须执行权限检查」的服务器校验模型不符。

---

## Decision

Date: 2026-08-13

Context: `readme.md` 权限表中「Publish own post: configurable」。

Decision: 增加环境变量 `ALLOW_USER_PUBLISH`（默认 `false`）：关闭时仅管理员可发布，作者提交后由管理员发布/驳回；开启时作者可直接发布自己的文章。

Reason: 将「configurable」固化为可配置项，默认按审核制执行，符合内容平台的常规审核工作流。

Alternatives: 固定为作者不可发布；固定为作者可发布。

Rejected: 两种固定值均无法覆盖「configurable」语义。

---

## Decision

Date: 2026-08-13

Context: 文章生命周期状态机（`readme.md`：draft → submitted → published / rejected）。

Decision: `Post.status` 取值 `draft` / `submitted` / `published` / `rejected`；状态转换在 service 层强制校验：`draft|rejected → submitted → published`，`published → draft`（取消发布），驳回由管理员执行；公开路由仅放行 `published`。

Reason: 状态机集中校验避免非法跳转；`published_at` 仅在发布时写入、取消发布时清空，保证公开列表排序稳定。

Alternatives: 单表布尔 is_published；枚举类型。

Rejected: 布尔标志无法表达 submitted/rejected 中间态；DB 枚举在 SQLite 上缺乏原生支持，字符串常量 + service 校验更简单。

---

## Decision

Date: 2026-08-13

Context: 路由表之外的必需端点（`readme.md` 要求「登录用户可以创建文章、管理自己的文章」）。

Decision: 增加 `GET /posts/mine`（我的文章列表，含全部状态）；管理后台在 `GET /admin/users` 之外增加 `POST /admin/users/{id}/toggle-active` 与 `POST /admin/users/{id}/role`。

Reason: 「管理自己的文章」需要入口；「管理用户」需要可执行的动作，只读列表不构成管理。

Alternatives: 不加端点，仅靠编辑页 URL 直达（无入口，不可用）。

Rejected: 无入口方案不可用；已在 `tree.md` 与 `AGENTS.md` 中记录差异。

---

## Decision

Date: 2026-08-13

Context: 新增依赖记录（协议 3.1 要求）。

Decision: 引入以下依赖并记录用途：

| 依赖 | 版本 | 用途 | 为何不能使用已有依赖 |
| --- | --- | --- | --- |
| fastapi | >=0.110 | Web 框架（路由 / 依赖注入 / 模板） | 需求指定 |
| uvicorn[standard] | >=0.29 | ASGI 服务器（含 watchfiles 热重载） | 需求指定 |
| jinja2 | >=3.1 | 服务端模板渲染（SSR） | 需求指定 |
| sqlalchemy | >=2.0 | ORM / 数据访问 | 需求指定 |
| pydantic-settings | >=2.0 | `.env` 配置加载（Pydantic 生态） | 需求要求 Pydantic 配置 |
| python-multipart | >=0.0.9 | 解析表单数据（FastAPI 必需） | FastAPI 表单依赖 |
| itsdangerous | >=2.1 | Session Cookie 签名（Starlette SessionMiddleware 依赖） | 会话签名必需 |
| pytest / httpx | >=8 / >=0.27 | 测试框架 / TestClient 传输层（需求指定） | dev 依赖 |

Alternatives: 配置加载用 python-dotenv（无 Pydantic 校验，放弃）；会话自研 HMAC（边界多，放弃）。

Rejected: python-dotenv —— 无类型校验与默认值能力，pydantic-settings 更贴合技术栈。

---

## Decision

Date: 2026-08-13

Context: 前端无构建链方案（`readme.md` 明确「不引入 Vite / Webpack 等重型前端构建链」）。

Decision: Tailwind CSS 使用 Play CDN；HTMX / Alpine.js / Lucide / marked.js / DOMPurify 全部通过 CDN 引入；`marked.parse` 输出经 DOMPurify 消毒后注入。

Reason: 零构建步骤符合「SSR + Progressive Enhancement」定位；DOMPurify 缓解 marked 不消毒 HTML 的 XSS 风险。

Alternatives: Tailwind 预编译（需 Node 构建链）；Python 端 markdown 渲染（引入新后端依赖）。

Rejected: Tailwind 预编译违反「无重型前端工程链」；服务端 markdown 渲染与 readme 前端技术清单（marked.js）不符。

---

## Decision

Date: 2026-08-13

Context: 演示环境需要便捷的管理员引导方式（用户直接要求）。`readme.md` 定义了 admin 角色与权限，但未规定管理员如何产生。

Decision: 两条引导路径：(1) 注册逻辑 —— 数据库为空（首个账号）时，注册用户自动成为 `admin`，之后注册的用户保持 `user`；(2) 提供一键提升脚本 `promote_admin.py` / `promote_admin.bat`（幂等，可将任意已有用户提升为 `admin`，用户名不存在时报错）。

Reason: 全新安装零操作即可获得管理员，符合演示场景；已有数据库（如先注册了普通用户）可通过脚本提升，无需手工改库；脚本幂等可反复执行。

Alternatives: 内置固定管理员账号；手工 SQL 更新 users 表。

Rejected: 内置账号 —— 硬编码凭据违反「密码/密钥不入库、不硬编码」的安全约束；手工 SQL —— 易错且对非技术使用者不友好。
