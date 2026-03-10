#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["rich"]
# ///
import os, sys, subprocess
from rich.console import Console
from rich.table import Table

console = Console()

class ZoeDoctor:
    def __init__(self, target_path="."):
        self.target = os.path.abspath(target_path)

    def scan_pressures(self):
        pressures = []
        if not os.path.exists(self.target): return []
        
        for f in os.listdir(self.target):
            f_path = os.path.join(self.target, f)
            if f.endswith((".py", ".sh")) and not os.access(f_path, os.X_OK):
                pressures.append({"type": "PERM", "file": f, "desc": "Missing exec bit"})
        
        if "pyproject.toml" in os.listdir(self.target):
            if not os.path.exists(os.path.join(self.target, ".venv")):
                pressures.append({"type": "ENV", "file": "pyproject.toml", "desc": "Virtual env missing"})
        return pressures

    def restore_balance(self, pressures):
        for p in pressures:
            console.print(f"🔧 [yellow]Healing {p['type']}[/yellow]: {p['file']}")
            if p["type"] == "PERM":
                os.chmod(os.path.join(self.target, p["file"]), 0o755)
            elif p["type"] == "ENV":
                subprocess.run(["uv", "venv"], cwd=self.target, capture_output=True)
        console.print("[green]✅ Balance Restored.[/green]")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    doc = ZoeDoctor(path)
    p_list = doc.scan_pressures()
    if p_list:
        doc.restore_balance(p_list)
    else:
        console.print("[green]System already balanced.[/green]")
