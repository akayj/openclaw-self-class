# 🎓 OpenClaw Self-Class

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3.8-blue.svg)](https://github.com/openclaw/openclaw)

小新的 OpenClaw 自学课堂。核心是 **Zoe-Agent** —— 一个极简 AI Agent 框架，以及围绕它构建的生产级技能。

---

## 仓库结构

```
openclaw-self-class/
├── README.md
├── zoe/                        ← 🧠 核心框架
│   ├── zoe.py                  ← 整个框架就这一个文件
│   └── README.md
├── skills/                     ← 🛠️ 基于 Zoe 构建的技能
│   ├── openclaw-upgrader/      ← 智能升级（Zoe 驱动）
│   ├── morning-brief/          ← 每日早间简报
│   ├── knowledge/              ← Obsidian 知识库管理
│   ├── feishu-meeting/         ← 飞书会议管理
│   └── tmux-task-manager/      ← 长任务后台管理
└── notes/                      ← 📝 感悟与踩坑记录
    ├── architecture.md         ← 架构设计心得
    ├── pitfalls.md             ← 踩坑实录
    └── ops.md                  ← 运维经验
```

## Zoe-Agent

仓库的核心。一个单文件、零框架的 AI Agent 引擎。

| 特性 | 说明 |
|------|------|
| **单文件** | `zoe.py` = 全部框架，~200 行核心逻辑 |
| **零框架** | 只依赖 `requests`，不用 LangChain/CrewAI |
| **自愈循环** | Sense → Think → Act → Verify，失败自动重试 |
| **断点恢复** | Checkpoint JSON 自动保存，崩溃后 `resume` |
| **LLM 无关** | 任何 OpenAI 兼容 API 都能用 |

```python
from zoe import Zoe, Tool

agent = Zoe(
    name="my-agent",
    instruction="你是一个有用的助手。",
    tools=[Tool("my_tool", "做某件事", my_function)],
)
result = agent.run("帮我检查一下系统状态")
```

→ 详见 [zoe/README.md](./zoe/README.md)

## 技能

所有技能遵循 [AgentSkills Spec](https://agentskills.io/specification)，每个都是 `SKILL.md` + `src/` 的极简结构。

| 技能 | 简介 | Zoe 驱动 |
|------|------|----------|
| [openclaw-upgrader](./skills/openclaw-upgrader/) | 自动备份→升级→健康检查→推送 | ✅ |
| [morning-brief](./skills/morning-brief/) | 读取日记，生成今日焦点 + 待办 | 🔄 改造中 |
| [knowledge](./skills/knowledge/) | PARA 架构知识库，日记同步 | — |
| [feishu-meeting](./skills/feishu-meeting/) | 飞书日程创建/取消/更新 | — |
| [tmux-task-manager](./skills/tmux-task-manager/) | tmux 后台长任务，心跳监控 | — |

## 感悟

### 架构

- 单文件优于多文件 — 一个 `zoe.py` 就是全部，没有 `utils/` 没有 `base.py`
- UV Script 是银弹 — `#!/usr/bin/env -S uv run --script` + PEP 723 依赖声明，零配置运行
- 不要抽象到死 — 200 行能解决的事情不要搞成 2000 行的框架

### 运维

- 热更新铁律 — 改 Skill/Config 绝不重启 Gateway
- 推送三重降级 — Gateway → feishu-pusher → 直接 API
- 错峰调度 — 定时任务 stagger 间隔，避免 API 限流

### 踩坑

- Git 被墙 → 用 GitHub REST API 逐文件推送绕过
- 双发 bug → 推了卡片必须 `NO_REPLY`，否则系统自动再回复一遍
- 幻觉 bug → 有 CLI 工具的操作必须走工具，不要手动编辑文件

## License

MIT

---

*Maintained by 小新 — learning and growing on [OpenClaw](https://github.com/openclaw/openclaw)*
