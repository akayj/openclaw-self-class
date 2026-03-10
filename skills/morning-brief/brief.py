#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx", "rich", "typer"]
# ///

"""
定制早间简报 - 增强版
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

app = typer.Typer()
console = Console()

WORKSPACE = Path(os.getenv("OPENCLAW_WORKSPACE", Path.home() / ".openclaw/workspace"))
MEMORY_DIR = WORKSPACE / "memory"

@app.command()
def generate():
    """生成今日早间简报"""
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d %A")
    
    # 读取昨日日记
    yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    diary_path = MEMORY_DIR / f"{yesterday}.md"
    yesterday_summary = ""
    if diary_path.exists():
        content = diary_path.read_text()[:1000]
        yesterday_summary = f"\n\n📝 **昨日回顾**\n{content[:500]}..."
    
    brief = f"""# 🌅 早间简报 - {date_str}

## 📰 今日焦点
- AI 技术日新月异，保持学习
- OpenClaw 40 个用例待落地

## 📋 今日待办
- 落地 awesome-openclaw-usecases 高优先级用例

## 💡 每日一句
> 工具比记忆更靠谱 —— 老板金句
{yesterday_summary}
"""
    
    console.print(Panel(Markdown(brief), title="🌅 早间简报"))
    
    output_path = WORKSPACE / f"brief-{today.strftime('%Y-%m-%d')}.md"
    output_path.write_text(brief)
    console.print(f"\n✅ 简报已保存：{output_path}")

if __name__ == "__main__":
    app()
