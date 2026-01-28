#!/bin/bash

echo "===================================="
echo "法律科技新闻Bot - 快速启动"
echo "===================================="
echo ""

# 检查Python3是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3，请先安装"
    echo "macOS: brew install python3"
    echo "Ubuntu: sudo apt-get install python3"
    exit 1
fi

# 检查.env文件是否存在
if [ ! -f .env ]; then
    echo "[警告] 未找到.env配置文件"
    echo "正在从.env.example创建.env文件..."
    cp .env.example .env
    echo ""
    echo "请先编辑.env文件，填写你的API密钥："
    echo "nano .env"
    echo "或"
    echo "code .env"
    echo ""
    exit 1
fi

# 检查依赖是否已安装
python3 -c "import requests" &> /dev/null
if [ $? -ne 0 ]; then
    echo "[提示] 检测到依赖包未安装，正在安装..."
    python3 -m pip install -r requirements.txt
    echo ""
fi

# 启动Bot
echo "[启动] 正在启动法律科技新闻Bot..."
echo "[提示] 按Ctrl+C可以停止Bot"
echo ""
python3 legal_tech_news_bot.py
