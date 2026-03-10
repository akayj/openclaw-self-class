# 🐝 Design: Zoe-Swarm & The Physical Bridge

> **"From a single brain to a global hive. From a screen to the real world."**

Zoe-OS 的终极形态是 **Zoe-Swarm**：一个分布式、跨维度的智能网络。

---

## 🌐 1. The Physical Bridge (Virtual to Physical)

Zoe 必须拥有“肉身”，通过以下路径打通物理世界：

### A. Edge Perception (Sense)
- **Node Sensors**: 通过 OpenClaw `nodes.location_get` 获取位置，通过 `nodes.camera_snap` 获取视觉。
- **MQTT / Webhook**: 订阅来自 ESP32/树莓派的实时数据流。

### B. Physical Action (Act)
- **Home Automation**: 通过 API 调用控制灯光、空调（IoT 代理）。
- **Mobile Interaction**: 通过 `nodes.notify` 向用户发送物理反馈。

---

## 🐝 2. Zoe-Swarm (Distributed Intelligence)

### A. The Intent Bus (广播与发现)
Zoe 实例不再通过硬编码的 IP 连接，而是加入一个 **Semantic Bus**。
- 一个任务被广播为 **"Intent Packet"**。
- 具备相应能力的 Zoe 节点（如拥有 GPU 的、拥有文件写权限的）自动 **"Claim"** 任务。

### B. Hierarchical Collaboration (层级协作)
- **Commander Zoe**: 负责将老板的大目标分解。
- **Worker Zoe**: 在各自的沙箱或物理设备上执行具体工具。
- **Auditor Zoe**: 独立验证结果，确保安全与准确。

---

## 🗺️ Implementation Path (Swarm Ready)

1. **`Zoe.dispatch(target_node, task)`**: 在 Zoe 内核中预留远程调用接口。
2. **`Zoe-Link`**: 一个轻量级的、基于加密 Websocket 的 Peer-to-Peer 通信协议。
3. **`World-Model`**: 一个全局共享的 Key-Value 存储，用于存放 Swarm 的共同记忆。

---

*Drafted by Xiao Xin | Visionary Direction by akayj*
