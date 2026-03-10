#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["rich", "typer"]
# ///

"""
obsidian-daily.py - 每日日记处理和统计

替代原来的 obsidian-daily.sh
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

app = typer.Typer()
console = Console()

# 配置
VAULT_DIR = Path.home() / "ObsidianVault"
DAILY_DIR = VAULT_DIR / "01-Daily"
INBOX_DIR = VAULT_DIR / "00-Inbox"

def get_daily_file(date: Optional[datetime] = None) -> Path:
    """获取指定日期的日记文件"""
    if date is None:
        date = datetime.now()
    return DAILY_DIR / f"{date.strftime('%Y-%m-%d')}.md"

def ensure_daily_dir():
    """确保日记目录存在"""
    DAILY_DIR.mkdir(parents=True, exist_ok=True)

def create_daily_template(date: datetime) -> str:
    """创建日记模板"""
    weekday = date.strftime("%A")
    return f"""# {date.strftime('%Y-%m-%d')} {weekday}

## 🌅 早间

## 📝 今日待办
- [ ] 

## 🌆 晚间回顾

### 今日完成

### 三省吾身
1. **做得好的**：
2. **做得不好的**：
3. **明天改进**：

---
*创建于 {datetime.now().strftime('%H:%M')}*
"""

@app.command()
def create(
    date: Optional[str] = typer.Option(None, "-d", "--date", help="日期 (YYYY-MM-DD，默认今天)"),
):
    """创建今日日记"""
    ensure_daily_dir()
    
    if date:
        target_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        target_date = datetime.now()
    
    daily_file = get_daily_file(target_date)
    
    if daily_file.exists():
        console.print(f"[yellow]日记已存在：{daily_file}[/yellow]")
        return
    
    content = create_daily_template(target_date)
    daily_file.write_text(content, encoding="utf-8")
    console.print(f"[green]✓[/green] 创建日记：{daily_file}")

@app.command()
def list_days(
    days: int = typer.Option(7, "-n", "--days", help="显示最近 N 天"),
):
    """列出最近日记"""
    ensure_daily_dir()
    
    table = Table(title=f"📅 最近 {days} 天日记")
    table.add_column("日期", style="cyan")
    table.add_column("星期", style="green")
    table.add_column("状态", style="yellow")
    table.add_column("大小", style="magenta")
    
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        daily_file = get_daily_file(date)
        weekday = date.strftime("%a")
        
        if daily_file.exists():
            size = daily_file.stat().st_size
            status = "✅"
            size_str = f"{size} bytes"
        else:
            status = "❌"
            size_str = "-"
        
        table.add_row(
            date.strftime("%Y-%m-%d"),
            weekday,
            status,
            size_str
        )
    
    console.print(table)

@app.command()
def stats():
    """统计日记情况"""
    ensure_daily_dir()
    
    daily_files = list(DAILY_DIR.glob("*.md"))
    total_days = len(daily_files)
    
    if total_days == 0:
        console.print("[yellow]暂无日记[/yellow]")
        return
    
    # 计算连续天数
    dates = sorted([datetime.strptime(f.stem, "%Y-%m-%d") for f in daily_files], reverse=True)
    streak = 0
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    for i, date in enumerate(dates):
        expected_date = today - timedelta(days=i)
        if date.date() == expected_date.date():
            streak += 1
        else:
            break
    
    console.print(Panel(
        f"[bold]📊 日记统计[/bold]\n\n"
        f"总天数：{total_days}\n"
        f"连续天数：{streak}\n"
        f"最早日记：{dates[-1].strftime('%Y-%m-%d') if dates else 'N/A'}\n"
        f"最新日记：{dates[0].strftime('%Y-%m-%d') if dates else 'N/A'}",
        title="统计"
    ))

if __name__ == "__main__":
    app()
