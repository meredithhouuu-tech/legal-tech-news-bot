# 📖 法律科技新闻Bot - 详细运行步骤指南

**适合人群**：完全小白，从未使用过Python
**预计时间**：15-20分钟
**目标**：从零开始，成功运行Bot

---

## 📋 目录

1. [准备工作](#1-准备工作)
2. [Windows系统运行步骤](#2-windows系统运行步骤)
3. [macOS系统运行步骤](#3-macos系统运行步骤)
4. [Linux系统运行步骤](#4-linux系统运行步骤)
5. [验证运行成功](#5-验证运行成功)
6. [常见问题排查](#6-常见问题排查)

---

## 1. 准备工作

### 在开始之前，你需要准备：

- ✅ 一台电脑
- ✅ 稳定的网络连接
- ✅ 一个飞书账号（用于创建机器人）
- ✅ 一个邮箱账号（用于注册API服务）

### 需要注册的3个服务（全部免费或低成本）：

1. **NewsAPI** - 免费（每天100次请求）
   - 注册地址：https://newsapi.org/register
   - 需要：邮箱
   
2. **Claude API** - 按量付费（约$0.03-0.15/月）
   - 注册地址：https://console.anthropic.com/
   - 需要：邮箱 + 信用卡（绑定计费）
   
3. **飞书** - 免费
   - 下载飞书客户端：https://www.feishu.cn/
   - 需要：手机号注册

---

## 2. Windows系统运行步骤

### 步骤 1/9：检查是否已安装Python

1. 按键盘 `Win + R`，输入 `cmd`，按回车
2. 在黑色窗口中输入：
   ```
   python --version
   ```
3. 按回车，查看结果：

**情况A：显示版本号（如 `Python 3.10.5`）**
- ✅ 已安装Python，直接跳到[步骤3](#步骤-39下载项目文件)

**情况B：显示 `'python' 不是内部或外部命令`**
- ❌ 未安装Python，继续[步骤2](#步骤-29安装python)

---

### 步骤 2/9：安装Python

1. 访问 Python官网：https://www.python.org/downloads/
2. 点击大按钮 "Download Python 3.x.x"
3. 下载完成后，双击安装包
4. **⚠️ 重要：勾选 "Add Python to PATH"**
   ```
   ☑ Add Python to PATH
   ```
5. 点击 "Install Now"
6. 等待安装完成（约2-5分钟）
7. 安装成功后，重新打开CMD，再次输入：
   ```
   python --version
   ```
8. 看到版本号 = 安装成功 ✅

---

### 步骤 3/9：下载项目文件

**方法A：你已经有项目文件**
- 确保以下文件在同一个文件夹中：
  - `legal_tech_news_bot.py`
  - `requirements.txt`
  - `.env.example`
  - `README.md`
  - 其他文件...

**方法B：从GitHub/git下载**
- 将项目文件夹放到一个固定位置，例如：
  - `D:\legal-tech-bot\`
  - `C:\Users\你的用户名\Desktop\legal-tech-bot\`

---

### 步骤 4/9：打开项目文件夹

1. 打开"文件资源管理器"
2. 找到项目文件夹（例如 `D:\legal-tech-bot`）
3. 在文件夹地址栏中输入：
   ```
   cmd
   ```
4. 按回车，会打开一个CMD窗口，路径已自动定位到项目文件夹

---

### 步骤 5/9：安装Python依赖包

在上一步打开的CMD窗口中，输入：

```bash
pip install -r requirements.txt
```

按回车，等待安装完成。

**成功标志**：看到类似这样的输出：
```
Successfully installed requests-2.31.0 schedule-1.2.0 python-dotenv-1.0.0
```

**如果报错**：
- 错误：`'pip' 不是内部或外部命令`
  - 解决：Python未正确安装，重新安装并勾选 "Add Python to PATH"
  
- 错误：`Connection timeout`
  - 解决：网络问题，尝试使用国内镜像：
    ```bash
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```

---

### 步骤 6/9：创建配置文件

1. 在项目文件夹中，找到 `.env.example` 文件
2. 右键点击 → 复制
3. 在空白处右键 → 粘贴
4. 将复制的文件重命名为 `.env`
   - ⚠️ 注意：文件名就是 `.env`，前面有个点，后面没有扩展名
   - ⚠️ Windows可能提示"必须输入文件名"，直接输入 `.env.` 即可

**重要：Windows如何显示文件扩展名**
1. 打开文件夹，点击顶部的"查看"
2. 勾选"文件扩展名"
3. 现在你可以看到完整文件名了

---

### 步骤 7/9：获取API密钥

#### 7.1 获取NewsAPI密钥（免费）

1. 访问：https://newsapi.org/register
2. 填写表单：
   - Email: 你的邮箱
   - Password: 设置密码
   - Organization: 个人或公司名（随意）
3. 点击 "Get API Key"
4. 注册成功后，你会看到一个API Key，类似：
   ```
   a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   ```
5. **复制并保存这个Key**（记事本临时保存）

#### 7.2 获取Claude API密钥（付费）

1. 访问：https://console.anthropic.com/
2. 点击 "Sign up" 或 "Log in"
3. 注册/登录后，进入控制台
4. 左侧菜单 → "API Keys"
5. 点击 "Create Key"
6. 给Key起个名字，如 "Legal Tech Bot"
7. 复制生成的Key，格式类似：
   ```
   sk-ant-api03-xxx...
   ```
8. **复制并保存这个Key**

**⚠️ 重要提示**：
- Claude API需要绑定信用卡计费
- 使用Haiku模型，每月成本约$0.03-0.15（每天1次）
- 可以设置使用限额，避免超支

#### 7.3 创建飞书机器人

1. 打开飞书客户端
2. 进入一个群聊（可以创建测试群）
3. 点击右上角 `...` → `群设置` → `群机器人`
4. 点击 `添加机器人` → `自定义机器人`
5. 设置机器人名称：`法律科技新闻Bot`
6. 上传头像（可选）
7. 点击 `添加`
8. **复制Webhook地址**，格式类似：
   ```
   https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxx
   ```
9. **复制并保存这个地址**

---

### 步骤 8/9：填写配置文件

1. 用记事本打开 `.env` 文件：
   - 右键 `.env` 文件
   - 选择"打开方式" → "记事本"
   
2. 填写你的API密钥：

```env
# ========== 必需配置（必须填写）==========

# NewsAPI 密钥（刚才复制的）
NEWS_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

# Claude API 密钥（刚才复制的）
CLAUDE_API_KEY=sk-ant-api03-xxx...

# 飞书 Webhook 地址（刚才复制的）
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxx

# ========== 可选配置（保持默认即可）==========

# 运行模式：test（测试）或 production（生产）
RUN_MODE=test

# 是否启用备用方案
ENABLE_FALLBACK=true

# 新闻数量
MAX_ARTICLES=10
```

3. 保存文件：
   - `Ctrl + S` 保存
   - `Ctrl + W` 关闭记事本

---

### 步骤 9/9：测试运行

#### 9.1 测试配置

1. 在CMD窗口中，输入：
   ```bash
   python legal_tech_news_bot.py
   ```
2. 按回车，观察输出：

**正常输出（成功）**：
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
⏰ 开始执行每日任务 - 2025-01-20 12:00:00
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

3. **检查飞书群**：
   - 打开飞书客户端
   - 进入你添加机器人的群聊
   - 应该能看到机器人发送的消息

#### 9.2 切换到生产模式

如果测试成功（飞书收到消息），现在可以切换到定时模式：

1. 重新打开 `.env` 文件（记事本）
2. 找到这一行：
   ```env
   RUN_MODE=test
   ```
3. 改为：
   ```env
   RUN_MODE=production
   ```
4. 保存文件

#### 9.3 正式运行

1. 在CMD窗口中，再次运行：
   ```bash
   python legal_tech_news_bot.py
   ```

2. 现在Bot会持续运行，每天中午12点自动推送新闻

3. 看到提示：
   ```
   📅 Bot已启动，将在每天中午12:00推送新闻
   💡 提示：按Ctrl+C可以停止Bot
   ```

4. **重要**：
   - 不要关闭CMD窗口
   - 如果关闭，Bot会停止运行
   - 想要Bot持续运行，可以参考[后台运行](#后台运行-windows)

---

### 后台运行（Windows）

**方法1：使用bat脚本（推荐）**

1. 使用项目中的 `run.bat` 脚本
2. 双击 `run.bat` 文件即可运行

**方法2：使用任务计划程序（开机自启）**

1. 按 `Win + R`，输入 `taskschd.msc`
2. 右侧 "创建基本任务"
3. 设置触发器：计算机启动时
4. 设置操作：启动程序
   - 程序：`python.exe` 的完整路径
   - 参数：`legal_tech_news_bot.py` 的完整路径
5. 完成设置

---

## 3. macOS系统运行步骤

### 步骤 1/7：检查Python是否已安装

1. 打开"终端"（Spotlight搜索"Terminal"）
2. 输入：
   ```bash
   python3 --version
   ```

**情况A：显示版本号**
- ✅ 已安装，跳到[步骤3](#步骤-33下载项目文件)

**情况B：未安装**
- 继续下一步

---

### 步骤 2/7：安装Python

**使用Homebrew安装（推荐）**：

1. 检查是否安装了Homebrew：
   ```bash
   brew --version
   ```

2. 如果未安装，先安装Homebrew：
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. 安装Python：
   ```bash
   brew install python3
   ```

---

### 步骤 3/7：下载项目文件

确保项目文件夹在固定位置，例如：
```bash
~/legal-tech-bot/
```

---

### 步骤 4/7：打开终端并进入项目目录

```bash
cd ~/legal-tech-bot
```

或者：
```bash
cd /Users/你的用户名/legal-tech-bot
```

---

### 步骤 5/7：安装依赖包

```bash
pip3 install -r requirements.txt
```

---

### 步骤 6/7：配置环境变量

1. 复制配置文件：
   ```bash
   cp .env.example .env
   ```

2. 编辑配置文件：
   ```bash
   nano .env
   ```
   或
   ```bash
   code .env
   ```

3. 填写API密钥（参考Windows部分的步骤7-8）

4. 保存：`Ctrl + O` → `Enter` → `Ctrl + X`

---

### 步骤 7/7：运行Bot

**测试运行**：
```bash
python3 legal_tech_news_bot.py
```

**后台运行**：
```bash
nohup python3 legal_tech_news_bot.py > bot.log 2>&1 &
```

**查看日志**：
```bash
tail -f news_bot.log
```

**停止Bot**：
```bash
ps aux | grep legal_tech_news_bot.py
kill <进程ID>
```

---

## 4. Linux系统运行步骤

与macOS类似，使用相同的命令：

```bash
# 1. 安装Python3（如果未安装）
sudo apt-get update
sudo apt-get install python3 python3-pip

# 2. 安装依赖
pip3 install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
nano .env

# 4. 运行
python3 legal_tech_news_bot.py

# 5. 后台运行
nohup python3 legal_tech_news_bot.py > bot.log 2>&1 &
```

---

## 5. 验证运行成功

### ✅ 成功标志

1. **终端/命令行输出**：
   - ✅ 看到"配置验证通过"
   - ✅ 看到"成功获取 X 条新闻"
   - ✅ 看到"Newsletter生成成功"
   - ✅ 看到"飞书通知发送成功"

2. **飞书群消息**：
   - ✅ 收到机器人推送的消息
   - ✅ 消息格式正常，包含新闻列表

3. **日志文件**：
   - ✅ 生成了 `news_bot.log` 文件
   - ✅ 日志内容没有大量错误

### ❌ 失败标志

1. **飞书未收到消息**：
   - 检查Webhook URL是否正确
   - 检查飞书机器人是否被禁用

2. **报错 "缺少必需的配置项"**：
   - 检查 `.env` 文件是否存在
   - 检查API密钥是否填写完整

3. **报错 "API请求失败"**：
   - 检查API密钥是否正确
   - 检查网络连接是否正常
   - 查看具体错误代码（401/429/400）

---

## 6. 常见问题排查

### 问题1：Python未安装或版本过低

**症状**：
```
'python' 不是内部或外部命令
Python 3.7（需要3.8+）
```

**解决**：
- Windows：重新安装Python 3.8+
- macOS：`brew install python3`
- Linux：`sudo apt-get install python3`

---

### 问题2：pip安装失败

**症状**：
```
ERROR: Could not find a version that satisfies the requirement...
```

**解决**：
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像（中国用户）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

### 问题3：.env文件找不到

**症状**：
```
缺少必需的配置项: NEWS_API_KEY
```

**解决**：
1. 确认文件名是 `.env`（不是 `.env.txt`）
2. Windows：显示文件扩展名后重命名
3. macOS/Linux：`ls -a` 查看隐藏文件

---

### 问题4：API密钥错误

**症状**：
```
❌ Claude API请求失败: 401 Client Error
❌ 请检查CLAUDE_API_KEY是否正确
```

**解决**：
1. 重新复制API密钥（确保没有多余空格）
2. 检查密钥是否完整（Claude密钥以 `sk-ant-` 开头）
3. 访问API控制台确认密钥状态

---

### 问题5：NewsAPI配额用尽

**症状**：
```
❌ NewsAPI配额已用完！今日已使用100次
```

**解决**：
1. 等到第二天配额重置
2. 或升级到付费版
3. 或换一个API密钥

---

### 问题6：飞书机器人不发送消息

**症状**：
- 日志显示"发送成功"，但飞书收不到

**解决**：
1. 检查飞书机器人是否被删除
2. 检查Webhook URL是否完整复制
3. 重新创建飞书机器人
4. 测试Webhook：
   ```bash
   curl -X POST "你的WebhookURL" -H "Content-Type: application/json" -d '{"msg_type":"text","content":{"text":"测试消息"}}'
   ```

---

### 问题7：如何停止Bot

**Windows**：
- 在CMD窗口按 `Ctrl + C`

**macOS/Linux**：
```bash
ps aux | grep legal_tech_news_bot.py
kill <进程ID>
```

---

## 7. 下一步

### ✅ 运行成功后

1. **设置为开机自启**：
   - Windows：使用任务计划程序
   - macOS：使用LaunchAgent
   - Linux：使用crontab或systemd service

2. **监控运行状态**：
   - 定期查看日志文件
   - 检查飞书是否每天收到消息

3. **优化配置**：
   - 调整推送时间
   - 修改新闻关键词
   - 增加新闻数量

### 📚 更多资源

- **完整文档**：`README.md`
- **快速指南**：`QUICKSTART.md`
- **配置测试**：`python test_config.py`
- **日志文件**：`news_bot.log`

---

## 📞 获取帮助

如果遇到问题：

1. **查看日志**：
   ```bash
   cat news_bot.log
   ```

2. **运行测试脚本**：
   ```bash
   python test_config.py
   ```

3. **查看常见问题**：
   - README.md 中的"常见问题"部分

4. **检查API状态**：
   - NewsAPI: https://newsapi.org/
   - Claude: https://console.anthropic.com/
   - 飞书开发者：https://open.feishu.cn/

---

**祝使用愉快！🎉**
