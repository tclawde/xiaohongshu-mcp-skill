#!/usr/bin/env python3
"""更有吸引力的标题和封面"""

import sys
sys.path.insert(0, "/Users/apple/.openclaw/workspace/title-cover-generator")
from generate import create_title_cover

import requests

BASE_URL = "http://localhost:18060"

# 更吸引力的标题
title = "一组数据告诉你 AI 烧钱有多恐怖"

content = """一组数据：

OpenAI 2024 年预计亏损 50 亿美元（来源：The Information）
Anthropic 2024 年预计亏损 27 亿美元（来源：The Information）
xAI 融资 60 亿，但开销惊人（来源：TechCrunch）
中国 AI 独角兽们，估值在跌，营收在跌（来源：36Kr）

加一下：50 + 27 = 77 亿美元

这只是 OpenAI 和 Anthropic 两家。

还不算谷歌、Meta、微软在 AI 上的亏损。

问题是：钱花在哪里？

1. 算力：英伟达 H100 一张 3 万美元
2. 人才：AI 研究员年薪百万起
3. 数据：获取成本越来越高

营收呢？

ChatGPT Plus 20 美元/月，用户不到 2000 万
API 调用，价格战打到几分钱一次

这意味着什么？

AI 公司现在就是烧钱换市场。

和当年的网约车一模一样。

等补贴战打完呢？

要么提价，要么合并，要么关门。

所以现在估值，全靠想象力支撑。

想象力这东西，最不可靠。

#AI行业 #亏损 #财报"""

print("=" * 60)
print("🦀 更有吸引力的内容")
print("=" * 60)

# 生成封面 - 更有冲击力
cover = create_title_cover(
    title=title,
    output_path="/tmp/viral_cover.jpg",
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
