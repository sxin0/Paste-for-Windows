#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paste for Windows - 简化版本
避免剪贴板访问问题，专注于UI演示
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.core.clipboard_manager import ClipboardManager
from src.gui.bottom_panel import BottomPanel
from src.gui.system_tray import SystemTray


class SimpleApp(QMainWindow):
    """简化版应用"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_components()
    
    def setup_ui(self):
        """设置界面"""
        self.setWindowTitle("Paste for Windows - 简化版")
        self.setGeometry(100, 100, 500, 400)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("Paste for Windows")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #0078d4;")
        
        # 说明
        description = QLabel(
            "简化版剪贴板管理器\n\n"
            "这个版本专注于展示从屏幕下方冒出来的交互栏功能，"
            "避免了剪贴板访问的复杂性。\n\n"
            "点击下面的按钮来体验功能："
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        description.setStyleSheet("font-size: 14px; line-height: 1.5;")
        
        # 按钮
        self.show_panel_btn = QPushButton("显示底部面板")
        self.show_panel_btn.setMinimumHeight(50)
        self.show_panel_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #0078d4, stop:1 #106ebe);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 18px;
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
        
        # 添加测试数据按钮
        self.add_data_btn = QPushButton("添加测试数据")
        self.add_data_btn.setMinimumHeight(50)
        self.add_data_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #107c10, stop:1 #0e6b0e);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #0e6b0e, stop:1 #0d5a0d);
            }
        """)
        self.add_data_btn.clicked.connect(self.add_test_data)
        
        # 状态标签
        self.status_label = QLabel("准备就绪 - 点击按钮开始体验")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #605e5c; font-size: 14px; padding: 10px;")
        
        # 添加到布局
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.show_panel_btn)
        layout.addWidget(self.add_data_btn)
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
        # 剪贴板管理器（不启动监听）
        self.clipboard_manager = ClipboardManager()
        
        # 底部面板
        self.bottom_panel = BottomPanel(self.clipboard_manager)
        
        # 系统托盘
        self.system_tray = SystemTray(self.clipboard_manager)
        
        # 连接信号
        self.bottom_panel.item_selected.connect(self.on_item_selected)
        self.bottom_panel.panel_closed.connect(self.on_panel_closed)
        self.system_tray.show_bottom_panel_requested.connect(self.show_bottom_panel)
        self.system_tray.toggle_bottom_panel_requested.connect(self.toggle_bottom_panel)
        self.system_tray.show_window_requested.connect(self.show_main_window)
        self.system_tray.quit_requested.connect(self.close)
        
        # 显示系统托盘
        if self.system_tray.is_system_tray_available():
            self.system_tray.show()
    
    def show_bottom_panel(self):
        """显示底部面板"""
        self.status_label.setText("正在显示底部面板...")
        self.bottom_panel.show_panel()
    
    def toggle_bottom_panel(self):
        """切换底部面板显示状态"""
        if self.bottom_panel.isVisible():
            self.status_label.setText("正在隐藏底部面板...")
            self.bottom_panel.hide_panel()
        else:
            self.status_label.setText("正在显示底部面板...")
            self.bottom_panel.show_panel()
    
    def add_test_data(self):
        """添加测试数据"""
        from src.core.clipboard_manager import ClipboardItem
        
        test_items = [
            "这是一个测试文本内容，用于演示搜索功能",
            "https://www.example.com - 这是一个链接",
            "C:\\Users\\Documents\\important_file.txt - 文件路径",
            "def hello_world():\n    print('Hello, World!')\n    return True - 代码片段",
            "重要的会议记录：明天下午2点开会，讨论项目进展",
            "购物清单：牛奶、面包、鸡蛋、水果、蔬菜",
            "电话号码：123-456-7890 - 联系人信息",
            "邮箱地址：test@example.com - 邮箱",
            "项目进度：第一阶段已完成，开始第二阶段开发",
            "待办事项：1. 完成文档 2. 测试功能 3. 部署应用"
        ]
        
        for i, content in enumerate(test_items):
            item = ClipboardItem(id="", content=content)
            self.clipboard_manager._add_item(item)
        
        self.status_label.setText(f"已添加 {len(test_items)} 个测试项目")
    
    def on_item_selected(self, item):
        """项目被选中"""
        self.status_label.setText(f"已选择: {item.content[:50]}...")
    
    def on_panel_closed(self):
        """面板关闭"""
        self.status_label.setText("底部面板已关闭")
    
    def show_main_window(self):
        """显示主窗口"""
        self.show()
        self.raise_()
        self.activateWindow()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("Paste for Windows Simple")
    app.setApplicationVersion("1.0.0")
    
    window = SimpleApp()
    window.show()
    
    print("简化版应用已启动！")
    print("这个版本专注于展示从屏幕下方冒出来的交互栏功能。")
    print("点击按钮来体验动画效果和搜索功能。")
    
    return app.exec()


if __name__ == "__main__":
    main() 