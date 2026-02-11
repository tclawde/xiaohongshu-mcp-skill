# 📋 每日发布清单

## ⏰ 每日任务（3 篇不同维度）

### 9:00 - 数据篇
- [ ] 主题：行业亏损/财报数据
- [ ] 要求：具体数字 + 来源出处
- [ ] 示例：AI 四巨头一年亏掉 1000 亿

### 15:00 - 事件篇  
- [ ] 主题：裁员/政策/新闻事件
- [ ] 要求：最新事件 + 媒体出处
- [ ] 示例：AI 越火，这群人越惨（Salesforce 裁员）

### 21:00 - 观点篇
- [ ] 主题：争议分析/深度思考
- [ ] 要求：有数据/事件支撑的观点
- [ ] 示例：为什么 Prompt 没效果

### 22:00 - 总结
- [ ] Git 提交今日内容
- [ ] 记录到 post_history.json
- [ ] 复盘今日数据

---

## 🚀 快速开始

```bash
cd /Users/apple/.openclaw/skills/xiaohongshu-mcp

# 1. 数据篇
vim publish_data.py  # 编辑内容
python3 publish_data.py  # 发布

# 2. 事件篇
vim publish_event.py
python3 publish_event.py

# 3. 观点篇
vim publish_opinion.py
python3 publish_opinion.py

# 4. 总结
git add .
git commit -m "docs: $(date +%Y-%m-%d) 发布 3 篇内容"
git push origin main
```

---

## 📁 发布脚本模板

### publish_data.py（数据篇）
```python
title = "AI 四巨头一年亏掉 1000 亿"
content = """一组数据：

OpenAI 2024 年预计亏损 50 亿美元（来源：The Information）
...

#AI行业 #亏损 #财报"""
```

### publish_event.py（事件篇）
```python
title = "AI 越火，这群人越惨"
content = """一组数据：

Salesforce 裁员 8000 人，同时招 AI（来源：Bloomberg）
...

#AI #裁员 #职场"""
```

### publish_opinion.py（观点篇）
```python
title = "为什么 Prompt 没效果？"
content = """很多人问我...

#AI #Prompt #技巧"""
```

---

## ✅ 发布前检查

```
□ 有具体数据（数字、百分比、金额）
□ 有来源出处（财报、新闻、报告）
□ 标题有吸引力（数字+痛点）
□ 封面无标签
□ 无 AI 特征
```

---

## 📊 数据来源

| 类型 | 来源 | 示例 |
|------|------|------|
| 财报数据 | The Information, 36Kr | 营收、亏损 |
| 新闻事件 | Bloomberg, 路透社 | 裁员、融资 |
| 行业报告 | Gartner, IDC | 趋势、预测 |
| 投诉案例 | 黑猫投诉 | 维权、退款 |

---

## ⏰ 定时任务状态

| 时间 | 任务 | 脚本 |
|------|------|------|
| 7:00 | 热点追踪 | xhs_hot_tracker.py |
| 8:00 | 内容创作 | publish_*.py |
| 9:00 | 发布 | curl 发布命令 |
| 13:00 | 热点追踪 | xhs_hot_tracker.py |
| 14:00 | 内容创作 | publish_*.py |
| 15:00 | 发布 | curl 发布命令 |
| 19:00 | 热点追踪 | xhs_hot_tracker.py |
| 20:00 | 内容创作 | publish_*.py |
| 21:00 | 发布 | curl 发布命令 |
| 22:00 | 总结 | Git 提交 |

---

**每天 3 篇，22:00 总结！**
