#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简单的边框测试
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

class SimpleCard(QWidget):
    """简单的卡片组件"""
    
    def __init__(self, text, color, parent=None):
        super().__init__(parent)
        self.text = text
        self.color = color
        self._setup_ui()
    
    def _setup_ui(self):
        # 设置对象名称
        self.setObjectName("SimpleCard")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 添加文本标签
        label = QLabel(self.text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        # 设置固定尺寸
        self.setFixedSize(200, 120)
        
        # 设置样式表
        self.setStyleSheet(f"""
            QWidget#SimpleCard {{
                background: white;
                border: 3px solid {self.color};
                border-radius: 8px;
            }}
            QWidget#SimpleCard:hover {{
                border: 4px solid {self.color};
                background: #f0f0f0;
            }}
        """)

def main():
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = QMainWindow()
    window.setWindowTitle("简单边框测试")
    window.setMinimumSize(800, 300)
    
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
    
    # 创建不同颜色的卡片
    cards = [
        ("蓝色边框", "#0078D4"),
        ("绿色边框", "#107C10"),
        ("红色边框", "#A4262C"),
        ("紫色边框", "#6B21A8"),
        ("橙色边框", "#ED7D31"),
    ]
    
    for text, color in cards:
        card = SimpleCard(text, color)
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
    main() 