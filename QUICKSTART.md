# 🚀 快速开始指南

5分钟快速启动法律科技新闻Bot！

## ⚡ 快速三步走

### 第1步：安装依赖（1分钟）

```bash
pip install -r requirements.txt
```

### 第2步：配置API（3分钟）

1. 复制配置文件：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填写三个必需的API密钥：
   ```env
   NEWS_API_KEY=你的密钥
   CLAUDE_API_KEY=你的密钥
   FEISHU_WEBHOOK_URL=你的Webhook地址
   
   # 保持默认设置
   RUN_MODE=test  # 测试模式
   ```

3. 获取API密钥：
   - NewsAPI：https://newsapi.org/register（免费）
   - Claude：https://console.anthropic.com/（付费，按量计费）
   - 飞书：在飞书群中添加自定义机器人

### 第3步：测试运行（1分钟）

```bash
python legal_tech_news_bot.py
```

看到飞书群收到消息 = ✅ 配置成功！

## 🎉 测试成功后

修改 `.env` 文件：
```env
RUN_MODE=production  # 改为生产模式
```

重新运行，Bot将在每天中午12点自动推送新闻！

## 💡 小贴士

- 首次使用建议先用 `RUN_MODE=test` 测试
- 程序会自动监控API使用次数，接近限制时会警告
- AI服务失败时会自动使用备用方案，保证服务可用
- 查看完整文档：`README.md`

## ❓ 遇到问题？

1. 运行测试脚本诊断：
   ```bash
   python test_config.py
   ```

2. 查看日志文件：
   ```bash
   cat news_bot.log
   ```

3. 查看 `README.md` 中的常见问题部分

---

**预计成本**：使用Claude Haiku模型，每月约 $0.03-0.15（每天运行1次）
