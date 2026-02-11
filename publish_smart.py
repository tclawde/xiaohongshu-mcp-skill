#!/usr/bin/env python3
"""
智能发布脚本 - 根据内容主题自动获取相关图片

功能：
1. 根据标题/内容主题搜索相关图片
2. 支持多种图片来源：Unsplash 图库、AI 生成、用户指定
3. 自动上传并发布到小红书
"""

import requests
import base64
import json
import os
import sys

BASE_URL = "http://localhost:18060"

def search_image_from_content(title, content):
    """根据内容主题搜索相关图片"""
    
    # 从标题和内容提取关键词
    keywords = []
    
    # 标题关键词
    if "美院" in title or "美术" in title or "绘画" in title:
        keywords.extend(["art", "painting", "drawing", "sketch", "art_student"])
    if "AI" in title or "人工智能" in content:
        keywords.extend(["AI", "technology", "computer"])
    if "设计" in title:
        keywords.extend(["design", "creative"])
    if "学生" in title or "学习" in content:
        keywords.extend(["student", "study", "learning"])
    if "工具" in title or "软件" in content:
        keywords.extend(["workplace", "computer"])
    
    # 默认关键词
    if not keywords:
        keywords = ["art", "technology", "creative"]
    
    # 尝试从 Unsplash 获取图片
    keyword = keywords[0]  # 使用第一个关键词
    
    print(f"🔍 搜索相关图片: {keyword}")
    
    try:
        # 使用 Unsplash Source API（免费图库）
        # 注意：这是演示用，生产环境建议使用付费 API
        image_url = f"https://source.unsplash.com/800x600/?{keyword}"
        
        # 下载图片
        resp = requests.get(image_url, timeout=10, allow_redirects=True)
        
        if resp.status_code == 200 and len(resp.content) > 1000:
            print(f"✅ 找到相关图片: {keyword}")
            return resp.content
        else:
            raise Exception("图片下载失败")
            
    except Exception as e:
        print(f"⚠️ Unsplash 失败: {e}")
        print("📋 使用备用方案...")
        return None


def generate_cover_image(title, topic):
    """生成封面图片（使用简单绘图）"""
    
    print(f"🎨 生成封面图片: {title[:20]}...")
    
    # 创建一个简单的彩色背景图
    try:
        # 使用 PIL 库
        from PIL import Image, ImageDraw, ImageFont
        
        # 创建图片
        img = Image.new('RGB', (800, 600), color='#1a1a2e')
        d = ImageDraw.Draw(img)
        
        # 绘制简单的装饰线条
        for i in range(0, 800, 20):
            d.line([(i, 0), (i, 600)], fill='#16213e', width=2)
        
        # 绘制标题文字（简化版）
        # 注意：实际使用时需要配置中文字体
        d.text((400, 280), "AI 批判", fill='#e94560', anchor='mm')
        d.text((400, 330), topic, fill='#ffffff', anchor='mm', font_size=24)
        
        # 保存
        img_path = "/tmp/cover_image.jpg"
        img.save(img_path, quality=85)
        
        with open(img_path, 'rb') as f:
            return f.read()
            
    except ImportError:
        print("⚠️ PIL 库未安装，无法生成图片")
        return None
    except Exception as e:
        print(f"❌ 生成图片失败: {e}")
        return None


def encode_image(image_bytes):
    """将图片字节编码为 base64"""
    return base64.b64encode(image_bytes).decode('utf-8')


