#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
底部面板演示脚本
展示从屏幕下方冒出来的交互栏功能
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.core.clipboard_manager import ClipboardManager
from src.gui.bottom_panel import BottomPanel


class DemoWindow(QMainWindow):
    """演示窗口"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_components()
    
    def setup_ui(self):
        """设置界面"""
        self.setWindowTitle("Paste for Windows - 底部面板演示")
        self.setGeometry(100, 100, 500, 300)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("底部面板演示")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #0078d4;")
        
        # 说明
        description = QLabel(
            "这个演示展示了从屏幕下方冒出来的交互栏功能。\n\n"
            "点击下面的按钮来测试底部面板的动画效果："
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        description.setStyleSheet("font-size: 14px; line-height: 1.5;")
        
        # 按钮
        self.show_panel_btn = QPushButton("显示底部面板")
        self.show_panel_btn.setMinimumHeight(40)
        self.show_panel_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #0078d4, stop:1 #106ebe);
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #106ebe, stop:1 #005a9e);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #005a9e, stop:1 #004578);
            }
        """)
        self.show_panel_btn.clicked.connect(self.show_bottom_panel)
        
        # 添加一些测试数据
        self.add_test_data_btn = QPushButton("添加测试数据")
        self.add_test_data_btn.setMinimumHeight(40)
        self.add_test_data_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #107c10, stop:1 #0e6b0e);
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #0e6b0e, stop:1 #0d5a0d);
            }
        """)
        self.add_test_data_btn.clicked.connect(self.add_test_data)
        
        # 状态标签
        self.status_label = QLabel("准备就绪")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #605e5c; font-size: 12px;")
        
        # 添加到布局
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.show_panel_btn)
        layout.addWidget(self.add_test_data_btn)
        layout.addWidget(self.status_label)
        layout.addStretch()
        
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 rgba(255,255,255,0.95),
                                          stop:1 rgba(255,255,255,0.85));
            }
        """)
    
    def setup_components(self):
        """设置组件"""
        # 剪贴板管理器
        self.clipboard_manager = ClipboardManager()
        
        # 底部面板
        self.bottom_panel = BottomPanel(self.clipboard_manager)
        
        # 连接信号
        self.bottom_panel.item_selected.connect(self.on_item_selected)
        self.bottom_panel.panel_closed.connect(self.on_panel_closed)
    
    def show_bottom_panel(self):
        """显示底部面板"""
        self.status_label.setText("正在显示底部面板...")
        self.bottom_panel.show_panel()
    
    def add_test_data(self):
        """添加测试数据"""
        from src.core.clipboard_manager import ClipboardItem
        
        test_items = [
            "这是一个测试文本内容",
            "https://www.example.com",
            "C:\\Users\\Documents\\test.txt",
            "def hello_world():\n    print('Hello, World!')",
            "重要的会议记录：明天下午2点开会",
            "购物清单：牛奶、面包、鸡蛋",
            "电话号码：123-456-7890",
            "邮箱地址：test@example.com"
        ]
        
        for i, content in enumerate(test_items):
            item = ClipboardItem(id="", content=content)
            self.clipboard_manager._add_item(item)
        
        self.status_label.setText(f"已添加 {len(test_items)} 个测试项目")
    
    def on_item_selected(self, item):
        """项目被选中"""
        self.status_label.setText(f"已选择: {item.content[:30]}...")
    
    def on_panel_closed(self):
        """面板关闭"""
        self.status_label.setText("底部面板已关闭")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("Paste for Windows Demo")
    app.setApplicationVersion("1.0.0")
    
    window = DemoWindow()
    window.show()
    
    print("底部面板演示已启动！")
    print("点击 '显示底部面板' 按钮来查看从屏幕下方冒出来的动画效果。")
    print("点击 '添加测试数据' 按钮来添加一些测试内容。")
    
    return app.exec()


if __name__ == "__main__":
    main() 