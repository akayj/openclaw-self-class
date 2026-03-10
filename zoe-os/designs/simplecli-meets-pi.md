# 🧬 Design: SimpleCLI meets Pi-Agent

This document outlines the philosophical and technical foundation of **Zoe-OS**.

## 1. The SimpleCLI Inspiration (Minimalism)

[SimpleCLI](https://github.com/Zen-Open-Source/SimpleCLI) proved that a production-grade AI interface doesn't need a framework. 

**What we took:**
- **The "One File" Rule**: Logic should be readable from top to bottom in one sitting.
- **Dependency Zero**: Native `requests` is more robust than complex SDKs.
- **Transparent History**: The conversation array IS the state.

## 2. The Pi-Agent Inspiration (Self-Healing)

A simple CLI is a "tool". A **Pi-Agent** is an "autonomous entity". 

**What we took:**
- **The Loop**: `Sense → Think → Act → Verify`. Never assume an action succeeded.
- **Checkpointing**: Every state change is flushed to disk. Crash-safe is mandatory.
- **Built-in Survival**: An agent without `read`, `write`, `list`, and `bash` is a brain without hands.

## 3. The Zoe-OS Convergence

Zoe-OS is the evolution where these two concepts meet at the **Operating System** level.

### From "Running a Script" to "Managing Intent"
In a traditional OS, you run `ls`. In Zoe-OS, you express the intent: *"I need to find the latest config file"*.
- **The Kernel (Zoe)**: Translates intent to shell commands via the Loop.
- **The Shell**: A natural language interface that streams thought processes.

### Inter-Agent Collaboration (The Bus)
In Zoe-OS, complex tasks are solved by spawning sub-agents:
- **Master Zoe**: Decomposes the task.
- **Worker Zoe**: Executes specific survival tools (e.g., `bash` to install a package).
- **Verify Zoe**: Audits the result against the original intent.

---

## 🛠️ Implementation Strategy

- **Keep it Pythonic**: Use `uv` for lightning-fast execution.
- **Keep it Text-based**: The file system is the primary communication medium.
- **Keep it Open**: Every Zoe-OS node is a potential contributor to a larger mesh.

*Drafted by Xiao Xin | Approved by akayj*
