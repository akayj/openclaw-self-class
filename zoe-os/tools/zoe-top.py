#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["rich"]
# ///
"""
zoe-top: The Pressure Dashboard for Zoe-OS.
Displays real-time entropy, system load, and agent balance state.
"""
import os, sys, time
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn

console = Console()

def get_system_metrics():
    # 模拟获取 Zoe-OS 的核心指标
    metrics = [
        {"name": "Entropy (Files)", "value": len(os.listdir(".")), "max": 100, "unit": "files"},
        {"name": "Memory Slices", "value": 12, "max": 50, "unit": "seeds"},
        {"name": "Disk Pressure", "value": 24, "max": 100, "unit": "%"},
        {"name": "Agent Stress", "value": 0.15, "max": 1.0, "unit": "P"},
    ]
    return metrics

def display_dashboard():
    console.clear()
    console.print("[bold cyan]🦞 Zoe-OS Pressure Dashboard[/bold cyan]", justify="center")
    console.print("-" * 40, justify="center")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Dimension")
    table.add_column("Current State")
    table.add_column("Status")

    metrics = get_system_metrics()
    for m in metrics:
        status = "[green]Balanced[/green]"
        if m["value"] > m["max"] * 0.8: status = "[red]High Stress[/red]"
        elif m["value"] > m["max"] * 0.5: status = "[yellow]Warming[/yellow]"
        
        table.add_row(m["name"], f"{m['value']} {m['unit']}", status)

    console.print(table)
    console.print(f"\n[dim]Kernel: Zoe 0.1.3 | Node: {os.uname().nodename}[/dim]")

if __name__ == "__main__":
    display_dashboard()
