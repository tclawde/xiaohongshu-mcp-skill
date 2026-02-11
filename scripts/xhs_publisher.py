#!/usr/bin/env python3
"""
小红书完整发布流程
- 搜索热点
- 生成争议性内容
- 创建配图
- 发布
"""

import os
import sys
import json
import base64
import argparse
from pathlib import Path

# 添加 skill 目录到路径
SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR))

try:
    import requests
except ImportError:
    print("❌ 需要安装 requests: pip install requests")
    sys.exit(1)

# 配置
MCP_URL = os.environ.get("MCP_URL", "http://localhost:18060")
COOKIES_FILE = SKILL_DIR / "data" / "cookies.json"

# 最小 PNG (1x1 白色像素) - base64 编码
MIN_PNG_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="


def get_min_png():
    """获取最小 PNG 字节"""
    return base64.b64decode(MIN_PNG_BASE64)


def save_min_png(path):
    """保存最小 PNG 到文件"""
    with open(path, "wb") as f:
        f.write(get_min_png())
    return path


def check_mcp_status():
    """检查 MCP 状态"""
    try:
        resp = requests.get(f"{MCP_URL}/api/v1/login/status", timeout=5)
        data = resp.json()
        if data.get("success") and data.get("data", {}).get("is_logged_in"):
            print("✅ MCP 已登录")
            return True
        else:
            print("❌ MCP 未登录")
            return False
    except Exception as e:
        print(f"❌ MCP 连接失败: {e}")
        return False


def search_hot(keyword, limit=5):
    """搜索热点"""
    try:
        resp = requests.post(f"{MCP_URL}/api/v1/feeds/search",
                            json={"keyword": keyword, "page": 1, "limit": limit},
                            timeout=30)
        data = resp.json()
        if data.get("success"):
            feeds = data.get("data", {}).get("feeds", [])
            print(f"✅ 找到 {len(feeds)} 条相关内容")
            return feeds
        else:
            print(f"❌ 搜索失败: {data}")
            return []
    except Exception as e:
        print(f"❌ 搜索出错: {e}")
        return []


def create_cover_image(text, output_path="/tmp/xhs_cover.png"):
    """创建封面图片（使用简单方法）"""
    # 使用最小 PNG
    save_min_png(output_path)
    print(f"📷 配图已创建: {output_path}")
    return output_path


def publish_note(title, content, images=None, tags=None):
    """发布笔记"""
    if images is None:
        images = []
    if tags is None:
        tags = []

    # 如果没有图片，使用最小 PNG
    if not images:
        img_path = "/tmp/xhs_cover.png"
        create_cover_image(content, img_path)
        images = [img_path]

    # 准备请求数据
    data = {
        "title": title,
        "content": content,
        "images": images,  # MCP 需要图片路径数组
        "tags": tags
    }

    print(f"📤 发布中...")
    print(f"   标题: {title}")
    print(f"   字数: {len(content)}")

    try:
        resp = requests.post(f"{MCP_URL}/api/v1/publish", json=data, timeout=60)
        result = resp.json()

        if result.get("success"):
            post_id = result.get("data", {}).get("post_id", "")
            print(f"✅ 发布成功！")
            print(f"   Post ID: {post_id}")
            return True
        else:
            print(f"❌ 发布失败: {result}")
            return False
    except Exception as e:
        print(f"❌ 发布出错: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="小红书完整发布流程")
    parser.add_argument("--keyword", "-k", default="AI", help="搜索关键词")
    parser.add_argument("--title", "-t", help="自定义标题")
    parser.add_argument("--content", "-c", help="自定义内容")
    parser.add_argument("--check", action="store_true", help="仅检查 MCP 状态")
    parser.add_argument("--search", action="store_true", help="仅搜索热点")
    parser.add_argument("--list", action="store_true", help="列出最近的热点")
    parser.add_argument("--draft", action="store_true", help="仅生成草稿，不发布")

    args = parser.parse_args()

    print("=" * 50)
    print("📱 小红书发布工具 v2.0")
    print("=" * 50)

    # 检查 MCP 状态
    if not check_mcp_status():
        print("\n💡 请先运行登录:")
        print(f"   cd {SKILL_DIR}")
        print("   bash xhs_login.sh --notify")
        sys.exit(1)

    # 仅检查状态
    if args.check:
        sys.exit(0)

    # 仅搜索
    if args.search:
        feeds = search_hot(args.keyword)
        for i, feed in enumerate(feeds[:5]):
            title = feed.get("noteCard", {}).get("displayTitle", "")
            print(f"  {i+1}. {title}")
        sys.exit(0)

    # 仅列出
    if args.list:
        feeds = search_hot(args.keyword, limit=10)
        for i, feed in enumerate(feeds[:10]):
            title = feed.get("noteCard", {}).get("displayTitle", "")
            interact = feed.get("noteCard", {}).get("interactInfo", {})
            likes = interact.get("likedCount", "0")
            print(f"  {i+1}. {title} (❤️ {likes})")
        sys.exit(0)

    # 使用自定义或生成内容
    if args.title and args.content:
        title = args.title
        content = args.content
    else:
        # 使用内容生成器
        from scripts.xhs_content_generator import generate_content

        print(f"\n🔍 搜索热点: {args.keyword}")
        feeds = search_hot(args.keyword)

        # 获取一个参考标题
        ref_title = ""
        if feeds:
            ref_title = feeds[0].get("noteCard", {}).get("displayTitle", "")

        print("\n✍️ 生成争议性内容...")
        result = generate_content("hot", topic=args.keyword, ref_title=ref_title)
        title = result["title"]
        content = result["content"]
        controversy = result["controversy"]

        print(f"\n📝 争议点: {controversy}")

    # 确认发布
    print("\n" + "=" * 50)
    print(f"📌 标题: {title}")
    print(f"📄 字数: {len(content)}")
    print("=" * 50)
    print(content)
    print("=" * 50)

    if args.draft:
        print("\n💾 草稿已保存（未发布）")
        # 保存到文件
        draft_file = f"/tmp/xhs_draft_{int(__import__('time').time())}.json"
        with open(draft_file, "w", encoding="utf-8") as f:
            json.dump({"title": title, "content": content}, f, ensure_ascii=False, indent=2)
        print(f"   文件: {draft_file}")
        sys.exit(0)

    # 发布
    success = publish_note(title, content)

    if success:
        print("\n🎉 完成！")
    else:
        print("\n❌ 发布失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
