#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["typer", "rich"]
# ///
import os, subprocess, datetime, typer, time, threading
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

app = typer.Typer()
console = Console()
TMUX_LOG_DIR = Path.home() / ".tmux-logs"
TMUX_LOG_DIR.mkdir(exist_ok=True)

def run_tmux(cmd):
    return subprocess.run(f"tmux {cmd}", shell=True, capture_output=True, text=True).stdout

def heartbeat_loop(session, interval, log_file: Path = None):
    """后台心跳线程 - 监控任务状态并显示进度（不写入日志）"""
    time.sleep(interval)
    last_size = log_file.stat().st_size if log_file and log_file.exists() else 0
    
    while True:
        result = subprocess.run(f"tmux has-session -t {session} 2>/dev/null", shell=True)
        if result.returncode == 0:
            # 检查日志文件是否有新内容
            if log_file and log_file.exists():
                current_size = log_file.stat().st_size
                if current_size > last_size:
                    # 读取新增内容（只读，不修改）
                    with open(log_file, 'r') as f:
                        f.seek(last_size)
                        new_content = f.read()
                        if new_content.strip():
                            lines = new_content.strip().split('\n')[-3:]  # 最后3行
                            # 只打印到控制台，不写入日志
                            console.print(f"[bold cyan]💓 [{session}] {datetime.datetime.now().strftime('%H:%M:%S')}[/bold cyan]")
                            for line in lines:
                                console.print(f"  {line}")
                    last_size = current_size
        else:
            console.print(f"[bold red]🚨 [{session}] 已结束[/bold red]")
            if log_file:
                # 追加结束标记
                with open(log_file, 'a') as f:
                    f.write(f"\n{'='*60}\n# Completed: {datetime.datetime.now()}\n")
                console.print(f"📄 完整日志：{log_file}")
            # 自动清理 tmux session（保留日志）
            run_tmux(f"kill-session -t {session} 2>/dev/null")
            console.print(f"[dim]🧹 已清理 session: {session}[/dim]")
            break
        time.sleep(interval)

@app.command()
def run(session: str, command: str, heartbeat: int = 60, attach: bool = False):
    """启动任务 + 后台心跳线程
    
    Args:
        session: 任务名称
        command: 要执行的命令
        heartbeat: 心跳间隔（秒）
        attach: 是否立即 attach 到会话
    """
    run_tmux(f"kill-session -t {session} 2>/dev/null")
    
    log_file = TMUX_LOG_DIR / f"{session}.log"
    log_header = f"# Session: {session}\n# Started: {datetime.datetime.now()}\n# Command: {command}\n{'='*60}\n"
    log_file.write_text(log_header)
    
    # 使用 tee 同时输出到终端和日志文件
    tee_command = f"{command} 2>&1 | tee -a '{log_file}'"
    run_tmux(f"new-session -d -s {session} '{tee_command}'")
    
    # 启动后台心跳线程（监控任务状态）
    t = threading.Thread(target=heartbeat_loop, args=(session, heartbeat, log_file), daemon=True)
    t.start()
    
    console.print(f"[green]✓[/green] [{session}] 已启动，心跳间隔 {heartbeat}秒")
    console.print(f"📄 日志：{log_file}")
    console.print(f"🔌 Attach: tmux attach -t {session}")
    
    if attach:
        console.print(f"[cyan]正在 attach 到会话 {session}...[/cyan]")
        os.system(f"tmux attach -t {session}")
    else:
        # 保持主进程运行
        try:
            while t.is_alive():
                time.sleep(10)
        except KeyboardInterrupt:
            console.print("[yellow]停止监控[/yellow]")

@app.command()
def peek(session: str, lines: int = 10, follow: bool = False):
    """查看任务输出
    
    Args:
        session: 任务名称
        lines: 显示最后多少行
        follow: 是否持续跟踪（类似 tail -f）
    """
    log_file = TMUX_LOG_DIR / f"{session}.log"
    
    if follow:
        # 持续跟踪日志
        console.print(f"[cyan]跟踪日志 {log_file} (Ctrl+C 停止)...[/cyan]")
        try:
            subprocess.run(f"tail -f '{log_file}'", shell=True)
        except KeyboardInterrupt:
            console.print("[yellow]停止跟踪[/yellow]")
    elif log_file.exists():
        # 读取日志文件
        content = log_file.read_text()
        output = '\n'.join(content.split('\n')[-lines:])
        console.print(Panel(output.strip() or "[dim]无输出[/dim]", title=f"📊 {session} (日志)"))
    else:
        # 回退到 capture-pane
        output = run_tmux(f"capture-pane -t {session} -p | tail -{lines}")
        console.print(Panel(output.strip() or "[dim]无输出[/dim]", title=f"📊 {session} (实时)"))

@app.command()
def list_sessions():
    output = run_tmux("list-sessions")
    console.print(output or "[dim]无任务[/dim]")

@app.command()
def stop(session: str):
    """停止任务"""
    run_tmux(f"kill-session -t {session}")
    log_file = TMUX_LOG_DIR / f"{session}.log"
    if log_file.exists():
        # 追加结束标记
        with open(log_file, 'a') as f:
            f.write(f"\n{'='*60}\n# Stopped: {datetime.datetime.now()}\n")
    console.print(f"[red]✗[/red] [{session}] 已停止")
    console.print(f"📄 日志保留：{log_file}")

@app.command()
def attach(session: str):
    """Attach 到运行中的会话"""
    result = subprocess.run(f"tmux has-session -t {session} 2>/dev/null", shell=True)
    if result.returncode == 0:
        console.print(f"[cyan]正在 attach 到 {session}...[/cyan]")
        os.system(f"tmux attach -t {session}")
    else:
        console.print(f"[red]✗[/red] 会话 {session} 不存在")
        # 尝试显示日志
        log_file = TMUX_LOG_DIR / f"{session}.log"
        if log_file.exists():
            console.print(f"📄 历史日志：{log_file}")
            peek(session, lines=20)

if __name__ == "__main__":
    app()
