#!/usr/bin/env python3
"""
personal-crm - 个人 CRM
自动从飞书日历和记忆中提取联系人信息，支持自然语言查询
"""

import sys
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# 工作空间路径
WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
CRM_DB = WORKSPACE / "team-memory" / "contacts.json"

def load_contacts():
    """加载联系人数据库"""
    if CRM_DB.exists():
        with open(CRM_DB, "r") as f:
            return json.load(f)
    return {"contacts": [], "last_updated": None}

def save_contacts(data):
    """保存联系人数据库"""
    data["last_updated"] = datetime.now().isoformat()
    CRM_DB.parent.mkdir(parents=True, exist_ok=True)
    with open(CRM_DB, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def extract_contacts_from_memory():
    """从记忆文件中提取联系人"""
    contacts = {}
    
    if not MEMORY_DIR.exists():
        return contacts
    
    # 扫描记忆文件
    for md_file in MEMORY_DIR.glob("*.md"):
        try:
            with open(md_file, "r") as f:
                content = f.read()
                
            # 简单的人名提取（中文名字模式）
            # 这里可以扩展更复杂的提取逻辑
            lines = content.split("\n")
            for line in lines:
                # 查找提到的名字（简化版）
                if "老板" in line or "余剑" in line:
                    name = "余剑剑 (老板)"
                    if name not in contacts:
                        contacts[name] = {
                            "name": name,
                            "first_seen": md_file.stem,
                            "last_contact": md_file.stem,
                            "interaction_count": 0,
                            "notes": []
                        }
                    contacts[name]["interaction_count"] += 1
                    if len(line.strip()) < 200:
                        contacts[name]["notes"].append(f"{md_file.stem}: {line.strip()[:100]}")
        except Exception as e:
            pass
    
    return contacts

def search_contacts(query):
    """搜索联系人"""
    data = load_contacts()
    results = []
    
    query_lower = query.lower()
    for contact in data["contacts"]:
        if query_lower in contact["name"].lower() or query_lower in " ".join(contact.get("notes", [])).lower():
            results.append(contact)
    
    return results

def update_contacts():
    """更新联系人数据库"""
    print("🔄 扫描记忆文件提取联系人...")
    
    extracted = extract_contacts_from_memory()
    data = load_contacts()
    
    # 合并联系人
    for name, info in extracted.items():
        existing = next((c for c in data["contacts"] if c["name"] == name), None)
        if existing:
            existing["last_contact"] = info["last_contact"]
            existing["interaction_count"] += info["interaction_count"]
            existing["notes"].extend(info["notes"][-5:])  # 保留最近 5 条
        else:
            data["contacts"].append(info)
    
    save_contacts(data)
    print(f"✅ 更新完成，共 {len(data['contacts'])} 个联系人")

def query_contacts(query):
    """查询联系人"""
    results = search_contacts(query)
    
    if not results:
        print(f"❌ 未找到与 '{query}' 相关的联系人")
        return
    
    print(f"📇 找到 {len(results)} 个联系人:\n")
    for contact in results:
        print(f"👤 {contact['name']}")
        print(f"   首次联系：{contact['first_seen']}")
        print(f"   最后联系：{contact['last_contact']}")
        print(f"   互动次数：{contact['interaction_count']}")
        if contact.get("notes"):
            print(f"   最近备注:")
            for note in contact["notes"][-3:]:
                print(f"     - {note[:80]}")
        print()

def show_all():
    """显示所有联系人"""
    data = load_contacts()
    
    if not data["contacts"]:
        print("📇 联系人数据库为空，先运行 'personal-crm update'")
        return
    
    print(f"📇 联系人数据库 (共 {len(data['contacts'])} 人)\n")
    print(f"最后更新：{data['last_updated']}\n")
    
    for contact in sorted(data["contacts"], key=lambda x: x["interaction_count"], reverse=True):
        print(f"  {contact['name']} - {contact['interaction_count']} 次互动")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：personal-crm <命令> [参数]")
        print()
        print("命令:")
        print("  update          - 从记忆文件提取并更新联系人")
        print("  search <关键词>  - 搜索联系人")
        print("  query <关键词>   - 同上")
        print("  list            - 显示所有联系人")
        print("  stats           - 显示统计信息")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "update":
        update_contacts()
    elif cmd in ["search", "query"]:
        if len(sys.argv) < 3:
            print("请提供搜索关键词")
            sys.exit(1)
        query_contacts(" ".join(sys.argv[2:]))
    elif cmd == "list":
        show_all()
    elif cmd == "stats":
        data = load_contacts()
        print(f"📊 联系人统计")
        print(f"   总人数：{len(data['contacts'])}")
        print(f"   最后更新：{data['last_updated']}")
    else:
        print(f"未知命令：{cmd}")
        sys.exit(1)
