# Plan — Mini Blog / LAN Content Platform

> 依据项目根目录 `readme.md`（唯一需求来源）制定，遵循 feature-change-workflow Skill / Base Engineering Protocol。

## 任务列表（历史）

- [x] 需求分析：完整读取 readme.md，提炼功能、路由、权限与测试要求
- [x] 初始化 plan.md 并提交（Phase 1）
- [x] Bootstrap：目录结构、AGENTS.md、.gitignore、pyproject.toml、.env.example、tree.md、decision.md、git init
- [x] feat(db): 初始化数据库模型（User / Post / Comment）与仓储层
- [x] feat(auth): 用户注册 / 登录 / 注销 + Session Cookie 会话
- [x] feat(posts): 文章 CRUD（创建 / 编辑 / 删除 / 草稿）
- [x] feat(posts): 发布工作流（draft → submitted → published / rejected）
- [x] feat(comments): 文章评论（发表 / 删除 / 权限）
- [x] feat(views): 公开页面（首页列表 / 详情 / Markdown 渲染 / 404）
- [x] style(ui): Tailwind 基础 UI（导航 / 卡片 / Badge / Dashboard）
- [x] feat(dynamic): HTMX 异步交互（发布切换 / 删除 / 评论）
- [x] feat(admin): 管理后台（Dashboard / 文章 / 评论 / 用户）
- [x] test(auth): 认证流程测试（已编写，见 tests/）
- [x] test(posts): 文章生命周期测试（已编写，见 tests/）
- [x] test(comments): 评论与权限测试（已编写，见 tests/）
- [x] test(permissions): 跨用户与访客权限测试（已编写，见 tests/）
- [x] test(routes): 路由级测试（已编写，见 tests/）
- [x] docs: architecture / authentication / content-workflow / development-log
- [ ] 补交上一会话遗留：tests/ 提交 + pytest 全量验证记录（并入本功能最终验证）

## 本期功能：界面美化 + 正文编辑体验（2026-08-14）

用户反馈：

> 美化界面，界面过于简单了，并且不能写内容，只能写标题。

### 分析与假设

- 后端与编辑模板已支持正文（content 字段实测可保存、可渲染），用户“只能写标题”的体验问题主要来自：编辑页正文区不够醒目 / 前端资源依赖公共 CDN（局域网或网络受限时样式与交互失效，界面显得简陋）。
- 本功能范围：全面美化 UI + 强化正文编辑器 + 将前端静态资源本地化（离线可用），不改变数据库 / API / 权限语义。
- 设计方向：现代清爽编辑风（indigo/violet 渐变点缀、玻璃拟态导航、卡片式布局、空状态与动效），保持 SSR + 轻量技术栈，不引入重型构建链。

### 任务列表（本期）

- [ ] 前端资源本地化：下载并托管 Tailwind Play CDN、htmx、Alpine.js、Lucide、marked 到 `app/static/vendor/`，`base.html` 改为本地引用
- [ ] 基础布局：`base.html` / `navbar.html` / footer / flash / status_badge 视觉升级
- [ ] 公开页面：首页 hero + 文章卡片（正文摘要、阅读时长、作者头像）+ 详情页排版美化
- [ ] 正文编辑器：工具栏（加粗 / 斜体 / 标题 / 引用 / 代码 / 列表 / 链接）、字数统计、占位提示、编辑/预览/分屏
- [ ] 认证与管理页面：登录 / 注册 / 管理后台 / 表格 / 空状态视觉统一
- [ ] 文档同步：plan.md / tree.md / decision.md / docs/knowledge 增量更新
- [ ] 最终验证：compileall + pytest 全量 + Acceptance Criteria 逐项检查

### Acceptance Criteria（本期）

- [ ] 首页具备现代视觉设计：hero、卡片含正文摘要与阅读时长、空状态友好
- [ ] 文章详情页排版精美：阅读进度、代码复制、返回顶部、评论区样式统一
- [ ] 编辑器正文输入醒目可用：正文输入框显著、占位提示、工具栏、字数统计、实时预览
- [ ] 新建 / 编辑文章时正文可保存并正确渲染（自动化测试覆盖）
- [ ] 前端静态资源全部本地化，页面无 CDN 依赖
- [ ] 登录 / 注册 / 管理后台视觉统一，移动端可用
- [ ] pytest 全量通过、`python -m compileall app tests scripts` 通过
- [ ] plan.md / tree.md / decision.md / docs/knowledge 与代码一致

## 当前 Agent State

ANALYZE（计划就绪后进入 PREPARE → IMPLEMENTING）

