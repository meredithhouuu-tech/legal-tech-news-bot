# GLM（智谱AI）配置指南

## 为什么使用GLM？

### GLM vs Claude 对比

| 特性 | GLM-4-Flash | Claude Haiku | 免费翻译 |
|------|-------------|--------------|----------|
| **中文理解** | ⭐⭐⭐⭐⭐（国产模型） | ⭐⭐⭐⭐ | ⭐⭐ |
| **翻译质量** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **响应速度** | 快（国内服务器） | 较快 | 快 |
| **成本** | 约¥0.1/万token | $0.25/百万token | 免费 |
| **国内访问** | ✅ 稳定 | ⚠️ 可能需要代理 | ✅ 稳定 |

### GLM的优势

- ✅ **中文理解能力强** - 国产模型，对中文语境理解更好
- ✅ **价格便宜** - CODING PLAN套餐免费额度大
- ✅ **国内访问稳定** - 无需代理，速度快
- ✅ **法律专业翻译好** - 对专业术语理解准确

---

## 📋 配置步骤

### 第1步：注册智谱AI账号

1. 访问：https://open.bigmodel.cn/
2. 点击右上角 **"注册"**
3. 使用手机号注册（需要验证码）
4. 完成实名认证（需要身份证）

---

### 第2步：获取API Key

1. 登录后，进入：https://open.bigmodel.cn/usercenter/apikeys
2. 点击 **"新建API Key"**
3. 复制生成的API Key（格式：`xxx.xxxxxxxxx...`）
4. **立即保存到安全的地方**（关闭页面后无法再查看）

⚠️ **安全提示**：
- API Key相当于密码，不要泄露给他人
- 不要提交到Git仓库
- 定期更换Key

---

### 第3步：配置API Key

#### 方式A：本地运行（.env文件）

1. 复制 `.env.example` 文件
2. 重命名为 `.env`
3. 填写你的GLM API Key：

```env
# GLM API 配置
GLM_API_KEY=你的API_Key_here

# 翻译提供商（设置为glm优先使用GLM）
TRANSLATION_PROVIDER=glm

# GLM 模型（可选）
GLM_MODEL=glm-4-flash
```

4. 保存文件

#### 方式B：GitHub Actions（推荐）

1. 访问你的GitHub仓库：https://github.com/meredithhouuu-tech/legal-tech-news-bot
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **"New repository secret"**
4. 创建以下Secrets：

| Secret名称 | 值 |
|-----------|---|
| `GLM_API_KEY` | 你的GLM API Key |

5. 点击 **"Add secret"** 保存

---

### 第4步：选择GLM模型

根据你的CODING PLAN套餐选择合适的模型：

| 模型 | 适用场景 | 速度 | 价格 |
|------|---------|------|------|
| **glm-4-flash** | 日常翻译（推荐） | 最快 | 最便宜 |
| **glm-4** | 高质量翻译 | 较快 | 中等 |
| **glm-3-turbo** | 简单翻译 | 快 | 最便宜 |

**配置方法**：

在 `.env` 文件中设置：
```env
GLM_MODEL=glm-4-flash
```

或在GitHub Secrets中添加：
- Name: `GLM_MODEL`
- Value: `glm-4-flash`

---

### 第5步：测试配置

#### 本地测试

```bash
# 运行测试
python legal_tech_news_bot.py
```

查看日志输出：
```
🤖 开始使用GLM API生成Newsletter（模型：glm-4-flash）...
✅ Newsletter生成成功（使用GLM API）
```

#### GitHub Actions测试

1. 在GitHub仓库点击 **Actions** 标签
2. 选择 **"Legal Tech News Bot"** workflow
3. 点击 **"Run workflow"** → **"Run workflow"**
4. 等待执行完成，查看日志

---

## 🔧 高级配置

### 配置1：多模型切换

你可以配置多个翻译提供商，自动切换：

```env
# 优先使用GLM，如果失败自动切换到Claude
TRANSLATION_PROVIDER=glm

# 或者优先使用Claude
TRANSLATION_PROVIDER=claude
```

