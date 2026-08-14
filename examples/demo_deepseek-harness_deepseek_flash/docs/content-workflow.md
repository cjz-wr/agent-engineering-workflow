# 内容工作流文档 — Mini Blog

## 1. 文章生命周期

```
draft ──提交──▶ submitted ──发布──▶ published
  ▲                │    │
  └──取消发布──────┘    └──驳回──▶ rejected ──编辑后重新提交──▶ submitted
```

| 状态 | 含义 | 可见性 |
| --- | --- | --- |
| `draft` | 草稿（新建默认） | 仅作者 / 管理员（非公开路由） |
| `submitted` | 已提交待审核 | 仅作者 / 管理员 |
| `published` | 已发布 | 公开（`GET /posts/{slug}`） |
| `rejected` | 被驳回 | 仅作者 / 管理员 |

状态转换规则（service 层强制）：

- `draft | rejected → submitted`：作者操作（编辑页「提交审核」或 `/posts/{id}/submit`）。
- `submitted → published`：管理员发布（后台或 `ALLOW_USER_PUBLISH=true` 时作者直接发布）。
- `submitted → rejected`：管理员驳回。
- `published → draft`：取消发布（作者 / 管理员），并清空 `published_at`。

## 2. 文章操作入口

| 操作 | 路径 | 权限 |
| --- | --- | --- |
| 我的文章 | `GET /posts/mine` | 登录用户 |
| 写文章 | `GET /posts/new` / `POST /posts` | 登录用户 |
| 编辑 | `GET /posts/{id}/edit` / `POST /posts/{id}` | 作者 / 管理员 |
| 提交审核 | `POST /posts/{id}/submit` | 作者 / 管理员 |
| 删除 | `POST /posts/{id}/delete` | 作者 / 管理员（HTMX 支持） |

## 3. Slug

- 自动生成：小写、`[^a-z0-9]+` 替换为 `-`、去首尾 `-`；中文标题等无 ASCII 内容时回退 `post-<random>`。
- 唯一性：冲突时追加 `-2`、`-3`…（`unique_slug`）。
- 公开路由按 slug 访问已发布文章；非公开状态一律 404。

## 4. 评论工作流

- 登录用户可在已发布文章下发表评论（`POST /posts/{slug}/comments`）。
- HTMX 模式：表单 `hx-post` 提交 → 服务端返回评论卡片 + OOB 表单重置片段 → 评论追加到列表、表单清空（无整页刷新）。
- 删除：作者删自己的评论；管理员删任意评论（`/comments/{id}/delete` 与 `/admin/comments/{id}/delete`，均支持 HTMX）。
- 软删除：`is_deleted = true`，删除后从所有列表隐藏（数据库保留审计痕迹）。

## 5. 管理后台工作流

- Dashboard（`GET /admin`）：文章 / 用户 / 评论总数、待审核数、状态统计、最近文章。
- 文章管理（`GET /admin/posts`）：发布 / 驳回 / 取消发布 / 删除，操作经 HTMX 局部刷新行。
- 评论管理（`GET /admin/comments`）：删除任意评论。
- 用户管理（`GET /admin/users`）：停用 / 启用、调整角色（user / admin）；不能停用自己、不能取消自己的管理员角色。

## 6. 编辑体验

- Markdown 原文编辑 + 实时预览（marked.js + DOMPurify），支持 编辑 / 预览 / 分屏 三种模式（Alpine.js）。
- Slug 实时建议；状态 Badge；保存草稿 / 提交审核 / 直接发布（按权限）/ 取消发布 按钮。
- 文章详情页：阅读进度条、代码块一键复制、返回顶部、评论区。
