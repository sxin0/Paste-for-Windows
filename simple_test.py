#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 PyQt6 兼容性测试
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QLinearGradient, QPainter

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 兼容性测试")
        self.setGeometry(100, 100, 400, 300)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加标签
        label = QLabel("PyQt6 兼容性测试成功！")
        label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #0078d4;
                padding: 20px;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
                border: 2px solid #0078d4;
            }
        """)
        layout.addWidget(label)
        
        # 添加按钮
        button = QPushButton("测试按钮")
        button.setStyleSheet("""
            QPushButton {
                background: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #106ebe;
            }
        """)
        layout.addWidget(button)
        
        # 设置窗口标志
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinMaxButtonsHint)
        
        # 设置全局样式
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 rgba(255,255,255,0.95),
                                          stop:1 rgba(255,255,255,0.85));
            }
        """)

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("PyQt6 测试")
    app.setApplicationVersion("1.0.0")
    
    # 创建窗口
    window = TestWindow()
    window.show()
    
    print("PyQt6 兼容性测试启动成功！")
    print("如果看到窗口，说明 PyQt6 配置正确。")
    
    # 运行应用程序
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 