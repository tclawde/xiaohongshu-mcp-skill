#!/usr/bin/env python3
"""
Xiaohongshu MCP Client - A Python client for xiaohongshu-mcp HTTP API.

Usage:
    python xhs_client.py <command> [options]

Commands:
    status              Check login status
    search <keyword>    Search notes by keyword
    detail <feed_id> <xsec_token>   Get note details
    feeds               Get recommended feed list
    publish <title> <content> <images>  Publish a note

Examples:
    python xhs_client.py status
    python xhs_client.py search "咖啡推荐"
    python xhs_client.py detail "abc123" "token456"
    python xhs_client.py feeds
"""

import argparse
import json
import os
import subprocess
import sys
import time
import requests
from pathlib import Path

BASE_URL = "http://localhost:18060"
TIMEOUT = 60
LOGIN_TIMEOUT = 300  # 5 minutes for login process


def get_login_tool_path():
    """Get the path to the xiaohongshu login tool."""
    # Check in common locations
    possible_paths = [
        Path("/Users/apple/.openclaw/workspace/xiaohongshu-login-darwin-arm64"),
        Path("/Users/apple/.openclaw/workspace/xiaohongshu-login-darwin-amd64"),
        Path("/opt/homebrew/bin/xiaohongshu-login-darwin-arm64"),
        Path.cwd() / "xiaohongshu-login-darwin-arm64",
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path)
    
    # Try to find it
    result = subprocess.run(
        ["find", "/Users/apple", "-name", "xiaohongshu-login*", "-type", "f"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode == 0:
        paths = result.stdout.strip().split("\n")
        for path in paths:
            if "arm64" in path or "amd64" in path:
                return path
    
    return None


def is_logged_in():
    """Check if user is logged in."""
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/login/status", timeout=TIMEOUT)
        data = resp.json()
        if data.get("success"):
            login_info = data.get("data", {})
            return login_info.get("is_logged_in", False)
        return False
    except:
        return False


def check_login_status_and_login():
    """Check login status and auto-login if needed."""
    print("🔐 Checking login status...")
    
    if is_logged_in():
        # Get username
        try:
            resp = requests.get(f"{BASE_URL}/api/v1/login/status", timeout=TIMEOUT)
            data = resp.json()
            username = data.get("data", {}).get("username", "Unknown")
            print(f"✅ Already logged in as: {username}")
            return True
        except:
            pass
    
    # Not logged in, need to login
    print("⚠️ Not logged in. Starting login process...")
    
    login_tool = get_login_tool_path()
    if not login_tool:
        print("❌ Login tool not found. Please download it from:")
        print("   https://github.com/xpzouying/xiaohongshu-mcp/releases")
        return False
    
    # Make sure login tool is executable
    try:
        os.chmod(login_tool, 0o755)
    except:
        pass
    
    print("📱 Please scan the QR code with Xiaohongshu app to login.")
    print("⏳ Waiting for login (timeout: 5 minutes)...")
    
    # Start login tool in background
    proc = subprocess.Popen(
        [login_tool],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Wait for login with polling
    start_time = time.time()
    last_status_time = 0
    
    while time.time() - start_time < LOGIN_TIMEOUT:
        # Check every 5 seconds
        time.sleep(5)
        
        # Check if still running
        if proc.poll() is not None:
            # Process ended
            output = proc.stdout.read()
            if "登录成功" in output or "login success" in output.lower():
                print("✅ Login successful!")
                return True
            else:
                print("❌ Login failed or was cancelled.")
                print(f"Output: {output}")
                return False
        
        # Poll login status periodically (every 30 seconds to avoid rate limiting)
        current_time = time.time()
        if current_time - last_status_time > 30:
            last_status_time = current_time
            if is_logged_in():
                print("✅ Login successful!")
                return True
            print("⌛ Still waiting for login...")
    
    # Timeout
    proc.kill()
    print("❌ Login timeout (5 minutes). Please try again.")
    return False


def ensure_logged_in(func):
    """Decorator to ensure user is logged in before executing command."""
    def wrapper(*args, **kwargs):
        if not check_login_status_and_login():
            sys.exit(1)
        return func(*args, **kwargs)
    return wrapper


def check_status():
    """Check login status (auto-login if needed)."""
    if not is_logged_in():
        print("⚠️ Not logged in. Starting login process...")
        if not check_login_status_and_login():
            return None
    
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/login/status", timeout=TIMEOUT)
        data = resp.json()
        if data.get("success"):
            login_info = data.get("data", {})
            if login_info.get("is_logged_in"):
                print(f"✅ Logged in as: {login_info.get('username', 'Unknown')}")
            else:
                print("❌ Not logged in. Please run 'login' command first.")
        else:
            print(f"❌ Error: {data.get('error', 'Unknown error')}")
        return data
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to MCP server. Make sure xiaohongshu-mcp is running on localhost:18060")
        sys.exit(1)


def login():
    """Manually trigger login process."""
    print("🚀 Starting manual login process...")
    success = check_login_status_and_login()
    sys.exit(0 if success else 1)


def search_notes(keyword, sort_by="综合", note_type="不限", publish_time="不限"):
    """Search notes by keyword with optional filters (auto-login if needed)."""
    # Auto-login if not logged in
    if not is_logged_in():
        print("⚠️ Not logged in. Auto-starting login process...")
        if not check_login_status_and_login():
            print("❌ Cannot search without login.")
            return None
    try:
        payload = {
            "keyword": keyword,
            "filters": {
                "sort_by": sort_by,
                "note_type": note_type,
                "publish_time": publish_time
            }
        }
        resp = requests.post(
            f"{BASE_URL}/api/v1/feeds/search",
            json=payload,
            timeout=TIMEOUT
        )
        data = resp.json()
        
        if data.get("success"):
            feeds = data.get("data", {}).get("feeds", [])
            print(f"🔍 Found {len(feeds)} notes for '{keyword}':\n")
            
            for i, feed in enumerate(feeds, 1):
                note_card = feed.get("noteCard", {})
                user = note_card.get("user", {})
                interact = note_card.get("interactInfo", {})
                
                print(f"[{i}] {note_card.get('displayTitle', 'No title')}")
                print(f"    Author: {user.get('nickname', 'Unknown')}")
                print(f"    Likes: {interact.get('likedCount', '0')} | Collects: {interact.get('collectedCount', '0')} | Comments: {interact.get('commentCount', '0')}")
                print(f"    feed_id: {feed.get('id')}")
                print(f"    xsec_token: {feed.get('xsecToken')}")
                print()
        else:
            print(f"❌ Search failed: {data.get('error', 'Unknown error')}")
        
        return data
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to MCP server.")
        sys.exit(1)


def get_note_detail(feed_id, xsec_token, load_comments=False):
    """Get detailed information about a specific note (auto-login if needed)."""
    # Auto-login if not logged in
    if not is_logged_in():
        print("⚠️ Not logged in. Auto-starting login process...")
        if not check_login_status_and_login():
            print("❌ Cannot get details without login.")
            return None
    try:
        payload = {
            "feed_id": feed_id,
            "xsec_token": xsec_token,
            "load_all_comments": load_comments
        }
        resp = requests.post(
            f"{BASE_URL}/api/v1/feeds/detail",
            json=payload,
            timeout=TIMEOUT
        )
        data = resp.json()
        
        if data.get("success"):
            note_data = data.get("data", {}).get("data", {})
            note = note_data.get("note", {})
            comments = note_data.get("comments", {})
            
            print(f"📝 Note Details:\n")
            print(f"Title: {note.get('title', 'No title')}")
            print(f"Author: {note.get('user', {}).get('nickname', 'Unknown')}")
            print(f"Location: {note.get('ipLocation', 'Unknown')}")
            print(f"\nContent:\n{note.get('desc', 'No content')}\n")
            
            interact = note.get("interactInfo", {})
            print(f"Likes: {interact.get('likedCount', '0')} | Collects: {interact.get('collectedCount', '0')} | Comments: {interact.get('commentCount', '0')}")
            
            comment_list = comments.get("list", [])
            if comment_list:
                print(f"\n💬 Top Comments ({len(comment_list)}):")
                for c in comment_list[:5]:
                    user_info = c.get("userInfo", {})
                    print(f"  - {user_info.get('nickname', 'Anonymous')}: {c.get('content', '')}")
        else:
            print(f"❌ Failed to get details: {data.get('error', 'Unknown error')}")
        
        return data
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to MCP server.")
        sys.exit(1)


def get_feeds():
    """Get recommended feed list (auto-login if needed)."""
    # Auto-login if not logged in
    if not is_logged_in():
        print("⚠️ Not logged in. Auto-starting login process...")
        if not check_login_status_and_login():
            print("❌ Cannot get feeds without login.")
            return None
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/feeds/list", timeout=TIMEOUT)
        data = resp.json()
        
        if data.get("success"):
            feeds = data.get("data", {}).get("feeds", [])
            print(f"📋 Recommended Feeds ({len(feeds)} notes):\n")
            
            for i, feed in enumerate(feeds, 1):
                note_card = feed.get("noteCard", {})
                user = note_card.get("user", {})
                interact = note_card.get("interactInfo", {})
                
                print(f"[{i}] {note_card.get('displayTitle', 'No title')}")
                print(f"    Author: {user.get('nickname', 'Unknown')}")
                print(f"    Likes: {interact.get('likedCount', '0')}")
                print()
        else:
            print(f"❌ Failed to get feeds: {data.get('error', 'Unknown error')}")
        
        return data
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to MCP server.")
        sys.exit(1)


def publish_note(title, content, images, tags=None):
    """Publish a new note (auto-login if needed)."""
    # Auto-login if not logged in
    if not is_logged_in():
        print("⚠️ Not logged in. Auto-starting login process...")
        if not check_login_status_and_login():
            print("❌ Cannot publish without login.")
            return None
    try:
        payload = {
            "title": title,
            "content": content,
            "images": images if isinstance(images, list) else [images]
        }
        if tags:
            payload["tags"] = tags if isinstance(tags, list) else [tags]
        
        resp = requests.post(
            f"{BASE_URL}/api/v1/publish",
            json=payload,
            timeout=120
        )
        data = resp.json()
        
        if data.get("success"):
            print(f"✅ Note published successfully!")
            print(f"   Post ID: {data.get('data', {}).get('post_id', 'Unknown')}")
        else:
            print(f"❌ Publish failed: {data.get('error', 'Unknown error')}")
        
        return data
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to MCP server.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Xiaohongshu MCP Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # status command
    subparsers.add_parser("status", help="Check login status (auto-login if needed)")
    
    # login command
    subparsers.add_parser("login", help="Manually trigger login process")
    
    # search command
    search_parser = subparsers.add_parser("search", help="Search notes")
    search_parser.add_argument("keyword", help="Search keyword")
    search_parser.add_argument("--sort", default="综合", 
                               choices=["综合", "最新", "最多点赞", "最多评论", "最多收藏"],
                               help="Sort by")
    search_parser.add_argument("--type", default="不限",
                               choices=["不限", "视频", "图文"],
                               help="Note type")
    search_parser.add_argument("--time", default="不限",
                               choices=["不限", "一天内", "一周内", "半年内"],
                               help="Publish time")
    search_parser.add_argument("--json", action="store_true", help="Output raw JSON")
    
    # detail command
    detail_parser = subparsers.add_parser("detail", help="Get note details")
    detail_parser.add_argument("feed_id", help="Feed ID")
    detail_parser.add_argument("xsec_token", help="Security token")
    detail_parser.add_argument("--comments", action="store_true", help="Load all comments")
    detail_parser.add_argument("--json", action="store_true", help="Output raw JSON")
    
    # feeds command
    feeds_parser = subparsers.add_parser("feeds", help="Get recommended feeds")
    feeds_parser.add_argument("--json", action="store_true", help="Output raw JSON")
    
    # publish command
    publish_parser = subparsers.add_parser("publish", help="Publish a note")
    publish_parser.add_argument("title", help="Note title")
    publish_parser.add_argument("content", help="Note content")
    publish_parser.add_argument("images", help="Image URLs (comma-separated)")
    publish_parser.add_argument("--tags", help="Tags (comma-separated)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "status":
        result = check_status()
    elif args.command == "login":
        result = login()
    elif args.command == "search":
        result = search_notes(args.keyword, args.sort, args.type, args.time)
        if hasattr(args, 'json') and args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "detail":
        result = get_note_detail(args.feed_id, args.xsec_token, args.comments)
        if hasattr(args, 'json') and args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "feeds":
        result = get_feeds()
        if hasattr(args, 'json') and args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "publish":
        images = args.images.split(",")
        tags = args.tags.split(",") if args.tags else None
        result = publish_note(args.title, args.content, images, tags)


if __name__ == "__main__":
    main()
