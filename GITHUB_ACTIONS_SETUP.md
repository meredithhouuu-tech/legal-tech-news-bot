# GitHub Actions 配置指南

## 步骤 1: 创建 GitHub 仓库

1. 在 GitHub 上创建一个新仓库（例如：`legal-tech-news-bot`）
2. 将代码推送到仓库：

```bash
cd "/Users/housiyi/Desktop/【工作】幂律智能/CLAUDE CODE/legaltech_newsletter_bot"

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Legal Tech News Bot"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/legal-tech-news-bot.git

# 推送到 GitHub
git push -u origin main
```

## 步骤 2: 配置 GitHub Secrets

在 GitHub 仓库中设置环境变量（不要直接写在代码里！）：

1. 打开你的 GitHub 仓库
2. 点击 **Settings**（设置）
3. 点击左侧 **Secrets and variables** > **Actions**
4. 点击 **New repository secret** 添加以下密钥：

### 必需的 Secrets

| Secret 名称 | 值 | 说明 |
|------------|-----|------|
| `NEWS_API_KEY` | `8627e9db59894c8f99c76dd4d2adcbdd` | NewsAPI 密钥 |
| `FEISHU_WEBHOOK_URL` | `https://open.feishu.cn/open-apis/bot/v2/hook/d4ebae86-11f6-4a01-9b49-8fd7ebbdb8d1` | 飞书 Webhook 地址 |

### 可选的 Secrets

| Secret 名称 | 值 | 说明 |
|------------|-----|------|
| `CLAUDE_API_KEY` | 你的 Claude API 密钥 | 如果不配置，会使用免费翻译 |
| `SEARCH_KEYWORDS` | `legal tech OR legaltech OR legal AI OR 法律科技 OR 法律AI` | 英文搜索关键词 |
| `SEARCH_KEYWORDS_CN` | `法律科技 OR 法律AI OR 法务AI OR 智能法务` | 中文搜索关键词 |

## 步骤 3: 启用 GitHub Actions

1. 在 GitHub 仓库中，点击 **Actions** 标签
2. 如果提示启用 Actions，点击 **I understand my workflows, go ahead and enable them**
3. 在左侧选择 **Legal Tech News Bot** 工作流
4. 点击 **Run workflow** 可以手动测试

## 步骤 4: 验证运行

### 查看运行日志
1. 点击 **Actions** 标签
2. 点击最近的运行记录
3. 展开 **运行新闻 Bot** 步骤查看详细日志

### 下载日志文件
每次运行后，可以在页面底部下载日志文件（保存7天）

## 定时说明

- **运行时间**：每天 UTC 04:00（北京时间 12:00）
- **手动触发**：在 Actions 页面点击 **Run workflow**
- **时区说明**：GitHub Actions 使用 UTC 时间，北京时间 = UTC + 8小时

## 常见问题

### Q: 如何修改运行时间？
A: 编辑 `.github/workflows/daily-news.yml` 文件中的 `cron` 字段：
```yaml
schedule:
  - cron: '0 4 * * *'  # 每天 UTC 04:00
```

Cron 格式：`分 时 日 月 周`
- `0 4 * * *` = 每天 04:00
- `0 */6 * * *` = 每6小时一次
- `0 8 * * 1-5` = 周一到周五每天 08:00

### Q: 如何调试？
A: 有两种方式：
1. **查看 Actions 日志**：在 GitHub Actions 页面查看详细输出
2. **手动触发**：点击 **Run workflow** 立即运行一次

### Q: 为什么没有推送？
A: 检查以下项：
1. Secrets 是否配置正确
2. 飞书 Webhook 是否有效
3. Actions 运行日志是否有错误

### Q: 免费额度有限制吗？
A: GitHub Actions 公开仓库完全免费，私有仓库每月有 2000 分钟免费额度（通常足够）
