#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试卡片布局效果
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from src.gui.bottom_panel import BottomPanel
from src.core.clipboard_manager import ClipboardManager
from src.core.clipboard_manager import ClipboardItem
from datetime import datetime

def test_cards_layout():
    """测试卡片布局"""
    app = QApplication(sys.argv)
    
    # 创建剪贴板管理器
    clipboard_manager = ClipboardManager()
    
    # 创建底部面板
    bottom_panel = BottomPanel(clipboard_manager)
    
    # 添加一些测试数据
    test_items = [
        ClipboardItem("1", "这是一段测试文本内容，用来测试卡片显示效果", "text", datetime.now()),
        ClipboardItem("2", "https://www.example.com", "link", datetime.now()),
        ClipboardItem("3", "print('Hello, World!')", "code", datetime.now()),
        ClipboardItem("4", "这是一个很长的文本内容，用来测试卡片在横向布局中的显示效果，看看文字是否会正确换行", "text", datetime.now()),
        ClipboardItem("5", "C:\\Users\\Documents\\test.txt", "file", datetime.now()),
    ]
    
    # 手动添加测试项目到面板
    for item in test_items:
        bottom_panel._add_item_to_list(item)
    
    # 显示面板
    bottom_panel.show_panel()
    
    return app.exec()

if __name__ == "__main__":
    test_cards_layout() 