**自动切换逻辑**：
```
指定的provider → 没有API Key？
    ↓ 是
尝试其他可用的provider → 都没有？
    ↓ 是
使用备用方案（免费翻译）
```

### 配置2：自定义API地址

如果你使用GLM的代理或其他兼容API：

```env
# 自定义API地址
GLM_API_URL=https://your-custom-api.com/v1/chat/completions
```

### 配置3：调整输出长度

```env
# 最大token数（控制Newsletter长度）
GLM_MAX_TOKENS=2000  # 默认2000
```

---

## 💰 成本对比

### GLM-4-Flash 定价

| 套餐 | 免费额度 | 超出后价格 |
|------|---------|-----------|
| **CODING PLAN** | 25百万token/月 | ¥0.1/万token |
| **FREE PLAN** | 有限额 | 按量计费 |

### 实际使用估算

假设每天生成1次Newsletter，每次处理15条新闻：

| 项目 | Token消耗 | 每月成本 |
|------|----------|---------|
| 输入（新闻内容） | ~3000 token | - |
| 输出（Newsletter） | ~1500 token | - |
| **每日总计** | ~4500 token | - |
| **每月总计** | ~13.5万 token | **¥0（免费额度内）** |

✅ **CODING PLAN免费额度完全够用！**

---

## 🆚 翻译效果对比

### 示例：法律新闻标题

**原文**：
```
AI Legal Tech Startup Raises $10M to Transform Contract Analysis
```

**免费翻译**：
```
AI法律科技初创公司筹集1000万美元以改变合同分析
```

**Claude Haiku**：
```
AI法律科技公司融资1000万美元，革新合同分析流程
```

**GLM-4-Flash**：
```
AI法律科技初创公司获1000万美元融资，推动合同分析智能化
```

**结论**：GLM对专业术语的理解更准确，翻译更符合中文表达习惯。

---

## ❓ 常见问题

### Q1: GLM API返回401错误

**原因**：API Key错误或已失效

**解决**：
1. 检查API Key是否正确复制（包含完整的格式）
2. 访问智谱AI控制台查看Key是否有效
3. 重新生成新的API Key

### Q2: GLM API返回429错误

**原因**：请求过于频繁

**解决**：
1. 等待几分钟后重试
2. 检查是否超过了免费额度
3. 升级到付费套餐

### Q3: 翻译质量不佳

**可能原因**：
- 使用了较低端的模型（如glm-3-turbo）
- Prompt不够明确

**解决**：
```env
# 使用更强的模型
GLM_MODEL=glm-4
```

### Q4: 如何查看API使用量？

访问智谱AI控制台：https://open.bigmodel.cn/usercenter/balance

可以看到：
- 剩余token数量
- 当月已使用量
- 账户余额

### Q5: 可以同时配置Claude和GLM吗？

**可以！** 推荐配置：

```env
# 配置两个API Key
CLAUDE_API_KEY=sk-ant-xxx
GLM_API_KEY=xxx.xxx

# 设置优先级
TRANSLATION_PROVIDER=glm  # 优先使用GLM
```

**好处**：
- GLM为主力（便宜、快速）
- Claude为备份（质量高）
- 自动切换，稳定性更好

---

## ✅ 配置完成检查清单

配置完成后，请确认：

- [ ] 已注册智谱AI账号
- [ ] 已创建API Key并保存
- [ ] 已配置到.env文件或GitHub Secrets
- [ ] 已设置TRANSLATION_PROVIDER=glm
- [ ] 本地测试成功（运行看到"使用GLM API"）
- [ ] 飞书收到翻译效果更好的新闻

---

## 🎉 完成！

配置完成后，你的新闻Bot将使用GLM API生成中文简报：

- ⏰ **每天12:00准时推送**
- 🤖 **GLM智能翻译**
- 📱 **推送到飞书**
- 💰 **几乎零成本**

---

**配置成功后，记得重新生成API Key（如果刚才在对话中暴露了的话）** 🔒

有问题随时查看智谱AI文档：https://open.bigmodel.cn/dev/api
