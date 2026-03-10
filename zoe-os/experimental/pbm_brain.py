#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["requests"]
# ///
"""
pbm_brain.py: The Cognitive Engine of Zoe-OS.
Receives raw physical data and uses LLM to deduce Balance Restoration Actions.
"""
import json, os, sys, subprocess
import requests

def get_physical_state():
    """Call Zig Sentinel to get raw physical data"""
    # 模拟 Zig Sentinel 吐出的原始物理特征 (未来通过 zoe-socket 获取)
    raw_entities = [
        {"name": "main.zig", "type": "FILE", "mode": "644"},
        {"name": "Cargo.toml", "type": "FILE", "mode": "644"},
        {"name": "scripts", "type": "DIR", "mode": "755"}
    ]
    return raw_entities

def deduce_balance_action(entities):
    """Bf: Reasoning layer using LLM (Not Hardcoded!)"""
    api_key = os.environ.get("ZOE_API_KEY", "")
    prompt = f"I am Zoe-OS Brain. Current Physical Entities: {entities}. Deduce if there is any Balance Gap (e.g., missing permissions, missing environment). Output exact Bash commands to fix."
    
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"model": "kimi-k2.5", "messages": [{"role": "user", "content": prompt}]}
    
    r = requests.post("https://api.moonshot.cn/v1/chat/completions", headers=headers, json=payload)
    return r.json()["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print("🧠 Zoe Brain: Analyzing raw physical state...")
    state = get_physical_state()
    actions = deduce_balance_action(state)
    print(f"\n🚀 Deduced Actions:\n{actions}")
