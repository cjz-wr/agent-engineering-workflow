# folder_summary

> 目录职责摘要。增量维护，仅更新受影响部分。

| 目录 | 职责 |
| --- | --- |
| `app/` | 应用主包：入口、配置、数据库、模型、仓储、服务、路由、模板、静态资源 |
| `app/models/` | SQLAlchemy ORM 模型（User / Post / Comment） |
| `app/repositories/` | 数据访问层（查询 / 写入封装） |
| `app/services/` | 业务逻辑层（认证、会话、文章、评论） |
| `app/routes/` | HTTP 路由层（auth / public / posts / comments / admin） |
| `app/templates/` | Jinja2 页面模板 |
| `app/static/` | 静态资源（CSS / JS） |
| `tests/` | pytest 测试（认证 / 文章 / 评论 / 权限 / 路由） |
| `docs/` | 项目文档与知识索引 |
| `scripts/` | 开发辅助脚本（create_admin.py） |

