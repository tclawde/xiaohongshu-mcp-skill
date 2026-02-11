# 🦀 Xiaohongshu MCP 使用指南

## 📋 目录

1. [快速开始](#快速开始)
2. [登录流程（详细）](#登录流程详细)
3. [常用命令](#常用命令)
4. [高级用法](#高级用法)
5. [故障排查](#故障排查)
6. [最佳实践总结](#最佳实践总结-v24-新增)

---

## 🚀 快速开始

### 前提条件

确保以下条件满足：
- [x] MCP 服务器运行中 (`./xiaohongshu-mcp-darwin-arm64`)
- [x] 登录工具已下载 (`xiaohongshu-login-darwin-arm64`)
- [x] Python 3.8+
- [x] requests 库 (`pip install requests`)

### 启动 MCP 服务器

```bash
# 在 skill 目录启动
cd /Users/apple/.openclaw/skills/xiaohongshu-mcp
./xiaohongshu-mcp-darwin-arm64

# 服务器默认监听端口 18060
# API 地址: http://localhost:18060
```

### 一次性设置

```bash
# 创建 cookies 符号链接（只需执行一次）
ln -sf ~/.openclaw/workspace/cookies.json /tmp/cookies.json

# 验证
ls -la /tmp/cookies.json
# 预期: /tmp/cookies.json -> /Users/apple/.openclaw/workspace/cookies.json
```

---

## 🔐 登录流程（详细）

### 场景1：首次登录或 Cookie 过期

当检测到未登录状态时，系统会自动启动登录流程。

#### 步骤1：启动登录工具

```bash
# 方式1：一键登录（推荐）
cd /Users/apple/.openclaw/skills/xiaohongshu-mcp
bash xhs_login.sh

# 方式2：一键登录并发送二维码到飞书
bash xhs_login.sh --notify

# 方式3：手动启动登录工具
python3 scripts/xhs_login_sop.py
```

#### 步骤2：获取二维码

登录工具会打开浏览器窗口显示二维码。

**用小红书 App 扫码登录**

#### 步骤3：等待登录成功

登录脚本会自动轮询检测登录状态（最多 60 秒）。

### 场景2：已登录状态

直接执行命令，无需登录：

```bash
python3 xhs_client.py status
# 输出: ✅ Logged in as: xiaohongshu-mcp
```

---

## 💻 常用命令

### 检查与管理

```bash
# 检查登录状态（自动刷新）
curl -s http://localhost:18060/api/v1/login/status

# 手动触发登录
python3 scripts/xhs_client.py login
```

### 搜索与浏览

```bash
# 搜索笔记
python3 scripts/xhs_client.py search "AI" --sort "最新" --type "图文"

# 获取笔记详情
python3 scripts/xhs_client.py detail "feed_id" "xsec_token"

# 获取推荐内容
python3 scripts/xhs_client.py feeds
```

### 发布内容

```bash
# 发布图文笔记
python3 scripts/xhs_client.py publish "标题" "内容" "https://example.com/image.jpg"

# 发布带标签的笔记
python3 scripts/xhs_client.py publish "标题" "内容" "https://image.jpg" --tags "AI,测评"
```

---

## 🎯 最佳实践总结（v2.4 新增）

**核心原则**：MCP 服务器默认启动，无需重启，只需刷新 cookies。

### 一次性设置（推荐）

```bash
# 创建 cookies 符号链接（只需执行一次）
ln -sf ~/.openclaw/workspace/cookies.json /tmp/cookies.json

# 验证
ls -la /tmp/cookies.json
# 预期: /tmp/cookies.json -> /Users/apple/.openclaw/workspace/cookies.json
```

### 日常发布流程

```bash
# 1. 检查 MCP 是否运行
ps aux | grep xiaohongshu-mcp | grep -v grep
# ✅ 应该看到: ./xiaohongshu-mcp-darwin-arm64

# 2. 登录（如需）
cd /Users/apple/.openclaw/skills/xiaohongshu-mcp
python3 scripts/xhs_login_sop.py

# 3. 登录成功后，刷新符号链接（登录脚本会自动更新 cookies.json）
# 无需重启 MCP！MCP 会自动读取新 cookies

# 4. 验证登录状态
curl -s http://localhost:18060/api/v1/login/status
# 预期: {"success":true,"data":{"is_logged_in":true,...}}

# 5. 发布内容
python3 publish_direct.py
```

### 关键要点

| 步骤 | 要点 | 正确做法 |
|------|------|---------|
| **cookies 刷新** | 登录后 cookies 已更新 | ✅ 符号链接自动生效 |
| **MCP 重启** | 不需要重启 | ✅ 保持 MCP 运行 |
| **验证方式** | 用 `curl` 直接验证 | ✅ 不需要重启 |
| **发布参数** | 必须提供图片 | ✅ 使用测试图或截图 |

### 符号链接原理

```
/tmp/cookies.json → ~/.openclaw/workspace/cookies.json
                    ↑
              登录后自动更新
                    ↓
              MCP 自动读取新 cookies（无需重启）
```

### 故障快速恢复

```bash
# 问题：登录状态不正确
# 检查：
curl -s http://localhost:18060/api/v1/login/status

# 解决：刷新符号链接
ln -sf ~/.openclaw/workspace/cookies.json /tmp/cookies.json

# 重新验证
curl -s http://localhost:18060/api/v1/login/status
```

---

## 📚 相关资源

- **项目地址**: https://github.com/xpzouying/xiaohongshu-mcp
- **OpenClaw Skill**: ~/clawd/skills/xiaohongshu-mcp/
- **SOP 文档**: ~/clawd/skills/xiaohongshu-mcp/SOP.md
- **策略文档**: ~/clawd/skills/xiaohongshu-mcp/STRATEGY.md
- **一键登录脚本**: ~/clawd/skills/xiaohongshu-mcp/xhs_login.sh

---

## 🔄 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v2.4 | 2026-02-11 | **优化最佳实践**：MCP 无需重启，使用符号链接刷新 cookies |
| v2.3 | 2026-02-11 | 添加最佳实践总结，修复登录脚本自动轮询，添加发布脚本 |
| v2.2 | 2026-02-09 | 添加一键登录脚本、优化登录流程文档 |
| v2.1 | 2026-02-09 | 添加登录流程详细说明、截图发送到飞书 SOP |
| v2.0 | 2026-02-09 | 添加自动登录检测功能 |
| v1.0 | 2026-02-04 | 初始版本，基本功能 |

---

*最后更新: 2026-02-11*
*维护者: TClawE 🦀*
