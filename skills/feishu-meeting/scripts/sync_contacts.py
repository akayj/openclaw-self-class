#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "duckdb",
#     "httpx",
#     "rich",
# ]
# ///

import json
import os
import sys
import time
from pathlib import Path

import duckdb
import httpx
from rich.console import Console
from rich.progress import Progress

# Config
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DB_PATH = SKILL_DIR / "data" / "contacts.duckdb"
CONFIG_PATH = SKILL_DIR / "references" / "config.json"

console = Console()

# Load Config
try:
    with open(CONFIG_PATH, "r") as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    console.print(f"[bold red]❌ Config not found at {CONFIG_PATH}[/]")
    sys.exit(1)

APP_ID = os.getenv("FEISHU_APP_ID") or CONFIG.get("app_id")
APP_SECRET = os.getenv("FEISHU_APP_SECRET") or CONFIG.get("app_secret")
BASE_URL = "https://open.feishu.cn/open-apis"

def get_token() -> str:
    url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
    resp = httpx.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    resp.raise_for_status()
    return resp.json()["tenant_access_token"]

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            name VARCHAR,
            email VARCHAR,
            open_id VARCHAR PRIMARY KEY,
            alias VARCHAR,
            updated_at TIMESTAMP
        );
    """)
    conn.close()

def sync_all():
    init_db()
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Get all departments
    console.print("🔍 Fetching departments...")
    dept_resp = httpx.get(f"{BASE_URL}/contact/v3/scopes", headers=headers)
    if dept_resp.json().get("code") != 0:
        console.print(f"[red]❌ Failed to get scopes: {dept_resp.text}[/]")
        return

    dept_ids = dept_resp.json()["data"].get("department_ids", [])
    console.print(f"✅ Found {len(dept_ids)} departments. Starting sync...")

    conn = duckdb.connect(str(DB_PATH))
    total_synced = 0
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Syncing contacts...", total=len(dept_ids))
        
        for dept_id in dept_ids:
            # Sync users in department
            has_more = True
            page_token = ""
            while has_more:
                url = f"{BASE_URL}/contact/v3/users?department_id={dept_id}&page_size=50&department_id_type=open_department_id"
                if page_token:
                    url += f"&page_token={page_token}"
                
                user_resp = httpx.get(url, headers=headers)
                data = user_resp.json()
                
                if data.get("code") != 0:
                    console.print(f"[yellow]⚠️ Failed to sync dept {dept_id}: {data.get('msg')}[/]")
                    break
                
                users = data["data"].get("items", [])
                for u in users:
                    name = u.get("name")
                    email = u.get("email", "")
                    open_id = u.get("open_id")
                    
                    if open_id:
                        conn.execute("""
                            INSERT INTO contacts (name, email, open_id, updated_at)
                            VALUES (?, ?, ?, now())
                            ON CONFLICT (open_id) DO UPDATE SET
                                name = EXCLUDED.name,
                                email = EXCLUDED.email,
                                updated_at = EXCLUDED.updated_at
                        """, [name, email, open_id])
                        total_synced += 1
                
                has_more = data["data"].get("has_more", False)
                page_token = data["data"].get("page_token", "")
                time.sleep(0.1) # Rate limit protection

            progress.update(task, advance=1)
            
    conn.close()
    console.print(f"[bold green]🎉 Sync Complete! Total contacts: {total_synced}[/]")

if __name__ == "__main__":
    sync_all()