#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试边框问题
"""

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class TestCard(QWidget):
    def __init__(self, text, color, parent=None):
        super().__init__(parent)
        self.text = text
        self.color = color
        self._setup_ui()
    
    def _setup_ui(self):
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
            QWidget {{
                background: rgba(255, 255, 255, 0.9);
                border: 3px solid {self.color};
                border-radius: 12px;
                margin: 2px;
            }}
            QWidget:hover {{
                background: rgba(255, 255, 255, 0.98);
                border-width: 4px;
            }}
        """)
        
        # 添加阴影
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)

def main():
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = QWidget()
    window.setWindowTitle("边框调试")
    window.setMinimumSize(600, 200)
    
    # 创建布局
    layout = QHBoxLayout(window)
    layout.setSpacing(20)
    
    # 创建不同颜色的卡片
    cards = [
        ("文本卡片", "rgba(0, 120, 212, 0.8)"),
        ("链接卡片", "rgba(16, 124, 16, 0.8)"),
        ("代码卡片", "rgba(107, 33, 168, 0.8)"),
    ]
    
    for text, color in cards:
        card = TestCard(text, color)
        layout.addWidget(card)
    
    # 添加弹性空间
    layout.addStretch()
    
    # 设置窗口背景
    window.setStyleSheet("""
        QWidget {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 rgba(240,240,240,0.9),
                                      stop:1 rgba(220,220,220,0.9));
        }
    """)
    
    window.show()
    return app.exec()

if __name__ == "__main__":
    main() 