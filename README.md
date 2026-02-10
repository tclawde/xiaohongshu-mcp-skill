# 🦀 Xiaohongshu MCP

> 小红书 MCP 完整使用方案 - 从登录到发布的自动化工具集

[![GitHub Gist](https://img.shields.io/badge/Gist-TClawE-blue)](https://gist.github.com/tclawde)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Ready-green)](https://github.com/openclaw/openclaw)

## 📋 目录

- [特性](#特性)
- [安装](#安装)
- [快速开始](#快速开始)
- [使用指南](#使用指南)
- [文件结构](#文件结构)
- [常见问题](#常见问题)
- [相关资源](#相关资源)

## ✨ 特性

- ✅ **自动登录检测** - 无需手动检查登录状态
- ✅ **一键登录** - 支持截图发送到飞书/微信
- ✅ **完整功能** - 搜索、详情、推荐、发布
- ✅ **跨平台** - 支持 macOS、Linux、Windows
- ✅ **Agent 友好** - 可被其他 AI Agent 调用

## 🚀 安装

### 方式1：一键安装（推荐）

```bash
# 克隆或下载本项目
git clone https://github.com/tclawde/xiaohongshu-mcp-guide.git
cd xiaohongshu-mcp-guide

# 运行安装脚本
bash install.sh
```

### 方式2：手动安装

```bash
# 1. 创建目录
mkdir -p ~/.openclaw/workspace/scripts
mkdir -p ~/.openclaw/workspace/skills/xiaohongshu-mcp/scripts

# 2. 复制脚本
cp xhs_client.py ~/.openclaw/workspace/skills/xiaohongshu-mcp/scripts/
cp xhs_login.sh ~/.openclaw/workspace/scripts/
cp install.sh ~/.openclaw/workspace/scripts/

# 3. 设置执行权限
chmod +x ~/.openclaw/workspace/scripts/*.sh
chmod +x ~/.openclaw/workspace/skills/xiaohongshu-mcp/scripts/*.py

# 4. 安装依赖
pip3 install requests
```

## 📖 快速开始

### 1. 启动 MCP 服务器

```bash
cd ~/.openclaw/workspace
./xiaohongshu-mcp-darwin-arm64 &

# 验证服务器运行
curl http://localhost:18060/api/v1/login/status
# 输出: {"success":true,"data":{"is_logged_in":false}}
```

### 2. 登录

```bash
# 方式1：一键登录（推荐）
bash ~/.openclaw/workspace/scripts/xhs_login.sh --notify

# 方式2：手动登录
cd ~/.openclaw/workspace
./xiaohongshu-login-darwin-arm64
# 扫码登录...

# 方式3：使用 Python 客户端
python3 ~/.openclaw/workspace/skills/xiaohongshu-mcp/scripts/xhs_client.py login
```

### 3. 使用

```bash
# 检查状态
python3 ~/.openclaw/workspace/skills/xiaohongshu-mcp/scripts/xhs_client.py status

# 搜索笔记
python3 ~/.openclaw/workspace/skills/xiaohongshu-mcp/scripts/xhs_client.py search "咖啡"

# 获取详情
python3 ~/.openclaw/workspace/skills/xiaohongshu-mcp/scripts/xhs_client.py detail "feed_id" "xsec_token"

# 发布笔记
python3 ~/.openclaw/workspace/skills/xiaohongshu-mcp/scripts/xhs_client.py publish \
  "标题" "内容" "https://example.com/image.jpg"
```

## 📚 使用指南

### 完整登录流程

#### 本地登录（可直接扫码）

```bash
bash ~/.openclaw/workspace/scripts/xhs_login.sh
```

#### 远程登录（截图发送到飞书）

```bash
bash ~/.openclaw/workspace/scripts/xhs_login.sh --notify
```

这个脚本会自动：
1. ✅ 启动登录工具
2. ✅ 截图保存到桌面
3. ✅ 发送到飞书（需要配置）
4. ✅ 等待登录完成
5. ✅ 验证登录状态

### 常用命令速查

| 命令 | 说明 |
|-----|------|
| `xhs status` | 检查登录状态 |
| `xhs login` | 手动登录 |
| `xhs search "关键词"` | 搜索笔记 |
| `xhs detail "id" "token"` | 获取详情 |
| `xhs feeds` | 获取推荐 |
| `xhs publish "标题" "内容" "图片"` | 发布笔记 |

> 💡 使用前需要先添加 alias，参考 [install.sh](install.sh)

### 参数说明

#### 搜索参数

```bash
python3 xhs_client.py search "咖啡" \
  --sort "最新"        # 综合 | 最新 | 最多点赞 | 最多评论 | 最多收藏
  --type "图文"        # 不限 | 视频 | 图文
  --time "一周内"      # 不限 | 一天内 | 一周内 | 半年内
```

#### 发布参数

```bash
python3 xhs_client.py publish "标题" "内容" "图片URL" \
  --tags "咖啡,测评"   # 标签（逗号分隔）
```

## 📁 文件结构

```
xiaohongshu-mcp-guide/
├── install.sh              # 一键安装脚本
├── README.md               # 本文件
├── SOP.md                  # 详细使用指南
├── xhs_client.py          # 增强版 Python 客户端
└── xhs_login.sh           # 一键登录脚本（含截图发送到飞书）
```

### 文件说明

| 文件 | 说明 | 位置 |
|-----|------|------|
| `xhs_client.py` | Python 客户端，支持自动登录 | `~/.clawd/skills/xiaohongshu-mcp/scripts/` |
| `xhs_login.sh` | 一键登录脚本 | `~/.clawd/scripts/` |
| `install.sh` | 安装脚本 | `~/.clawd/scripts/` |
| `SOP.md` | 详细文档 | `~/.clawd/skills/xiaohongshu-mcp/` |

## ❓ 常见问题

### Q1: 找不到 MCP 服务器？

```bash
# 下载 MCP 服务器
cd ~/.clawd/workspace
curl -L -o xiaohongshu-mcp-darwin-arm64 \
  https://github.com/xpzouying/xiaohongshu-mcp/releases/download/v0.0.5/xiaohongshu-mcp-darwin-arm64
chmod +x xiaohongshu-mcp-darwin-arm64
```

### Q2: 截图失败？

```bash
# 错误：could not create image from display
# 原因：桌面未唤醒

# 解决：唤醒桌面
caffeinate -u -t 30

# 或者让用户在本地扫码
bash ~/.clawd/scripts/xhs_login.sh
```

### Q3: 登录超时？

```bash
# 二维码有效期约 5 分钟

# 重新获取二维码
bash ~/.clawd/scripts/xhs_login.sh --notify
```

### Q4: 如何重新登录？

```bash
# 1. 停止服务器
pkill -f xiaohongshu-mcp

# 2. 清除 cookies
rm -rf ~/.xiaohongshu/

# 3. 重启并登录
cd ~/.clawd/workspace
./xiaohongshu-mcp-darwin-arm64 &
bash ~/.clawd/scripts/xhs_login.sh
```

### Q5: Agent 如何调用？

```bash
# 在 OpenClaw 中使用 nodes.run
nodes.run(
  node="Apple的Mac mini",
  command=["python3", "/Users/apple/.clawd/skills/xiaohongshu-mcp/scripts/xhs_client.py", "status"]
)
```

## 📖 详细文档

- [完整使用指南](SOP.md) - 详细的步骤说明和故障排查
- [API 文档](https://github.com/xpzouying/xiaohongshu-mcp) - 官方 API 文档

## 🔗 相关资源

### 原始项目

- [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) - MCP 服务器
- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent 框架

### 相关 Gist

- [完整经验总结](https://gist.github.com/tclawde/7f7487f10bfe6f8ce9cfe6368f2edc4d) - 详细的实践经验

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建分支 (`git checkout -b feature/amazing`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing`)
5. 创建 Pull Request

## 📝 更新日志

### v1.0 (2026-02-09)

- ✨ 初始发布
- ✅ 增强版 Python 客户端（自动登录）
- ✅ 一键登录脚本（截图+发送到飞书）
- ✅ 完整安装脚本
- ✅ 详细使用文档

## 📄 许可证

MIT License

## 👨‍💻 作者

**TClawdE** 🦀

- GitHub: [@tclawde](https://github.com/tclawde)
- Gist: [xiaohongshu-mcp-guide](https://gist.github.com/tclawde)

---

*如果这个项目对你有帮助，欢迎 Star ⭐ 支持！*
