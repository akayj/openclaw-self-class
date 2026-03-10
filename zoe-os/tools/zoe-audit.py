#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["rich"]
# ///
"""
zoe-audit: The Safety & Quality Gatekeeper for OpenClaw.
Monitors the 'skills/' directory to ensure no secrets leak and specs are met.
"""
import os, sys, re
from rich.console import Console
from rich.table import Table

console = Console()

# 核心安全模式（PBM 压力源）
SENSITIVE_PATTERNS = {
    "Feishu ID": r"ou_[a-z0-9]{32}",
    "GitHub Token": r"ghp_[a-zA-Z0-9]{36}",
    "AI Secret": r"sk-[a-zA-Z0-9]{48}"
}

class ZoeAudit:
    def __init__(self, skills_dir="/root/.openclaw/workspace/skills"):
        self.skills_dir = skills_dir

    def scan_safety_leaks(self):
        """Sense: Checking for sensitive information in skills."""
        issues = []
        for root, _, files in os.walk(self.skills_dir):
            for f in files:
                if f.endswith((".py", ".json", ".md")):
                    path = os.path.join(root, f)
                    content = open(path, "r", errors="ignore").read()
                    for name, pattern in SENSITIVE_PATTERNS.items():
                        if re.search(pattern, content):
                            issues.append({"file": os.path.relpath(path, self.skills_dir), "issue": f"Leaked {name}"})
        return issues

    def run_report(self):
        console.print("\n[bold cyan]🦞 Zoe-OS | OpenClaw Skill Auditor[/bold cyan]\n")
        leaks = self.scan_safety_leaks()
        
        table = Table(title="Skill Safety & Spec Audit")
        table.add_column("Component", style="dim")
        table.add_column("Security Status")
        table.add_column("PBM Pressure")

        if not leaks:
            table.add_row("Skills Directory", "[green]SECURE[/green]", "0.0 (Balanced)")
        else:
            for l in leaks:
                table.add_row(l["file"], f"[red]⚠️ {l['issue']}[/red]", "0.9 (CRITICAL)")

        console.print(table)

if __name__ == "__main__":
    auditor = ZoeAudit()
    auditor.run_report()
