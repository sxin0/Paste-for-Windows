#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试主程序启动时的测试卡片
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from src.main import MainWindow

def test_startup_cards():
    """测试主程序启动时的测试卡片"""
    app = QApplication(sys.argv)
    
    print("🚀 启动主程序...")
    print("📋 程序将自动添加测试卡片")
    print("🎨 包含不同颜色边框的卡片类型")
    print("")
    
    # 创建主窗口
    main_window = MainWindow()
    
    # 显示主窗口
    main_window.show()
    
    print("✅ 主程序已启动！")
    print("")
    print("📝 测试步骤：")
    print("1. 查看主窗口中的功能说明")
    print("2. 按 Win+V 或点击托盘图标")
    print("3. 观察底部面板中的卡片效果")
    print("4. 测试搜索功能")
    print("5. 点击卡片查看复制效果")
    print("")
    print("🎯 预期效果：")
    print("- 6个不同颜色的测试卡片")
    print("- 每个卡片都有对应的边框颜色")
    print("- 悬停时边框会变粗")
    print("- 有阴影效果")
    
    return app.exec()

if __name__ == "__main__":
    test_startup_cards() 