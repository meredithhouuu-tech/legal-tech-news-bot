# 📖 macOS系统 - 法律科技新闻Bot详细运行步骤

**适合人群**：使用macOS，从未或很少使用终端
**预计时间**：10-15分钟
**目标**：在Mac上成功运行Bot

---

## 📋 开始前的准备

### 你需要准备：

- ✅ 一台Mac电脑
- ✅ 稳定的网络连接
- ✅ 一个飞书账号
- ✅ 一个邮箱账号（用于注册API服务）

### 需要注册的3个服务：

1. **NewsAPI** - 免费（每天100次请求）
   - 注册地址：https://newsapi.org/register
   
2. **Claude API** - 按量付费（约$0.03-0.15/月）
   - 注册地址：https://console.anthropic.com/
   
3. **飞书** - 免费
   - 下载地址：https://www.feishu.cn/

---

## 步骤 1/10：检查Python是否已安装

### 1.1 打开终端

**方法1：通过Spotlight搜索**（推荐）
1. 按 `Command + 空格` 打开Spotlight搜索
2. 输入 `终端` 或 `Terminal`
3. 按回车打开

**方法2：通过Launchpad**
1. 点击Launchpad（启动台）
2. 在搜索框输入"终端"
3. 点击终端图标

**方法3：通过Finder**
1. 打开Finder
2. 应用程序 → 实用工具 → 终端

### 1.2 检查Python版本

在终端窗口中，输入以下命令：

```bash
python3 --version
```

按回车，查看结果：

