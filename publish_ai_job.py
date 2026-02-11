#!/usr/bin/env python3
"""AI 裁员数据 + 有吸引力标题"""

import sys
sys.path.insert(0, "/Users/apple/.openclaw/workspace/title-cover-generator")
from generate import create_title_cover

import requests

BASE_URL = "http://localhost:18060"

# 有吸引力的标题 + 数据支撑
title = "AI 越火，这群人越惨"

content = """一组数据：

Salesforce 裁员 8000 人，同时招 AI（来源：Bloomberg）
谷歌 AI 负责人被曝薪酬大涨，普通员工普调 0%（来源：The Information）
IBM 用 AI 取代 30% 岗位（来源：路透社）
国内某大厂，AI 部门 HC 锁了，非 AI 部门也在锁

发生了什么？

**AI 在抢谁的饭碗？**

1. 初级程序员：Copilot 代码写得比初级快
2. 设计师：Midjourney 出图比实习生快
3. 客服：AI 24 小时在线，不用交社保
4. 文案：ChatGPT 写文案不要钱

**但谁在赚钱？**

会写 Prompt 的人
会调模型的人
会整合 AI 工作流的人

**这意味着什么？**

AI 不是让人类失业，是让不会用 AI 的人失业。

以前学 Excel 能加工资
现在学 Prompt 能加工资

不是 AI 太强，是你太懒。

#AI #裁员 #职场 #AI 替代"

print("=" * 60)
print("🦀 AI 裁员 + 有吸引力标题")
print("=" * 60)

# 生成封面
cover = create_title_cover(
    title=title,
    output_path="/tmp/job_cover.jpg",
    font_size=90
)

# 发布
resp = requests.post(
    f"{BASE_URL}/api/v1/publish",
    json={"title": title, "content": content, "images": [cover]},
    timeout=120
)

result = resp.json()
if result.get("success"):
    print(f"\n✅ 发布成功: {result.get('data', {}).get('post_id')}")
else:
    print(f"\n❌ 失败: {result.get('error')}")
