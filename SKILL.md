---
name: xiaohongshu-mcp
description: >
  Xiaohongshu MCP Skill - Based on xpzouying/xiaohongshu-mcp (8.4k+ stars). Features:
  (1) Login with Feishu notification, (2) Search notes and trends,
  (3) Publish image/text/video content, (4) Interact with posts (likes, comments).
  Built-in login fix for Xiaohongshu page changes.
  Triggers: xiaohongshu, rednote, 小红书 automation.
---

# Xiaohongshu MCP Skill

> 基于 [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) 构建

## 概述

本 Skill 提供小红书完整自动化解决方案，包含登录修复（小红书登录页面变更）、飞书通知集成。

**核心功能：**
- 🔐 登录管理（支持截图发送到飞书）
- 🔍 搜索内容
- 📄 获取笔记详情
- 📤 发布图文/视频
- 👥 互动操作

**来源：**
- MCP 服务器: [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) (8.4k+ stars)

## 安装

### 方式1：一键安装（推荐）

```bash
git clone https://github.com/tclawde/xiaohongshu-mcp-skill.git
cd xiaohongshu-mcp-skill
bash install.sh
```

### 方式2：手动安装

```bash
# 1. 克隆 Skill
git clone https://github.com/tclawde/xiaohongshu-mcp-skill.git ~/.openclaw/skills/xiaohongshu-mcp

# 2. 安装 MCP 服务器
cd ~/.openclaw/skills/xiaohongshu-mcp
bash install.sh

# 3. 安装依赖
pip3 install requests playwright
playwright install chromium
```

## 使用

### 1. 登录

```bash
# 本地登录
bash xhs_login.sh

# 登录并发送到飞书
bash xhs_login.sh --notify
```

> **登录修复**：小红书更新了登录页面，本 Skill 已修复从探索页面点击登录按钮。

### 2. 启动 MCP 服务器

```bash
cd ~/.openclaw/skills/xiaohongshu-mcp
./xiaohongshu-mcp-darwin-arm64 &
```

### 3. 使用功能

```bash
# 检查状态
python3 scripts/xhs_client.py status

# 搜索
python3 scripts/xhs_client.py search "咖啡"

# 发布
python3 scripts/xhs_client.py publish "标题" "内容" "图片URL"
```

## 文件结构

```
xiaohongshu-mcp-skill/
├── SKILL.md              # 本文档
├── README.md             # 中文文档
├── SOP.md                # 详细指南
├── install.sh            # 安装脚本
├── xhs_login.sh         # 一键登录
└── scripts/
    ├── xhs_client.py    # Python 客户端
    └── xhs_login_sop.py # 登录 SOP（修复版）
```

## 常见问题

### MCP 服务器从哪里获取？

```bash
# install.sh 会自动下载
# 或手动下载：
curl -L -o xiaohongshu-mcp-darwin-arm64 \
  https://github.com/xpzouying/xiaohongshu-mcp/releases/download/v0.0.8/xiaohongshu-mcp-darwin-arm64
```

### 登录失败？

小红书可能更新了登录页面，使用本 Skill 的修复版登录：

```bash
bash xhs_login.sh --notify
```

## 致谢

- [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) - MCP 服务器核心
- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent 框架
