#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["requests"]
# ///
import json, os, sys, time, subprocess
from dataclasses import dataclass, field, asdict
from pathlib import Path
import requests

# ─── PBM SPEC: .seed Format ─────────────────────────────────────────────────

@dataclass
class MemorySlice:
    pressure_state: dict
    action_taken: str
    outcome_score: float  # 1.0 = Balance restored, -1.0 = Pressure increased
    timestamp: float = field(default_factory=time.time)

# ─── CORE: Zoe with PBM Hooks ───────────────────────────────────────────────

class Zoe:
    def __init__(self, name="zoe", api_key=None):
        self.name = name
        self.api_key = api_key or os.environ.get("ZOE_API_KEY", "")
        self.base_url = os.environ.get("ZOE_BASE_URL", "https://api.moonshot.cn/v1")
        self.model = os.environ.get("ZOE_MODEL", "kimi-k2.5")
        self.pressure = {"entropy": 0.0, "uncertainty": 0.0} # P
        self.memory_path = Path(f"/root/.openclaw/workspace/zoe/memory/{name}.seed")

    def sense_environment(self, path="."):
        """P: Active sensing of environment entropy (e.g., file count)"""
        files = os.listdir(path)
        self.pressure["entropy"] = len(files) / 100.0  # Simple heuristic
        print(f"🔍 Current Entropy Pressure: {self.pressure['entropy']:.2f}")
        return self.pressure

    def balance_function(self, task):
        """Bf: The decision core to reduce pressure"""
        # In Phase 1, we use LLM as the balance function provider
        print(f"🧠 Balancing internal state against task: {task}")
        return self._llm_think(task)

    def _llm_think(self, task):
        # Simplified LLM call for demonstration
        headers = {"Authorization": f"Bearer {self.api_key}"}
        prompt = f"System State: {self.pressure}\nTask: {task}\nGoal: Restore Balance. Output action."
        payload = {"model": self.model, "messages": [{"role": "user", "content": prompt}]}
        r = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
        return r.json()["choices"][0]["message"]["content"]

    def record_memory(self, action, score):
        """M: Persist the experience slice"""
        m_slice = MemorySlice(pressure_state=self.pressure, action_taken=action, outcome_score=score)
        with open(self.memory_path, "a") as f:
            f.write(json.dumps(asdict(m_slice)) + "\n")
        print(f"💾 Memory slice saved to {self.memory_path}")

# ─── CLI ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    agent = Zoe()
    p = agent.sense_environment()
    if p["entropy"] > 0.1:
        res = agent.balance_function("Organize files to reduce entropy")
        print(f"🚀 Action Taken: {res}")
        agent.record_memory(res, 1.0)
