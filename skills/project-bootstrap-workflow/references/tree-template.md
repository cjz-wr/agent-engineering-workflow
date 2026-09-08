# tree.md Template

> v2.3 — 从 Base Protocol 第 2.3 节提取。文件位于 `.workflow/tree.md`，可直接复制使用。

## 目录结构

```
.
├── src/
│   └── ...
├── tests/
│   └── ...
└── ...
```

## 记录约束

MUST NOT 记录以下内容：

- `node_modules/`、`build/`、`dist/`、`.git/`、`.workflow/` 等依赖、产物与工作流文档目录。
- 临时文件、缓存文件、日志文件。
