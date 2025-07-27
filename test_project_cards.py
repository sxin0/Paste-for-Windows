#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试项目中的卡片效果
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from src.gui.bottom_panel import BottomPanel, ClipboardItemWidget
from src.core.clipboard_manager import ClipboardManager, ClipboardItem
from datetime import datetime

def test_project_cards():
    """测试项目中的卡片效果"""
    app = QApplication(sys.argv)
    
    # 创建剪贴板管理器
    clipboard_manager = ClipboardManager()
    
    # 创建主窗口
    window = QMainWindow()
    window.setWindowTitle("项目卡片测试")
    window.setMinimumSize(1000, 500)
    
    # 创建中央部件
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    # 主布局
    main_layout = QVBoxLayout(central_widget)
    main_layout.setContentsMargins(20, 20, 20, 20)
    
    # 标题
    title = QLabel("项目卡片测试 - 模拟实际项目中的卡片效果")
    title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 20px; color: #333;")
    main_layout.addWidget(title)
    
    # 创建底部面板
    bottom_panel = BottomPanel(clipboard_manager)
    main_layout.addWidget(bottom_panel)
    
    # 添加一些测试数据到剪贴板管理器
    test_items = [
        ClipboardItem("", "这是一段文本内容，用于测试文本类型的卡片", "text"),
        ClipboardItem("", "https://www.example.com - 这是一个链接", "link"),
        ClipboardItem("", "print('Hello, World!') - 这是一段代码", "code"),
        ClipboardItem("", "C:\\Users\\Documents\\test.txt - 这是一个文件路径", "file"),
        ClipboardItem("", "image.jpg - 这是一个图片文件", "image"),
        ClipboardItem("", "另一段文本内容，用于测试多个文本卡片", "text"),
        ClipboardItem("", "https://github.com - 另一个链接", "link"),
        ClipboardItem("", "def hello(): return 'Hello' - 另一段代码", "code"),
    ]
    
    # 手动添加测试数据到管理器
    for item in test_items:
        clipboard_manager._add_item(item)
    
    # 显示面板
    bottom_panel.show_panel()
    
    # 设置窗口样式
    window.setStyleSheet("""
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 rgba(240,240,240,0.9),
                                      stop:1 rgba(220,220,220,0.9));
        }
    """)
    
    window.show()
    return app.exec()

if __name__ == "__main__":
    test_project_cards() 