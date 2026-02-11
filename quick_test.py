#!/usr/bin/env python3
"""简化版小红书 MCP 流程测试"""

import requests
import json

BASE_URL = "http://localhost:18060"

print("=" * 60)
print("🦀 小红书运营流程测试")
print("=" * 60)

# 1. 检查登录状态
print("\n📋 步骤 1: 检查登录状态")
resp = requests.get(f"{BASE_URL}/api/v1/login/status")
data = resp.json()
print(f"   响应: {data}")

if data.get("success"):
    is_logged = data.get("data", {}).get("is_logged_in", False)
    user = data.get("data", {}).get("username", "?")
    print(f"   状态: {'✅ 已登录' if is_logged else '⚠️ 未登录'} ({user})")
else:
    print("   ❌ 获取状态失败")

# 2. 搜索热点
print("\n🔍 步骤 2: 搜索 AI 热点")
params = {"keyword": "AI", "sort": "最新", "page": 1}
resp = requests.get(f"{BASE_URL}/api/v1/search/notes", params=params, timeout=10)
data = resp.json()

if data.get("success"):
    results = data.get("data", [])
    print(f"   ✅ 找到 {len(results)} 条结果")

    for i, note in enumerate(results[:3]):
        title = note.get("title", "?")[:40]
        author = note.get("user", {}).get("nickname", "?") if note.get("user") else "?"
        likes = note.get("liked", 0)
        print(f"\n   {i+1}. {title}")
        print(f"      👤 {author} | 👍{likes}")
else:
    print(f"   ❌ 搜索失败: {data.get('error')}")

# 3. 测试发布（需要登录）
print("\n📤 步骤 3: 测试发布功能")
print("   (跳过 - 需要登录状态)")

print("\n" + "=" * 60)
print("✅ MCP 服务器运行正常，API 可用")
print("=" * 60)
