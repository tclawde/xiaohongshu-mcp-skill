#!/usr/bin/env python3
"""
Xiaohongshu MCP Protocol Caller - Complete Implementation
"""

import json
import sys
import time

import requests

BASE_URL = "http://localhost:18060"
MCP_URL = f"{BASE_URL}/mcp"
TIMEOUT = 30


class XiaohongshuMCP:
    def __init__(self):
        self.session_id = None
        self.initialize()
    
    def initialize(self):
        """Initialize MCP session."""
        resp = requests.post(
            MCP_URL,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "xhs-client", "version": "1.0.0"}
                }
            },
            timeout=TIMEOUT
        )
        result = resp.json()
        if "result" in result:
            self.session_id = result.get("result", {}).get("sessionId")
            # Send initialized notification
            headers = {"Content-Type": "application/json"}
            if self.session_id:
                headers["Mcp-Session-Id"] = self.session_id
            
            requests.post(
                MCP_URL,
                json={
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized",
                    "params": {}
                },
                headers=headers,
                timeout=TIMEOUT
            )
            print("✅ MCP session initialized")
            return True
        print(f"❌ Initialize failed: {result}")
        return False
    
    def call_tool(self, name, arguments):
        """Call an MCP tool."""
        payload = {
            "jsonrpc": "2.0",
            "id": int(time.time() * 1000),
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }
        headers = {"Content-Type": "application/json"}
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        
        resp = requests.post(
            MCP_URL,
            json=payload,
            headers=headers,
            timeout=TIMEOUT
        )
        return resp.json()
    
    def list_tools(self):
        """List all available tools."""
        result = self.call_tool("resources/list", {})
        if "result" in result:
            tools = result.get("result", {}).get("tools", [])
            print(f"\n📋 Available tools ({len(tools)}):\n")
            for tool in tools:
                print(f"  • {tool.get('name')}")
                print(f"    {tool.get('description')}\n")
            return tools
        return []
    
    def post_comment(self, feed_id, xsec_token, content):
        """Post a comment to a feed."""
        print(f"📝 Posting comment to {feed_id}...")
        result = self.call_tool("post_comment_to_feed", {
            "feed_id": feed_id,
            "xsec_token": xsec_token,
            "content": content
        })
        
        if "result" in result:
            print("✅ Comment posted!")
            print(f"   {json.dumps(result, ensure_ascii=False)}")
            return True
        else:
            print(f"❌ Failed: {result}")
            return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python xhs_mcp_call.py <command> [args]")
        print("\nCommands:")
        print("  tools                          - List all available tools")
        print("  comment <feed_id> <token> <content>  - Post a comment")
        sys.exit(1)
    
    mcp = XiaohongshuMCP()
    cmd = sys.argv[1]
    
    if cmd == "tools":
        mcp.list_tools()
    elif cmd == "comment" and len(sys.argv) >= 5:
        feed_id = sys.argv[2]
        token = sys.argv[3]
        content = sys.argv[4]
        success = mcp.post_comment(feed_id, token, content)
        sys.exit(0 if success else 1)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
