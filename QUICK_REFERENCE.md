# ⚡ 快速参考

## 一键发布

```bash
cd /Users/apple/.openclaw/skills/xiaohongshu-mcp
python3 publish_controversy.py
```

## 发布前检查

- [ ] 有争议点
- [ ] 反直觉
- [ ] 封面无标签
- [ ] 无 AI 特征

## Git 提交

```bash
git add . && git commit -m "feat: 更新内容" && git push
```

## 检查状态

```bash
curl -s http://localhost:18060/api/v1/login/status
tail -5 mcp.log
```

## 封面生成

```bash
cd /Users/apple/.openclaw/workspace/title-cover-generator
python3 generate.py "标题"
```

## 核心文件

- `BEST_PRACTICE.md` - 完整指南
- `STRATEGY.md` - 运营策略
- `publish_controversy.py` - 发布脚本
