#!/usr/bin/env python3
"""
Xiaohongshu MCP Comment Test - Direct MCP Protocol Call

This script directly implements the MCP protocol to call post_comment_to_feed
since it's not exposed via HTTP REST API.
"""

import argparse
import json
import sys
import time

import requests

BASE_URL = "http://localhost:18060"
MCP_URL = f"{BASE_URL}/mcp"
TIMEOUT = 60


def mcp_request(method, params=None):
    """Make a direct MCP protocol request."""
    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000),
        "method": method,
        "params": params or {}
    }
    
    try:
        resp = requests.post(
            MCP_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        return resp.json()
    except Exception as e:
        print(f"❌ MCP request failed: {e}")
        return None


def list_tools():
    """List all available MCP tools."""
    print("🔧 Listing available MCP tools...")
    result = mcp_request("tools/list")
    
    if result and "result" in result:
        tools = result.get("result", {}).get("tools", [])
        print(f"\n📋 Found {len(tools)} tools:\n")
        for tool in tools:
            print(f"  • {tool.get('name', 'Unknown')}")
            print(f"    Description: {tool.get('description', 'N/A')}")
            print()
    else:
        print(f"❌ Failed to list tools: {result}")


def post_comment(feed_id, xsec_token, content):
    """Post a comment to a feed using MCP protocol."""
    print(f"📝 Posting comment to feed {feed_id}...")
    print(f"   Content: {content}")
    
    result = mcp_request("tools/call", {
        "name": "post_comment_to_feed",
        "arguments": {
            "feed_id": feed_id,
            "xsec_token": xsec_token,
            "content": content
        }
    })
    
    if result and "result" in result:
        print("✅ Comment posted successfully!")
        print(f"   Result: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return True
    else:
        print(f"❌ Failed to post comment: {result}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Xiaohongshu MCP Comment Test - Direct MCP Protocol",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # list tools
    subparsers.add_parser("tools", help="List all available MCP tools")
    
    # comment command
    comment_parser = subparsers.add_parser("comment", help="Post a comment to a feed")
    comment_parser.add_argument("feed_id", help="Feed ID")
    comment_parser.add_argument("xsec_token", help="XSec Token")
    comment_parser.add_argument("content", help="Comment content")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "tools":
        list_tools()
    elif args.command == "comment":
        success = post_comment(args.feed_id, args.xsec_token, args.content)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
