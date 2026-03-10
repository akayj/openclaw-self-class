#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["rich", "requests"]
# ///
import os, sys, json
from rich.console import Console
from rich.table import Table

# Add local zoe to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../zoe/src"))
from zoe import Zoe

console = Console()

def analyze_file(path: str) -> str:
    """Uses Zoe Kernel to classify file nature."""
    agent = Zoe(instruction="You are an OS kernel analyzer. Classify file nature in 2 words.")
    name = os.path.basename(path)
    return agent.run(f"Analyze nature of file: {name}")

def list_semantic(path="."):
    table = Table(title=f"Zoe-OS FS: {os.path.abspath(path)}")
    table.add_column("Name"); table.add_column("Nature")

    for item in sorted(os.listdir(path)):
        if item.startswith("."): continue
        # For performance in this test, we only analyze .py and .md
        nature = analyze_file(item) if item.endswith((".py", ".md")) else "Data"
        table.add_row(item, nature)

    console.print(table)

if __name__ == "__main__":
    list_semantic(sys.argv[1] if len(sys.argv) > 1 else ".")
