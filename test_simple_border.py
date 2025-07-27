#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试卡片边框效果
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from src.gui.bottom_panel import ClipboardItemWidget
from src.core.clipboard_manager import ClipboardItem
from datetime import datetime

def test_simple_borders():
    """简单测试卡片边框效果"""
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = QMainWindow()
    window.setWindowTitle("简单边框测试")
    window.setMinimumSize(800, 400)
    
    # 创建中央部件
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    # 主布局
    main_layout = QVBoxLayout(central_widget)
    main_layout.setContentsMargins(20, 20, 20, 20)
    
    # 标题
    title = QLabel("简单边框测试 - 每个卡片应该有不同颜色的边框")
    title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 20px; color: #333;")
    main_layout.addWidget(title)
    
    # 创建水平布局来放置卡片
    cards_layout = QHBoxLayout()
    cards_layout.setSpacing(10)  # 卡片间距
    
    # 创建不同类型的测试数据
    test_items = [
        ClipboardItem("", "这是文本类型的卡片，应该有蓝色边框", "text", datetime.now()),
        ClipboardItem("", "https://example.com - 链接类型，应该有绿色边框", "link", datetime.now()),
        ClipboardItem("", "print('Hello, World!') - 代码类型，应该有紫色边框", "code", datetime.now()),
        ClipboardItem("", "C:\\Users\\Documents\\test.txt - 文件类型，应该有红色边框", "file", datetime.now()),
        ClipboardItem("", "图片文件 - 图片类型，应该有橙色边框", "image", datetime.now()),
    ]
    
    # 创建卡片
    for item in test_items:
        card = ClipboardItemWidget(item)
        cards_layout.addWidget(card)
    
    # 添加弹性空间
    cards_layout.addStretch()
    
    main_layout.addLayout(cards_layout)
    
    # 说明文字
    description = QLabel("说明：每个卡片应该有不同颜色的边框，鼠标悬停时边框会变粗")
    description.setStyleSheet("font-size: 12px; color: #666; margin-top: 20px;")
    main_layout.addWidget(description)
    
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
    test_simple_borders() 