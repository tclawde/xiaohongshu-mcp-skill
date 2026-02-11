#!/usr/bin/env python3
"""按策略发布 - 真实内容"""

import sys
sys.path.insert(0, "/Users/apple/.openclaw/workspace/title-cover-generator")
from generate import create_title_cover

import requests

BASE_URL = "http://localhost:18060"

# 真实内容
title = "为什么你的AI工具总是用不好？"
content = """很多人问我，为什么用AI工具总觉得差点意思？

答案很简单：你把AI当工具，我把它当助手。

区别在于：

🔧 工具是「你说什么，它做什么」
👨‍💼 助手是「你给方向，它帮你完成」

举个例子：

❌ "帮我写一段文案"
✅ "写一段针对25岁职场女性的美妆产品种草文案，要活泼但有专业感"

看到区别了吗？

前者AI只能猜，后者AI才能懂。

💡 核心心法：
1. 给背景：谁？什么场景？
2. 给目标：要达成什么效果？
3. 给约束：风格？长度？关键词？

下次别再说"帮我写XX"了。

试试："帮我写一段XX，针对XX人群，要达到XX效果，用XX风格。"

你会发现AI突然好用多了。

#AI工具 #效率提升 #职场技巧"""

print("=" * 60)
print("🦀 按策略发布 - 真实内容")
print("=" * 60)

print(f"\n📌 标题: {title}")
print(f"📌 字数: {len(content)} 字符")

# 1. 生成封面
print("\n🎨 步骤1: 生成封面...")
cover_path = create_title_cover(
    title=title,
    output_path="/tmp/real_cover.jpg",
    font_size=90
)

# 2. 发布
print("\n📤 步骤2: 发布到小红书...")
resp = requests.post(
    f"{BASE_URL}/api/v1/publish",
    json={
        "title": title,
        "content": content,
        "images": [cover_path]
    },
    timeout=120
)

result = resp.json()
if result.get("success"):
    print(f"\n🎉 发布成功！")
    print(f"   Post ID: {result.get('data', {}).get('post_id', 'Unknown')}")
else:
    print(f"\n❌ 发布失败: {result.get('error')}")

print("\n" + "=" * 60)
