# 认证与授权文档 — Mini Blog

## 1. 认证方式

Session Cookie 会话认证：

1. 用户提交用户名 / 密码。
2. 服务端以 PBKDF2-HMAC-SHA256 校验密码哈希（`app/security.py`）。
3. 校验通过后，Starlette `SessionMiddleware` 将 `{"user_id": <id>}` 签名后写入 Cookie（`itsdangerous` 签名，密钥来自 `SECRET_KEY`）。
4. 后续请求：`get_current_user` 依赖从 Session 读取 `user_id`，从数据库重新加载用户并校验 `is_active`。

Session 中**不**存用户名 / 角色，角色变更即时生效；账号停用后会话立即失效。

## 2. 密码安全

- 哈希：`pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>`，默认 600,000 次迭代，每用户随机 128-bit 盐。
- 校验：`hmac.compare_digest` 恒定时间比较。
- 明文密码绝不落库、绝不写入日志。

## 3. 环境变量（见 `.env.example`）

| 变量 | 说明 |
| --- | --- |
| `SECRET_KEY` | **必填**；Session 签名密钥，缺失则启动失败。生成：`python -c "import secrets; print(secrets.token_hex(32))"` |
| `ALLOW_USER_PUBLISH` | `false`（默认）仅管理员发布；`true` 时作者可直接发布自己的文章 |

## 4. 授权模型

| 依赖 | 行为 |
| --- | --- |
| `get_current_user` | 解析 Session → 返回 `User \| None` |
| `require_login` | 未登录 → 303 重定向到 `/login?next=<path>` |
| `require_admin` | 非管理员 → 403 |

资源归属校验（service 层）：

- 文章：`post_service.can_manage(user, post)` —— 管理员或作者本人。
- 评论：`comment_service.can_delete(user, comment)` —— 管理员或评论作者。

## 5. 安全要点（对应 readme「Security Notes」）

- 密码不明文存储 ✅（PBKDF2）
- Session Secret 必须通过环境变量配置 ✅（`SECRET_KEY` 必填，`.env` 不入库）
- 服务端权限检查 ✅（依赖注入 + service 归属校验，不依赖前端隐藏按钮）
- 草稿 / 待审核文章服务端阻止公开访问 ✅（公开路由仅放行 `published`）
- 管理员操作服务端角色校验 ✅（`require_admin` → 403）
- 评论内容服务端校验 ✅（非空校验）
