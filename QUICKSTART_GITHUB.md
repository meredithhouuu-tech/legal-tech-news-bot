# 🚀 GitHub Actions 快速部署指南

> 在 5 分钟内将 Bot 部署到 GitHub Actions，实现完全免费的 24/7 自动推送！

## 前置条件

✅ 已有 GitHub 账号
✅ 已获取飞书 Webhook URL
✅ 已获取 NewsAPI 密钥

---

## 第一步：推送到 GitHub

### 1.1 创建 GitHub 仓库

1. 访问 [GitHub](https://github.com/new) 创建新仓库
2. 仓库名称：`legal-tech-news-bot`（或其他名称）
3. 设置为 **Public**（公开仓库，Actions 免费额度更多）
4. 不要勾选 "Add a README file"
5. 点击 **Create repository**

### 1.2 推送代码

在终端中运行以下命令（替换 `你的用户名`）：

```bash
cd "/Users/housiyi/Desktop/【工作】幂律智能/CLAUDE CODE/legaltech_newsletter_bot"

# 初始化 Git
git init
git add .
git commit -m "Initial commit: Legal Tech News Bot with GitHub Actions"

# 添加远程仓库
git remote add origin https://github.com/你的用户名/legal-tech-news-bot.git
git branch -M main

# 推送到 GitHub
git push -u origin main
```

---

## 第二步：配置 GitHub Secrets

### 2.1 打开仓库设置

1. 在 GitHub 仓库页面，点击 **Settings**（设置）
2. 左侧菜单点击 **Secrets and variables** → **Actions**
3. 点击 **New repository secret** 按钮

### 2.2 添加必需的 Secrets

依次添加以下密钥（点击 **New repository secret** → 输入 Name 和 Value → **Add secret**）：

#### Secret 1: NEWS_API_KEY
- **Name**: `NEWS_API_KEY`
- **Value**: `8627e9db59894c8f99c76dd4d2adcbdd`

#### Secret 2: FEISHU_WEBHOOK_URL
- **Name**: `FEISHU_WEBHOOK_URL`
- **Value**: `https://open.feishu.cn/open-apis/bot/v2/hook/d4ebae86-11f6-4a01-9b49-8fd7ebbdb8d1`

#### Secret 3: SEARCH_KEYWORDS (可选)
- **Name**: `SEARCH_KEYWORDS`
- **Value**:
  ```
  legal tech OR legaltech OR legal AI OR law technology OR 法律科技 OR 法律AI
  ```

#### Secret 4: SEARCH_KEYWORDS_CN (可选)
- **Name**: `SEARCH_KEYWORDS_CN`
- **Value**:
  ```
  法律科技 OR 法律AI OR 法务AI OR 智能法务 OR 法律大模型 OR 法律人工智能
  ```

> 💡 **提示**：如果你有 Claude API Key，也可以添加 `CLAUDE_API_KEY`

---

## 第三步：运行测试

### 3.1 启用 GitHub Actions

1. 在仓库页面点击 **Actions** 标签
2. 如果提示启用 Actions，点击 **I understand my workflows, go ahead and enable them**

### 3.2 手动触发测试

1. 在左侧选择 **Legal Tech News Bot** 工作流
2. 点击右侧 **Run workflow** 按钮
3. 点击绿色的 **Run workflow** 按钮

### 3.3 查看运行日志

1. 等待几秒后，会看到新的运行记录
2. 点击运行记录查看详情
3. 展开 **运行新闻 Bot** 步骤查看日志

### 3.4 验证结果

- ✅ 如果看到 "✅ 飞书通知发送成功"，说明配置正确！
- ✅ 检查飞书群是否收到测试推送
- ❌ 如果失败，查看日志中的错误信息

---

## 第四步：完成！

🎉 恭喜！你的 Bot 已经成功部署到 GitHub Actions。

### 自动运行说明

- **运行时间**：每天 UTC 04:00（北京时间 12:00）
- **自动执行**：无需任何操作，GitHub 会自动运行
- **本机关闭**：即使你的电脑关机，Bot 仍会正常运行

### 后续操作

**查看历史运行记录**：
- 点击仓库的 **Actions** 标签
- 查看所有历史运行记录和日志

**下载日志文件**：
- 在运行记录页面底部，可以下载 `bot-logs`（保存7天）

**修改运行时间**：
- 编辑 `.github/workflows/daily-news.yml` 文件
- 修改 `cron: '0 4 * * *'` 字段
- 提交修改后自动生效

**手动触发**：
- 点击 **Run workflow** 可以立即运行一次

---

## 常见问题

### Q: 为什么 Actions 显示失败？

**A**: 检查以下项：
1. Secrets 是否配置正确（名称和值都要完全匹配）
2. 飞书 Webhook URL 是否有效
3. NewsAPI 密钥是否正确

### Q: 如何修改推送时间？

**A**: 编辑 `.github/workflows/daily-news.yml`，修改 cron 表达式：
```yaml
schedule:
  - cron: '0 4 * * *'  # UTC 时间，北京时间 = UTC + 8
```

示例：
- `0 4 * * *` = 北京时间 12:00
- `0 8 * * *` = 北京时间 16:00
- `0 0 * * *` = 北京时间 08:00
- `0 */6 * * *` = 每6小时一次

### Q: 会产生费用吗？

**A**:
- GitHub Actions: 公开仓库**完全免费**
- NewsAPI: 免费版每天100次请求（每天用1次，足够）
- Claude API: 可选，不用 Claude 就用免费翻译
- **总成本：$0**

### Q: 如何停止自动运行？

**A**:
1. 删除 `.github/workflows/daily-news.yml` 文件
2. 或者在仓库 Settings → Actions → General → Disable actions

---

## 下一步

✅ 一切就绪！你的 Bot 现在会每天自动推送法律科技新闻到飞书。

**需要帮助？**
- 查看详细配置：[GitHub Actions 配置指南](./GITHUB_ACTIONS_SETUP.md)
- 查看本地运行：[README.md](./README.md)
- 提交 Issue：在 GitHub 仓库提交问题

---

**祝你使用愉快！** 🎉
