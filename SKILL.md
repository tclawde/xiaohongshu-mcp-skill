---
name: xiaohongshu-mcp
description: "Automate Xiaohongshu (RedNote/小红书) via MCP: search posts by keyword, publish notes with cover images, reply to and like comments, collect posts, check login status, and manage cookies. Use when the user wants to post content to Xiaohongshu, search RedNote feeds, interact with 小红书 comments, automate rednote publishing workflows, or manage a Xiaohongshu account programmatically."
---

# Xiaohongshu MCP Skill

> 基于 [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) 构建

## Quick Start

### 1. 登录

```bash
# 方式1：一键登录（推荐）
bash xhs_login.sh --notify

# 方式2：本地登录
bash xhs_login.sh
```

Verify login succeeded before proceeding:

```bash
python3 scripts/xhs_client.py status
```

If status shows logged out, re-run `bash xhs_login.sh` and scan the QR code.

### 2. 启动 MCP 服务器

```bash
./xiaohongshu-mcp-darwin-arm64 &
```

Confirm the server is running:

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:18060/mcp
```

A `405` response means the server is up. No response means it failed to start — check `mcp.log`.

### 3. 使用功能

```bash
# 检查登录状态
python3 scripts/xhs_client.py status

# 搜索内容
python3 scripts/xhs_client.py search "AI"

# 发布内容
python3 scripts/xhs_client.py publish "标题" "内容" "图片URL"
```

---

## MCP Tools

| 工具 | 功能 | 使用场景 |
|------|------|---------|
| `check_login_status` | 检查登录状态 | 确认账号状态 |
| `list_feeds` | 获取推荐列表 | 发现热门内容 |
| `search_feeds` | 搜索内容 | 关键词搜索 |
| `get_feed_detail` | 获取帖子详情 | 查看评论 |
| `publish_content` | 发布图文 | 创作新内容 |
| `publish_with_video` | 发布视频 | 视频内容 |
| `post_comment_to_feed` | 发表评论 | 回复粉丝 |
| `reply_comment_in_feed` | 回复评论 | 互动 |
| `like_feed` | 点赞 | 点赞帖子 |
| `favorite_feed` | 收藏 | 收藏帖子 |
| `delete_cookies` | 删除 cookies | 重置登录 |
| `get_login_qrcode` | 获取二维码 | 重新登录 |
| `user_profile` | 获取用户主页 | 查看主页 |

---

## 评论互动策略

For full comment strategy (persona, reply templates, tone rules), see [STRATEGY.md](STRATEGY.md).

---

## 技术实现

### MCP Session 获取

```bash
# 初始化
RESPONSE=$(curl -s -i -X POST http://localhost:18060/mcp \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}')

# 提取 Session ID
SESSION_ID=$(echo "$RESPONSE" | grep -i "Mcp-Session-Id:" | cut -d' ' -f2)
```

### 示例：完整发布流程

```bash
#!/bin/bash
MCP_URL="http://localhost:18060/mcp"
COOKIE_FILE="cookies.txt"

# 1. 初始化
RESPONSE=$(curl -s -i -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -c "$COOKIE_FILE" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}')

SESSION_ID=$(echo "$RESPONSE" | grep -i "Mcp-Session-Id:" | cut -d' ' -f2)

# 2. 发送初始化通知
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' > /dev/null

# 3. 发布内容
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "id": 100,
    "method": "tools/call",
    "params": {
      "name": "publish_content",
      "arguments": {
        "title": "AI正在毁掉这一代年轻人？",
        "content": "🔥 争议话题...\n\n详细内容...",
        "images": ["/tmp/cover.jpg"]
      }
    }
  }'
```

If the response contains `"error"`, check login status and retry. Common errors: expired cookies (re-login), missing images (verify file path exists).

---

## 脚本工具

### xhs_client.py - Python 客户端

```bash
# 检查状态
python3 scripts/xhs_client.py status

# 搜索
python3 scripts/xhs_client.py search "AI" --sort "最新" --type "图文" --time "一周内"

# 发布
python3 scripts/xhs_client.py publish "标题" "内容" "图片URL" --tags "标签1,标签2"

# 获取详情
python3 scripts/xhs_client.py detail <feed_id> <xsec_token> --comments
```

### xhs_mcp.py - MCP 直接调用

```bash
# 列出所有工具
python3 scripts/xhs_mcp.py tools

# 发表评论
python3 scripts/xhs_mcp.py comment <feed_id> <xsec_token> "评论内容"
```

### generate_cover.py - 封面生成器

```bash
# 生成封面
python3 generate_cover.py --title "标题" --output /tmp/cover.jpg

# 选项
--font-size 80      # 字体大小
--padding 60         # 内边距
--max-width 600      # 最大宽度
```

---

## File Structure

```
xiaohongshu-mcp-skill/
├── SKILL.md              # 本文档
├── README.md             # 中文文档
├── STRATEGY.md          # 运营策略（含评论互动）
├── install.sh            # 安装脚本
├── xhs_login.sh         # 一键登录
├── generate_cover.py     # 封面生成器
├── data/
│   ├── post_history.json   # 发布记录
│   ├── hot_topics.json    # 热点选题
│   └── cookies.json       # 登录 cookies
└── scripts/
    ├── xhs_client.py     # Python 客户端
    ├── xhs_mcp.py       # MCP 直接调用
    ├── xhs_login_sop.py  # 登录 SOP
    └── publish_smart.py   # 智能发布脚本
```

---

## Resources

- [README.md](README.md) — Full Chinese documentation
- [STRATEGY.md](STRATEGY.md) — Content strategy and comment interaction rules
- [BEST_PRACTICE.md](BEST_PRACTICE.md) — Publishing best practices
- [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) — Upstream MCP server