## Before Snapshot（本期）

```
commit hash:   34d65d3（chore: track project readme and routes package init）
branch:        feature/ui-polish（自 feature/mini-blog 创建）
modified files: app/templates/**/*.html、app/static/css/style.css、app/static/js/main.js、
                app/static/vendor/*（新增）、app/templating.py、plan.md、tree.md、
                decision.md、docs/knowledge/*
risk level:    L2（模板 + 静态资源 + 模板辅助函数；不涉及数据库 / API / 权限）
```

## 模糊点与待确认项

无阻塞性模糊点。实现层面的默认选择记录于 decision.md：

- “只能写标题”经实测为体验 / 资源加载问题而非后端缺陷：本期通过醒目正文编辑器 + 资源本地化解决。
- 前端资源本地化采用静态 vendor 目录方案（无构建链），版本固定，避免局域网 CDN 不可达。

## Vector Backend Status

Backend: Markdown（markdown-fallback）
Status:  degraded
Environment: Windows；Python 3.11.9（D:\python11\python.exe，已含项目全部依赖）
Index: docs/knowledge/folder_summary.md + docs/knowledge/file_summary.md
Initialization: 2026-08-14
Commit: n/a

Reason:

- MCP：当前环境无可用 MCP 资源（list_mcp_resources 返回空）。
- Python local vector backend：readme.md 明确“不引入无必要依赖”，不安装本地向量库，采用 Markdown fallback。

Attempted:

- MCP（无可用资源）
- Python（检测到 D:\python11，仅用于项目运行依赖，不用于向量后端）

## Acceptance Criteria（历史）

- [x] 项目可安装、可运行（`uvicorn app.main:app`）
- [x] 认证：注册 / 登录 / 注销 / Session 会话
- [x] 文章：CRUD + draft → submitted → published / rejected
- [x] 评论：登录用户可发表 / 删除，管理员可删除任意评论
- [x] 权限：跨用户越权、Guest 访问受保护路由、管理员角色校验均由服务端执行
- [x] 公开路由不得暴露草稿 / 待审核文章
- [x] plan.md / tree.md / AGENTS.md / decision.md 与 readme.md 一致

---

## 本期功能：主页渐变标题动态化（2026-08-14）

用户反馈：

> 主页渐变标题改成动态效果

### 分析与假设

- 首页 hero 区当前为静态渐变背景（`bg-gradient-to-br from-indigo-600 via-violet-600 to-fuchsia-600`）+ 白色标题。
- 本次将 hero 渐变背景改为动态流转，标题改为渐变流光文字，装饰光斑增加漂浮动效；纯 CSS 实现，不引入 JS / 依赖，尊重 `prefers-reduced-motion`。
- 范围：`app/templates/public/home.html` + `app/static/css/style.css`，不涉及后端逻辑 / 数据库 / API / 权限。

### 任务列表（本期）

- [x] hero 渐变背景动态化（CSS `animate-gradient` + `@keyframes gradient-shift`）
- [x] 标题渐变流光文字（CSS `animate-gradient-text` + `@keyframes text-shimmer`）
- [x] hero 装饰光斑漂浮动效（`animate-float` / `animate-float-delay`）
- [x] 减少动态效果偏好适配（`prefers-reduced-motion`）
- [x] 验证：compileall 通过 + 页面视觉确认（浏览器实测动画推进）；pytest 按用户要求跳过
- [x] 文档同步：plan.md / docs/knowledge 增量更新

### Acceptance Criteria（本期）

- [x] 首页 hero 渐变背景随时间平滑流转，视觉效果明显但不过度（浏览器实测 background-position 1.67%→9.66%）
- [x] 首页标题呈现渐变流光效果，文字清晰可读（background-clip: text，流光位置 121%→162%）
- [x] 系统开启“减少动态效果”时动画全部停用（`prefers-reduced-motion: reduce` 下 `animation: none`）
- [~] pytest 全量通过 —— 用户明确要求跳过测试（“不用测试了”）；`python -m compileall app tests scripts` 已通过
- [x] 未引入新依赖、未修改后端逻辑 / 数据库 / API / 权限

### Before Snapshot（本期）

```
commit hash:   6dcd2ad（feature/ui-polish 工作树干净）
branch:        feature/animated-hero-title
modified files: app/templates/public/home.html、app/static/css/style.css、plan.md
risk level:    L1（展示层修改：模板 + CSS；无数据库 / API / 权限变更）
```

### Agent State（本期）

DONE（已完成并提交：`feature/animated-hero-title` 分支；测试按用户要求跳过，交付报告见会话记录）
