---
name: knowledge
description: 用于 Obsidian 知识库的 PARA 管理、日记同步、快速捕获和周期性回顾。当需要记录想法、查看往期记录或进行知识整理时触发。不要总结流程！
---

# Knowledge - 个人知识管理飞轮

基于 Obsidian + TELOS 框架的知识管理系统。让 AI 真正理解你、记录你、协助你进化。

## 核心架构 (PARA)

- **00-Inbox** — 临时想法、快速捕获
- **01-Daily** — 每日日记（从 memory/ 同步）
- **02-Projects** — 活跃项目笔记
- **03-Areas** — 长期维护的领域知识
- **04-Resources** — 外部资料、参考库
- **05-Archive** — 归档内容
- **MOC (Map of Content)** — 知识索引

## 指令

### 1. 快速记录
当用户提到想法、灵感或需要记录的内容时：
```bash
knowledge capture "灵感内容"
```

### 2. 同步与日记
每天开始或结束时同步进度：
```bash
knowledge sync              # 同步今日
knowledge daily             # 查看今日日记
knowledge daily 2026-03-07  # 查看指定日记
```

### 3. 搜索与读取
查找历史知识：
```bash
knowledge search "关键词"
knowledge read moc 反思      # 读取 MOC 索引
knowledge read area 长期记忆  # 读取领域知识
```

### 4. 回顾报告
生成总结报告：
```bash
knowledge review daily      # 每日回顾（含昨日反思）
knowledge review weekly     # 每周回顾（本周新增笔记统计）
```

### 5. 系统状态
```bash
knowledge stats             # 查看库统计
knowledge list-moc          # 列出所有索引
```

## 铁律 (Constraints)

1. **单数据源** — 只有 `memory/` 是写入源，Obsidian 是其增强层。
2. **三省吾身** — 每日日记必须包含反思区块。
3. **沉淀至上** — 交互中产生的重要结论，必须通过 `capture` 或更新 `Areas` 笔记来沉淀。
4. **自包裹依赖** — 脚本必须使用 `uv` shebang (`#!/usr/bin/env -S uv run --script`) 管理依赖。
5. **系统 memory flush 响应** — 收到 "Pre-compaction memory flush" 提示时：
   - 先用 `knowledge capture` 沉淀重要内容
   - 再用 `knowledge sync` 同步到 Obsidian
   - **禁止直接编辑文件**
6. **及时记录原则** — **每次完成任务后立即 capture**，不要等系统提示或老板提醒：
   - 完成 Skill 开发 → `knowledge capture "Skill 名称 + 核心功能 + 时间"`
   - 解决复杂问题 → `knowledge capture "问题 + 解决方案 + 教训"`
   - 学到新技巧 → `knowledge capture "技巧 + 应用场景"`
   - 老板的新要求 → `knowledge capture "要求 + 上下文"`
   - **任务完成 → capture → 继续下一个任务**（不是等所有任务完成再记录）

## 示例

### 场景：老板问"我之前的偏好是什么？"
1. `knowledge search "偏好"`
2. `knowledge read moc 老板偏好`
3. 结合读取的内容回答。

### 场景：完成了一个复杂任务
1. `knowledge capture "任务总结：解决了 XX 问题，教训是..."`
2. `knowledge sync` 同步到知识库。

---
*Powered by Python + uv + Typer*
