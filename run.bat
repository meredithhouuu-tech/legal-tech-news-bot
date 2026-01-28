@echo off
chcp 65001 >nul
echo ====================================
echo 法律科技新闻Bot - 快速启动
echo ====================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查.env文件是否存在
if not exist .env (
    echo [警告] 未找到.env配置文件
    echo 正在从.env.example创建.env文件...
    copy .env.example .env >nul
    echo.
    echo 请先编辑.env文件，填写你的API密钥
    echo 然后重新运行此脚本
    echo.
    notepad .env
    pause
    exit /b 1
)

REM 检查依赖是否已安装
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [提示] 检测到依赖包未安装，正在安装...
    python -m pip install -r requirements.txt
    echo.
)

REM 启动Bot
echo [启动] 正在启动法律科技新闻Bot...
echo [提示] 按Ctrl+C可以停止Bot
echo.
python legal_tech_news_bot.py

pause
