---
name: idea-validator
description: 当老板有新创意/项目想法时触发。在开始构建任何新项目前，自动检查 GitHub/HN/npm/PyPI 是否已有类似解决方案，计算 reality_signal 分数，提供差异化建议。不要总结流程！
---

# idea-validator - 创意验证器

在开始构建任何新项目前，自动检查是否已有类似解决方案。

## 功能

- 🔍 搜索 GitHub（按 star 排序）
- 📰 搜索 Hacker News 讨论
- 📦 搜索 npm 包
- 🐍 搜索 PyPI 包
- 📊 计算 `reality_signal` 分数 (0-100)
- 💡 提供差异化建议

## 安装

```bash
# 已预装在 /root/.openclaw/workspace/skills/idea-validator/
ln -sf /root/.openclaw/workspace/skills/idea-validator/idea_validator.py /usr/local/bin/idea-validator
chmod +x /usr/local/bin/idea-validator
```

## 使用

```bash
# 命令行
idea-validator "AI code review tool"
idea-validator "MCP server for idea validation"

# 在 OpenClaw 中
!idea-validator <你的创意>
```

## 输出示例

```
🔍 验证创意：AI code review tool

📊 reality_signal: 90/100
⚠️  空间非常拥挤，建议重新考虑或寻找差异化角度

🐙 GitHub Top Competitors:
  1. reviewdog/reviewdog - ⭐9,104 - Automated code review tool
  2. danger/danger - ⭐5,649 - Stop saying "you forgot to…" in code review

💡 差异化建议:
  - 聚焦特定语言/框架
  - 针对特定行业/场景
  - 做现有工具的插件/扩展
```

## 决策规则

| reality_signal | 建议 |
|----------------|------|
| > 70 | ⚠️ STOP - 空间拥挤，需差异化 |
| 30-70 | ⚡ 谨慎 - 找到独特定位 |
| < 30 | ✅ 开放 - 可以构建 |

## 来源

基于 [awesome-openclaw-usecases/pre-build-idea-validator](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/pre-build-idea-validator.md)
