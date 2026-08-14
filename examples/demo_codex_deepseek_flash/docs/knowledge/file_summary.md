# file_summary

> 文件职责摘要。增量维护，仅更新受影响部分。

| 文件 | 职责 |
| --- | --- |
| `readme.md` | 产品需求来源（用户提供，不可修改） |
| `AGENTS.md` | AI 开发规范 |
| `plan.md` | 开发计划与进度 |
| `tree.md` | 目录结构说明 |
| `decision.md` | 关键工程决策日志 |
| `pyproject.toml` | 项目元数据、依赖与工具配置 |
| `app/main.py` | FastAPI 应用入口（路由注册、静态资源、启动初始化） |
| `app/config.py` | 环境配置加载（.env） |
| `app/db.py` | 数据库引擎、会话工厂与依赖注入 |
| `app/models/user.py` | User ORM 模型（角色、激活状态、时间戳） |
| `app/models/post.py` | Post ORM 模型（标题、slug、正文、状态、发布时间） |
| `app/models/comment.py` | Comment ORM 模型（软删除标记、关联文章与作者） |
| `app/repositories/user.py` | 用户数据访问（按用户名/ID 查询、创建、列表、角色与状态更新） |
| `app/repositories/post.py` | 文章数据访问（按 slug/ID 查询、创建、按状态/作者列出、统计、删除） |
| `app/repositories/comment.py` | 评论数据访问（创建、按文章列出、软删除、统计） |
| `app/services/session.py` | HMAC 签名会话 Cookie（编码/解码、SessionBox 变更与应用） |
| `app/services/auth.py` | 认证业务（PBKDF2 密码哈希、注册、登录校验） |
| `app/dependencies.py` | 共享依赖（当前用户、require_user / require_admin 守卫） |
| `app/templating.py` | Jinja2 模板、Markdown 过滤、状态 Badge 帮助函数 |
| `app/routes/auth.py` | 认证路由（/register /login /logout） |
| `app/services/post.py` | 文章业务（slug 生成与唯一性、生命周期、越权校验） |
| `app/routes/posts.py` | 文章路由（/posts/new、/posts、/posts/{id}/edit、submit、delete） |
| `app/services/comment.py` | 评论业务（内容校验、作者/管理员删除权限） |
| `app/routes/comments.py` | 评论路由（发表、删除；HTMX 片段返回） |
| `app/routes/public.py` | 公开路由（首页列表、文章详情、仅发布文章可见） |
| `app/routes/admin.py` | 管理路由（仪表盘、文章发布/驳回/取消/删除、评论与用户管理） |
| `app/templates/admin/dashboard.html` | 管理仪表盘（统计卡片、状态分布、最近评论） |
| `app/templates/admin/posts.html` | 文章管理页 |
| `app/templates/admin/comments.html` | 评论管理页 |
| `app/templates/admin/users.html` | 用户管理页（角色、启用/禁用） |
| `app/templates/components/admin_post_row.html` | 管理文章行组件（HTMX 发布/驳回/取消/删除） |
| `app/templates/public/home.html` | 首页（hero 渐变动态标题 + 已发布文章卡片网格） |
| `app/templates/public/post_detail.html` | 文章详情页（Markdown 正文、评论、阅读进度、返回顶部） |
| `app/templates/components/post_card.html` | 文章卡片组件 |
| `app/templates/404.html` | 404 错误页 |
| `app/static/js/main.js` | 前端脚本（Lucide、代码复制、阅读进度、返回顶部） |
| `app/static/css/style.css` | 自定义样式（Markdown 排版、复制按钮、动画渐变 hero/流光标题） |
| `scripts/create_admin.py` | 管理员创建/提升脚本（用于演示与运维） |
| `app/templates/components/comment_item.html` | 单条评论组件（HTMX 删除） |
| `app/templates/components/comment_form.html` | 评论发表表单（HTMX 提交） |
| `app/templates/posts/editor.html` | 文章编辑器（Markdown 编辑/预览、保存/提交/删除） |
| `app/templates/components/status_badge.html` | 文章状态 Badge 组件 |
| `app/templates/components/post_actions.html` | 作者文章操作组件（提交审核，HTMX 刷新） |
| `app/templates/base.html` | 基础页面布局（导航、页脚、脚本） |
| `app/templates/auth/login.html` | 登录页 |
| `app/templates/auth/register.html` | 注册页 |
| `app/templates/components/navbar.html` | 导航栏（登录状态感知） |
| `app/templates/components/flash.html` | 提示消息组件 |
| `app/static/js/main.js` | 前端脚本入口（Lucide 初始化） |
| `app/static/css/style.css` | 自定义样式 |
