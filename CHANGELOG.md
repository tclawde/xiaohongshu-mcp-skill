# 更新日志

## v1.4.0 (2026-02-11)

### 新增
- ✅ 登录流程修复（小rednote 登录页面变更）
  - 新增 `xhs_login_sop.py` Playwright 自动化脚本
  - 修复从探索页面点击登录按钮触发二维码
- ✅ MCP 二进制预集成（install.sh 自动下载）

### 改进
- 📝 更新文档，添加 MCP 来源引用
- 🔗 添加 MCP 服务器来源说明（xpzouying/xiaohongshu-mcp）

### 修复
- 🔐 登录二维码获取问题（小rednote 更新登录页面）

## v1.3.0 (2026-02-11)

### 新增
- ✅ Skill 完全自包含重构
  - 所有文件移到 `skills/xiaohongshu-mcp/` 目录
  - 预置 MCP 二进制文件
  - 脚本和配置在一起，方便打包和维护

### 改进
- 📝 更新 SKILL.md 文档

## v1.2.0 (2026-02-11)

### 新增
- ✅ 飞书通知集成
  - 登录二维码自动发送到飞书
  - 新增 `--notify` 参数支持

### 改进
- 🔗 优化 cookies 保存机制（同时保存到多个位置）

## v1.1.0 (2026-02-11)

### 新增
- ✅ 一键登录脚本 `xhs_login.sh`
- ✅ Python 客户端 `xhs_client.py`

### 改进
- 📖 详细使用文档 SOP.md

## v1.0.0 (2026-02-09)

### 初始发布

- ✨ 基于 [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) 构建
- ✅ 完整功能：登录、搜索、详情、发布
- ✅ 一键安装脚本
- ✅ 详细使用文档

---

## 变更格式

### 类型
- `✨` 新增功能
- `✅` 功能改进
- `🐛` Bug 修复
- `📝` 文档更新
- `🔗` 依赖/引用更新
- `⚠️` 重要说明

---

## 相关项目

- **MCP 服务器**: [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) (8.4k+ stars)
- **AI Agent 框架**: [OpenClaw](https://github.com/openclaw/openclaw)
