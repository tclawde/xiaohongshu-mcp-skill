#!/usr/bin/env python3
"""
小红书内容生成器 - AI 反对者/民科风格

争议性内容 + 热点结合 + 去 AI 化
"""

import argparse
import json
import random
from datetime import datetime
from pathlib import Path

# 数据路径
DATA_DIR = Path(__file__).parent.parent / "data"
HISTORY_FILE = DATA_DIR / "post_history.json"
HOT_TOPICS_FILE = DATA_DIR / "hot_topics.json"

# 原理篇争议内容
PRINCIPLE_CONTROVERSY = [
    {
        "title": "深度学习就是统计学，别被那些术语骗了",
        "content": """今天看到一个说法，说深度学习是"模仿人脑神经网络"。

我就笑了。

人脑神经元是电化学信号，深度学习是矩阵乘法。这俩有半毛钱关系？

所谓"神经网络"，就是一个个数学公式嵌套在一起。输入数据 → 矩阵运算 → 输出结果。仅此而已。

深度学习做的事情就是：给定一堆输入输出，找出让它们对应起来的数学公式。

这不是智能，这是高级计算器。""",
        "controversy": "把深度学习说成是AI是偷换概念"
    },
    {
        "title": "AI 不理解任何东西，它只是在查表",
        "content": """经常有人说："AI 理解了语言的含义。"

我就问一个问题：如果你把"我喜欢苹果"和"苹果降价了"放在一起，AI 知道哪个苹果是水果，哪个是公司吗？

它不知道。它只是发现这几个字经常一起出现。

所谓的"理解"，不过是统计规律。

所以别再说什么"AI 有理解能力"了，它连自己在说什么都不知道。""",
        "controversy": "AI 无法理解任何东西，这是原理决定的"
    },
    {
        "title": "神经网络就是个黑盒，说得清楚原理吗？",
        "content": """很多人说深度学习"原理清晰"。

我就问一个问题：为什么这个神经网络有效，换一个结构就不行？

不知道。

这就是为什么我说深度学习是"炼金术"：我们知道它有用，但不知道它为什么有用。

科学追求"为什么"，深度学习只关心"是什么"。

这不是科学，这是经验主义。""",
        "controversy": "深度学习是经验主义，不是科学"
    },
    {
        "title": "所谓 AGI 是皇帝的新衣，你们都信？",
        "content": """全都在喊 AGI 要来了。

我就问一个问题：现在的 AI，能通过小学数学考试吗？

不能。

连简单的推理都做不好，还 AGI？

所谓 AGI，就是皇帝的新衣。

没人愿意承认自己看不见。""",
        "controversy": "AGI 是皇帝的新衣"
    },
    {
        "title": "AI 越进步，人类越蠢",
        "content": """有人说 AI 是工具，帮助人类进步。

我看到的是：AI 越强，人类越懒。

计算器让我们不会心算了，导航让我们不会认路了。

AI 让我们不会思考了。

关键是：AI 替你想，你就不想了。

这不是进步，这是退化。""",
        "controversy": "AI 导致人类认知退化"
    },
]

# 数据篇争议内容
DATA_CONTROVERSY = [
    {
        "title": "AI 四巨头每年烧掉几百亿，靠什么活着？",
        "content": """算一笔账。

OpenAI 每年亏损可能超过 50 亿美元。Google、Meta、Microsoft 也好不到哪去。

钱花哪了？GPU 电费、人才工资、数据中心。

问题是：什么时候能回本？

答案是：不知道。

AI 公司现在的估值，不是靠利润，是靠想象。""",
        "controversy": "AI 公司靠想象估值，不是靠利润"
    },
    {
        "title": "训练一次 GPT-4 的电费，够普通家庭用电多少年？",
        "content": """有研究说，训练 GPT-4 大概用了 50 亿度电。

50 亿度是什么概念？

一个普通家庭一年用 3000 度。

算一下：5000000000 ÷ 3000 ≈ 166万年

没错，够一个家庭用电 166 万年。

这就是为什么我说：AI 是电老虎。

所谓的"科技进步"，代价是什么？""",
        "controversy": "AI 是能源浪费"
    },
    {
        "title": "AI 公司亏损全记录，看谁先撑不住",
        "content": """列个清单：

OpenAI：预计 2024 年亏损 50 亿
Anthropic：预计 2024 年亏损 27 亿
Google AI：年年亏损上百亿
Meta AI：亏损无上限

钱从哪里来？投资人。

投资人为什么投？相信故事。

故事什么时候破？不知道。

但我知道：总有破的一天。""",
        "controversy": "AI 公司靠投资人的钱活着"
    },
    {
        "title": "AI 岗位薪资大降薪，有人知道吗？",
        "content": """都在说 AI 薪资高。

我说个反的：AI 岗位薪资在降。

为什么？因为会的人多了。

2023 年 AI 工程师薪资顶峰，2024 年开始回落。

为什么？供需关系。

培训班出来一批，学生毕业一批，薪资能不降吗？

高位接盘的，都是相信自己不会是最后一棒的人。""",
        "controversy": "AI 岗位薪资在降，不是涨"
    },
    {
        "title": "AI 课程割韭菜全记录，看你中招没",
        "content": """ypescript 和 Python 培训班都在喊：学 AI ，月薪百万。

实际呢？

初级 AI 岗位要求硕士学历 + 论文 + 竞赛 + 实习。

培训班教的都是皮毛。

出来能找到工作吗？

大部分不能。

这就是割韭菜：教你入门，然后告诉你"继续深造"。

深造就花钱，继续割。""",
        "controversy": "AI 培训课程是割韭菜"
    },
]

