# Zoe-Agent

> One file. No framework. Self-healing.

极简 AI Agent 框架。整个引擎就是 `zoe.py` 一个文件。

## 设计来源

| 灵感 | 取了什么 |
|------|----------|
| [SimpleCLI](https://github.com/Zen-Open-Source/SimpleCLI) | 单文件哲学、零框架、5 分钟可读 |
| Pi-Agent | Sense→Think→Act→Verify 循环、断点恢复、自愈重试 |

## 架构

```
  SENSE   →  收集上下文
    ↓
  THINK   →  LLM 决定下一步
    ↓
   ACT    →  执行工具
    ↓
  VERIFY  →  成功？→ Done
    │
    └── 失败 → 退避重试 → 回到 SENSE
```

## 核心 API

```python
from zoe import Zoe, Tool

# 定义工具
def ping(host: str) -> str:
    import subprocess
    r = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True)
    return r.stdout

# 创建 Agent
agent = Zoe(
    name="net-checker",
    instruction="你是一个网络诊断助手。",
    tools=[Tool("ping", "Ping 一个主机", ping)],
    api_key="your-key",
)

# 运行
result = agent.run("检查 8.8.8.8 是否可达")
```

## CLI 模式

```bash
ZOE_API_KEY=sk-xxx ./zoe.py run "你好"
./zoe.py status
./zoe.py resume
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `ZOE_API_KEY` | 必填 | LLM API 密钥 |
| `ZOE_BASE_URL` | moonshot | API 端点 |
| `ZOE_MODEL` | kimi-k2.5 | 模型 |

## 约束

- 只依赖 `requests`
- 只有一个文件
- 任何 OpenAI 兼容 API 都能用
- 不到 300 行
