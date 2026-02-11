# ⚡ 快速参考

## 核心要求：数据 + 事件

每个内容必须有：
- ✅ 具体数据（数字、百分比、金额）
- ✅ 数据来源（财报、报告、新闻）
- ✅ 最新事件（1周内）
- ✅ 事件出处（媒体、官方）

## 发布前检查

- [ ] 有数据支撑
- [ ] 有事件佐证
- [ ] 争议点清晰
- [ ] 封面无标签
- [ ] 无 AI 特征

## 一键发布

```bash
cd /Users/apple/.openclaw/skills/xiaohongshu-mcp
python3 publish_controversy.py
```

## Git 提交

```bash
git add . && git commit -m "feat: 更新内容" && git push
```

## 检查状态

```bash
curl -s http://localhost:18060/api/v1/login/status
tail -5 mcp.log
```

## 核心文件

- `BEST_PRACTICE.md` - 完整指南
- `STRATEGY.md` - 运营策略（含数据要求）
- `publish_controversy.py` - 发布脚本
