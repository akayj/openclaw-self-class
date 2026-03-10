#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["requests"]
# ///
import json, os, sys, subprocess
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Callable
import requests

def read_file(path: str) -> str:
    try: return Path(path).read_text(encoding="utf-8")
    except Exception as e: return f"Error: {e}"

def write_file(path: str, content: str) -> str:
    try:
        p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Success"
    except Exception as e: return f"Error: {e}"

def list_dir(path: str = ".") -> str:
    try: return "\n".join(os.listdir(path)) or "(empty)"
    except Exception as e: return f"Error: {e}"

def bash(command: str) -> str:
    try:
        r = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return f"STDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}"
    except Exception as e: return f"Error: {e}"

@dataclass
class Tool:
    name: str; description: str; fn: Callable
    parameters: dict = field(default_factory=lambda: {"type": "object", "properties": {}})
    def to_spec(self): 
        return {"type": "function", "function": {"name": self.name, "description": self.description, "parameters": self.parameters}}

class Zoe:
    def __init__(self, name="zoe", instruction="Direct assistant."):
        self.name = name; self.instruction = instruction
        self.api_key = os.environ.get("ZOE_API_KEY", "")
        self.base_url = (os.environ.get("ZOE_BASE_URL", "https://api.moonshot.cn/v1")).rstrip("/")
        self.model = os.environ.get("ZOE_MODEL", "kimi-k2.5")
        self.tools = {
            "read_file": Tool("read_file", "Read file", read_file, {"type": "object", "properties": {"path": {"type": "string"}}}),
            "write_file": Tool("write_file", "Write file", write_file, {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}}),
            "list_dir": Tool("list_dir", "List files", list_dir, {"type": "object", "properties": {"path": {"type": "string"}}}),
            "bash": Tool("bash", "Run command", bash, {"type": "object", "properties": {"command": {"type": "string"}}})
        }

    def run(self, task: str):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        messages = [{"role": "system", "content": self.instruction}, {"role": "user", "content": task}]
        for _ in range(5):
            r = requests.post(f"{self.base_url}/chat/completions", headers=headers, 
                             json={"model": self.model, "messages": messages, "tools": [t.to_spec() for t in self.tools.values()]})
            msg = r.json()["choices"][0]["message"]; messages.append(msg)
            if not msg.get("tool_calls"): return msg.get("content", "")
            for tc in msg["tool_calls"]:
                fn, args = tc["function"]["name"], json.loads(tc["function"].get("arguments", "{}"))
                out = self.tools[fn].fn(**args)
                messages.append({"role": "tool", "tool_call_id": tc["id"], "content": out})
        return "Limit reached"

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "run": return
    print(Zoe().run(sys.argv[2]))

if __name__ == "__main__": main()