# 热点篇争议内容
HOT_CONTROVERSY = [
    {
        "title": "AI 不会取代你，但会用 AI 的人会",
        "content": """每次 AI 出新消息，就有人说"要失业了"。

我觉得这个说法有问题。

汽车没有取代马车夫，汽车司机这个新职业出现了。

AI 也不会取代人，用 AI 的人会淘汰不用 AI 的人。

问题是：你是想当那个"用 AI 的人"，还是"被淘汰的人"？

自己选。""",
        "controversy": "不是 AI 取代人，是会用 AI 的人淘汰不会用的人"
    },
    {
        "title": "当 AI 说谎时，它自己也不知道",
        "content": """AI 有个很严重的问题：它会一本正经地胡说八道。

更可怕的是，它不知道自己说了谎。

因为它不理解语言，它只是在概率性地生成文字。

所以：AI 说的话，不能全信。

尤其是那些看起来很专业的。""",
        "controversy": "AI 会说谎，而且自己不知道"
    },
    {
        "title": "AI 客服的噩梦：为什么 AI 永远在绕圈子",
        "content": """你们打过 AI 客服吗？

我说一个我的经历：

我想退订，说了十遍"退订"，AI 还在问"您确定要退订吗？"

我说"确定"，它回"好的，为您推荐我们的新套餐"。

我当场去世。

AI 客服就是：你在和一段 if-else 代码对话。

它永远在绕圈子，永远不会说"好的，我帮你退"。""",
        "controversy": "AI 客服是灾难"
    },
    {
        "title": "所谓 AI 绘画，就是偷窃艺术家的作品",
        "content": """AI 绘画火了对吧？

怎么火的？喂了无数艺术家的作品。

问过艺术家吗？没有。

授权了吗？没有。

这叫什么？

叫偷窃。

换了个名字叫"训练"，就合法了？

我不信。""",
        "controversy": "AI 绘画是偷窃"
    },
    {
        "title": "AI 编程工具让我担心：代码质量越来越差",
        "content": """公司里来了批用 AI 编程的年轻人。

写的代码，能跑，但没法看。

为什么？因为 AI 生成的代码，能用就行，不讲究。

长此以往，代码库会变成什么样？

一团浆糊。

AI 让编程变简单了，但也让代码变烂了。""",
        "controversy": "AI 让代码质量下降"
    },
    {
        "title": "朋友被 AI 课程割韭菜，拦都拦不住",
        "content": """朋友跟我说：有个 AI 课，学会了月入 5 万。

我问：什么内容？
答：教我用 ChatGPT 写文案。
我问：会写文案就能月入 5 万？
答：老师说可以。
我问：老师月入多少？
答：......

拦都拦不住。

这年头，焦虑是最好的镰刀。""",
        "controversy": "AI 课程是焦虑驱动的镰刀"
    },
    {
        "title": "AI 不会让你失业，不用 AI 的人会让你失业",
        "content": """又一个反直觉的观点：

不是 AI 让你失业，是不用 AI 的人让你失业。

什么意思？

你的竞争对手会用 AI 提效，成本比你低。

老板选谁？选成本低的。

所以你失业不是因为 AI，是因为有人比你更会用 AI。

问题来了：你是那个"用 AI 的人"吗？""",
        "controversy": "不用 AI 的人才会失业"
    },
]

