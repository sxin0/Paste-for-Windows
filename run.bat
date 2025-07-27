 @echo off
chcp 65001 >nul
title Paste for Windows - 剪贴板管理器

echo.
echo ================================================
echo     Paste for Windows - 剪贴板管理器
echo ================================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python环境
    echo 请确保已安装Python 3.7或更高版本
    echo.
    pause
    exit /b 1
)

REM 检查是否在正确的目录
if not exist "main.py" (
    echo [错误] 找不到main.py文件
    echo 请确保在正确的目录下运行此脚本
    echo.
    pause
    exit /b 1
)

echo [信息] 正在启动剪贴板管理器...
echo.

REM 启动程序
python main.py

if errorlevel 1 (
    echo.
    echo [错误] 程序启动失败
    echo 如果这是第一次运行，请先执行 install.py 安装依赖
    echo.
    pause
)

exit /b 0