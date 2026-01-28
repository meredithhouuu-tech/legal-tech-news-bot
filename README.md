# 🤖 法律科技新闻汇总Bot

一个自动化工具，每天抓取全球法律科技（Legal Tech）相关新闻，使用AI整理成中文Newsletter，并通过飞书机器人自动推送。

## ✨ 功能特点

- 🔍 **自动抓取**：每天从NewsAPI获取最新的法律科技新闻
- 🤖 **AI整理**：使用Claude API将英文新闻整理成中文简报
- 📱 **自动推送**：每天中午12点通过飞书机器人推送到指定群聊
- 📝 **日志记录**：详细的运行日志，方便排查问题
- 🛡️ **异常处理**：完善的错误处理，确保程序稳定运行
- 🔄 **智能备用**：AI服务失败时自动切换到备用方案，保证服务可用
- 📊 **API监控**：自动监控API使用配额，接近限制时发出警告
- 🧪 **测试模式**：支持单次测试运行，方便验证配置

## 📋 准备工作

### 1. 获取NewsAPI密钥

1. 访问 [NewsAPI官网](https://newsapi.org/register)
2. 注册账号（免费）
3. 在控制台获取API Key
4. 免费版限制：每天最多100次请求

### 2. 获取Claude API密钥（可选）

> 💡 **提示**：如果不配置 Claude API，程序会使用免费的 Google 翻译，完全免费！

1. 访问 [Anthropic控制台](https://console.anthropic.com/)
2. 注册/登录账号
3. 进入 Account Settings → API Keys
4. 创建新的API Key
5. 记录下API密钥（建议使用Claude 3 Haiku，成本低）

### 3. 创建飞书机器人

1. 打开飞书客户端，进入要接收新闻的群聊
2. 点击群聊右上角 **...** → **群设置** → **群机器人** → **添加机器人**
3. 选择 **自定义机器人**
4. 设置机器人名称（如"法律科技新闻Bot"）
5. 复制Webhook URL（格式：`https://open.feishu.cn/open-apis/bot/v2/hook/xxx`）

## 🚀 部署方式

本项目支持两种部署方式：

### 方式1：GitHub Actions（推荐）⭐

**优势**：
- ✅ 完全免费
- ✅ 不依赖本地电脑（24/7运行）
- ✅ 无需服务器
- ✅ 自动定时执行

**配置步骤**：
1. 将代码推送到 GitHub 仓库
2. 在 GitHub 仓库中配置 Secrets（API密钥）
3. GitHub Actions 会自动每天执行

**详细配置教程**：查看 [GitHub Actions 配置指南](./GITHUB_ACTIONS_SETUP.md)

### 方式2：本地运行

适合测试或需要实时控制的场景。详见下方「本地安装步骤」。

---

## 本地安装步骤

### Windows系统

#### 步骤1：安装Python

1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载并安装Python 3.8或更高版本
3. **重要**：安装时勾选 "Add Python to PATH"
4. 验证安装：打开命令提示符（CMD），输入：
   ```bash
   python --version
   ```
   如果显示版本号，说明安装成功

#### 步骤2：下载项目文件

将以下文件放在同一个文件夹中（例如：`D:\legal-tech-bot`）：
- `legal_tech_news_bot.py`（主程序）
- `requirements.txt`（依赖列表）
- `.env.example`（配置模板）

#### 步骤3：安装依赖包

1. 打开命令提示符（CMD）
2. 进入项目文件夹：
   ```bash
   cd D:\legal-tech-bot
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

#### 步骤4：配置环境变量

1. 在项目文件夹中，复制 `.env.example` 文件
2. 重命名为 `.env`（注意：文件名就是 `.env`，没有其他前缀）
3. 用记事本打开 `.env` 文件
4. 填写你的API密钥：
   ```env
   # 必需配置
   NEWS_API_KEY=你从NewsAPI获取的密钥
   CLAUDE_API_KEY=你从Claude获取的密钥
   FEISHU_WEBHOOK_URL=你从飞书获取的Webhook地址

   # 可选配置（首次使用建议保持默认）
   RUN_MODE=test  # 测试模式，先测试配置是否正确
   ENABLE_FALLBACK=true  # 启用备用方案
   MAX_ARTICLES=10  # 获取10条新闻
   ```
5. 保存文件

#### 步骤5：测试配置

**重要：在正式运行前，先测试配置是否正确！**

1. 确保 `.env` 文件中 `RUN_MODE=test`（已默认设置）
2. 运行Bot：
   ```bash
   python legal_tech_news_bot.py
   ```
3. 观察日志输出：
   - ✅ 如果看到"测试模式：立即执行一次任务"，说明配置正确
   - ✅ 检查飞书群是否收到测试消息
   - ❌ 如果有错误，查看日志中的错误提示

4. 测试成功后，修改为生产模式：
   - 打开 `.env` 文件
   - 将 `RUN_MODE=test` 改为 `RUN_MODE=production`
   - 保存文件

#### 步骤6：正式运行

**方法1：直接运行**
```bash
python legal_tech_news_bot.py
```

**方法2：使用快速启动脚本**
```bash
# Windows
run.bat

# macOS/Linux
./run.sh
```

Bot启动后会显示：
```
🚀 法律科技新闻Bot启动
📅 Bot已启动，将在每天中午12:00推送新闻
💡 提示：按Ctrl+C可以停止Bot
```

### macOS/Linux系统

#### 步骤1：安装Python

```bash
# 检查是否已安装Python
python3 --version

# 如果未安装，使用Homebrew安装
brew install python3
```

#### 步骤2：下载项目文件

```bash
# 创建项目目录
mkdir ~/legal-tech-bot
cd ~/legal-tech-bot

# 将项目文件复制到此目录
```

#### 步骤3：安装依赖包

```bash
pip3 install -r requirements.txt
```

#### 步骤4：配置环境变量

```bash
# 复制配置文件模板
cp .env.example .env

# 编辑配置文件
nano .env
# 或使用VS Code：code .env
```

填写你的API密钥后保存（Ctrl+O保存，Ctrl+X退出）：

```env
# 必需配置
NEWS_API_KEY=你从NewsAPI获取的密钥
CLAUDE_API_KEY=你从Claude获取的密钥
FEISHU_WEBHOOK_URL=你从飞书获取的Webhook地址

# 可选配置
RUN_MODE=test  # 先测试，确认无误后改为production
ENABLE_FALLBACK=true
MAX_ARTICLES=10
```

#### 步骤5：测试配置

```bash
# 运行测试
python3 legal_tech_news_bot.py
```

检查飞书群是否收到测试消息，确认配置正确。

#### 步骤6：正式运行

**前台运行**：
```bash
python3 legal_tech_news_bot.py
```

**后台运行（推荐）**：
```bash
# 使用nohup在后台运行
nohup python3 legal_tech_news_bot.py > bot.log 2>&1 &

# 查看运行日志
tail -f news_bot.log

# 停止Bot
ps aux | grep legal_tech_news_bot.py
kill <进程ID>
```

## 📊 文件结构

```
legal-tech-bot/
├── legal_tech_news_bot.py   # 主程序
├── requirements.txt          # Python依赖包
├── .env.example             # 配置文件模板
├── .env                     # 你的配置（需自己创建）
├── run.bat                  # Windows快速启动脚本
├── run.sh                   # macOS/Linux快速启动脚本
├── test_config.py           # 配置测试脚本
├── news_bot.log             # 运行日志（自动生成）
└── README.md                # 使用说明
```

## 🔧 配置说明

### 运行模式配置

在 `.env` 文件中配置 `RUN_MODE` 参数：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `test` | 立即执行一次任务 | 首次配置、测试API密钥、验证功能 |
| `production` | 定时运行，每天12点执行 | 正式使用、日常运行 |

**切换方法**：
```bash
# 测试模式（默认）
RUN_MODE=test

# 生产模式
RUN_MODE=production
```

### 其他可选配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `ENABLE_FALLBACK` | 是否启用备用方案（AI失败时） | `true` |
| `MAX_ARTICLES` | 每次获取的新闻数量 | `10` |
| `SEARCH_KEYWORDS` | 新闻搜索关键词 | `legal tech OR ...` |

### 修改推送时间

默认是每天中午12:00推送，如需修改，编辑 `legal_tech_news_bot.py` 文件：

```python
# 修改为你想要的时间，24小时制
schedule.every().day.at("09:00").do(self.run_daily_task)  # 改为早上9点
```

### 修改新闻关键词

编辑 `legal_tech_news_bot.py` 文件的第58行：

```python
self.search_keywords = 'legal tech OR law OR legal AI'  # 添加更多关键词
```

### 修改AI模型

如果想使用更强大的Claude模型，编辑第144行：

```python
'model': 'claude-3-5-sonnet-20241022',  # 改为Sonnet模型
```

## 💰 API限制与成本

### NewsAPI 限制

| 版本 | 价格 | 请求限制 |
|------|------|----------|
| 免费版 | 免费 | 每天100次请求 |
| 付费版 | $449/月 | 每天10,000次请求 |

**程序特性**：
- ✅ 自动监控API使用次数
- ✅ 剩余10次以下时发出警告
- ✅ 达到限制时自动停止请求
- 📝 日志显示：`NewsAPI今日已使用: 1/100`

### Claude API 成本

| 模型 | 输入成本 | 输出成本 | 说明 |
|------|----------|----------|------|
| Haiku | $0.25/百万token | $1.25/百万token | 快速、低成本（推荐） |
| Sonnet | $3/百万token | $15/百万token | 平衡性能和成本 |
| Opus | $15/百万token | $75/百万token | 最强性能 |

**预估成本**（Haiku模型）：
- 每天运行1次：约 $0.001-0.005/天
- 每月成本：约 $0.03-0.15/月

**成本优化**：
- 默认使用Haiku模型，成本最低
- 限制每次获取10条新闻，减少token使用
- `max_tokens=2000`，控制输出长度

## 🔄 备用方案

当Claude API调用失败时，程序会自动切换到备用方案：

### 备用方案特点

✅ **无需API**：不依赖任何AI服务
✅ **稳定性高**：纯格式化，不会失败
⚠️ **无翻译**：保持英文原文，无中文摘要
📧 **仍可推送**：确保每天都能收到新闻

### 备用方案示例

```
📰 法律科技日报 - 2025年01月20日

⚠️ 注意：由于AI服务暂时不可用，今日为英文原始新闻

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 新闻 1
标题: AI Legal Tech Startup Raises $10M
摘要: The company plans to expand its AI-powered contract analysis...
来源: TechCrunch
链接: https://techcrunch.com/...
...
```

### 控制备用方案

在 `.env` 文件中设置：

```env
# 启用备用方案（推荐）
ENABLE_FALLBACK=true

# 禁用备用方案（API失败时将不发送Newsletter）
ENABLE_FALLBACK=false
```

**建议**：
- ✅ 日常使用：保持 `ENABLE_FALLBACK=true`
- ⚠️ 仅在需要严格验证AI功能时设置为 `false`

## 🐛 常见问题

### 1. 提示"缺少必需的配置项"

**原因**：`.env` 文件未正确配置或文件名错误

**解决方法**：
- 确认文件名是 `.env`（不是 `.env.txt`）
- Windows：在文件资源管理器中，查看 → 勾选"文件扩展名"
- 确认三个配置项都已填写

### 2. NewsAPI请求失败

**原因**：API密钥错误或达到请求限制

**解决方法**：
- 检查API密钥是否正确复制
- 确认未超过免费版限制（每天100次）
- 访问 NewsAPI 控制台查看使用情况

### 3. Claude API调用失败

**原因**：API密钥错误或余额不足

**解决方法**：
- 检查API密钥格式（应该以 `sk-ant-` 开头）
- 在 [Anthropic控制台](https://console.anthropic.com/) 检查账户余额
- Haiku模型成本：约$0.25/百万输入token

### 4. 飞书机器人无响应

**原因**：Webhook URL错误或机器人被禁用

**解决方法**：
- 确认Webhook URL完整复制（包含 `https://`）
- 在飞书群中检查机器人状态
- 尝试重新创建飞书机器人

### 5. 程序运行但没有推送

**原因**：定时任务未到执行时间

**解决方法**：
- 查看日志文件 `news_bot.log`
- 使用单次运行模式测试：
  ```python
  bot.run_once()  # 改为run_once()
  ```

## 📝 开发说明

### 代码结构

```
legal_tech_news_bot.py
├── Config类              # 配置管理
├── NewsFetcher类         # 新闻获取
├── NewsletterGenerator类 # AI内容生成
├── FeishuNotifier类      # 飞书推送
└── LegalTechNewsBot类    # 主控制器
```

### 日志文件

程序运行时会生成 `news_bot.log` 文件，记录所有操作和错误：

```bash
# 查看实时日志（macOS/Linux）
tail -f news_bot.log

# 查看最后50行
tail -n 50 news_bot.log
```

### 依赖更新

定期更新依赖包以获得安全和性能改进：

```bash
pip install --upgrade -r requirements.txt
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

如有问题，请提交Issue或联系开发者。

---

**⚠️ 重要提醒**：
- 请妥善保管API密钥，不要分享给他人或提交到代码仓库
- 建议将 `.env` 文件添加到 `.gitignore`
- 定期检查API使用量和费用
