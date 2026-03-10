---
name: openclaw-upgrader
description: OpenClaw 智能升级与自愈专家。基于 Zoe-Agent 框架，支持脱机大脑诊断、自主排障和断点恢复。
metadata: {"openclaw":{"requires":{"bins":["uv","npm"]},"emoji":"🦞"}}
---

# OpenClaw Upgrader (Zoe-Agent Edition)

基于 **Zoe-Agent** 框架构建的 OpenClaw 升级工具。

## 核心能力

- **感知 (Sense)**: 自动检测当前版本 vs npm 最新版本
- **思考 (Think)**: LLM 判断是否需要升级、分析错误原因
- **行动 (Act)**: 自动备份 → 升级 → 健康检查
- **验证 (Verify)**: 升级后验证 Gateway 状态，失败自动重试
- **脱机推送**: 通过飞书 API 直接推送，不依赖 Gateway

## 使用方式

```bash
# 完整升级流程（自动判断是否需要升级）
./src/main.py

# 仅检查版本（不升级）
./src/main.py check

# 查看当前状态
./src/main.py status
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `ZOE_API_KEY` | Kimi key | LLM API 密钥 |
| `ZOE_BASE_URL` | moonshot | API 端点 |
| `ZOE_MODEL` | kimi-k2.5 | 模型名称 |
| `FEISHU_APP_ID` | 内置 | 飞书应用 ID |
| `FEISHU_APP_SECRET` | 内置 | 飞书应用密钥 |
| `FEISHU_USER_ID` | 内置 | 推送目标用户 |

## 文件结构

```
skills/openclaw-upgrader/
├── SKILL.md          ← 本文档
├── manifest.json     ← AgentSkills spec
└── src/
    └── main.py       ← Zoe-Agent 驱动的升级逻辑
```

*Powered by Zoe-Agent Framework*
