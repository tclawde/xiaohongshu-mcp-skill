# 📋 每日发布清单

## ⏰ 每日任务

| 时间 | 维度 | 要求 |
|------|------|------|
| 9:00 | 数据篇 | AI + 行业数据 |
| 15:00 | 事件篇 | AI + 社会热点 |
| 21:00 | 观点篇 | AI + 独特视角 |
| 22:00 | 总结 | Git 提交+复盘 |

## ⚠️ 重要提醒

### 不要暴露意图
- ❌ 标签写"民科"
- ❌ 刻意制造争议
- ❌ 暴露账号身份

### 正确方式
- ✅ 标签自然（职场、就业、焦虑）
- ✅ AI + 社会话题结合
- ✅ 内容有厚度（数据/事件/共鸣）
- ✅ 观点自然（不是刻意杠）

## 话题范围

### AI + 社会话题 ✅
- AI 时代的就业焦虑
- AI 对职场的影响
- AI 与生活压力
- AI 与年轻人选择

### 不要 ❌
- 只谈科技原理
- 完全脱离 AI
- 刻意制造争议

## 发布前检查

- [ ] 标签没有暴露身份
- [ ] 话题是 AI + 社会结合
- [ ] 内容有厚度（数据/事件/共鸣）
- [ ] 观点自然不是刻意
- [ ] 像普通人有感而发

## 内容厚度

### 要有 ✅
- 近期热点新闻
- 具体案例
- 真实数据
- 普遍共鸣

### 不要只 ❌
- 输出观点
- 刻意制造争议
- 暴露身份

## 快速开始

```bash
cd /Users/apple/.openclaw/skills/xiaohongshu-mcp

# 数据篇
vim publish_data.py
python3 publish_data.py

# 事件篇
vim publish_event.py
python3 publish_event.py

# 观点篇
vim publish_opinion.py
python3 publish_opinion.py

# 总结
git add .
git commit -m "$(date +%Y-%m-%d) 发布 3 篇 AI+社会话题"
git push origin main
```
