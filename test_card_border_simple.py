#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单卡片边框测试
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

def test_card_borders():
    """测试卡片边框效果"""
    print("启动测试...")
    app = QApplication(sys.argv)
    print("QApplication 已创建")
    
    # 创建主窗口
    window = QMainWindow()
    window.setWindowTitle("卡片边框测试")
    window.setMinimumSize(800, 300)
    
    # 创建中央部件
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    # 主布局
    main_layout = QVBoxLayout(central_widget)
    main_layout.setContentsMargins(20, 20, 20, 20)
    
    # 标题
    title = QLabel("卡片边框测试")
    title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
    main_layout.addWidget(title)
    
    # 创建水平布局来放置卡片
    cards_layout = QHBoxLayout()
    cards_layout.setSpacing(20)
    
    # 创建测试数据
    test_items = [
        ClipboardItem("", "文本类型", "text", datetime.now()),
        ClipboardItem("", "链接类型", "link", datetime.now()),
        ClipboardItem("", "代码类型", "code", datetime.now()),
    ]
    
    # 创建卡片
    for item in test_items:
        card = ClipboardItemWidget(item)
        cards_layout.addWidget(card)
    
    # 添加弹性空间
    cards_layout.addStretch()
    
    main_layout.addLayout(cards_layout)
    
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
    test_card_borders() 