#!/usr/bin/env python3
"""
小红书热点追踪器

追踪 AI 相关热点，记录争议话题
"""

import argparse
import json
import requests
from datetime import datetime
from pathlib import Path

# 配置
BASE_URL = "http://localhost:18060"
DATA_DIR = Path(__file__).parent.parent / "data"
HOT_TOPICS_FILE = DATA_DIR / "hot_topics.json"
CONTROVERSY_FILE = DATA_DIR / "controversy_ideas.json"

def search_hot(keyword="AI", limit=20):
    """搜索小红书热点"""
    try:
        resp = requests.post(
            f"{BASE_URL}/api/v1/search",
            params={"keyword": keyword},
            json={"limit": limit},
            timeout=60
        )
        data = resp.json()
        if data.get("success"):
            return data.get("data", [])
        return []
    except Exception as e:
        print(f"❌ 搜索失败: {e}")
        return []

def analyze_controversy(note):
    """分析笔记的争议性"""
    controversy_score = 0
    
    # 争议关键词
    positive_words = ["颠覆", "革命", "取代", "失业", "未来", "突破"]
    negative_words = ["炒作", "泡沫", "亏损", "浪费", "虚假", "危险"]
    
    title = note.get("title", "")
    desc = note.get("desc", "")
    
    # 检查是否有争议点
    for word in positive_words:
        if word in title or word in desc:
            controversy_score += 1
    
    for word in negative_words:
        if word in title or word in desc:
            controversy_score += 1
    
    return controversy_score

def track_hot_topics(content_type="AI", limit=50):
    """追踪热点"""
    notes = search_hot(content_type, limit)
    
    results = []
    for note in notes[:20]:  # 只处理前 20 个
        score = analyze_controversy(note)
        results.append({
            "title": note.get("title", ""),
            "desc": note.get("desc", "")[:200],
            "controversy_score": score,
            "source": "xiaohongshu",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "url": note.get("link", ""),
            "status": "pending"
        })
    
    # 按争议性排序
    results.sort(key=lambda x: x["controversy_score"], reverse=True)
    
    return results

def save_hot_topics(topics):
    """保存热点"""
    with open(HOT_TOPICS_FILE, 'w', encoding='utf-8') as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)
    print(f"✅ 保存 {len(topics)} 条热点到 {HOT_TOPICS_FILE}")

def add_controversy_idea(topic, angle, status="pending"):
    """添加争议话题"""
    ideas = []
    if CONTROVERSY_FILE.exists():
        with open(CONTROVERSY_FILE) as f:
            ideas = json.load(f)
    
    ideas.append({
        "topic": topic,
        "angle": angle,
        "status": status,
        "created_at": datetime.now().strftime("%Y-%m-%d")
    })
    
    with open(CONTROVERSY_FILE, 'w', encoding='utf-8') as f:
        json.dump(ideas, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 添加争议话题: {topic}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="小红书热点追踪器")
    parser.add_argument("--keyword", "-k", default="AI", help="搜索关键词")
    parser.add_argument("--limit", "-l", type=int, default=50, help="搜索数量")
    parser.add_argument("--save", "-s", action="store_true", help="保存到文件")
    parser.add_argument("--list", action="store_true", help="列出保存的热点")
    parser.add_argument("--add", "-a", nargs=2, metavar=("TOPIC", "ANGLE"), help="添加争议话题")
    
    args = parser.parse_args()
    
    if args.list:
        # 列出保存的热点
        if HOT_TOPICS_FILE.exists():
            with open(HOT_TOPICS_FILE) as f:
                topics = json.load(f)
            print(f"\n📊 共 {len(topics)} 条热点记录\n")
            for i, t in enumerate(topics[:10]):
                print(f"{i+1}. [{t['controversy_score']}⭐] {t['title'][:50]}")
        else:
            print("无保存的热点记录")
        exit(0)
    
    if args.add:
        add_controversy_idea(args.add[0], args.add[1])
        exit(0)
    
    # 搜索并追踪
    print(f"🔍 搜索热点: {args.keyword}")
    topics = track_hot_topics(args.keyword, args.limit)
    
    print(f"\n📊 找到 {len(topics)} 条相关内容\n")
    print("🔥 争议性最高的 TOP 5:\n")
    
    for i, t in enumerate(topics[:5]):
        print(f"{i+1}. {t['title'][:60]}...")
        print(f"   争议指数: {'⭐' * t['controversy_score']}")
        print()
    
    if args.save:
        save_hot_topics(topics)
