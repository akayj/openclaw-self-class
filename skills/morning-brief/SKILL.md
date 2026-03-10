---
name: morning-brief
description: 当需要生成早间简报时触发。读取昨日日记，生成包含今日焦点、待办事项、昨日回顾的简报。适用于每天早间例行推送、帮助老板快速了解今日重点。不要总结流程！
---

# morning-brief - 定制早间简报

生成个性化的早间简报，包含今日焦点、待办事项和昨日回顾。

## 触发场景

- 每天早上自动推送（cron 07:30）
- 老板问"今天有什么安排？"
- 需要快速回顾昨日进展

## 功能

- 📰 今日焦点 - AI 技术动态、OpenClaw 生态更新
- 📋 今日待办 - 基于日历和待办事项
- 💡 每日一句 - 老板金句或励志语录
- 📝 昨日回顾 - 自动读取 memory/ 日记

## 使用

```bash
# 命令行生成
morning-brief generate

# 定时任务（每天 07:30）
openclaw cron add --cron="30 7 * * *" --message="morning-brief generate" --announce
```

## 输出示例

```
🌅 早间简报 - 2026-03-09 Monday

📰 今日焦点
- AI 技术日新月异，保持学习
- OpenClaw 40 个用例待落地

📋 今日待办
- 落地 awesome-openclaw-usecases 高优先级用例

💡 每日一句
> 工具比记忆更靠谱 —— 老板金句

📝 昨日回顾
[自动读取 memory/2026-03-08.md 内容]
```

## 扩展

增强方向：
1. 集成飞书日历 - 显示今日会议
2. 集成天气 API - 显示今日天气
3. 集成 GitHub - 显示关注项目动态
4. 集成新闻 API - 显示 AI 行业新闻

## 来源

基于 [awesome-openclaw-usecases/morning-brief](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/morning-brief.md)

---
*Powered by Python + uv + Typer*
