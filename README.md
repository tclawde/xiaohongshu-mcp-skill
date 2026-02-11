# 🦀 Xiaohongshu MCP Skill

> 小红书 MCP 完整使用方案 - 基于 [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)

[![GitHub](https://img.shields.io/badge/xpzouying-xiaohongshu--mcp-8.4k-blue)](https://github.com/xpzouying/xiaohongshu-mcp)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Ready-green)](https://github.com/openclaw/openclaw)

## 📋 目录

- [概述](#概述)
- [特性](#特性)
- [安装](#安装)
- [快速开始](#快速开始)
- [文件结构](#文件结构)
- [常见问题](#常见问题)
- [致谢](#致谢)

## 📖 概述

本 Skill 基于 [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) (8.4k+ stars) 构建，提供完整的小红书自动化解决方案。

**核心功能：**
- 🔐 登录管理（支持截图发送到飞书）
- 🔍 搜索内容
- 📄 获取笔记详情
- 📤 发布图文/视频
- 👥 互动操作（点赞、评论等）

**引用来源：**
- MCP 服务器: [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)
- 框架: [OpenClaw](https://github.com/openclaw/openclaw)

## ✨ 特性

- ✅ **登录修复** - 从探索页面点击登录按钮（小红书页面变更修复）
- ✅ **飞书集成** - 二维码自动发送到飞书
- ✅ **一键登录** - 自动化登录流程
- ✅ **完整功能** - 搜索、详情、推荐、发布
- ✅ **Agent 友好** - 可被 OpenClaw 调用
- ✅ **跨平台** - macOS、Linux、Windows

## 🚀 安装

### 方式1：一键安装（推荐）

```bash
# 克隆本 Skill
git clone https://github.com/tclawde/xiaohongshu-mcp-skill.git
cd xiaohongshu-mcp-skill

# 运行安装脚本
bash install.sh
```

### 方式2：手动安装

```bash
# 1. 克隆本 Skill
git clone https://github.com/tclawde/xiaohongshu-mcp-skill.git ~/.openclaw/skills/xiaohongshu-mcp

# 2. 安装 MCP 服务器（二进制文件）
cd ~/.openclaw/skills/xiaohongshu-mcp
bash install.sh

# 3. 安装依赖
pip3 install requests playwright
playwright install chromium
```

## 📦 文件结构

```
xiaohongshu-mcp-skill/
├── SKILL.md              # 本文档
├── README.md             # 英文文档
├── SOP.md                # 详细使用指南
├── install.sh            # 安装脚本（下载 MCP 二进制）
├── xhs_login.sh          # 一键登录脚本
└── scripts/
    ├── xhs_client.py     # Python 客户端
    └── xhs_login_sop.py  # 登录 SOP（Playwright 自动化）
```

## 🚀 快速开始

### 1. 安装 MCP 服务器

```bash
cd ~/.openclaw/skills/xiaohongshu-mcp
bash install.sh
```

### 2. 登录

```bash
# 本地登录
bash xhs_login.sh

# 或登录并发送到飞书
bash xhs_login.sh --notify
```

### 3. 启动 MCP 服务器

```bash
cd ~/.openclaw/skills/xiaohongshu-mcp
./xiaohongshu-mcp-darwin-arm64 &
```

### 4. 使用

```bash
# 检查登录状态
python3 scripts/xhs_client.py status

# 搜索笔记
python3 scripts/xhs_client.py search "咖啡"

# 发布笔记
python3 scripts/xhs_client.py publish "标题" "内容" "图片URL"
```

## 📖 详细文档

- [SOP.md](SOP.md) - 完整使用指南和故障排查
- [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) - 官方 API 文档

## ❓ 常见问题

### Q1: MCP 服务器从哪里下载？

```bash
# MCP 服务器由 install.sh 自动下载
# 手动下载：
curl -L -o xiaohongshu-mcp-darwin-arm64 \
  https://github.com/xpzouying/xiaohongshu-mcp/releases/download/v0.0.8/xiaohongshu-mcp-darwin-arm64
```

### Q2: 登录失败？

```bash
# 小红书登录页面可能变更，使用修复版登录：
bash scripts/xhs_login.sh --notify
```

### Q3: 如何重新登录？

```bash
# 1. 清除 cookies
rm ~/.openclaw/workspace/cookies.json

# 2. 重新登录
bash xhs_login.sh --notify
```

## 🙏 致谢

- [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) - MCP 服务器核心实现
- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent 框架

## 📝 更新日志

### v1.4.0 (2026-02-11)
- ✅ 修复登录流程（小rednote 登录页面变更）
- ✅ 新增 Playwright 自动化登录 SOP
- ✅ 二维码自动发送到飞书
- ✅ MCP 二进制预集成

## 📄 许可证

MIT License

## 👨‍💻 作者

**TClawDE** 🦀

- GitHub: [@tclawde](https://github.com/tclawde)

---

*基于 [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) 构建*
