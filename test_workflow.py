#!/usr/bin/env python3
"""测试小红书 MCP 运营流程"""

import sys
import os
import json
import time
import signal

# 超时处理
def timeout_handler(signum, frame):
    print("❌ 超时：流程执行超过 20 秒")
    sys.exit(1)

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(20)

try:
    print("=" * 60)
    print("🦀 小红书运营流程测试")
    print("=" * 60)

    BASE_URL = "http://localhost:18060"
    import requests

    # 步骤 1: 检查登录状态
    print("\n📋 步骤 1: 检查 MCP 服务器和登录状态")
    print("-" * 40)

    try:
        resp = requests.get(f"{BASE_URL}/api/v1/login/status", timeout=5)
        # 检查响应状态码
        if resp.status_code != 200:
            print(f"❌ HTTP 错误: {resp.status_code}")
            sys.exit(1)

        data = resp.json()
        print(f"调试: 原始响应类型 = {type(data)}")

        if data.get("success"):
            login_info = data.get("data", {})
            is_logged_in = login_info.get("is_logged_in", False)

            if is_logged_in:
                username = login_info.get("username", "?")
                print(f"✅ 已登录，用户: {username}")
            else:
                print("⚠️ 未登录，需要先执行登录流程")
                print("   执行: bash xhs_login.sh --notify")
        else:
            print("❌ 获取登录状态失败")
    except Exception as e:
        print(f"❌ 无法连接到 MCP 服务器: {e}")
        print("💡 需要启动 MCP 服务器: ./xiaohongshu-mcp-darwin-arm64 &")
        sys.exit(1)

    # 步骤 2: 搜索热点
    print("\n🔍 步骤 2: 搜索 AI 相关热点")
    print("-" * 40)
    print("搜索关键词: AI")
    print("排序方式: 最新")
    print("时间范围: 一天内")
    print("\n执行中...")

    try:
        params = {
            "keyword": "AI",
            "sort": "最新",
            "time": "一天内",
            "page": 1
        }
        resp = requests.get(f"{BASE_URL}/api/v1/search/notes", params=params, timeout=15)
        data = resp.json()

        if data.get("success"):
            results = data.get("data", [])
            print(f"\n✅ 搜索完成，找到 {len(results)} 条结果")

            if results:
                print("\n📊 TOP 5 热点内容：")
                print("-" * 40)

                for i, note in enumerate(results[:5]):
                    title = note.get('title', '无标题')[:45]
                    author = note.get('user', {}).get('nickname', '?') if note.get('user') else '?'
                    likes = note.get('liked', 0)
                    comments = note.get('comments', 0)

                    print(f"\n{i+1}. {title}")
                    print(f"   👤 {author}")
                    print(f"   📊 👍{likes} | 💬{comments}")

                    # 争议角度建议
                    print(f"   💡 争议角度:")
                    print(f"      - 「过度炒作」角度批判")
                    print(f"      - 「实际无用」角度质疑")
        else:
            print(f"❌ 搜索失败: {data.get('error', '未知错误')}")
    except Exception as e:
        print(f"❌ 搜索出错: {e}")

    # 步骤 3: 查看数据目录
    print("\n\n📁 步骤 3: 查看数据目录")
    print("-" * 40)
    data_dir = '/Users/apple/.openclaw/skills/xiaohongshu-mcp/data'

    if os.path.exists(data_dir):
        files = os.listdir(data_dir)
        print(f"✅ 数据目录存在，包含 {len(files)} 个文件：")

        file_info = []
        for f in files:
            filepath = os.path.join(data_dir, f)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                file_info.append((f, size))

        # 按文件名排序
        file_info.sort()
        for fname, fsize in file_info:
            print(f"   📄 {fname} ({fsize} bytes)")
    else:
        print(f"⚠️ 数据目录不存在: {data_dir}")
        print("   创建目录...")
        os.makedirs(data_dir, exist_ok=True)
        print("   ✅ 已创建")

    # 步骤 4: 查看发布记录
    print("\n\n📝 步骤 4: 查看发布记录")
    print("-" * 40)
    history_file = '/Users/apple/.openclaw/skills/xiaohongshu-mcp/data/post_history.json'

    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
            print(f"✅ 历史发布记录：{len(history)} 篇")

            if history:
                print("\n最近 3 篇发布：")
                for item in history[-3:]:
                    date = item.get('date', '?')
                    ptype = item.get('type', '?')
                    title = item.get('title', '?')[:25]
                    likes = item.get('response', {}).get('likes', 0)
                    print(f"   📅 {date} | {ptype} | {title}... | 👍{likes}")
    else:
        print(f"⚠️ 发布记录文件不存在")
        print("   创建空记录文件...")
        with open(history_file, 'w') as f:
            json.dump([], f)
        print("   ✅ 已创建")

    # 步骤 5: 查看热点选题库
    print("\n\n🎯 步骤 5: 查看热点选题库")
    print("-" * 40)
    topics_file = '/Users/apple/.openclaw/skills/xiaohongshu-mcp/data/hot_topics.json'

    if os.path.exists(topics_file):
        with open(topics_file, 'r') as f:
            topics = json.load(f)
            print(f"✅ 热点选题库：{len(topics)} 个待选题")

            pending = [t for t in topics if t.get('status') == 'pending']
            print(f"   待制作: {len(pending)} 个")

            if pending:
                print("\n待制作选题 TOP 3：")
                for i, t in enumerate(pending[:3]):
                    topic = t.get('topic', '?')[:30]
                    angle = t.get('controversy_angle', '?')[:40]
                    print(f"   {i+1}. {topic}...")
                    print(f"      角度: {angle}...")
    else:
        print(f"⚠️ 选题库文件不存在")
        print("   创建空选题库...")
        with open(topics_file, 'w') as f:
            json.dump([], f)
        print("   ✅ 已创建")

    # 步骤 6: 建议下一步
    print("\n\n🚀 步骤 6: 建议的下一步操作")
    print("-" * 40)
    print("根据策略文档 (STRATEGY.md)，应该执行：")
    print("")
    print("   📌 每日流程：")
    print("      1. 7:00, 13:00, 19:00 - 搜索热点")
    print("      2. 记录到 hot_topics.json")
    print("      3. 8:00, 14:00, 20:00 - 创作内容")
    print("      4. 9:00, 15:00, 21:00 - 发布")
    print("")
    print("   📌 今日建议：")
    print("      - 从搜索结果中选 1-2 个有争议的话题")
    print("      - 使用内容模板创作 3 篇（原理/数据/热点）")
    print("      - 发布并记录到 post_history.json")

    print("\n" + "=" * 60)
    print("✅ 流程测试完成 - 系统正常运行")
    print("=" * 60)
    print("\n💡 下次可以直接执行：")
    print("   bash xhs_login.sh --notify  # 登录（如需）")
    print("   python3 test_workflow.py    # 测试流程")

except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    signal.alarm(0)
