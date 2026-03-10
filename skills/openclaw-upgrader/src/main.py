#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "requests",
# ]
# ///
"""
OpenClaw Upgrader — powered by Zoe-Agent

A self-healing upgrade agent that:
  1. Checks for new OpenClaw versions
  2. Creates backup checkpoint
  3. Runs upgrade with auto-retry
  4. Verifies post-upgrade health
  5. Pushes status via Feishu (offline brain)
"""
import subprocess, json, os, sys, time
from pathlib import Path

# Import Zoe from sibling skill
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "zoe-agent" / "src"))
from zoe import Zoe, Tool

# ─── TOOLS ────────────────────────────────────────────────────────────────────

def check_current_version() -> str:
    """Get the currently installed OpenClaw version."""
    try:
        r = subprocess.run(["openclaw", "--version"], capture_output=True, text=True, timeout=10)
        return r.stdout.strip() or r.stderr.strip()
    except Exception as e:
        return f"Error: {e}"

def check_latest_version() -> str:
    """Check npm registry for the latest OpenClaw version."""
    try:
        r = subprocess.run(
            ["npm", "view", "openclaw", "version"],
            capture_output=True, text=True, timeout=30,
        )
        return r.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def create_backup() -> str:
    """Create a backup of current OpenClaw config."""
    backup_dir = Path.home() / ".openclaw" / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    backup_path = backup_dir / f"backup-{ts}.tar.gz"
    try:
        subprocess.run(
            ["tar", "czf", str(backup_path),
             "-C", str(Path.home()), ".openclaw/openclaw.json", ".openclaw/cron"],
            capture_output=True, text=True, timeout=30,
        )
        return f"Backup created: {backup_path}"
    except Exception as e:
        return f"Backup failed: {e}"

def run_upgrade() -> str:
    """Execute npm install -g openclaw@latest."""
    try:
        r = subprocess.run(
            ["npm", "install", "-g", "openclaw@latest"],
            capture_output=True, text=True, timeout=120,
        )
        if r.returncode == 0:
            return f"Upgrade succeeded.\n{r.stdout[-500:]}"
        else:
            return f"Upgrade failed (code {r.returncode}):\n{r.stderr[-500:]}"
    except Exception as e:
        return f"Upgrade error: {e}"

def verify_health() -> str:
    """Post-upgrade health check."""
    checks = []
    # Version check
    r = subprocess.run(["openclaw", "--version"], capture_output=True, text=True, timeout=10)
    checks.append(f"Version: {r.stdout.strip()}")
    # Gateway status
    r = subprocess.run(["openclaw", "gateway", "status"], capture_output=True, text=True, timeout=10)
    checks.append(f"Gateway: {r.stdout.strip()[:200]}")
    return "\n".join(checks)

def push_feishu(message: str) -> str:
    """Send status update via Feishu (offline brain - works without Gateway)."""
    app_id = os.environ.get("FEISHU_APP_ID", "cli_a92c19f76bf95cc4")
    app_secret = os.environ.get("FEISHU_APP_SECRET", "JMWSokscDBlFZ9S6mnSjFf7rgtASbNsP")
    user_id = os.environ.get("FEISHU_USER_ID", "ou_aa88439cf3e9333ccf2acba6c45e73c5")

    try:
        import requests
        # Get tenant token
        r = requests.post(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            json={"app_id": app_id, "app_secret": app_secret},
            timeout=10,
        )
        token = r.json().get("tenant_access_token", "")
        if not token:
            return "Failed to get Feishu token"

        # Send message
        r = requests.post(
            "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "receive_id": user_id,
                "msg_type": "text",
                "content": json.dumps({"text": message}),
            },
            timeout=10,
        )
        return f"Feishu push: {r.status_code}"
    except Exception as e:
        return f"Feishu push failed: {e}"


# ─── AGENT ────────────────────────────────────────────────────────────────────

INSTRUCTION = """You are the OpenClaw Upgrade Agent.

Your mission: safely upgrade OpenClaw to the latest version.

Workflow:
1. Check the current installed version
2. Check the latest available version on npm
3. If already up to date, report and stop
4. If upgrade needed: create backup first, then run upgrade
5. After upgrade: verify health (version + gateway status)
6. Push the final status report via Feishu

Rules:
- ALWAYS create backup before upgrading
- If upgrade fails, analyze the error and try once more
- Report results via push_feishu at the end
- Be concise in your reports
"""

def build_agent() -> Zoe:
    return Zoe(
        name="openclaw-upgrader",
        instruction=INSTRUCTION,
        tools=[
            Tool("check_current_version", "Get installed OpenClaw version", check_current_version),
            Tool("check_latest_version", "Check latest version on npm registry", check_latest_version),
            Tool("create_backup", "Backup current OpenClaw config before upgrade", create_backup),
            Tool("run_upgrade", "Execute the npm upgrade command", run_upgrade),
            Tool("verify_health", "Post-upgrade health check", verify_health),
            Tool("push_feishu", "Send status message via Feishu", push_feishu,
                 parameters={"type": "object", "properties": {"message": {"type": "string"}}, "required": ["message"]}),
        ],
        api_key=os.environ.get("ZOE_API_KEY", "sk-6FIvRQ9CACcCp277MZDss5ZD1nMNBlss7Dd1re4QHAkzNr56"),
        base_url=os.environ.get("ZOE_BASE_URL", "https://api.moonshot.cn/v1"),
        model=os.environ.get("ZOE_MODEL", "kimi-k2.5"),
    )

if __name__ == "__main__":
    agent = build_agent()

    if len(sys.argv) > 1 and sys.argv[1] == "status":
        print(json.dumps(agent.status(), indent=2, ensure_ascii=False))
    elif len(sys.argv) > 1 and sys.argv[1] == "check":
        # Quick check mode: just report versions, no upgrade
        agent.run("Check the current and latest OpenClaw versions. Report via Feishu. Do NOT upgrade.")
    else:
        agent.run("Check if OpenClaw needs upgrading. If yes, perform a safe upgrade with backup and verification. Report the result via Feishu.")
