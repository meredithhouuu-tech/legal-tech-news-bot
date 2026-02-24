#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
法律科技新闻汇总Bot
功能：每天自动抓取Legal Tech新闻，用AI整理成中文Newsletter，通过飞书推送
作者：AI Assistant
日期：2025
"""

import os        # 用于读取环境变量
import json      # 用于处理JSON数据
import time      # 用于时间处理和等待
import schedule  # 用于定时任务
import logging   # 用于日志记录
from datetime import datetime
from typing import List, Dict

import requests      # 用于HTTP请求
from dotenv import load_dotenv  # 用于加载.env配置文件
from deep_translator import GoogleTranslator  # 用于免费翻译
import feedparser      # 用于RSS解析
import re              # 用于正则表达式清理HTML
import string          # 用于字符串处理
from difflib import SequenceMatcher  # 用于计算字符串相似度

# ====================== 配置日志系统 ======================
# 日志会输出到文件和控制台，方便调试
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('news_bot.log', encoding='utf-8'),  # 输出到文件
        logging.StreamHandler()  # 输出到控制台
    ]
)
logger = logging.getLogger(__name__)


# ====================== 配置管理 ======================
class Config:
    """配置类：统一管理所有配置项"""

    def __init__(self):
        """加载.env文件中的配置"""
        # 加载.env文件
        load_dotenv()

        # ========== 必需配置 ==========
        # NewsAPI配置
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.news_api_url = 'https://newsapi.org/v2/everything'
        # NewsAPI免费版限制：每天最多100次请求
        self.news_api_daily_limit = 100  # 免费版每日限制
        self.news_api_request_count = 0  # 当日已使用次数

        # Claude API配置
        self.claude_api_key = os.getenv('CLAUDE_API_KEY')
        self.claude_api_url = 'https://api.anthropic.com/v1/messages'
        # Claude Haiku价格：约$0.25/百万输入token，$1.25/百万输出token
        self.claude_max_tokens = 2000  # 每次请求最大token数

        # GLM API配置（智谱AI）
        self.glm_api_key = os.getenv('GLM_API_KEY')
        self.glm_api_url = os.getenv('GLM_API_URL', 'https://open.bigmodel.cn/api/paas/v4/chat/completions')
        self.glm_model = os.getenv('GLM_MODEL', 'glm-4-flash')  # 默认使用glm-4-flash（快速且便宜）
        self.glm_max_tokens = int(os.getenv('GLM_MAX_TOKENS', '2000'))
        # 翻译优先级：claude > glm > fallback
        self.translation_provider = os.getenv('TRANSLATION_PROVIDER', 'claude').lower()  # claude/glm/fallback

        # 飞书机器人配置
        self.feishu_webhook = os.getenv('FEISHU_WEBHOOK_URL')

        # ========== 可选配置 ==========
        # 新闻搜索关键词（英文）
        self.search_keywords = os.getenv('SEARCH_KEYWORDS',
                                       'legal tech OR legal technology OR lawtech OR legal AI')

        # 中文新闻搜索关键词（用于获取国内新闻）
        self.search_keywords_cn = os.getenv('SEARCH_KEYWORDS_CN',
                                           '法律科技 OR 法律AI OR 法务AI OR 智能法务 OR 法律大模型 OR 法律人工智能')

        # 运行模式：test（测试模式，立即执行一次）或 production（生产模式，定时运行）
        self.run_mode = os.getenv('RUN_MODE', 'production').lower()

        # 是否启用备用方案（当Claude API失败时）
        self.enable_fallback = os.getenv('ENABLE_FALLBACK', 'true').lower() == 'true'

        # 新闻数量限制
        self.max_articles = int(os.getenv('MAX_ARTICLES', '15'))

        # ========== RSS新闻源配置 ==========

        # ---------- 法律科技专业源 ----------
        # 1. Google News RSS（多语言，基于关键词搜索）
        self.rss_google_news = 'https://news.google.com/rss/search?q=legal+tech+OR+legal+AI+OR+法律科技&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'

        # 2. JDSupra Legal Tech RSS（英文，科技相关法律新闻）
        self.rss_jdsupra = 'https://www.jdsupra.com/resources/syndication/docsRSSfeed.aspx?ftype=ScienceComputersTechnology&premium=1'

        # 3. Artificial Lawyer RSS（英文，法律AI专业博客）
        self.rss_artificial_lawyer = 'https://www.artificiallawyer.com/feed/'

        # 4. Above the Law RSS（英文，法律新闻）
        self.rss_above_the_law = 'https://abovethelaw.com/feed/'

        # 5. TechLaw RSS（英文，法律科技）
        self.rss_techlaw = 'https://feeds.feedburner.com/techlaw'

        # ---------- 国内科技媒体源（法律+AI） ----------
        # 6. 36氪 - 人工智能频道
        self.rss_36kr_ai = 'https://36kr.com/api/channel/1011/kr-column-list?per_page=20'

        # 7. 虎嗅网 - 科技频道
        self.rss_huxiu = 'https://www.huxiu.com/rss/0.xml'

        # 8. 钛媒体 - 科技频道
        self.rss_ttm = 'https://www.tmtpost.com/rss/caijing.xml'

        # 9. InfoQ 中文 - AI频道
        self.rss_infoq = 'https://www.infoq.cn/feed'

        # 10. 极客公园 - 科技资讯
        self.rss_geekpark = 'https://www.geekpark.net/rss'

        # ---------- AI专业媒体源 ----------
        # 11. 量子位 - 国内AI专业媒体
        self.rss_qbitai = 'https://www.qbitai.com/feed'

        # 12. 机器之心 - AI专业媒体
        self.rss_jiqizhixin = 'https://www.jiqizhixin.com/rss'

        # 13. 新智元 - AI资讯
        self.rss_aiyuan = 'https://www.ai-yuan.com/feed'

        # ---------- 国外AI权威源 ----------
        # 14. TechCrunch AI
        self.rss_techcrunch_ai = 'https://techcrunch.com/category/artificial-intelligence/feed/'

        # 15. The Verge AI
        self.rss_verge_ai = 'https://www.theverge.com/ai-artificial-intelligence/rss/index.xml'

        # 验证必需的配置项
        self._validate_config()
        self._log_api_limits()

    def _validate_config(self):
        """验证所有必需的配置是否存在"""
        required_configs = {
            'NEWS_API_KEY': self.news_api_key,
            'FEISHU_WEBHOOK_URL': self.feishu_webhook
        }

        # Claude API密钥是可选的，如果没有则使用简单格式
        optional_configs = {
            'CLAUDE_API_KEY': self.claude_api_key
        }

        missing_configs = [name for name, value in required_configs.items() if not value]

        if missing_configs:
            raise ValueError(
                f"缺少必需的配置项: {', '.join(missing_configs)}\n"
                f"请在.env文件中配置这些项"
            )

        logger.info("✅ 配置验证通过")
        logger.info(f"📊 运行模式: {self.run_mode}")

        # 提示Claude API状态
        if not self.claude_api_key:
            logger.info("💡 未配置Claude API，将使用简单格式（英文原新闻）")
        else:
            logger.info("✅ 已配置Claude API，将生成中文Newsletter")

    def _log_api_limits(self):
        """记录API限制信息"""
        logger.info("\n" + "=" * 60)
        logger.info("📋 API限制说明")
        logger.info("=" * 60)
        logger.info(f"NewsAPI: 免费版每天最多 {self.news_api_daily_limit} 次请求")

        if self.claude_api_key:
            logger.info(f"Claude API: Haiku模型，约$0.25/百万输入token")
            logger.info(f"当前配置: 最大{self.claude_max_tokens} tokens/次")
        else:
            logger.info("Claude API: 未配置（使用免费简单格式）")

        logger.info(f"备用方案: {'✅ 已启用' if self.enable_fallback else '❌ 已禁用'}")
        logger.info("=" * 60 + "\n")


# ====================== 多源新闻获取模块 ======================
class NewsFetcher:
    """新闻获取类：从多个来源（NewsAPI + RSS）获取法律科技新闻"""

    def __init__(self, config: Config):
        """
        初始化新闻获取器
        :param config: 配置对象
        """
        self.config = config
        self.session = requests.Session()  # 使用Session可以提高HTTP请求效率

    def _fetch_from_rss(self, rss_url: str, source_name: str, max_items: int = 10) -> List[Dict]:
        """
        从RSS源获取新闻
        :param rss_url: RSS链接
        :param source_name: 源名称（用于日志）
        :param max_items: 最大获取数量
        :return: 新闻列表
        """
        articles = []
        try:
            logger.info(f"📡 正在获取 {source_name} RSS...")
            feed = feedparser.parse(rss_url)

            if feed.bozo:
                logger.warning(f"⚠️ {source_name} RSS解析可能有误: {feed.bozo_exception}")

            if not feed.entries:
                logger.warning(f"⚠️ {source_name} RSS没有返回任何内容")
                return articles

            # 解析RSS条目
            for entry in feed.entries[:max_items]:
                # 提取发布时间
                published_at = ''
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    try:
                        published_at = datetime(*entry.published_parsed[:6]).isoformat()
                    except:
                        pass
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    try:
                        published_at = datetime(*entry.updated_parsed[:6]).isoformat()
                    except:
                        pass

                # 构建标准化的新闻格式
                # 清理description中的HTML标签
                description_raw = entry.get('description', '')
                title_raw = entry.get('title', '无标题')

                # 清理HTML标签和多余空格
                description_clean = re.sub(r'<[^>]+>', '', description_raw)
                description_clean = re.sub(r'\s+', ' ', description_clean).strip()

                # 如果description为空或与标题相同，尝试从content中获取
                if not description_clean or description_clean.lower() == title_raw.lower():
                    if hasattr(entry, 'content') and entry.get('content'):
                        content_raw = entry.get('content', [{}])[0].get('value', '')
                        description_clean = re.sub(r'<[^>]+>', '', content_raw)
                        description_clean = re.sub(r'\s+', ' ', description_clean).strip()

                        # 限制长度（取前200个字符）
                        if len(description_clean) > 200:
                            description_clean = description_clean[:200] + '...'

                    # 如果content也没有或者还是和标题一样，就留空
                    if not description_clean or description_clean.lower() == title_raw.lower():
                        description_clean = ''

                article = {
                    'title': title_raw,
                    'description': description_clean,
                    'url': entry.get('link', ''),
                    'source': {'name': source_name},
                    'publishedAt': published_at,
                    'content': entry.get('content', [{}])[0].get('value', '') if hasattr(entry, 'content') else ''
                }
                articles.append(article)

            logger.info(f"✅ {source_name} RSS获取 {len(articles)} 条")

        except Exception as e:
            logger.error(f"❌ 获取 {source_name} RSS失败: {e}")

        return articles

    def fetch_legal_tech_news(self) -> List[Dict]:
        """
        从多个来源（5个RSS + NewsAPI）获取法律科技新闻
        :return: 新闻列表，每条新闻包含标题、描述、URL、来源等
        """
        logger.info("🔍 开始获取法律科技新闻（多源模式）...")

        all_articles = []

        # ========== 第一步：从5个RSS源获取新闻（免费，无限制）==========
        logger.info("\n" + "=" * 60)
        logger.info("📡 开始获取RSS新闻源（5个源）...")
        logger.info("=" * 60)

        # 1. Google News RSS
        google_news_articles = self._fetch_from_rss(
            self.config.rss_google_news,
            'Google News',
            max_items=20
        )
        all_articles.extend(google_news_articles)

        # 2. JDSupra Legal Tech RSS
        jdsupra_articles = self._fetch_from_rss(
            self.config.rss_jdsupra,
            'JDSupra Legal Tech',
            max_items=20
        )
        all_articles.extend(jdsupra_articles)

        # 3. Artificial Lawyer RSS
        artificial_lawyer_articles = self._fetch_from_rss(
            self.config.rss_artificial_lawyer,
            'Artificial Lawyer',
            max_items=20
        )
        all_articles.extend(artificial_lawyer_articles)

        # 4. Above the Law RSS
        above_the_law_articles = self._fetch_from_rss(
            self.config.rss_above_the_law,
            'Above the Law',
            max_items=20
        )
        all_articles.extend(above_the_law_articles)

        # 5. TechLaw RSS
        techlaw_articles = self._fetch_from_rss(
            self.config.rss_techlaw,
            'TechLaw',
            max_items=10
        )
        all_articles.extend(techlaw_articles)

        logger.info(f"\n✅ 法律科技RSS源共获取 {len(all_articles)} 条新闻")

        # ========== 第二步：获取国内科技媒体新闻 ==========
        logger.info("\n" + "=" * 60)
        logger.info("📡 开始获取国内科技媒体新闻（5个源）...")
        logger.info("=" * 60)

        # 6. 虎嗅网
        huxiu_articles = self._fetch_from_rss(
            self.config.rss_huxiu,
            '虎嗅网',
            max_items=15
        )
        all_articles.extend(huxiu_articles)

        # 7. 钛媒体
        ttm_articles = self._fetch_from_rss(
            self.config.rss_ttm,
            '钛媒体',
            max_items=15
        )
        all_articles.extend(ttm_articles)

        # 8. InfoQ 中文
        infoq_articles = self._fetch_from_rss(
            self.config.rss_infoq,
            'InfoQ',
            max_items=15
        )
        all_articles.extend(infoq_articles)

        # 9. 极客公园
        geekpark_articles = self._fetch_from_rss(
            self.config.rss_geekpark,
            '极客公园',
            max_items=10
        )
        all_articles.extend(geekpark_articles)

        logger.info(f"\n✅ 国内科技媒体共获取 {len(all_articles)} 条新闻")

        # ========== 第三步：获取AI专业媒体新闻 ==========
        logger.info("\n" + "=" * 60)
        logger.info("🤖 开始获取AI专业媒体新闻（5个源）...")
        logger.info("=" * 60)

        # 10. 量子位
        qbitai_articles = self._fetch_from_rss(
            self.config.rss_qbitai,
            '量子位',
            max_items=20
        )
        all_articles.extend(qbitai_articles)

        # 11. 机器之心
        jiqizhixin_articles = self._fetch_from_rss(
            self.config.rss_jiqizhixin,
            '机器之心',
            max_items=20
        )
        all_articles.extend(jiqizhixin_articles)

        # 12. 新智元
        aiyuan_articles = self._fetch_from_rss(
            self.config.rss_aiyuan,
            '新智元',
            max_items=15
        )
        all_articles.extend(aiyuan_articles)

        # 13. TechCrunch AI
        techcrunch_ai_articles = self._fetch_from_rss(
            self.config.rss_techcrunch_ai,
            'TechCrunch AI',
            max_items=15
        )
        all_articles.extend(techcrunch_ai_articles)

        # 14. The Verge AI
        verge_ai_articles = self._fetch_from_rss(
            self.config.rss_verge_ai,
            'The Verge AI',
            max_items=10
        )
        all_articles.extend(verge_ai_articles)

        logger.info(f"\n✅ AI专业媒体共获取 {len(all_articles)} 条新闻")

        # ========== 第四步：从NewsAPI获取新闻（补充）==========
        logger.info("\n" + "=" * 60)
        logger.info("📰 开始获取NewsAPI新闻...")
        logger.info("=" * 60)

        # 检查API配额
        self.config.news_api_request_count += 1
        remaining_requests = self.config.news_api_daily_limit - self.config.news_api_request_count

        if remaining_requests <= 0:
            logger.warning(f"⚠️ NewsAPI配额已用完，仅使用RSS源")
        elif remaining_requests <= 10:
            logger.warning(f"⚠️ NewsAPI配额即将用尽：剩余 {remaining_requests}/{self.config.news_api_daily_limit} 次")

        try:
            # 计算日期范围（前3天）
            from datetime import timedelta
            from_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
            today = datetime.now().strftime('%Y-%m-%d')
            logger.info(f"📅 搜索日期范围: {from_date} 至 {today}（近3天）")

            # 构建搜索关键词
            precise_keywords = 'legal tech OR legaltech OR legal AI OR law technology OR 法律科技 OR 法律AI'
            logger.info(f"🔑 搜索关键词: {precise_keywords}")

            # 构建API请求参数
            params = {
                'q': precise_keywords,
                'sortBy': 'relevance',
                'from': from_date,
                'to': today,
                'pageSize': 20,  # 获取20条用于补充
                'apiKey': self.config.news_api_key
            }

            # 发送API请求
            response = self.session.get(self.config.news_api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 'ok':
                newsapi_articles = data.get('articles', [])
                all_articles.extend(newsapi_articles)
                logger.info(f"✅ NewsAPI获取 {len(newsapi_articles)} 条新闻")

        except Exception as e:
            logger.warning(f"⚠️ NewsAPI获取失败: {e}，继续使用RSS源")

        # ========== 第三步：智能去重（URL + 标题相似度）==========
        logger.info("\n" + "=" * 60)
        logger.info("🔍 开始智能去重...")
        logger.info("=" * 60)

        def is_similar_title(title1, title2):
            """判断两个标题是否相似（避免重复新闻）"""
            if not title1 or not title2:
                return False

            # 清理标题
            t1 = title1.lower().strip()
            t2 = title2.lower().strip()

            # 完全相同
            if t1 == t2:
                return True

            # 一个标题是另一个的子集（超过80%相似度）
            if len(t1) > 0 and len(t2) > 0:
                if t1 in t2 or t2 in t1:
                    # 检查长度相似度
                    ratio = min(len(t1), len(t2)) / max(len(t1), len(t2))
                    if ratio >= 0.8:  # 80%以上相似
                        return True

            return False

        # 第一层去重：URL去重
        seen_urls = set()
        unique_by_url = []
        for article in all_articles:
            url = article.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_by_url.append(article)

        logger.info(f"✅ URL去重后剩余 {len(unique_by_url)} 条新闻")

        # 第二层去重：标题相似度去重
        unique_articles = []
        seen_titles = []

        for article in unique_by_url:
            title = article.get('title', '')
            is_duplicate = False

            # 检查是否与已见过的标题相似
            for seen_title in seen_titles:
                if is_similar_title(title, seen_title):
                    is_duplicate = True
                    logger.debug(f"🔄 发现相似标题，已去重: {title[:50]}...")
                    break

            if not is_duplicate:
                seen_titles.append(title)
                unique_articles.append(article)

        removed_count = len(unique_by_url) - len(unique_articles)
        if removed_count > 0:
            logger.info(f"✅ 标题相似度去重：移除 {removed_count} 条重复新闻")

        logger.info(f"✅ 最终去重后剩余 {len(unique_articles)} 条新闻")

        # ========== 第五步：智能评分排序（来源权重 + 相关性评分）+ 新闻分类 ==========
        logger.info("🎯 开始智能评分排序和分类...")

        # 定义来源权重
        source_weights = {
            # 法律科技专业源
            'Artificial Lawyer': 3.0,
            'JDSupra Legal Tech': 3.0,
            'Above the Law': 2.0,
            'Law.com': 2.0,
            'LegalTechnology.News': 2.5,
            'TechLaw': 2.0,
            # AI专业媒体（高权重）
            '量子位': 3.0,
            '机器之心': 3.0,
            '新智元': 2.8,
            'TechCrunch AI': 2.5,
            'The Verge AI': 2.5,
            # 国内科技媒体
            '虎嗅网': 1.8,
            '钛媒体': 1.8,
            'InfoQ': 1.8,
            '极客公园': 1.5,
            '36氪': 1.5,
            # 通用新闻
            'Google News': 1.5,
            'Business Insider': 1.0,
            'TechCrunch': 1.0,
            'Forbes': 1.0,
        }

        # ========== 法律科技关键词 ==========
        legal_tech_keywords = [
            'legal ai', 'legal artificial intelligence', '法律ai', '法律AI', '法律人工智能'
        ]

        legal_tech_secondary = [
            'legal tech', 'legal technology', 'legaltech', 'lawtech',
            'law tech', 'law technology', '法律科技',
            'legal automation', 'contract AI', 'e-discovery', 'document automation'
        ]

        # ========== AI重大新闻关键词（国内 + 国外）==========
        # 国内AI公司和产品
        ai_major_domestic = [
            # 大模型产品
            'kimi', '月之暗面', 'moonshot',
            'chatglm', '智谱ai', '智谱AI', 'zhipu',
            '文心一言', 'ernie bot', '百度ai', 'paddlepaddle',
            '通义千问', 'qwen', '阿里ai', '通义',
            '混元', 'hunyuan', '腾讯ai',
            '星火', '讯飞ai', 'iflytek',
            '豆包', '字节ai', '字节跳动ai',
            '百川智能', 'baichuan',
            '零一万物', '01ai', 'yi模型',
            '深度求索', 'deepseek',
            '面壁智能', 'cpm',
            'minimax',
            # 开源模型
            '开源大模型', '开源llm', '开源模型',
            '世界模型', 'world model',
            # AI公司动态
            '发布', '上线', '推出', '开源', '更新',
            # AI技术和应用
            'gpt-4', 'gpt4', 'claude', 'anthropic',
            'gemini', 'llama', 'meta ai', 'grok',
            'sora', 'midjourney', 'stable diffusion',
            'chatgpt', 'openai',
        ]

        # AI技术关键词
        ai_tech_keywords = [
            '大模型', 'llm', '大型语言模型',
            'aigc', '生成式ai', 'generative ai',
            'transformer', 'attention机制',
            '多模态', '视觉模型', '语音模型',
            'agent', 'ai代理', '智能体',
            'rag', '检索增强生成',
            '微调', 'fine-tuning', '训练',
        ]

        # 合并所有关键词（用于筛选）
        all_keywords = legal_tech_keywords + legal_tech_secondary + ai_major_domestic + ai_tech_keywords

        def calculate_relevance_score(article):
            """计算单条新闻的相关性得分"""
            score = 0
            title = str(article.get('title') or '').lower()
            description = str(article.get('description') or '').lower()
            source = article.get('source', {}).get('name', '') or ''

            # 1. 来源权重（0-30分）
            source_weight = source_weights.get(source, 1.0)
            score += source_weight * 10

            # 2. 关键词匹配得分
            # 检查标题中的关键词匹配
            for keyword in all_keywords:
                if keyword in title:
                    # 法律科技核心关键词
                    if keyword in legal_tech_keywords:
                        score += 60  # 最高优先级
                    # AI重大新闻关键词
                    elif keyword in ai_major_domestic:
                        score += 55  # 高优先级
                    # 法律科技次要关键词
                    elif keyword in legal_tech_secondary:
                        score += 45
                    # AI技术关键词
                    elif keyword in ai_tech_keywords:
                        score += 40
                    else:
                        score += 20

                    # 关键词在标题开头（前50个字符）
                    if len(title) > 0 and keyword in title[:50]:
                        score += 10

            # 检查描述中的关键词匹配
            desc_keyword_count = sum(1 for kw in all_keywords if kw in description)
            score += desc_keyword_count * 5  # 每个关键词+5分

            # 3. 时间新鲜度得分（0-20分）
            pub_time = article.get('publishedAt', '')
            if pub_time:
                try:
                    from datetime import timezone, timedelta
                    dt = datetime.fromisoformat(pub_time.replace('Z', '+00:00'))
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)

                    now = datetime.now(timezone.utc)
                    time_diff = (now - dt).total_seconds() / 3600  # 小时

                    if time_diff <= 24:
                        score += 20  # 24小时内
                    elif time_diff <= 48:
                        score += 10  # 48小时内
                    elif time_diff <= 168:  # 7天
                        score += 5
                except:
                    pass

            return score

        def classify_article(article):
            """将新闻分类为：法律科技新闻、AI重大新闻、或其他"""
            title = str(article.get('title') or '').lower()
            description = str(article.get('description') or '').lower()

            # 检查是否包含法律科技关键词
            has_legal_tech = any(kw in title or kw in description for kw in legal_tech_keywords + legal_tech_secondary)

            # 检查是否包含AI重大新闻关键词
            has_ai_major = any(kw in title or kw in description for kw in ai_major_domestic + ai_tech_keywords)

            if has_legal_tech and has_ai_major:
                return 'both'  # 两者都是
            elif has_legal_tech:
                return 'legal_tech'
            elif has_ai_major:
                return 'ai_major'
            else:
                return 'other'

        # 为每条新闻计算得分、分类并保留通过基本筛选的
        scored_articles = []
        for article in unique_articles:
            title = str(article.get('title') or '').lower()
            description = str(article.get('description') or '').lower()
            pub_time = article.get('publishedAt', '')

            # 时间筛选：只保留3天内的新闻
            is_recent = True
            if pub_time:
                try:
                    from datetime import timezone, timedelta
                    dt = datetime.fromisoformat(pub_time.replace('Z', '+00:00'))
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)

                    now = datetime.now(timezone.utc)
                    time_diff = (now - dt).total_seconds() / 86400  # 转换为天数

                    if time_diff > 3:  # 超过3天
                        is_recent = False
                except:
                    pass

            if not is_recent:
                continue  # 跳过超过3天的新闻

            # 基本筛选：必须包含至少一个关键词
            contains_keyword = any(
                kw in title or kw in description
                for kw in all_keywords
            )

            if contains_keyword:
                score = calculate_relevance_score(article)
                category = classify_article(article)
                article['_score'] = score
                article['_category'] = category
                scored_articles.append(article)

        # 按得分排序（从高到低）
        scored_articles.sort(key=lambda x: x.get('_score', 0), reverse=True)

        logger.info(f"✅ 评分后剩余 {len(scored_articles)} 条精准新闻")

        # 统计分类
        legal_tech_count = sum(1 for a in scored_articles if a.get('_category') in ['legal_tech', 'both'])
        ai_major_count = sum(1 for a in scored_articles if a.get('_category') in ['ai_major', 'both'])
        both_count = sum(1 for a in scored_articles if a.get('_category') == 'both')

        logger.info(f"📊 新闻分类统计：")
        logger.info(f"   • 法律科技新闻：{legal_tech_count} 条")
        logger.info(f"   • AI重大新闻：{ai_major_count} 条")
        if both_count > 0:
            logger.info(f"   • 两者重叠：{both_count} 条")

        # 显示得分最高的前3条新闻
        if scored_articles:
            logger.info("\n🏆 得分最高的新闻预览:")
            for i, article in enumerate(scored_articles[:3], 1):
                score = article.get('_score', 0)
                title = article.get('title', '无标题')[:50]
                source = article.get('source', {}).get('name', '未知')
                category = article.get('_category', 'unknown')
                logger.info(f"   {i}. [{score}分] [{category}] {source}: {title}...")

        # ========== 第六步：处理无新闻的情况 ==========
        if len(scored_articles) == 0:
            logger.warning("⚠️ 今日暂无精准的法律科技/AI相关新闻")
            return [{
                'no_news_message': '今日暂无精准的法律科技/AI相关新闻'
            }]

        # ========== 第七步：取前N条（按综合得分排序）==========
        final_articles = scored_articles[:self.config.max_articles]
        logger.info(f"🎯 最终选取 {len(final_articles)} 条新闻（按综合得分排序）")

        # 保留分类信息
        for article in final_articles:
            if '_category' not in article:
                article['_category'] = classify_article(article)

        # 显示来源分布
        source_count = {}
        for article in final_articles:
            source = article.get('source', {}).get('name', '未知')
            source_count[source] = source_count.get(source, 0) + 1

        logger.info("\n📊 新闻来源分布:")
        for source, count in source_count.items():
            logger.info(f"   • {source}: {count} 条")

        return final_articles


# ====================== Claude AI 内容生成模块 ======================
class NewsletterGenerator:
    """Newsletter生成类：使用Claude API将新闻整理成中文格式"""

    def __init__(self, config: Config):
        """
        初始化Newsletter生成器
        :param config: 配置对象
        """
        self.config = config
        self.session = requests.Session()

    def generate_newsletter(self, articles: List[Dict]) -> str:
        """
        使用Claude API生成中文Newsletter
        :param articles: 新闻列表
        :return: 格式化后的中文Newsletter文本
        """
        # ========== 检查是否有"无新闻"的标记 ==========
        if not articles:
            logger.warning("⚠️ 没有新闻可供整理")
            return "今日暂无法律科技相关新闻"

        # 检查是否是无精准新闻的特殊标记
        if len(articles) == 1 and 'no_news_message' in articles[0]:
            logger.info("📭 今日暂无精准新闻，使用提示信息")
            date_str = datetime.now().strftime('%Y年%m月%d日')
            return f"""📰 法律科技日报 - {date_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📭 {articles[0]['no_news_message']}

💡 提示：今日没有找到符合标准的法律科技/法律AI相关新闻。这可能是由于：
  • 当天相关新闻发布较少
  • 新闻来源未覆盖所有渠道
  • 关键词匹配需要进一步优化

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 由法律科技新闻Bot自动推送"""

        # 根据配置选择翻译提供商
        provider = self.config.translation_provider

        logger.info(f"📋 当前配置的翻译提供商: {provider}")
        logger.info(f"📋 GLM API Key状态: {'已配置' if self.config.glm_api_key else '未配置'}")
        logger.info(f"📋 Claude API Key状态: {'已配置' if self.config.claude_api_key else '未配置'}")

        # 如果指定的provider没有API Key，尝试使用其他可用的
        if provider == 'claude' and not self.config.claude_api_key:
            if self.config.glm_api_key:
                logger.info("💡 Claude API未配置，切换到GLM API")
                provider = 'glm'
            else:
                logger.error("❌ Claude和GLM API都未配置，使用备用方案")
                return self._fallback_newsletter(articles)
        elif provider == 'glm' and not self.config.glm_api_key:
            if self.config.claude_api_key:
                logger.info("💡 GLM API未配置，切换到Claude API")
                provider = 'claude'
            else:
                logger.error("❌ GLM和Claude API都未配置，使用备用方案")
                logger.error("❌ 请检查GitHub Secrets中是否配置了GLM_API_KEY或CLAUDE_API_KEY")
                return self._fallback_newsletter(articles)

        logger.info(f"✅ 将使用 {provider.upper()} API 生成Newsletter")
        # 使用选定的provider生成Newsletter
        if provider == 'glm':
            return self._call_glm_api(articles)
        else:  # claude
            return self._call_claude_api(articles)

    def _call_claude_api(self, articles: List[Dict]) -> str:
        """
        使用Claude API生成中文Newsletter
        :param articles: 新闻列表
        :return: 格式化后的中文Newsletter文本
        """
        logger.info("🤖 开始使用Claude API生成Newsletter...")

        # 检查是否启用备用方案
        if not self.config.enable_fallback:
            logger.info("📌 备用方案已禁用，仅使用Claude API")

        try:
            # 构建发送给Claude的新闻摘要
            news_summary = self._prepare_news_summary(articles)

            # 构建Claude API请求
            headers = {
                'x-api-key': self.config.claude_api_key,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json'
            }

            # Claude API请求体
            payload = {
                'model': 'claude-3-5-haiku-20241022',  # 使用Haiku模型，成本低
                'max_tokens': self.config.claude_max_tokens,  # 最大返回token数
                'messages': [{
                    'role': 'user',
                    'content': self._build_prompt(news_summary, 'Claude')
                }]
            }

            # 发送请求到Claude API
            response = self.session.post(
                self.config.claude_api_url,
                headers=headers,
                json=payload,
                timeout=30  # 30秒超时
            )

            # 检查响应状态
            response.raise_for_status()

            # 解析响应
            result = response.json()
            newsletter_content = result['content'][0]['text']

            # 强制修正落款：使用正则表达式匹配并替换最后的落款行
            import re
            # 匹配各种可能的落款格式
            patterns_to_replace = [
                r'🤖 由法律科技新闻Bot自动推送（使用备用翻译方案）',
                r'🤖 由法律科技新闻Bot自动推送（使用免费翻译）',
                r'🤖 由法律科技新闻Bot自动推送（使用本地翻译）',
                r'🤖 由法律科技新闻Bot自动推送$',
            ]
            correct_signature = '🤖 由法律科技新闻Bot自动推送（使用Claude API翻译）'

            # 尝试匹配并替换
            for pattern in patterns_to_replace:
                newsletter_content = re.sub(pattern, correct_signature, newsletter_content, flags=re.MULTILINE)

            # 如果没有找到任何落款，在末尾添加正确的落款
            if '由法律科技新闻Bot自动推送' not in newsletter_content:
                newsletter_content = newsletter_content.rstrip() + '\n\n' + correct_signature

            logger.info("✅ Newsletter生成成功（使用Claude API）")
            return newsletter_content

        except requests.exceptions.HTTPError as e:
            logger.error(f"❌ Claude API请求失败: {e}")
            if e.response.status_code == 401:
                logger.error("💡 提示：请检查CLAUDE_API_KEY是否正确")
            elif e.response.status_code == 429:
                logger.error("💡 提示：请求过于频繁，请稍后再试")
            elif e.response.status_code == 400:
                logger.error("💡 提示：请求参数错误或API余额不足")

            # 使用备用方案
            if self.config.enable_fallback:
                logger.info("🔄 自动切换到备用方案...")
                return self._fallback_newsletter(articles)
            else:
                logger.error("❌ 备用方案已禁用，无法生成Newsletter")
                return "抱歉，Newsletter生成失败，且备用方案已禁用"

        except requests.exceptions.Timeout:
            logger.error("❌ Claude API请求超时")
            if self.config.enable_fallback:
                logger.info("🔄 自动切换到备用方案...")
                return self._fallback_newsletter(articles)
            else:
                return "抱歉，API请求超时，且备用方案已禁用"

        except Exception as e:
            logger.error(f"❌ Newsletter生成失败: {e}")
            if self.config.enable_fallback:
                logger.info("🔄 自动切换到备用方案...")
                return self._fallback_newsletter(articles)
            else:
                return "抱歉，Newsletter生成失败，且备用方案已禁用"

    def _call_glm_api(self, articles: List[Dict]) -> str:
        """
        使用GLM API（智谱AI）生成中文Newsletter
        :param articles: 新闻列表
        :return: 格式化后的中文Newsletter文本
        """
        logger.info(f"🤖 开始使用GLM API生成Newsletter（模型：{self.config.glm_model}）...")

        # 检查是否启用备用方案
        if not self.config.enable_fallback:
            logger.info("📌 备用方案已禁用，仅使用GLM API")

        try:
            # 构建发送给GLM的新闻摘要
            news_summary = self._prepare_news_summary(articles)

            # 构建GLM API请求
            headers = {
                'Authorization': f'Bearer {self.config.glm_api_key}',
                'Content-Type': 'application/json'
            }

            # GLM API请求体
            payload = {
                'model': self.config.glm_model,
                'max_tokens': self.config.glm_max_tokens,
                'messages': [{
                    'role': 'user',
                    'content': self._build_prompt(news_summary, 'GLM')
                }]
            }

            # 发送请求到GLM API
            response = self.session.post(
                self.config.glm_api_url,
                headers=headers,
                json=payload,
                timeout=30  # 30秒超时
            )

            # 检查响应状态
            response.raise_for_status()

            # 解析响应
            result = response.json()
            newsletter_content = result['choices'][0]['message']['content']

            # 🔍 调试日志：输出GLM API返回的原始内容（最后500字符）
            logger.info(f"🔍 GLM API返回内容（末尾500字符）:\n{newsletter_content[-500:]}")

            # 强制修正落款：使用正则表达式匹配并替换最后的落款行
            import re
            # 匹配各种可能的落款格式
            patterns_to_replace = [
                r'🤖 由法律科技新闻Bot自动推送（使用备用翻译方案）',
                r'🤖 由法律科技新闻Bot自动推送（使用免费翻译）',
                r'🤖 由法律科技新闻Bot自动推送（使用本地翻译）',
                r'🤖 由法律科技新闻Bot自动推送$',
            ]
            correct_signature = '🤖 由法律科技新闻Bot自动推送（使用GLM API翻译）'

            # 🔍 调试日志：检查原始内容中是否包含错误落款
            for pattern in patterns_to_replace:
                if re.search(pattern, newsletter_content, re.MULTILINE):
                    logger.warning(f"⚠️ 发现错误落款，正则匹配: {pattern}")

            # 尝试匹配并替换
            for pattern in patterns_to_replace:
                newsletter_content = re.sub(pattern, correct_signature, newsletter_content, flags=re.MULTILINE)

            # 如果没有找到任何落款，在末尾添加正确的落款
            if '由法律科技新闻Bot自动推送' not in newsletter_content:
                logger.warning("⚠️ 未找到任何落款，将在末尾添加")
                newsletter_content = newsletter_content.rstrip() + '\n\n' + correct_signature

            # 🔍 调试日志：输出修正后的内容（最后500字符）
            logger.info(f"🔍 修正后的内容（末尾500字符）:\n{newsletter_content[-500:]}")

            logger.info("✅ Newsletter生成成功（使用GLM API）")
            return newsletter_content

        except requests.exceptions.HTTPError as e:
            logger.error(f"❌ GLM API请求失败: {e}")
            if e.response.status_code == 401:
                logger.error("💡 提示：请检查GLM_API_KEY是否正确")
            elif e.response.status_code == 429:
                logger.error("💡 提示：请求过于频繁，请稍后再试")
            elif e.response.status_code == 400:
                logger.error("💡 提示：请求参数错误或API余额不足")
                # 尝试解析错误信息
                try:
                    error_detail = e.response.json()
                    logger.error(f"📋 错误详情：{error_detail}")
                except:
                    pass

            # 使用备用方案
            if self.config.enable_fallback:
                logger.info("🔄 自动切换到备用方案...")
                return self._fallback_newsletter(articles)
            else:
                logger.error("❌ 备用方案已禁用，无法生成Newsletter")
                return "抱歉，Newsletter生成失败，且备用方案已禁用"

        except requests.exceptions.Timeout:
            logger.error("❌ GLM API请求超时")
            if self.config.enable_fallback:
                logger.info("🔄 自动切换到备用方案...")
                return self._fallback_newsletter(articles)
            else:
                return "抱歉，API请求超时，且备用方案已禁用"

        except Exception as e:
            logger.error(f"❌ Newsletter生成失败: {e}")
            if self.config.enable_fallback:
                logger.info("🔄 自动切换到备用方案...")
                return self._fallback_newsletter(articles)
            else:
                return "抱歉，Newsletter生成失败，且备用方案已禁用"

    def _prepare_news_summary(self, articles: List[Dict]) -> str:
        """
        将新闻列表格式化为文本摘要，按分类组织
        :param articles: 新闻列表
        :return: 格式化的文本摘要
        """
        # 按分类整理新闻
        legal_tech_articles = []
        ai_major_articles = []
        other_articles = []

        for article in articles:
            category = article.get('_category', 'other')
            if category == 'legal_tech':
                legal_tech_articles.append(article)
            elif category == 'ai_major':
                ai_major_articles.append(article)
            elif category == 'both':
                # 两者都有的，优先放到法律科技类
                legal_tech_articles.append(article)
            else:
                other_articles.append(article)

        summary_lines = []

        # 第一部分：法律科技新闻
        if legal_tech_articles:
            summary_lines.append("【法律科技新闻】")
            for i, article in enumerate(legal_tech_articles[:10], 1):
                title = article.get('title', '无标题')
                description = article.get('description', '无描述')
                url = article.get('url', '')
                source = article.get('source', {}).get('name', '未知来源')
                published_at = article.get('publishedAt', '')

                summary_lines.append(
                    f"{i}. 标题: {title}\n"
                    f"   来源: {source}\n"
                    f"   描述: {description}\n"
                    f"   链接: {url}\n"
                )

        # 第二部分：AI重大新闻
        if ai_major_articles:
            if legal_tech_articles:
                summary_lines.append("")  # 空行分隔
            summary_lines.append("【AI重大新闻】")
            for i, article in enumerate(ai_major_articles[:10], 1):
                title = article.get('title', '无标题')
                description = article.get('description', '无描述')
                url = article.get('url', '')
                source = article.get('source', {}).get('name', '未知来源')
                published_at = article.get('publishedAt', '')

                summary_lines.append(
                    f"{i}. 标题: {title}\n"
                    f"   来源: {source}\n"
                    f"   描述: {description}\n"
                    f"   链接: {url}\n"
                )

        return '\n'.join(summary_lines)

    def _build_prompt(self, news_summary: str, api_provider: str = 'API') -> str:
        """
        构建发送给Claude的提示词
        :param news_summary: 新闻摘要
        :param api_provider: API提供商（'GLM' 或 'Claude'）
        :return: 完整的提示词
        """
        prompt = f"""你是一个专业的法律科技新闻编辑。请将以下新闻整理成一份简明扼要的中文Newsletter。

**严格按照以下格式输出：**

```
法律科技与AI日报 - {datetime.now().strftime('%Y年%m月%d日')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌【法律科技新闻】

➤ 新闻标题1
摘要: xxx
来源: xxx
发布时间: xxx
链接: xxx

➤ 新闻标题2
摘要: xxx
来源: xxx
发布时间: xxx
链接: xxx

……………………………………………………………………………………………………

🎂【AI重大新闻】

➤ 新闻标题1
摘要: xxx
来源: xxx
发布时间: xxx
链接: xxx

➤ 新闻标题2
摘要: xxx
来源: xxx
发布时间: xxx
链接: xxx

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 由法律科技新闻Bot自动推送（使用{api_provider} API翻译）
```

**重要格式要求：**
1. 标题必须是：法律科技与AI日报 - 日期（不要用"科技AI快讯"或其他标题）
2. 必须分为📌【法律科技新闻】和🎂【AI重大新闻】两个区块
3. 每条新闻标题前必须用 ➤ 符号（不要用编号1. 2. 3.）
4. 两个区块之间用点线分隔（……………………………………………………………………………………………………）
5. 字段标签不要用方括号：摘要: xxx（不要用【摘要】xxx）
6. 所有内容使用中文
7. 每个区块最多5条新闻
8. 如果某个区块没有新闻，就省略该区块
9. **最后落款必须是：🤖 由法律科技新闻Bot自动推送（使用{api_provider} API翻译）**

以下是今天的新闻（已按分类整理）：

{news_summary}

请严格按照上述格式输出Newsletter内容，不要修改格式结构。"""

        return prompt

    def _clean_html(self, html_text: str) -> str:
        """
        清理HTML标签，保留纯文本
        :param html_text: 包含HTML标签的文本
        :return: 清理后的纯文本
        """
        if not html_text:
            return html_text

        # 移除HTML标签
        # 移除<script>标签及其内容
        clean_text = re.sub(r'<script.*?>.*?</script>', '', html_text, flags=re.DOTALL | re.IGNORECASE)
        # 移除<style>标签及其内容
        clean_text = re.sub(r'<style.*?>.*?</style>', '', clean_text, flags=re.DOTALL | re.IGNORECASE)
        # 移除所有HTML标签
        clean_text = re.sub(r'<[^>]+>', '', clean_text)
        # 移除HTML实体（如&nbsp;, &lt;, &gt;等）
        clean_text = re.sub(r'&nbsp;', ' ', clean_text)
        clean_text = re.sub(r'&lt;', '<', clean_text)
        clean_text = re.sub(r'&gt;', '>', clean_text)
        clean_text = re.sub(r'&amp;', '&', clean_text)
        clean_text = re.sub(r'&quot;', '"', clean_text)
        clean_text = re.sub(r'&#39;', "'", clean_text)
        clean_text = re.sub(r'&apos;', "'", clean_text)
        # 移除多余的空白字符
        clean_text = re.sub(r'\s+', ' ', clean_text)
        # 去除首尾空格
        clean_text = clean_text.strip()

        return clean_text

    def _translate_text(self, text: str, max_length: int = 5000) -> str:
        """
        使用免费的Google翻译翻译文本
        :param text: 要翻译的文本
        :param max_length: 最大文本长度（Google翻译限制）
        :return: 翻译后的文本
        """
        if not text or not text.strip():
            return text

        try:
            # 如果文本太长，截断翻译
            if len(text) > max_length:
                text = text[:max_length] + "..."

            translator = GoogleTranslator(source='auto', target='zh-CN')
            translated = translator.translate(text)
            return translated
        except Exception as e:
            logger.warning(f"⚠️ 翻译失败: {e}，保留原文")
            return text

    def _fallback_newsletter(self, articles: List[Dict]) -> str:
        """
        备用方案：当Claude API调用失败时，使用简单的格式化
        现在包含免费翻译功能，并支持分类展示
        :param articles: 新闻列表
        :return: 简单格式化的新闻文本
        """
        logger.info("🔄 使用备用方案生成Newsletter（包含免费翻译和分类展示）")

        date_str = datetime.now().strftime('%Y年%m月%d日')
        lines = [
            f"📰 法律科技与AI日报 - {date_str}",
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            ""
        ]

        # 按分类整理新闻
        legal_tech_articles = []
        ai_major_articles = []
        other_articles = []

        for article in articles[:self.config.max_articles]:
            category = article.get('_category', 'other')
            if category == 'legal_tech':
                legal_tech_articles.append(article)
            elif category == 'ai_major':
                ai_major_articles.append(article)
            elif category == 'both':
                # 两者都有的，优先放到法律科技类
                legal_tech_articles.append(article)
            else:
                other_articles.append(article)

        # 添加一个辅助函数来格式化单条新闻
        def format_article(article, index):
            title = article.get('title', '无标题')
            description = article.get('description', '')
            url = article.get('url', '')
            source = article.get('source', {}).get('name', '未知来源')
            published_at = article.get('publishedAt', '')

            # 格式化发布时间
            publish_time = ''
            if published_at:
                try:
                    dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    publish_time = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    publish_time = published_at

            # 翻译标题和描述（先清理HTML标签）
            try:
                title_clean = self._clean_html(title)
                description_clean = self._clean_html(description) if description else ""

                # 计算标题和摘要的相似度
                should_show_description = False
                if description_clean:
                    title_normalized = title_clean.lower()
                    desc_normalized = description_clean.lower()
                    translator = str.maketrans('', '', string.punctuation + ' ')
                    title_normalized = title_normalized.translate(translator)
                    desc_normalized = desc_normalized.translate(translator)
                    similarity = SequenceMatcher(None, title_normalized, desc_normalized).ratio()
                    if similarity < 0.95:
                        should_show_description = True

                title_translated = self._translate_text(title_clean)
                description_translated = self._translate_text(description_clean) if should_show_description else ""

                result = [
                    f"📌 {index}. {title_translated}",
                ]
                if description_translated:
                    result.append(f"摘要: {description_translated}")
                result.append(f"来源: {source}")
                if publish_time:
                    result.append(f"发布时间: {publish_time}")
                result.append(f"链接: {url}")
                return result
            except Exception as e:
                logger.warning(f"⚠️ 翻译新闻失败: {e}，使用原文")
                result = [f"📌 {index}. {title}"]
                if description and str(description).lower() != str(title).lower():
                    result.append(f"摘要: {description}")
                result.append(f"来源: {source}")
                if publish_time:
                    result.append(f"发布时间: {publish_time}")
                result.append(f"链接: {url}")
                return result

        # ========== 第一部分：法律科技新闻 ==========
        if legal_tech_articles:
            lines.append("🔖 【法律科技新闻】")
            lines.append("")
            for i, article in enumerate(legal_tech_articles[:8], 1):  # 最多8条
                lines.extend(format_article(article, i))
                lines.append("")

        # ========== 第二部分：AI重大新闻 ==========
        if ai_major_articles:
            # 添加模块间分隔线（如果第一部分存在）
            if legal_tech_articles:
                lines.append("················································")
                lines.append("")

            lines.append("🤖 【AI重大新闻】")
            lines.append("")
            for i, article in enumerate(ai_major_articles[:8], 1):  # 最多8条
                lines.extend(format_article(article, i))
                lines.append("")

        # ========== 第三部分：其他相关新闻 ==========
        if other_articles and len(legal_tech_articles) + len(ai_major_articles) < 10:
            # 添加模块间分隔线（如果前两部分存在）
            if legal_tech_articles or ai_major_articles:
                lines.append("················································")
                lines.append("")

            lines.append("📰 【其他相关新闻】")
            lines.append("")
            for i, article in enumerate(other_articles[:5], 1):  # 最多5条
                lines.extend(format_article(article, i))
                lines.append("")

        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("")
        lines.append("🤖 由法律科技新闻Bot自动推送（使用备用翻译方案）")

        return '\n'.join(lines)


# ====================== 飞书推送模块 ======================
class FeishuNotifier:
    """飞书通知类：通过Webhook发送消息到飞书群"""

    def __init__(self, config: Config):
        """
        初始化飞书通知器
        :param config: 配置对象
        """
        self.config = config
        self.session = requests.Session()

    def send_newsletter(self, newsletter_content: str):
        """
        发送Newsletter到飞书群
        :param newsletter_content: Newsletter内容
        """
        logger.info("📤 开始发送飞书通知...")

        try:
            # 构建飞书消息格式
            message = {
                "msg_type": "text",
                "content": {
                    "text": newsletter_content
                }
            }

            # 发送POST请求到飞书Webhook
            response = self.session.post(
                self.config.feishu_webhook,
                json=message,
                timeout=10
            )

            # 检查响应状态
            response.raise_for_status()

            result = response.json()

            # 检查飞书API返回码
            if result.get('code') == 0:
                logger.info("✅ 飞书通知发送成功")
            else:
                logger.error(f"❌ 飞书API返回错误: {result}")

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 飞书通知发送失败: {e}")

        except Exception as e:
            logger.error(f"❌ 未知错误: {e}")


# ====================== Bot主控制器 ======================
class LegalTechNewsBot:
    """法律科技新闻Bot主控制器"""

    def __init__(self):
        """初始化Bot"""
        logger.info("=" * 60)
        logger.info("🚀 法律科技新闻Bot启动")
        logger.info("=" * 60)

        # 初始化配置
        self.config = Config()

        # 初始化各个模块
        self.news_fetcher = NewsFetcher(self.config)
        self.newsletter_generator = NewsletterGenerator(self.config)
        self.feishu_notifier = FeishuNotifier(self.config)

    def run_daily_task(self):
        """
        执行每日任务：抓取新闻 -> 生成Newsletter -> 推送到飞书
        """
        logger.info("\n" + "=" * 60)
        logger.info(f"⏰ 开始执行每日任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60 + "\n")

        try:
            # 步骤1: 获取新闻
            articles = self.news_fetcher.fetch_legal_tech_news()

            if not articles:
                logger.warning("⚠️ 未获取到新闻，任务结束")
                return

            # 步骤2: 生成Newsletter
            newsletter = self.newsletter_generator.generate_newsletter(articles)

            # 步骤3: 发送到飞书
            self.feishu_notifier.send_newsletter(newsletter)

            logger.info("\n" + "=" * 60)
            logger.info("✅ 今日任务完成")
            logger.info("=" * 60 + "\n")

        except Exception as e:
            logger.error(f"\n❌ 任务执行出错: {e}")
            logger.error("=" * 60 + "\n")

    def start(self):
        """
        启动Bot：设置定时任务，每天中午12点执行
        """
        # 设置每天12:00执行任务
        schedule.every().day.at("12:00").do(self.run_daily_task)

        logger.info("📅 Bot已启动，将在每天中午12:00推送新闻")
        logger.info("💡 提示：按Ctrl+C可以停止Bot\n")

        # 立即执行一次（可选，用于测试）
        # self.run_daily_task()

        # 持续运行
        try:
            while True:
                # 检查是否有待执行的任务
                schedule.run_pending()
                # 每隔60秒检查一次
                time.sleep(60)

        except KeyboardInterrupt:
            logger.info("\n👋 Bot已停止")

    def run_once(self):
        """
        单次运行模式：立即执行一次任务（用于测试）
        """
        logger.info("🧪 单次运行模式")
        self.run_daily_task()


# ====================== 主程序入口 ======================
def main():
    """
    主函数：程序入口
    支持两种运行模式：
    1. test模式：立即执行一次任务（用于测试）
    2. production模式：定时运行，每天12点执行（用于生产环境）

    模式切换：在.env文件中设置 RUN_MODE=test 或 RUN_MODE=production
    """
    try:
        # 创建Bot实例
        bot = LegalTechNewsBot()

        # 根据配置选择运行模式
        if bot.config.run_mode == 'test':
            logger.info("🧪 测试模式：立即执行一次任务")
            logger.info("💡 提示：如需切换到定时模式，请在.env中设置 RUN_MODE=production")
            bot.run_once()
        else:
            logger.info("🚀 生产模式：定时运行中")
            logger.info("💡 提示：如需切换到测试模式，请在.env中设置 RUN_MODE=test")
            bot.start()

    except ValueError as e:
        logger.error(f"❌ 配置错误: {e}")
        logger.error("请检查.env文件中的配置项是否正确")

    except Exception as e:
        logger.error(f"❌ 程序异常: {e}")


# 如果直接运行此脚本，则执行main函数
if __name__ == '__main__':
    main()