def publish_to_xiaohongshu(title, content, image_bytes=None):
    """发布到小红书"""
    
    # 处理图片
    if image_bytes:
        image_base64 = encode_image(image_bytes)
        images = [image_base64]
        print(f"✅ 图片已处理: {len(image_bytes)} bytes")
    else:
        # 使用默认测试图片
        default_path = "/tmp/test_cover.jpg"
        if os.path.exists(default_path):
            with open(default_path, 'rb') as f:
                image_bytes = f.read()
            images = [encode_image(image_bytes)]
            print(f"⚠️ 使用默认图片")
        else:
            print("❌ 没有可用图片")
            return False
    
    # 准备发布数据
    data = {
        "title": title,
        "content": content,
        "images": images
    }
    
    print(f"\n📤 准备发布...")
    print(f"   标题: {title[:30]}...")
    print(f"   内容: {len(content)} 字符")
    print(f"   图片: {len(images)} 张")
    
    # 发布
    try:
        resp = requests.post(
            f"{BASE_URL}/api/v1/publish",
            json=data,
            timeout=120
        )
        
        result = resp.json()
        
        if result.get("success"):
            print(f"\n🎉 发布成功！")
            post_id = result.get('data', {}).get('post_id', 'Unknown')
            print(f"   Post ID: {post_id}")
            
            # 保存到记录
            save_publish_record(title, topic, post_id)
            
            return True
        else:
            print(f"\n❌ 发布失败: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return False


def save_publish_record(title, topic, post_id):
    """保存发布记录"""
    
    record = {
        "date": "2026-02-11",
        "time": "17:00",
        "type": "智能发布",
        "title": title,
        "topic": topic,
        "post_id": post_id,
        "response": {
            "likes": 0,
            "comments": 0,
            "shares": 0
        }
    }
    
    # 读取现有记录
    history_file = "/Users/apple/.openclaw/skills/xiaohongshu-mcp/data/post_history.json"
    try:
        with open(history_file, 'r') as f:
            history = json.load(f)
    except:
        history = []
    
    # 添加新记录
    history.append(record)
    
    # 保存
    with open(history_file, 'w') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    print(f"\n📝 记录已保存: {history_file}")


def main():
    """主函数"""
    
    print("=" * 60)
    print("🦀 智能发布 - 根据内容主题获取相关图片")
    print("=" * 60)
    
    # 示例：使用之前创作的内容
    title = "美院学生都在用AI？我就笑了"
    topic = "AI工具与基本功"
    content = """刷到一条笔记，说什么"美院学生常用的AI视频工具大合集"。我就笑了。

这些工具是干嘛的？帮你省事儿的。帮你跳过手绘、构图、色彩训练那些枯燥的东西。

问题是：美院学生不学基本功，以后拿什么吃饭？

AI 能帮你出一张图，能帮你做一条视频。但它能教你怎么配色吗？能告诉你为什么这幅画看着舒服吗？

现在一个个都在炫耀会用多少 AI 工具。我就问一句：离开这些工具，你还剩什么？

当年达芬奇画鸡蛋的时候，可没有什么 AI 帮他省事。基本功这东西，没得省。

以后市场上不缺会写提示词的人，缺的是真正懂美学、懂设计语言的人。

你花时间学 AI 工具，不如花时间画两张速写。

以上。

#AI工具 #美院 #设计 #基本功"""
    
    print(f"\n📌 主题: {topic}")
    print(f"📌 标题: {title}")
    
    # 步骤1：搜索相关图片
    print("\n" + "-" * 60)
    print("步骤 1: 搜索相关图片")
    print("-" * 60)
    
    image_bytes = search_image_from_content(title, content)
    
    # 步骤2：如果没找到，生成封面
    if not image_bytes:
        print("\n" + "-" * 60)
        print("步骤 2: 生成封面图片")
        print("-" * 60)
        
        image_bytes = generate_cover_image(title, topic)
    
    # 步骤3：发布
    if image_bytes:
        print("\n" + "-" * 60)
        print("步骤 3: 发布到小红书")
        print("-" * 60)
        
        success = publish_to_xiaohongshu(title, content, image_bytes)
        
        if success:
            print("\n" + "=" * 60)
            print("✅ 完整发布流程完成！")
            print("=" * 60)
        else:
            print("\n❌ 发布失败")
    else:
        print("\n❌ 无法获取图片，取消发布")


if __name__ == "__main__":
    main()
