# 🏗️ Architecture: The Zig + Python Dual-Engine

Zoe-OS 采用 **“身脑分离”** 的二元架构，彻底移除 Rust 以追求极致的极简与透明。

---

## 1. 🧬 The Physical Layer (Zig)
- **Role**: Muscle & Reflexes.
- **Components**:
    - **Zoe-Kernel**: 微秒级 PBM 平衡计算。
    - **Zoe-Socket**: 基于内存映射的极速协议插口。
    - **Survival Proxies**: 直接操控文件系统与进程的低级接口。
- **Why Zig?**: Zero hidden control flow. What you see is what you get on the CPU.

## 2. 🧠 The Cognitive Layer (Python)
- **Role**: Intelligence & Reasoning.
- **Components**:
    - **Intent Translator**: 将自然语言任务翻译为 Zoe-Socket 指令。
    - **Swarm Orchestrator**: 协调多个 Zoe 节点的协作逻辑。
    - **Seed Manager**: 记忆切片的检索与 RAG 增强。
- **Why Python?**: Rapid iteration and seamless LLM ecosystem integration.

## 3. Why Zig? (The Hardcore Choice)
我们选择 Zig 而非 Rust 或纯 Python，是因为 Zoe 需要一种**“不带任何隐藏逻辑”**的物理外壳。
- **透明度**：Zig 没有任何隐藏的控制流，每一行代码的代价在 CPU 上都是清晰的。
- **反射弧**：对于 PBM 的实时压力计算，Zig 提供的微秒级响应是系统“自愈”的物理保障。
- **极简即安全**：更少的语言特性意味着更少的未知 Bug。
- **Zoe-Socket**: Python 脑通过 Unix Socket 与 Zig 身通讯。
- **Shared Memory**: 大规模数据交换采用共享内存映射，避免序列化开销。

---

*“Simplicity is not the absence of complexity, but the mastery of it.”*
