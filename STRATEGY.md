# 📚 Xiaohongshu MCP 运营策略

## 核心理念

**简洁至上** - 只展示标题，不加额外标签

## 封面策略

| 项目 | 要求 |
|------|------|
| **内容** | 只显示标题 |
| **风格** | 浅黄色便签纸 + 左边红线 |
| **字体** | STHeiti Medium 90px |
| **颜色** | 黑字，无其他装饰 |
| **比例** | 9:16 (900x1600) |
| **换行** | 精确测量，不超边界 |

## 发布策略

### 内容规范
- 标题要有冲击力/好奇心
- 正文要有实用价值/个人观点
- 标签只加在正文中（#AI工具 #效率提升 等）
- 封面**不加任何标签**

### 发布节奏
- 间隔至少 5 分钟
- 避免短时间内发布多篇

## 技术集成

### 封面生成
```python
from generate import create_title_cover

# 只传标题，不传副标题
create_title_cover("你的标题")
```

### 发布脚本
```bash
cd /Users/apple/.openclaw/skills/xiaohongshu-mcp
python3 publish_real.py
```

## GitHub 仓库

- **封面生成器**: https://github.com/tclawde/title-cover-generator
- **小红书 MCP**: https://github.com/tclawde/xiaohongshu-mcp-skill

## 维护记录

| 日期 | 更新 |
|------|------|
| 2026-02-11 | 移除封面标签，简洁策略 |
