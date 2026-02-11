# 🏆 小红书运营最佳实践 v1.0

> **最后更新**: 2026-02-11
> **核心原则**: 人设统一、操作规范、信息不丢失

---

## 🎯 账号定位

| 项目 | 内容 |
|------|------|
| **人设** | AI 反对者 / 民科 / 理性思考者 |
| **风格** | 有态度、有争议、不跟风 |
| **原则** | 用数据和常识说话 |

---

## 🚫 发布前自检清单

### 内容检查
- [ ] 有明确的争议点
- [ ] 反直觉观点清晰
- [ ] 无 "AI 生成的 emoji" 序列
- [ ] 无 "你怎么看" 类引导语
- [ ] 无 "赋能"、"迭代" 等黑话
- [ ] 口语化表达，有真实语气

### 封面检查
- [ ] 只显示标题
- [ ] 无底部标签
- [ ] 字体大小合适
- [ ] 换行不超边界

### 流程检查
- [ ] 使用 `publish_*.py` 脚本发布
- [ ] 记录到 `data/post_history.json`
- [ ] 封面已保存到 `/Users/apple/.openclaw/workspace/`

---

## 📋 标准发布流程

### 方式 1：争议性内容模板

```bash
cd /Users/apple/.openclaw/skills/xiaohongshu-mcp

# 编辑发布脚本
vim publish_controversy.py

# 运行发布
python3 publish_controversy.py
```

### 方式 2：curl 直接发布

```bash
# 封面路径
COVER="/Users/apple/.openclaw/workspace/cover.jpg"

# 发布
curl -s -X POST http://localhost:18060/api/v1/publish \
  -H "Content-Type: application/json" \
  -d '{
    "title": "你的标题",
    "content": "你的正文",
    "images": ["'"$COVER"'"]
  }'
```

---

## 📁 核心文件清单

| 文件 | 路径 | 作用 |
|------|------|------|
| **STRATEGY.md** | `/xiaohongshu-mcp/STRATEGY.md` | 运营策略（完整版） |
| **封面生成器** | `/title-cover-generator/` | 自动生成封面 |
| **发布脚本** | `/xiaohongshu-mcp/publish_controversy.py` | 争议内容发布 |
| **历史记录** | `/xiaohongshu-mcp/data/post_history.json` | 发布历史 |

---

## ⚠️ 防止信息丢失

### Git 提交规范

**每次更新后必须执行：**
```bash
cd /Users/apple/.openclaw/skills/xiaohongshu-mcp

# 1. 检查状态
git status

# 2. 添加更改
git add .

# 3. 提交（写清楚内容）
git commit -m "feat: 新增XX内容

- 封面样式调整
- 内容策略更新"

# 4. 推送
git push origin main
```

### 关键命令速查

```bash
# 检查 MCP 状态
curl -s http://localhost:18060/api/v1/login/status

# 查看最近日志
tail -10 /Users/apple/.openclaw/skills/xiaohongshu-mcp/mcp.log

# 查看 Git 提交历史
git log --oneline -10
```

---

## 🎨 封面生成器使用

### 独立使用

```bash
cd /Users/apple/.openclaw/workspace/title-cover-generator

# 生成封面
python3 generate.py "你的标题"

# 输出位置
/tmp/title_cover.jpg
```

### 集成使用

```python
import sys
sys.path.insert(0, "/Users/apple/.openclaw/workspace/title-cover-generator")
from generate import create_title_cover

# 生成封面
create_title_cover("标题", output_path="/Users/apple/.openclaw/workspace/cover.jpg")
```

### 封面规范

| 项目 | 要求 |
|------|------|
| 比例 | 9:16 (900x1600) |
| 背景 | 浅黄色便签纸 |
| 字体 | STHeiti Medium 90px |
| 颜色 | 黑字 |
| 装饰 | 左边红线 |
| **禁止** | 底部标签 |

---

## 📊 发布记录模板

每次发布后，添加到 `data/post_history.json`：

```json
{
  "date": "2026-02-11",
  "time": "18:09",
  "type": "controversy",
  "title": "AI 培训课？就是焦虑税",
  "controversy_point": "3999 课程是割韭菜",
  "response": {
    "likes": 0,
    "comments": 0,
    "shares": 0,
    "sentiment": "待观察"
  },
  "notes": "结合热点话题"
}
```

---

## 🔧 常见问题处理

### Q: MCP API 返回空响应
A: MCP 仍在处理，等待 20-60 秒后重试

### Q: 封面超出边界
A: 字体改为 75px，或减少标题字数

### Q: 发布太频繁被限制
A: 间隔至少 5 分钟

### Q: Git 提交丢失
A: 确保每次改动后立即 `git add && commit && push`

---

## 📦 GitHub 仓库

| 项目 | 地址 |
|------|------|
| 小红书 MCP | https://github.com/tclawde/xiaohongshu-mcp-skill |
| 封面生成器 | https://github.com/tclawde/title-cover-generator |

---

## ✅ 每日操作清单

```
□ 7:00   搜索热点 (python3 scripts/xhs_client.py search "AI")
□ 8:00   创作内容
□ 9:00   发布并记录
□ 13:00  追踪热点
□ 14:00  创作内容
□ 15:00  发布并记录
□ 19:00  追踪热点
□ 20:00  创作内容
□ 21:00  发布并记录
□ 22:00  Git 提交并推送
```

---

**遵循此文档，确保每次操作规范、信息不丢失。**

---

## ⏰ 定时任务配置

已配置以下 cron 任务（Asia/Shanghai 时区）：

| 时间 | 任务 | 说明 |
|------|------|------|
| 7:00 | xhs-hot-morning | 搜索最新 AI 热点 |
| 8:00 | xhs-content-morning | 创作原理篇内容 |
| 9:00 | xhs-publish-morning | 发布并记录 |
| 13:00 | xhs-hot-noon | 追踪午间热点 |
| 14:00 | xhs-content-noon | 创作数据篇内容 |
| 15:00 | xhs-publish-noon | 发布并记录 |
| 19:00 | xhs-hot-evening | 追踪晚间热点 |
| 20:00 | xhs-content-evening | 创作热点篇内容 |
| 21:00 | xhs-publish-evening | 发布并记录 |
| 22:00 | xhs-git-push | Git 提交并推送 |

### 查看定时任务

```bash
openclaw cron list
```

### 手动运行任务

```bash
openclaw cron run <job-id>
```
