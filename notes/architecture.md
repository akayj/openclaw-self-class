# 架构设计心得

## 单文件哲学

框架的代码量和它能解决的问题成正比？不是的。

Zoe-Agent 证明了一件事：200 行 Python + `requests` 就能实现一个完整的 Tool-Calling Agent，包括自愈循环和断点恢复。不需要 LangChain 的 30 万行代码。

**原则**：如果你不能在 5 分钟内读完框架源码，那这个框架太重了。

## UV Script 是正确答案

PEP 723 的 `# /// script` 依赖声明 + `#!/usr/bin/env -S uv run --script` shebang = 零配置运行。

不需要 `pip install`，不需要 `requirements.txt`，不需要虚拟环境。`chmod +x && ./script.py` 就跑起来了。

这在 OpenClaw Skill 场景下尤其重要：Skill 可能在任何机器上被加载，不应该假设用户已经装好了依赖。

## Sense-Think-Act-Verify

不是每个 Agent 都需要这个循环。但是当你的任务涉及**外部副作用**（API 调用、文件修改、系统升级）时，Verify 步骤是必须的。

```
不验证：  Action → 祈祷它成功了
要验证：  Action → 读取结果 → 判断是否符合预期 → 不符合就重来
```

后者才是"生产级"。

## 不要过早抽象

刚开始写的时候，我想搞一个 `BaseAgent` + `ToolRegistry` + `StateManager` 的三层架构。后来发现：

- `BaseAgent` 只有一个实现，抽象毫无意义
- `ToolRegistry` 就是个 dict
- `StateManager` 就是 `json.dump` + `json.load`

把它们合并成一个 class，代码量少了 60%，可读性提升了 200%。
