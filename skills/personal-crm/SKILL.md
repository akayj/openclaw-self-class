---
name: personal-crm
description: 当需要管理/查询联系人信息时触发。自动从飞书日历和记忆文件提取联系人，支持自然语言搜索、互动统计。适用于维护人脉网络、查找联系人详情、跟踪互动历史。不要总结流程！
---

# personal-crm - 个人 CRM

自动从飞书日历和记忆中提取联系人信息，支持自然语言查询。

## 功能

- 📇 自动从记忆文件提取联系人
- 🔍 自然语言搜索联系人
- 📊 互动统计
- 📅 未来支持飞书日历集成（需邮件权限）

## 安装

```bash
ln -sf /root/.openclaw/workspace/skills/personal-crm/personal_crm.py /usr/local/bin/personal-crm
chmod +x /usr/local/bin/personal-crm
```

## 使用

```bash
# 更新联系人数据库（从记忆文件提取）
personal-crm update

# 搜索联系人
personal-crm search 老板
personal-crm query 余剑

# 显示所有联系人
personal-crm list

# 统计信息
personal-crm stats
```

## 输出示例

```
📇 找到 1 个联系人:

👤 余剑剑 (老板)
   首次联系：2026-03-03
   最后联系：2026-03-09
   互动次数：156
   最近备注:
     - 2026-03-09: 老板，我在这呢！刚看到系统提示模型切换到了 qwen3.5-plus
     - 2026-03-08: 老板质问知识管理
```

## 定时任务

```bash
# 每天 6AM 自动更新联系人
openclaw cron add --cron="0 6 * * *" --message="personal-crm update"
```

## 未来扩展

1. **飞书日历集成** - 需要 `calendar:calendar:readonly` 权限
2. **飞书邮件集成** - 需要 `mail:mailbox:readonly` 权限
3. **关系图谱** - 可视化联系人关系网络

## 来源

基于 [awesome-openclaw-usecases/personal-crm](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/personal-crm.md)
