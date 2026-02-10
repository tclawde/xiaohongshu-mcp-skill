# 🦀 Xiaohongshu MCP 使用指南

## 📋 目录

1. [快速开始](#快速开始)
2. [登录流程（详细）](#登录流程详细)
3. [常用命令](#常用命令)
4. [高级用法](#高级用法)
5. [故障排查](#故障排查)

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
# 在后台运行 MCP 服务器
cd /Users/apple/.openclaw/workspace
./xiaohongshu-mcp-darwin-arm64

# 或者在前台运行（会占用终端）
./xiaohongshu-mcp-darwin-arm64 -headless=false
```

### 基本使用

```bash
# 检查登录状态（会自动登录）
python3 xhs_client.py status

# 搜索笔记
python3 xhs_client.py search "咖啡"

# 发布笔记
python3 xhs_client.py publish "标题" "内容" "图片URL"
```

---

## 🔐 登录流程（详细）

### 场景1：首次登录或 Cookie 过期

当检测到未登录状态时，系统会自动启动登录流程。

#### 步骤1：启动登录工具

```bash
# 方式1：一键登录（推荐）
bash /Users/apple/.openclaw/workspace/scripts/xhs_login.sh

# 方式2：一键登录并发送二维码到飞书
bash /Users/apple/.openclaw/workspace/scripts/xhs_login.sh --notify

# 方式3：手动启动登录工具
cd /Users/apple/.openclaw/workspace
./xiaohongshu-login-darwin-arm64
```

#### 步骤2：获取二维码

登录工具会打开浏览器窗口显示二维码。有两种方式获取二维码：

**方式A：直接在弹出的浏览器中操作**
1. 登录工具会自动打开默认浏览器
2. 显示二维码页面
3. **用小红书 App 扫码登录**

**方式B：截图发送到其他设备**
如果需要在其他设备上扫码：

```bash
# 1. 启动登录工具（不关闭）
./xiaohongshu-login-darwin-arm64

# 2. 截图并发送到飞书
# 方式1：使用截图脚本（推荐）
bash /Users/apple/.openclaw/skills/screenshot-to-feishu/scripts/screenshot-to-feishu.sh

# 方式2：手动截图
/usr/sbin/screencapture -x ~/Desktop/xhs_qr.png

# 3. 发送截图到飞书
message --file ~/Desktop/xhs_qr.png --target "user:ou_715534dc247ce18213aee31bc8b224cf"
```

#### 步骤3：扫码登录

1. 打开小红书 App
2. 扫描屏幕上的二维码
3. 确认登录

#### 步骤4：验证登录

登录成功后，系统会自动检测并显示：

```bash
🔐 Checking login status...
✅ Already logged in as: xiaohongshu-mcp
```

### 场景2：已登录状态

直接执行命令，无需登录：

```bash
python3 xhs_client.py status
# 输出: ✅ Logged in as: xiaohongshu-mcp

python3 xhs_client.py search "咖啡"
# 直接搜索，无需登录
```

### 场景3：需要重新登录

如果登录失效或需要切换账号：

```bash
# 1. 清除旧 cookies（可选）
rm -rf ~/.xiaohongshu/

# 2. 重新登录
python3 xhs_client.py login

# 或者
bash /Users/apple/.openclaw/workspace/scripts/xhs_login.sh
```

---

## 📱 截图发送到飞书 SOP

当需要在远程设备上扫码时，需要将二维码截图发送到飞书。

### 完整流程

#### 步骤1：启动登录工具（保持运行）

```bash
# 方式1：一键登录并发送二维码到飞书（推荐）
bash /Users/apple/.openclaw/workspace/scripts/xhs_login.sh --notify

# 方式2：手动操作
cd /Users/apple/.openclaw/workspace
./xiaohongshu-login-darwin-arm64
```

**预期输出：**
```
time="2026-02-09T12:02:15+08:00" level=info msg="当前登录状态: false"
time="2026-02-09T12:02:15+08:00" level=info msg="开始登录流程..."
```

#### 步骤2：截图

```bash
# 推荐：使用截图脚本
bash /Users/apple/.openclaw/skills/screenshot-to-feishu/scripts/screenshot-to-feishu.sh

# 或手动截图
/usr/sbin/screencapture -x ~/Desktop/xhs_qr.png
```

#### 步骤3：发送到飞书

使用 message 工具发送：

```bash
# 发送截图给用户
message --action send \
  --channel feishu \
  --target "user:ou_715534dc247ce18213aee31bc8b224cf" \
  --file ~/Desktop/xhs_qr.png \
  --message "🦀 小红书登录二维码！\n\n请用小红书 App 扫码登录。\n\n登录成功后告诉我～"
```

**使用 OpenClaw message 工具（如果可用）：**
```python
# 在 OpenClaw 中
message.send(
  channel="feishu",
  target="user:ou_715534dc247ce18213aee31bc8b224cf",
  filePath="/tmp/xhs_qr.png",
  message="🦀 小红书登录二维码！请扫码登录",
  caption="登录二维码"
)
```

#### 步骤4：等待用户扫码

发送截图后通知用户扫码，用户扫码成功后会收到确认。

#### 步骤5：验证登录状态

```bash
python3 xhs_client.py status
# 输出: ✅ Logged in as: xiaohongshu-mcp
```

### 自动化脚本

推荐使用一键登录脚本（已预装）：

```bash
# 仅登录
bash /Users/apple/.openclaw/workspace/scripts/xhs_login.sh

# 登录并发送二维码到飞书
bash /Users/apple/.openclaw/workspace/scripts/xhs_login.sh --notify
```

一键登录脚本功能：
- ✅ 自动检查依赖
- ✅ 截图并发送到飞书（带 --notify 参数）
- ✅ 等待登录完成
- ✅ 验证登录状态

**脚本位置**: `/Users/apple/.openclaw/workspace/scripts/xhs_login.sh`

---

## 💻 常用命令

### 检查与管理

```bash
# 检查登录状态
python3 xhs_client.py status

# 手动触发登录
python3 xhs_client.py login

# 查看帮助
python3 xhs_client.py --help
```

### 搜索与浏览

```bash
# 搜索笔记
python3 xhs_client.py search "咖啡"
python3 xhs_client.py search "咖啡" --sort "最新" --type "图文" --time "一周内"

# 获取笔记详情
python3 xhs_client.py detail "feed_id" "xsec_token"

# 获取推荐内容
python3 xhs_client.py feeds
```

### 发布内容

```bash
# 发布图文笔记（单图）
python3 xhs_client.py publish "标题" "内容" "https://example.com/image.jpg"

# 发布图文笔记（多图）
python3 xhs_client.py publish "标题" "内容" "https://img1.jpg,https://img2.jpg,https://img3.jpg"

# 发布带标签的笔记
python3 xhs_client.py publish "标题" "内容" "https://image.jpg" --tags "咖啡,测评,好物"
```

---

## 🔧 高级用法

### MCP 服务器管理

```bash
# 检查服务器是否运行
ps aux | grep xiaohongshu-mcp

# 启动服务器
cd /Users/apple/.openclaw/workspace
./xiaohongshu-mcp-darwin-arm64

# 停止服务器
pkill -f xiaohongshu-mcp
```

### Cookie 管理

```bash
# 查看 cookies 文件
ls -la ~/.xiaohongshu/

# 清除 cookies（需要重新登录）
rm -rf ~/.xiaohongshu/

# 备份 cookies（可选）
cp -r ~/.xiaohongshu/ ~/.xiaohongshu.backup/
```

### 在 OpenClaw 中使用

在 OpenClaw 中可以直接调用 MCP 工具：

```bash
# 使用 nodes.run 在 Mac mini 上执行
nodes.run(
  node="Apple的Mac mini",
  command=["python3", "/Users/apple/.openclaw/workspace/skills/xiaohongshu-mcp/scripts/xhs_client.py", "status"]
)
```

---

## ❓ 故障排查

### 问题1：找不到登录工具

```bash
# 错误：login tool not found
# 解决：下载登录工具

# 下载 macOS ARM64 版本
cd /Users/apple/.openclaw/workspace
curl -L -o xiaohongshu-login-darwin-arm64 \
  https://github.com/xpzouying/xiaohongshu-mcp/releases/download/v0.0.5/xiaohongshu-login-darwin-arm64

chmod +x xiaohongshu-login-darwin-arm64
```

### 问题2：MCP 服务器连接失败

```bash
# 错误：Cannot connect to MCP server
# 解决：启动 MCP 服务器

cd /Users/apple/.openclaw/workspace
./xiaohongshu-mcp-darwin-arm64
```

### 问题3：截图失败

```bash
# 错误：could not create image from display
# 原因：桌面未唤醒或无显示会话
# 解决：

# 方案1：唤醒桌面
caffeinate -u -t 30

# 方案2：使用登录工具的截图（如果有）
# 方案3：在本地终端手动截图

# 方案4：让用户在其他设备扫码
# 直接运行登录工具
./xiaohongshu-login-darwin-arm64
```

### 问题4：登录超时

```bash
# 错误：Login timeout (5 minutes)
# 解决：

# 1. 重新运行登录
python3 xhs_client.py login

# 2. 或手动启动登录工具
./xiaohongshu-login-darwin-arm64

# 3. 确保网络连接正常
# 4. 确保小红书账号状态正常
```

### 问题5：扫码后无反应

```bash
# 可能原因：
# 1. 二维码已过期（5分钟）
# 2. 网络连接问题
# 3. 小红书 App 问题

# 解决：
# 1. 重新运行登录
python3 xhs_client.py login

# 2. 检查 MCP 服务器状态
python3 xhs_client.py status

# 3. 清除 cookies 后重试
rm -rf ~/.xiaohongshu/
python3 xhs_client.py login
```

---

## 📚 相关资源

- **项目地址**: https://github.com/xpzouying/xiaohongshu-mcp
- **OpenClaw Skill**: ~/clawd/skills/xiaohongshu-mcp/
- **SOP 文档**: ~/clawd/skills/xiaohongshu-mcp/SOP.md
- **一键登录脚本**: ~/scripts/xhs_login.sh

---

## 🔄 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v2.2 | 2026-02-09 | 添加一键登录脚本、优化登录流程文档 |
| v2.1 | 2026-02-09 | 添加登录流程详细说明、截图发送到飞书 SOP |
| v2.0 | 2026-02-09 | 添加自动登录检测功能 |
| v1.0 | 2026-02-04 | 初始版本，基本功能 |

---

*最后更新: 2026-02-09*
*维护者: TClawE 🦀*
