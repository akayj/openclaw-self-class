#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["rich", "typer"]
# ///

"""
obsidian-review.py - 生成回顾报告

替代原来的 obsidian-review.sh
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

app = typer.Typer()
console = Console()

# 配置
VAULT_DIR = Path.home() / "ObsidianVault"
DAILY_DIR = VAULT_DIR / "01-Daily"
INBOX_DIR = VAULT_DIR / "00-Inbox"

def get_daily_file(date: datetime) -> Path:
    """获取指定日期的日记文件"""
    return DAILY_DIR / f"{date.strftime('%Y-%m-%d')}.md"

def parse_daily_content(content: str) -> dict:
    """解析日记内容，提取关键信息"""
    info = {
        "todos": [],
        "completed": [],
        "reflections": {},
        "captures": []
    }
    
    # 提取待办
    for line in content.split("\n"):
        if line.strip().startswith("- [ ]"):
            info["todos"].append(line.replace("- [ ]", "").strip())
        elif line.strip().startswith("- [x]") or line.strip().startswith("- [X]"):
            info["completed"].append(line.replace("- [x]", "").replace("- [X]", "").strip())
    
    # 提取三省吾身
    reflection_pattern = r"### 三省吾身.*?1\. \*\*做得好的\*\*：(.*?)2\. \*\*做得不好的\*\*：(.*?)3\. \*\*明天改进\*\*：(.*?)(?:---|$)"
    match = re.search(reflection_pattern, content, re.DOTALL)
    if match:
        info["reflections"] = {
            "good": match.group(1).strip(),
            "bad": match.group(2).strip(),
            "improve": match.group(3).strip()
        }
    
    return info

@app.command()
def daily(
    date: Optional[str] = typer.Option(None, "-d", "--date", help="日期 (YYYY-MM-DD，默认昨天)"),
):
    """查看指定日期的日记回顾"""
    
    if date:
        target_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        target_date = datetime.now() - timedelta(days=1)
    
    daily_file = get_daily_file(target_date)
    
    if not daily_file.exists():
        console.print(f"[yellow]日记不存在：{daily_file}[/yellow]")
        return
    
    content = daily_file.read_text(encoding="utf-8")
    info = parse_daily_content(content)
    
    console.print(Panel(
        f"[bold]📅 {target_date.strftime('%Y-%m-%d')} 回顾[/bold]\n\n"
        f"[bold]✅ 已完成 ({len(info['completed'])}):[/bold]\n" +
        "\n".join([f"  • {c}" for c in info['completed'][:5]]) + "\n\n" +
        f"[bold]⏳ 待完成 ({len(info['todos'])}):[/bold]\n" +
        "\n".join([f"  • {t}" for t in info['todos'][:5]]) + "\n\n" +
        (f"[bold]💭 三省吾身：[/bold]\n"
         f"  做得好的：{info['reflections'].get('good', 'N/A')}\n"
         f"  做得不好的：{info['reflections'].get('bad', 'N/A')}\n"
         f"  明天改进：{info['reflections'].get('improve', 'N/A')}" if info['reflections'] else ""),
        title="每日回顾"
    ))

@app.command()
def weekly(
    week: Optional[int] = typer.Option(None, "-w", "--week", help="周数（默认上周）"),
):
    """生成周回顾"""
    
    today = datetime.now()
    
    if week is None:
        # 上周
        start_of_week = today - timedelta(days=today.weekday() + 7)
    else:
        # 指定周
        start_of_year = today.replace(month=1, day=1)
        start_of_week = start_of_year + timedelta(weeks=week-1)
    
    end_of_week = start_of_week + timedelta(days=6)
    
    console.print(f"[bold]📊 {start_of_week.strftime('%Y-%m-%d')} ~ {end_of_week.strftime('%Y-%m-%d')} 周回顾[/bold]\n")
    
    # 收集本周数据
    all_completed = []
    all_todos = []
    reflections = []
    
    for i in range(7):
        date = start_of_week + timedelta(days=i)
        daily_file = get_daily_file(date)
        
        if daily_file.exists():
            content = daily_file.read_text(encoding="utf-8")
            info = parse_daily_content(content)
            all_completed.extend(info["completed"])
            all_todos.extend(info["todos"])
            if info["reflections"]:
                reflections.append(info["reflections"])
    
    # 统计
    table = Table(title="本周统计")
    table.add_column("指标", style="cyan")
    table.add_column("数量", style="green")
    
    table.add_row("日记天数", "7" if len(all_completed) > 0 else "0")
    table.add_row("完成任务", str(len(all_completed)))
    table.add_row("待办任务", str(len(all_todos)))
    table.add_row("有反思", str(len(reflections)))
    
    console.print(table)
    
    # 显示完成的任务
    if all_completed:
        console.print(f"\n[bold]✅ 本周完成的任务 ({len(all_completed)}):[/bold]")
        for c in all_completed[:10]:
            console.print(f"  • {c}")
        if len(all_completed) > 10:
            console.print(f"  ... 还有 {len(all_completed) - 10} 个")

@app.command()
def inbox(
    days: int = typer.Option(7, "-d", "--days", help="最近 N 天"),
):
    """查看 Inbox 捕获统计"""
    
    cutoff = datetime.now() - timedelta(days=days)
    captures = []
    
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        inbox_file = INBOX_DIR / f"{date.strftime('%Y-%m-%d')}.md"
        
        if inbox_file.exists():
            content = inbox_file.read_text(encoding="utf-8")
            # 统计 ## 开头的条目
            entries = len(re.findall(r"^## \d{2}:\d{2}", content, re.MULTILINE))
            captures.append({
                "date": date,
                "entries": entries,
                "size": len(content)
            })
    
    if not captures:
        console.print("[yellow]暂无捕获记录[/yellow]")
        return
    
    table = Table(title=f"📥 最近 {days} 天 Inbox 捕获")
    table.add_column("日期", style="cyan")
    table.add_column("条目数", style="green")
    table.add_column("大小", style="magenta")
    
    total_entries = 0
    for c in captures:
        table.add_row(
            c["date"].strftime("%Y-%m-%d"),
            str(c["entries"]),
            f"{c['size']} bytes"
        )
        total_entries += c["entries"]
    
    console.print(table)
    console.print(f"\n[bold]总计：{total_entries} 条捕获[/bold]")

if __name__ == "__main__":
    app()