def load_history():
    """加载发布历史"""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return []

def save_history(history):
    """保存发布历史"""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_hot_topics():
    """加载热点选题"""
    if HOT_TOPICS_FILE.exists():
        with open(HOT_TOPICS_FILE) as f:
            return json.load(f)
    return []

def add_to_history(content_type, title, controversy):
    """添加到发布历史"""
    history = load_history()
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "type": content_type,
        "title": title,
        "controversy_point": controversy,
        "response": {
            "likes": 0,
            "comments": 0,
            "shares": 0
        }
    }
    history.insert(0, entry)
    save_history(history[-100:])  # 只保留最近 100 条
    return entry

def get_templates(content_type):
    """获取内容模板"""
    templates = {
        "principle": PRINCIPLE_CONTROVERSY,
        "data": DATA_CONTROVERSY,
        "hot": HOT_CONTROVERSY,
    }
    return templates.get(content_type, [])

def generate_content(content_type, topic=None, add_to_history_flag=False):
    """
    生成小红书内容（民科风格，有争议，去 AI 化）
    
    Args:
        content_type: principle(原理), data(数据), hot(热点)
        topic: 可选的自定义主题
        add_to_history_flag: 是否添加到历史记录
    """
    if topic:
        # 根据主题生成内容
        content = generate_custom_content(topic)
    else:
        # 随机模板
        templates = get_templates(content_type)
        if not templates:
            print("❌ 无可用模板")
            return None
        item = random.choice(templates)
        content = {
            "title": item["title"],
            "content": item["content"],
            "controversy": item["controversy"]
        }
    
    # 可选：添加到历史
    if add_to_history_flag:
        add_to_history(content_type, content["title"], content["controversy"])
    
    return content

def generate_custom_content(topic):
    """根据自定义主题生成内容（争议风格）"""
    
    # 争议性开场
    openers = [
        f"关于「{topic}」，网上一片叫好。",
        f"都说topic是未来。",
        f"最近「{topic}」很火对吧？",
    ]
    
    # 反直觉观点
    angles = [
        "但我觉得这就是个泡沫。",
        "但真相可能让你失望。",
        "但我想说点不一样的。",
        "不过先让我泼盆冷水。",
    ]
    
    # 争议点
    controversy_points = [
        "为什么？因为背后的逻辑很简单，只是被包装得很玄乎。",
        "为什么？因为大多数人只是在跟风，根本没搞清楚状况。",
        "为什么？因为利益相关者在制造焦虑，然后收割你。",
        "为什么？因为这就是皇帝的新衣，没人愿意第一个说破。",
    ]
    
    # 结尾态度
    endings = [
        "反正我是不信的。",
        "你信不信是你的事。",
        "总之我觉得不对劲。",
        "以上就是我的看法，不服来辩。",
    ]
    
    opener = random.choice(openers)
    angle = random.choice(angles)
    controversy = random.choice(controversy_points)
    ending = random.choice(endings)
    
    content = f"""{opener}{angle}

{controversy}

这就是为什么我说：很多人在制造焦虑，真正的问题没人关心。

{ending}"""
    
    return {
        "title": f"关于「{topic}」，我想说几句真话",
        "content": content,
        "controversy": f"反直觉观点：{topic} 可能不是你想的那样"
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="小红书内容生成器 - AI 反对者/民科风格")
    parser.add_argument("type", choices=["principle", "data", "hot"], 
                        help="内容类型")
    parser.add_argument("--topic", "-t", help="自定义主题")
    parser.add_argument("--save", "-s", action="store_true", 
                        help="保存到历史记录")
    parser.add_argument("--list", "-l", action="store_true",
                        help="列出所有模板")
    
    args = parser.parse_args()
    
    if args.list:
        # 列出所有模板
        for ct in ["principle", "data", "hot"]:
            print(f"\n{'='*50}")
            print(f"【{ct.upper()}】")
            print('='*50)
            for i, t in enumerate(get_templates(ct)):
                print(f"\n{i+1}. {t['title']}")
        exit(0)
    
    # 生成内容
    content = generate_content(args.type, args.topic, args.save)
    
    if content:
        print(f"\n{'='*60}")
        print(f"【标题】{content['title']}")
        print(f"【争议点】{content['controversy']}")
        print('='*60)
        print(f"\n{content['content']}")
        print(f"\n{'='*60}")
        print(f"字数：{len(content['content'])}")
        if args.save:
            print(f"✅ 已保存到历史记录")
