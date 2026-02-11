#!/usr/bin/env python3
"""
智能发布脚本 v2.0 - 集成标题封面生成器

功能：
- 自动生成标题封面（便签风格）
- 一键发布到小红书
"""

import requests
import json
import sys

BASE_URL = "http://localhost:18060"

# 导入标题封面生成器
sys.path.insert(0, "/Users/apple/.openclaw/workspace/title-cover-generator")
from generate import create_title_cover


def generate_cover(title: str, content: str = "") -> str:
    """根据标题生成封面"""
    return create_title_cover(
        title=title,
        output_path="/tmp/title_cover.jpg",
        font_size=90
    )


def publish(title: str, content: str, image_path: str = None) -> bool:
    """发布到小红书"""
    
    # 如果没有图片，自动生成封面
    if not image_path:
        print("🎨 自动生成封面...")
        image_path = generate_cover(title, content)
    
    print(f"\n📤 发布到小红书...")
    print(f"   标题: {title[:30]}...")
    print(f"   图片: {image_path}")
    
    try:
        resp = requests.post(
            f"{BASE_URL}/api/v1/publish",
            json={
                "title": title,
                "content": content,
                "images": [image_path]
            },
            timeout=120
        )
        
        result = resp.json()
        
        if result.get("success"):
            print(f"\n🎉 发布成功！")
            post_id = result.get('data', {}).get('post_id', 'Unknown')
            print(f"   Post ID: {post_id}")
            return True
        else:
            print(f"\n❌ 发布失败: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return False


def main():
    """主函数"""
    
    print("=" * 60)
    print("🦀 智能发布 v2.0 - 集成标题封面生成器")
    print("=" * 60)
    
    # 内容
    title = "美院学生都在用AI？我就笑了"
    content = """刷到一条笔记，说什么"美院学生常用的AI视频工具大合集"。我就笑了。

这些工具是干嘛的？帮你省事儿的。帮你跳过手绘、构图、色彩训练那些枯燥的东西。

问题是：美院学生不学基本功，以后拿什么吃饭？

AI 能帮你出一张图，能帮你做一条视频。但它能教你怎么配色吗？

当年达芬奇画鸡蛋的时候，可没有什么 AI 帮他省事。基本功这东西，没得省。

以后市场上不缺会写提示词的人，缺的是真正懂美学、懂设计语言的人。

你花时间学 AI 工具，不如花时间画两张速写。

#AI工具 #美院 #设计 #基本功"""
    
    print(f"\n📌 标题: {title}")
    print(f"📌 字数: {len(content)} 字符")
    
    # 发布（自动生成封面）
    success = publish(title, content)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ 发布完成！")
        print("=" * 60)
    else:
        print("\n❌ 发布失败")


if __name__ == "__main__":
    main()
