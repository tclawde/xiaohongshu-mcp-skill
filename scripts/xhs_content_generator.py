#!/usr/bin/env python3
"""
小红书内容生成器 - AI 反对者/民科风格

根据策略生成去 AI 化的自然内容
"""

import argparse
import json
import random
from datetime import datetime

# 原理篇模板
PRINCIPLE_TEMPLATES = [
    {
        "title": "深度学习就是统计学，别被那些术语骗了",
        "content": """今天看到一个说法，说深度学习是"模仿人脑神经网络"。

我就笑了。

人脑神经元是电化学信号，深度学习是矩阵乘法。这俩有半毛钱关系？

所谓"神经网络"，就是一个个数学公式嵌套在一起。输入数据 → 矩阵运算 → 输出结果。仅此而已。

深度学习做的事情就是：给定一堆输入输出，找出让它们对应起来的数学公式。

这不是智能，这是高级计算器。"""
    },
    {
        "title": "AI 不理解任何东西，它只是在查表",
        "content": """经常有人说："AI 理解了语言的含义。"

我就问一个问题：如果你把"我喜欢苹果"和"苹果降价了"放在一起，AI 知道哪个苹果是水果，哪个是公司吗？

它不知道。它只是发现这几个字经常一起出现。

所谓的"理解"，不过是统计规律。"""

    },
]

# 数据篇模板
DATA_TEMPLATES = [
    {
        "title": "AI 四巨头每年烧掉几百亿，靠什么活着？",
        "content": """算一笔账。

OpenAI 每年亏损可能超过 50 亿美元。Google、Meta、Microsoft 也好不到哪去。

钱花哪了？GPU 电费、人才工资、数据中心。

问题是：什么时候能回本？

答案是：不知道。

AI 公司现在的估值，不是靠利润，是靠想象。"""
    },
    {
        "title": "训练一次 GPT-4 的电费，够普通家庭用电多少年？",
        "content": """有研究说，训练 GPT-4 大概用了 50 亿度电。

50 亿度是什么概念？

一个普通家庭一年用 3000 度。

算一下：5000000000 ÷ 3000 ≈ 166万年

没错，够一个家庭用电 166 万年。

这就是为什么我说：AI 是电老虎。"""
    },
]

# 热点篇模板
HOT_TEMPLATES = [
    {
        "title": "AI 不会取代你，但会用 AI 的人会",
        "content": """每次 AI 出新消息，就有人说"要失业了"。

我觉得这个说法有问题。

汽车没有取代马车夫，汽车司机这个新职业出现了。

AI 也不会取代人，用 AI 的人会淘汰不用 AI 的人。

问题是：你是想当那个"用 AI 的人"，还是"被淘汰的人"？"""
    },
    {
        "title": "当 AI 说谎时，它自己也不知道",
        "content": """AI 有个很严重的问题：它会一本正经地胡说八道。

更可怕的是，它不知道自己说了谎。

因为它不理解语言，它只是在概率性地生成文字。

所以：AI 说的话，不能全信。"""
    },
]

def get_random_content(content_type: str) -> dict:
    """获取随机内容模板"""
    templates = {
        "principle": PRINCIPLE_TEMPLATES,
        "data": DATA_TEMPLATES,
        "hot": HOT_TEMPLATES,
    }
    
    if content_type not in templates:
        raise ValueError(f"未知内容类型: {content_type}")
    
    return random.choice(templates[content_type])

def generate_content(content_type: str, topic: str = None) -> dict:
    """
    生成小红书内容（民科风格，去 AI 化）
    
    Args:
        content_type: principle(原理), data(数据), hot(热点)
        topic: 可选的自定义主题
    
    Returns:
        dict: 包含 title 和 content
    """
    if topic:
        # 根据主题生成自定义内容
        return {
            "title": f"关于「{topic}」，我想说几句",
            "content": f"""关于「{topic}」，网上有各种说法。

有人说好，有人说坏。

我的看法是：{topic} 这事，没有那么玄乎。

原因有三：

第一，{topic} 不是新事物，只是换了名字重新包装。

第二，背后的逻辑很简单，只是被说得太复杂。

第三，真正的问题不在技术，在于人怎么用。

以上。"""
        }
    
    # 使用随机模板
    return get_random_content(content_type)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="小红书内容生成器")
    parser.add_argument("type", choices=["principle", "data", "hot"], 
                        help="内容类型: principle(原理), data(数据), hot(热点)")
    parser.add_argument("--topic", "-t", help="自定义主题")
    
    args = parser.parse_args()
    
    content = generate_content(args.type, args.topic)
    
    print(f"\n标题：{content['title']}")
    print(f"\n内容：{content['content']}")
    print(f"\n字数：{len(content['content'])}")