**情况A：显示版本号**（如 `Python 3.9.7` 或 `3.10.5` 等）
- ✅ 已安装Python 3.8或更高版本
- ✅ 可以直接跳到[步骤3](#步骤-310下载项目文件)

**情况B：显示 `command not found`**
- ❌ 未安装Python
- ❌ 需要继续[步骤2](#步骤-29安装python)

**情况C：显示版本过低**（如 `Python 3.7`）
- ⚠️ 版本过低，需要升级
- 继续下一步安装新版本

---

## 步骤 2/10：安装Python

### 方法A：使用Homebrew安装（推荐）

#### 2.1 检查是否安装了Homebrew

在终端输入：

```bash
brew --version
```

**如果显示版本号**：已安装Homebrew，跳到2.3

**如果显示 `command not found`**：需要先安装Homebrew

#### 2.2 安装Homebrew（如果未安装）

在终端输入以下命令并按回车：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

安装过程：
1. 系统会提示你输入密码（你的Mac登录密码）
2. 输入密码时屏幕不会显示，这是正常的
3. 输入后按回车
4. 等待安装完成（可能需要5-10分钟）
5. 看到 "Installation successful!" 表示成功

#### 2.3 使用Homebrew安装Python

在终端输入：

```bash
brew install python3
```

按回车，等待安装完成（可能需要3-5分钟）

### 方法B：从官网安装（备选）

1. 访问 Python官网：https://www.python.org/downloads/macos/
2. 下载最新版的Python安装包（如 `python-3.x.x-macos11.pkg`）
3. 双击安装包
4. 按照安装向导完成安装
5. 安装完成后，重新打开终端
6. 再次输入 `python3 --version` 确认安装成功

---

## 步骤 3/10：下载项目文件

### 3.1 确定项目存放位置

建议将项目放在一个固定位置，例如：

```bash
~/legal-tech-bot/              # 用户目录下
~/Desktop/legal-tech-bot/      # 桌面
~/Documents/legal-tech-bot/    # 文档文件夹
```

### 3.2 准备项目文件

确保以下文件在同一个文件夹中：

```
legal-tech-bot/
├── legal_tech_news_bot.py
├── requirements.txt
├── .env.example
├── run.sh
├── README.md
└── 其他文件...
```

**如果从git/zip下载**：
- 下载后解压到固定位置
- 记住这个文件夹的路径

---

## 步骤 4/10：在终端中进入项目目录

### 4.1 使用cd命令进入项目文件夹

**假设项目在桌面**：

```bash
cd ~/Desktop/legal-tech-bot
```

**假设项目在用户目录**：

```bash
cd ~/legal-tech-bot
```

**假设项目在文档文件夹**：

```bash
cd ~/Documents/legal-tech-bot
```

### 4.2 验证是否进入了正确目录

输入以下命令：

```bash
ls
```

按回车，应该能看到项目文件列表：
```
README.md              legal_tech_news_bot.py
requirements.txt       run.sh
.env.example           test_config.py
```

**如果看不到这些文件**：
- 说明目录不对，重新使用 `cd` 命令进入正确位置
- 或者直接拖拽文件夹到终端窗口，会自动显示路径

**技巧：快速进入目录**
1. 在Finder中找到项目文件夹
2. 输入 `cd ` （注意cd后面有个空格）
3. 将文件夹从Finder拖到终端窗口
4. 终端会自动填入完整路径
5. 按回车

---

## 步骤 5/10：安装Python依赖包

### 5.1 安装依赖

在终端（确保已在项目目录）输入：

```bash
pip3 install -r requirements.txt
```

按回车，等待安装完成。

### 5.2 查看安装结果

成功的输出类似这样：

```
Collecting requests>=2.31.0
  Downloading requests-2.31.0-py3-none-any.whl (62 kB)
Collecting schedule>=1.2.0
  Downloading schedule-1.2.0-py3-none-any.whl (10 kB)
Collecting python-dotenv>=1.0.0
  Downloading python_dotenv-1.0.0-py3-none-any.whl (19 kB)
Installing collected packages: requests, schedule, python-dotenv
Successfully installed requests-2.31.0 schedule-1.2.0 python-dotenv-1.0.0
```

### 5.3 故障排查

**问题1：`pip3: command not found`**
```bash
# 解决方案：重新安装Python
brew reinstall python3
```

**问题2：权限错误 `Permission denied`**
```bash
# 解决方案：使用用户目录安装
pip3 install --user -r requirements.txt
```

**问题3：网络超时**
```bash
# 解决方案：使用国内镜像源
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 步骤 6/10：创建配置文件

### 6.1 复制配置文件模板

在终端输入：

```bash
cp .env.example .env
```

按回车，这会创建一个名为 `.env` 的配置文件。

### 6.2 验证文件创建成功

输入：

```bash
ls -la | grep .env
```

应该能看到：
```
-rw-r--r--  1 yourname  staff   xxx Jan 20 12:00 .env
-rw-r--r--  1 yourname  staff   xxx Jan 20 12:00 .env.example
```

**⚠️ 注意**：
- `.env` 是隐藏文件（以点开头）
- Finder中默认看不到，需要在终端查看

**如何让Finder显示隐藏文件**：
```bash
# 在终端输入，然后按回车
defaults write com.apple.finder AppleShowAllFiles -bool true
killall Finder
```

---

## 步骤 7/10：获取API密钥

### 7.1 获取NewsAPI密钥（免费）

1. 打开浏览器，访问：https://newsapi.org/register
2. 填写注册表单：
   - **Email**: 你的邮箱地址
   - **Password**: 设置一个密码
   - **Password confirmation**: 再次输入密码
   - **Organization**: 个人或公司名称（可以随便填，如"Personal"）
3. 点击 **"Get API Key"** 按钮
4. 注册成功后，页面会显示你的API Key，格式类似：
   ```
   a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   ```
5. **复制这个Key并保存到记事本或备忘录**

**⚠️ 重要**：
- NewsAPI免费版每天最多100次请求
- 对于每天运行1次的Bot，完全够用

### 7.2 获取Claude API密钥（付费）

1. 打开浏览器，访问：https://console.anthropic.com/
2. 点击右上角的 **"Sign up"** 或 **"Log in"**
3. 使用邮箱注册或登录
4. 登录后，进入控制台
5. 左侧菜单中点击 **"API Keys"**
6. 点击右上角的 **"Create Key"** 按钮
7. 在弹出的对话框中：
   - **Name**: 输入Key的名称，如 `Legal Tech Bot`
   - 点击 **"Create key"**
8. 复制生成的API Key，格式类似：
   ```
   sk-ant-api03-xxx-xxx-xxx
   ```
9. **保存这个Key到记事本或备忘录**

**⚠️ 重要提示**：
- 需要绑定信用卡用于计费
- 使用Haiku模型，每天运行1次，每月约$0.03-0.15
- 可以在控制台设置使用限额
- API Key只显示一次，请立即保存

**预估成本计算**：
- Haiku输入：$0.25/百万tokens
- 每次约2000 tokens × 30天 = 60,000 tokens/月
- 成本：60,000 ÷ 1,000,000 × $0.25 ≈ $0.015/月

### 7.3 创建飞书机器人

1. 打开飞书客户端
2. 选择一个群聊（可以创建测试群）
3. 点击群聊右上角的 **...** 按钮
4. 选择 **"群设置"**
5. 找到 **"群机器人"** 选项
6. 点击 **"添加机器人"**
7. 选择 **"自定义机器人"**
8. 设置机器人信息：
   - **名称**: 法律科技新闻Bot（或其他你喜欢的名字）
   - **描述**: 每天推送法律科技新闻
   - **头像**: 可以上传图片（可选）
9. 点击 **"添加"**
10. 复制Webhook地址，格式类似：
    ```
    https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    ```
11. **保存这个地址到记事本或备忘录**

**⚠️ 注意**：
- Webhook URL包含机器人权限，不要泄露给他人
- 可以在群设置中随时删除或禁用机器人

---

## 步骤 8/10：填写配置文件

### 8.1 打开配置文件

**方法A：使用nano编辑器（终端内置）**

在终端输入：

```bash
nano .env
```

按回车，会打开nano编辑器

**方法B：使用VS Code**

如果你安装了VS Code：

```bash
code .env
```

**方法C：使用TextEdit（文本编辑）**

```bash
open -a TextEdit .env
```

### 8.2 填写API密钥

将文件内容修改为：

```env
# ========== 必需配置（必须填写）==========

# NewsAPI 密钥（粘贴刚才复制的密钥）
NEWS_API_KEY=你的NewsAPI密钥粘贴在这里

# Claude API 密钥（粘贴刚才复制的密钥）
CLAUDE_API_KEY=你的Claude密钥粘贴在这里

# 飞书 Webhook 地址（粘贴刚才复制的地址）
FEISHU_WEBHOOK_URL=你的飞书Webhook地址粘贴在这里

# ========== 可选配置（保持默认即可）==========

# 运行模式：test（测试模式，立即执行一次）或 production（生产模式，每天12点执行）
RUN_MODE=test

# 是否启用备用方案（当Claude API失败时自动使用简单格式）
ENABLE_FALLBACK=true

# 新闻搜索关键词（使用 OR 连接多个关键词）
SEARCH_KEYWORDS=legal tech OR legal technology OR lawtech OR legal AI

# 每次获取的新闻数量（建议10-20条）
MAX_ARTICLES=10
```

### 8.3 保存配置文件

**如果使用nano编辑器**：
1. 按下 `Ctrl + O`（写入文件）
2. 按下 `Enter` 确认
3. 按下 `Ctrl + X` 退出编辑器

**如果使用VS Code或TextEdit**：
1. `Command + S` 保存
2. `Command + Q` 退出

### 8.4 验证配置文件

查看文件内容：

```bash
cat .env
```

确保：
- ✅ 三个API密钥都已填写
- ✅ 没有多余的空格或换行
- ✅ RUN_MODE=test（测试模式）

---

## 步骤 9/10：测试运行

### 9.1 运行Bot

在终端输入：

```bash
python3 legal_tech_news_bot.py
```

按回车，观察输出。

### 9.2 查看输出结果

**正常的成功输出**：

```
============================================================
🚀 法律科技新闻Bot启动
============================================================

============================================================
📋 API限制说明
============================================================
NewsAPI: 免费版每天最多 100 次请求
Claude API: Haiku模型，约$0.25/百万输入token
当前配置: 最大2000 tokens/次
备用方案: ✅ 已启用
============================================================

✅ 配置验证通过
📊 运行模式: test

🧪 测试模式：立即执行一次任务
💡 提示：如需切换到定时模式，请在.env中设置 RUN_MODE=production

============================================================
⏰ 开始执行每日任务 - 2025-01-20 xx:xx:xx
============================================================

🔍 开始获取法律科技新闻...
✅ 成功获取 10 条新闻
📊 NewsAPI今日已使用: 1/100

🤖 开始使用Claude API生成Newsletter...
✅ Newsletter生成成功（使用Claude API）

📤 开始发送飞书通知...
✅ 飞书通知发送成功

============================================================
✅ 今日任务完成
============================================================
```

### 9.3 检查飞书群

1. 打开飞书客户端
2. 进入你添加机器人的群聊
3. 查看是否收到机器人推送的消息

**消息示例**：
```
📰 法律科技日报 - 2025年01月20日

🔥 今日头条
1. 【AI律师助手】某公司推出新的法律AI工具...
   摘要：这款工具可以帮助律师...
   来源：TechCrunch
   链接：https://techcrunch.com/...
...
```

### 9.4 故障排查

**错误1：缺少必需的配置项**
```

❌ 配置错误: 缺少必需的配置项: NEWS_API_KEY
```
**解决**：

- 检查 `.env` 文件是否存在
- 检查三个密钥是否都已填写
- 检查密钥前后是否有多余空格

**错误2：API密钥错误**
```
❌ Claude API请求失败: 401 Client Error
💡 提示：请检查CLAUDE_API_KEY是否正确
```
**解决**：
- 重新复制API密钥
- 确保完整复制（Claude密钥以 `sk-ant-` 开头）
- 去掉密钥前后的空格

**错误3：网络请求失败**
```
❌ 网络请求异常
```
**解决**：
- 检查网络连接
- 检查是否使用代理/VPN
- 尝试关闭VPN后重试

**错误4：飞书未收到消息**
```
✅ 飞书通知发送成功（但飞书群里看不到）
```
**解决**：
- 检查Webhook URL是否完整复制
- 检查飞书机器人是否被删除
- 测试Webhook：
  ```bash
  curl -X POST "你的WebhookURL" \
    -H "Content-Type: application/json" \
    -d '{"msg_type":"text","content":{"text":"测试消息"}}'
  ```

---

## 步骤 10/10：正式运行

### 10.1 切换到生产模式

如果测试成功（飞书收到了消息），现在可以切换到定时模式。

1. 重新打开 `.env` 文件：
   ```bash
   nano .env
   ```

2. 找到这一行：
   ```env
   RUN_MODE=test
   ```

3. 改为：
   ```env
   RUN_MODE=production
   ```

4. 保存并退出（`Ctrl + O` → `Enter` → `Ctrl + X`）

### 10.2 启动Bot

**方法1：前台运行（适合测试）**

```bash
python3 legal_tech_news_bot.py
```

Bot会持续运行，每天中午12点自动推送新闻。

看到提示：
```
📅 Bot已启动，将在每天中午12:00推送新闻
💡 提示：按Ctrl+C可以停止Bot
```

**重要**：
- 不要关闭终端窗口
- 如果关闭终端，Bot会停止
- 适合临时测试使用

**方法2：后台运行（推荐）**

使用 `nohup` 命令让Bot在后台持续运行：

```bash
nohup python3 legal_tech_news_bot.py > bot.log 2>&1 &
```

解释：
- `nohup`: 不挂断运行
- `> bot.log`: 输出到日志文件
- `2>&1`: 错误也输出到日志
- `&`: 后台运行

运行后，终端会显示一个进程ID，如：
```
[1] 12345
```

**查看Bot是否在运行**：
```bash
ps aux | grep legal_tech_news_bot.py
```

**查看实时日志**：
```bash
tail -f news_bot.log
```

按 `Ctrl + C` 退出日志查看（不会停止Bot）

**停止后台运行的Bot**：

1. 找到进程ID：
   ```bash
   ps aux | grep legal_tech_news_bot.py
   ```
   输出类似：
   ```
   yourname  12345  0.0  0.5  ... python3 legal_tech_news_bot.py
   ```
   `12345` 就是进程ID

2. 停止进程：
   ```bash
   kill 12345
   ```

**方法3：使用启动脚本（最方便）**

项目已提供 `run.sh` 脚本：

```bash
./run.sh
```

这会自动检查依赖并运行Bot。

---

## 高级设置（可选）

### 1. 设置开机自启

使用LaunchAgent让Bot开机自动运行：

1. 创建LaunchAgent配置文件：
   ```bash
   nano ~/Library/LaunchAgents/com.legaltech.newsbot.plist
   ```

2. 粘贴以下内容（替换路径为你的实际路径）：

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
     "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.legaltech.newsbot</string>
       
       <key>ProgramArguments</key>
       <array>
           <string>/usr/local/bin/python3</string>
           <string>/Users/你的用户名/legal-tech-bot/legal_tech_news_bot.py</string>
       </array>
       
       <key>RunAtLoad</key>
       <true/>
       
       <key>KeepAlive</key>
       <true/>
       
       <key>WorkingDirectory</key>
       <string>/Users/你的用户名/legal-tech-bot</string>
       
       <key>StandardOutPath</key>
       <string>/Users/你的用户名/legal-tech-bot/news_bot.log</string>
       
       <key>StandardErrorPath</key>
       <string>/Users/你的用户名/legal-tech-bot/news_bot.log</string>
   </dict>
   </plist>
   ```

3. 保存并退出（`Ctrl + O` → `Enter` → `Ctrl + X`）

4. 加载配置：
   ```bash
   launchctl load ~/Library/LaunchAgents/com.legaltech.newsbot.plist
   ```

5. 查看状态：
   ```bash
   launchctl list | grep legaltech
   ```

6. 停止自启：
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.legaltech.newsbot.plist
   ```

### 2. 修改推送时间

默认是每天12:00推送，如需修改，编辑主程序：

```bash
nano legal_tech_news_bot.py
```

找到这一行（约第430行）：

```python
schedule.every().day.at("12:00").do(self.run_daily_task)
```

改为你想要的时间，24小时制：

```python
schedule.every().day.at("09:00").do(self.run_daily_task)  # 改为早上9点
schedule.every().day.at("18:00").do(self.run_daily_task)  # 改为下午6点
```

保存并重启Bot。

### 3. 查看日志文件

日志文件 `news_bot.log` 记录了所有运行信息：

```bash
# 查看完整日志
cat news_bot.log

# 查看最后50行
tail -n 50 news_bot.log

# 实时监控日志
tail -f news_bot.log

# 搜索错误
grep "ERROR" news_bot.log
```

---

## 验证成功清单

运行Bot后，检查以下项目：

### ✅ 终端输出
- [ ] 看到"配置验证通过"
- [ ] 看到"成功获取 X 条新闻"
- [ ] 看到"Newsletter生成成功"
- [ ] 看到"飞书通知发送成功"
- [ ] 没有大量ERROR信息

### ✅ 飞书群
- [ ] 收到机器人推送的消息
- [ ] 消息格式正常
- [ ] 包含新闻标题、来源、链接

### ✅ 日志文件
- [ ] 生成了 `news_bot.log` 文件
- [ ] 日志内容正常
- [ ] 没有异常错误

### ✅ 后台运行
- [ ] Bot在后台持续运行
- [ ] 使用 `ps aux` 能看到进程
- [ ] 关闭终端后Bot仍在运行

---

## 常见问题快速参考

### Q1: 如何停止Bot？

```bash
# 找到进程
ps aux | grep legal_tech_news_bot.py

# 停止进程
kill <进程ID>

# 如果无法停止，强制停止
kill -9 <进程ID>
```

### Q2: Bot没有在12点推送消息？

```bash
# 1. 检查Bot是否在运行
ps aux | grep legal_tech_news_bot.py

# 2. 检查.env文件中的RUN_MODE
cat .env | grep RUN_MODE

# 3. 查看日志
tail -n 50 news_bot.log
```

### Q3: 如何重新配置？

```bash
# 停止Bot
kill <进程ID>

# 编辑配置
nano .env

# 重新启动
python3 legal_tech_news_bot.py
```

### Q4: 如何升级依赖包？

```bash
pip3 install --upgrade -r requirements.txt
```

### Q5: 忘记了API密钥怎么办？

- NewsAPI: 登录 https://newsapi.org/ 查看
- Claude: 登录 https://console.anthropic.com/ 查看
- 飞书: 在群设置中重新创建机器人

---

## 下一步建议

### 1. 监控Bot运行状态

定期检查：
- 每天查看飞书群是否收到消息
- 每周查看日志文件是否有异常
- 每月检查API使用量和费用

### 2. 优化配置

根据需求调整：
- 推送时间
- 新闻关键词
- 新闻数量
- 是否启用备用方案

### 3. 备份重要数据

备份以下文件：
- `.env` 配置文件
- `news_bot.log` 日志文件
- 修改过的源代码

---

## 📞 获取帮助

### 遇到问题时：

1. **查看日志**
   ```bash
   cat news_bot.log
   ```

2. **运行测试脚本**
   ```bash
   python3 test_config.py
   ```

3. **查看完整文档**
   - `README.md` - 完整功能说明
   - `QUICKSTART.md` - 快速开始指南

4. **检查API状态**
   - NewsAPI: https://newsapi.org/
   - Claude: https://console.anthropic.com/
   - 飞书开发者：https://open.feishu.cn/

---

## 🎉 恭喜！

如果你已经成功运行Bot，恭喜！你现在拥有了一个每天自动推送法律科技新闻的个人助手。

**最后提醒**：
- ✅ 定期检查API使用量
- ✅ 保持 `.env` 文件安全，不要分享给他人
- ✅ 定期查看日志文件
- ✅ 根据需要调整配置

**祝使用愉快！** 🎊
