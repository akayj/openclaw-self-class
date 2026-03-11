#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["requests"]
# ///
import json, os, sys, subprocess
from pathlib import Path
import requests

def read_file(path: str) -> str:
    try: return Path(path).read_text(encoding="utf-8")
    except Exception as e: return f"Error: {e}"

def write_file(path: str, content: str) -> str:
    try:
        p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return "Success"
    except Exception as e: return f"Error: {e}"

def list_dir(path: str = ".") -> str:
    try: return "\n".join(os.listdir(path)) or "(empty)"
    except Exception as e: return f"Error: {e}"

def bash(command: str) -> str:
    try:
        r = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return f"STDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}"
    except Exception as e: return f"Error: {e}"

class Zoe:
    def __init__(self, name="zoe", instruction="Direct assistant."):
        self.name = name; self.instruction = instruction
        self.api_key = os.environ.get("ZOE_API_KEY", "")
        self.base_url = (os.environ.get("ZOE_BASE_URL", "https://api.moonshot.cn/v1")).rstrip("/")
        self.model = os.environ.get("ZOE_MODEL", "kimi-k2.5")
        self.tools = {
            "read_file": {"fn": read_file, "desc": "Read file contents", "params": {
                "type": "object", "properties": {"path": {"type": "string", "description": "File path to read"}},
                "required": ["path"]
            }},
            "write_file": {"fn": write_file, "desc": "Write content to file", "params": {
                "type": "object", "properties": {
                    "path": {"type": "string", "description": "File path to write"},
                    "content": {"type": "string", "description": "Content to write"}
                }, "required": ["path", "content"]
            }},
            "list_dir": {"fn": list_dir, "desc": "List files in directory", "params": {
                "type": "object", "properties": {"path": {"type": "string", "description": "Directory path (default: current)"}}
            }},
            "bash": {"fn": bash, "desc": "Execute shell command", "params": {
                "type": "object", "properties": {"command": {"type": "string", "description": "Shell command to execute"}},
                "required": ["command"]
            }}
        }

    def run(self, task: str, max_iterations: int = 10):
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        messages = [{"role": "system", "content": self.instruction}, {"role": "user", "content": task}]
        tools_spec = [{"type": "function", "function": {"name": k, "description": v["desc"], "parameters": v["params"]}} for k, v in self.tools.items()]
        
        for _ in range(max_iterations):
            try:
                r = requests.post(f"{self.base_url}/chat/completions", headers=headers, 
                                 json={"model": self.model, "messages": messages, "tools": tools_spec}, timeout=60)
                data = r.json()
                if "choices" not in data: return f"LLM Error: {data.get('error', 'Unknown')}"
                
                msg = data["choices"][0]["message"]
                messages.append(msg)
                
                if not msg.get("tool_calls"):
                    return msg.get("content", "(no response)")
                
                # Execute tool calls
                for tc in msg["tool_calls"]:
                    name = tc["function"]["name"]
                    args = json.loads(tc["function"].get("arguments", "{}"))
                    # Filter args to only include valid parameters for the function
                    import inspect
                    fn = self.tools[name]["fn"]
                    valid_params = set(inspect.signature(fn).parameters.keys())
                    filtered_args = {k: v for k, v in args.items() if k in valid_params}
                    if name in self.tools:
                        result = fn(**filtered_args)
                    else:
                        result = f"Unknown tool: {name}"
                    messages.append({"role": "tool", "tool_call_id": tc["id"], "content": result})
            except Exception as e:
                return f"Runtime Error: {e}"
        
        return "Max iterations reached"

def main():
    """CLI entry point for zoe command."""
    if len(sys.argv) > 2 and sys.argv[1] == "run":
        print(Zoe().run(sys.argv[2]))
    elif len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h", "help"]:
        print("Usage: zoe run <task>")
        print("")
        print("A minimalist AI Agent. One file, no framework.")
        print("")
        print("Commands:")
        print("  run <task>    Execute a task")
        print("")
        print("Environment variables:")
        print("  ZOE_API_KEY       API key for LLM (required)")
        print("  ZOE_BASE_URL      Base URL for API (default: https://api.moonshot.cn/v1)")
        print("  ZOE_MODEL         Model name (default: kimi-k2.5)")
    else:
        print("Usage: zoe run <task>")
        print("Run 'zoe --help' for more information.")

if __name__ == "__main__":
    main()
