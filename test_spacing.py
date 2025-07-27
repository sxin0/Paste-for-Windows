#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试卡片间距改进效果
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from src.gui.bottom_panel import ClipboardItemWidget
from src.core.clipboard_manager import ClipboardItem
from datetime import datetime

class SpacingTestWindow(QMainWindow):
    """间距测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("卡片间距测试")
        self.setMinimumSize(800, 400)
        self.resize(1000, 500)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建水平布局来放置卡片
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)  # 卡片间距
        
        # 创建测试数据
        test_items = [
            ClipboardItem("1", "这是第一个测试卡片，用来验证间距效果", "text", datetime.now()),
            ClipboardItem("2", "第二个卡片，包含一些链接内容 https://example.com", "link", datetime.now()),
            ClipboardItem("3", "代码卡片：print('Hello, World!')", "code", datetime.now()),
            ClipboardItem("4", "这是一个很长的文本内容，用来测试卡片在横向布局中的显示效果", "text", datetime.now()),
            ClipboardItem("5", "文件路径：C:\\Users\\Documents\\test.txt", "file", datetime.now()),
        ]
        
        # 创建卡片
        for item in test_items:
            card = ClipboardItemWidget(item)
            cards_layout.addWidget(card)
        
        # 添加弹性空间
        cards_layout.addStretch()
        
        main_layout.addLayout(cards_layout)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 rgba(240,240,240,0.9),
                                          stop:1 rgba(220,220,220,0.9));
            }
        """)

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 创建测试窗口
    window = SpacingTestWindow()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    main() 