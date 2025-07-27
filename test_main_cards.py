#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试主程序中的卡片效果
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from src.main import MainWindow
from src.core.clipboard_manager import ClipboardItem
from datetime import datetime

def test_main_cards():
    """测试主程序中的卡片效果"""
    app = QApplication(sys.argv)
    
    # 创建主窗口
    main_window = MainWindow()
    
    # 添加一些测试数据到剪贴板管理器
    test_items = [
        ClipboardItem("1", "这是文本类型的卡片，用来测试边框效果", "text", datetime.now()),
        ClipboardItem("2", "https://www.example.com", "link", datetime.now()),
        ClipboardItem("3", "print('Hello, World!')", "code", datetime.now()),
        ClipboardItem("4", "C:\\Users\\Documents\\test.txt", "file", datetime.now()),
        ClipboardItem("5", "图片文件内容", "image", datetime.now()),
    ]
    
    # 手动添加测试项目
    for item in test_items:
        main_window.clipboard_manager._add_item(item)
    
    # 显示主窗口
    main_window.show()
    
    # 显示底部面板来查看卡片效果
    main_window.show_bottom_panel()
    
    print("主程序已启动！")
    print("可以看到底部面板中的卡片效果：")
    print("- 每个卡片都有不同颜色的边框")
    print("- 卡片之间有明显的间距")
    print("- 悬停时边框会变粗")
    print("- 有阴影效果")
    
    return app.exec()

if __name__ == "__main__":
    test_main_cards() 