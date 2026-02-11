#!/usr/bin/env python3
"""
Xiaohongshu MCP Client - Direct Protocol Implementation

This module provides direct access to MCP tools including post_comment_to_feed
which is not available via HTTP REST API.

Usage:
    python xhs_mcp.py tools                    # List all available tools
    python xhs_mcp.py comment <id> <token> <msg>  # Post a comment
"""

import argparse
import json
import subprocess
import sys
import time

BASE_URL = "http://localhost:18060"
MCP_ENDPOINT = f"{BASE_URL}/mcp"


def mcp_request(method, params=None, session_id=None, cookie_file=None):
    """Make MCP request via curl."""
    cmd = [
        "curl", "-s", "-X", "POST", MCP_ENDPOINT,
        "-H", "Content-Type: application/json"
    ]
    
    if session_id:
        cmd.extend(["-H", f"Mcp-Session-Id: {session_id}"])
    
    if cookie_file:
        cmd.extend(["-c", cookie_file, "-b", cookie_file])
    
    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000),
        "method": method,
        "params": params or {}
    }
    cmd.extend(["-d", json.dumps(payload)])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout) if result.stdout else None
    except json.JSONDecodeError:
        return {"raw": result.stdout, "stderr": result.stderr}


def init_session(cookie_file):
    """Initialize MCP session and return session ID."""
    resp = mcp_request(
        "initialize",
        params={
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "xhs-client", "version": "1.0.0"}
        },
        cookie_file=cookie_file
    )
    
    # Extract session ID from curl output (it's in the header)
    cmd = [
        "curl", "-s", "-i", "-X", "POST", MCP_ENDPOINT,
        "-H", "Content-Type: application/json",
        "-c", cookie_file,
        "-d", json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "xhs-client", "version": "1.0.0"}
            }
        })
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Extract session ID from headers
    session_id = None
    for line in result.stdout.split('\n'):
        if line.lower().startswith('mcp-session-id:'):
            session_id = line.split(':', 1)[1].strip()
            break
    
    return session_id


def list_tools():
    """List all available MCP tools."""
    cookie_file = f"/tmp/xhs_mcp_{int(time.time())}.cookies"
    session_id = init_session(cookie_file)
    
    if not session_id:
        print("❌ Failed to initialize MCP session")
        return []
    
    # Send initialized notification
    mcp_request("notifications/initialized", session_id=session_id, cookie_file=cookie_file)
    
    # List tools
    result = mcp_request("tools/list", session_id=session_id, cookie_file=cookie_file)
    
    if result and "result" in result:
        tools = result.get("result", {}).get("tools", [])
        print(f"\n📋 Available MCP Tools ({len(tools)}):\n")
        for tool in tools:
            name = tool.get("name", "Unknown")
            desc = tool.get("description", "No description")
            print(f"  • {name}")
            print(f"    {desc}\n")
        return tools
    else:
        print(f"❌ Failed to list tools: {result}")
        return []


def post_comment(feed_id, xsec_token, content):
    """Post a comment to a Xiaohongshu feed."""
    cookie_file = f"/tmp/xhs_mcp_{int(time.time())}.cookies"
    session_id = init_session(cookie_file)
    
    if not session_id:
        print("❌ Failed to initialize MCP session")
        return False
    
    # Send initialized notification
    mcp_request("notifications/initialized", session_id=session_id, cookie_file=cookie_file)
    
    # Post comment
    print(f"📝 Posting comment to {feed_id}...")
    result = mcp_request("tools/call", session_id=session_id, cookie_file=cookie_file, params={
        "name": "post_comment_to_feed",
        "arguments": {
            "feed_id": feed_id,
            "xsec_token": xsec_token,
            "content": content
        }
    })
    
    if result and "result" in result:
        print("✅ Comment posted successfully!")
        print(f"   {json.dumps(result, ensure_ascii=False, indent=2)}")
        return True
    else:
        print(f"❌ Failed to post comment: {result}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Xiaohongshu MCP Client - Direct Protocol Access",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # tools command
    subparsers.add_parser("tools", help="List all available MCP tools")
    
    # comment command
    comment_parser = subparsers.add_parser("comment", help="Post a comment to a feed")
    comment_parser.add_argument("feed_id", help="Feed ID (from search or feeds list)")
    comment_parser.add_argument("xsec_token", help="XSec token (from search or feeds list)")
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
