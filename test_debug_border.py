#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试边框和背景色测试
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

class DebugCard(QWidget):
    """调试卡片组件"""
    
    def __init__(self, text, bg_color, border_color, parent=None):
        super().__init__(parent)
        self.text = text
        self.bg_color = bg_color
        self.border_color = border_color
        self._setup_ui()
    
    def _setup_ui(self):
        # 设置对象名称
        self.setObjectName("DebugCard")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 添加文本标签
        label = QLabel(self.text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        # 设置固定尺寸
        self.setFixedSize(200, 120)
        
        # 设置样式表 - 使用 !important 确保样式生效
        self.setStyleSheet(f"""
            QWidget#DebugCard {{
                background-color: {self.bg_color} !important;
                border: 3px solid {self.border_color} !important;
                border-radius: 8px !important;
            }}
            QWidget#DebugCard:hover {{
                border: 4px solid {self.border_color} !important;
                background-color: {self.bg_color} !important;
            }}
            QWidget#DebugCard > QLabel {{
                background: transparent !important;
                border: none !important;
                color: #333 !important;
                font-size: 14px !important;
            }}
        """)

def main():
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = QMainWindow()
    window.setWindowTitle("调试边框测试")
    window.setMinimumSize(800, 300)
    
    # 创建中央部件
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    # 主布局
    main_layout = QVBoxLayout(central_widget)
    main_layout.setContentsMargins(20, 20, 20, 20)
    
    # 标题
    title = QLabel("调试边框测试 - 检查背景色和边框是否生效")
    title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 20px; color: #333;")
    main_layout.addWidget(title)
    
    # 创建水平布局来放置卡片
    cards_layout = QHBoxLayout()
    cards_layout.setSpacing(10)  # 卡片间距
    
    # 创建不同颜色的卡片
    cards = [
        ("蓝色背景", "#E3F2FD", "#2196F3"),
        ("绿色背景", "#E8F5E8", "#4CAF50"),
        ("红色背景", "#FFEBEE", "#F44336"),
        ("紫色背景", "#F3E5F5", "#9C27B0"),
        ("橙色背景", "#FFF3E0", "#FF9800"),
    ]
    
    for text, bg_color, border_color in cards:
        card = DebugCard(text, bg_color, border_color)
        cards_layout.addWidget(card)
    
    # 添加弹性空间
    cards_layout.addStretch()
    
    main_layout.addLayout(cards_layout)
    
    # 说明文字
    description = QLabel("说明：每个卡片应该有不同颜色的背景和边框，如果这个测试有效，说明样式设置是正确的")
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
    main() 