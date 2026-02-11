# 📚 Xiaohongshu MCP 策略文档

## 概述

集成 `title-cover-generator` 实现自动封面生成。

## 组件

### 1. 标题封面生成器
- **仓库**: https://github.com/tclawde/title-cover-generator
- **功能**: 自动生成便签风格标题封面
- **特点**: 大字体、精确换行、9:16 比例

### 2. 智能发布脚本
- **文件**: `publish_smart_v2.py`
- **功能**: 集成封面生成 + 小红书发布

## 集成方式

```python
import sys
sys.path.insert(0, "/Users/apple/.openclaw/workspace/title-cover-generator")
from generate import create_title_cover

# 生成封面
create_title_cover("你的标题", output_path="/tmp/cover.jpg")
```

## 封面特点

| 特性 | 说明 |
|------|------|
| 比例 | 9:16 (900x1600) |
| 背景 | 浅黄色便签纸 |
| 字体 | STHeiti Medium 90px |
| 颜色 | 黑字 + 红色强调 |
| 换行 | 精确测量，无溢出 |

## 发布流程

```bash
cd /Users/apple/.openclaw/skills/xiaohongshu-mcp
python3 publish_smart_v2.py
```

## 依赖

- `Pillow>=9.0.0`
- macOS (系统字体)

## 维护

- 封面生成器独立更新
- 发布脚本引用最新版本

*最后更新: 2026-02-11*
