#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
托盘图标功能演示
展示点击托盘图标唤醒底部交互窗口的功能
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


class TrayDemoWindow(QMainWindow):
    """托盘功能演示窗口"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_components()
    
    def setup_ui(self):
        """设置界面"""
        self.setWindowTitle("托盘图标功能演示")
        self.setGeometry(100, 100, 600, 400)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("托盘图标功能演示")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #0078d4;")
        
        # 说明
        description = QLabel(
            "这个演示展示了托盘图标的功能：\n\n"
            "🎯 **单击托盘图标** - 显示底部交互窗口\n"
            "🎯 **双击托盘图标** - 显示底部交互窗口\n"
            "🎯 **右键托盘图标** - 显示菜单选项\n\n"
            "现在你可以：\n"
            "1. 点击'添加测试数据'按钮\n"
            "2. 最小化这个窗口\n"
            "3. 点击系统托盘图标\n"
            "4. 观察底部交互窗口从屏幕下方冒出来"
        )
        description.setAlignment(Qt.AlignmentFlag.AlignLeft)
        description.setWordWrap(True)
        description.setStyleSheet("font-size: 14px; line-height: 1.6; padding: 15px; background: rgba(255,255,255,0.8); border-radius: 8px;")
        
        # 按钮
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
        
        self.show_panel_btn = QPushButton("手动显示底部面板")
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
        """)
        self.show_panel_btn.clicked.connect(self.show_bottom_panel)
        
        # 状态标签
        self.status_label = QLabel("准备就绪 - 托盘图标已激活")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #605e5c; font-size: 14px; padding: 10px; background: rgba(0,120,212,0.1); border-radius: 8px;")
        
        # 添加到布局
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.add_data_btn)
        layout.addWidget(self.show_panel_btn)
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
            self.status_label.setText("✅ 托盘图标已激活 - 点击托盘图标唤醒底部窗口")
        else:
            self.status_label.setText("❌ 托盘图标不可用")
    
    def add_test_data(self):
        """添加测试数据"""
        from src.core.clipboard_manager import ClipboardItem
        
        test_items = [
            "托盘图标功能演示 - 这是一个测试文本",
            "https://www.example.com - 示例链接",
            "C:\\Users\\Documents\\demo.txt - 示例文件路径",
            "def tray_demo():\n    print('托盘功能演示')\n    return True - 示例代码",
            "重要提醒：点击托盘图标可以快速唤醒底部交互窗口",
            "购物清单：苹果、香蕉、橙子、葡萄",
            "联系方式：demo@example.com",
            "项目进度：托盘功能开发完成",
            "待办事项：1. 测试托盘功能 2. 优化用户体验",
            "使用技巧：单击或双击托盘图标都可以唤醒底部窗口"
        ]
        
        for i, content in enumerate(test_items):
            item = ClipboardItem(id="", content=content)
            self.clipboard_manager._add_item(item)
        
        self.status_label.setText(f"✅ 已添加 {len(test_items)} 个测试项目 - 现在可以点击托盘图标测试")
    
    def show_bottom_panel(self):
        """显示底部面板"""
        self.status_label.setText("🎬 正在显示底部面板...")
        self.bottom_panel.show_panel()
    
    def toggle_bottom_panel(self):
        """切换底部面板显示状态"""
        if self.bottom_panel.isVisible():
            self.status_label.setText("🔒 正在隐藏底部面板...")
            self.bottom_panel.hide_panel()
        else:
            self.status_label.setText("🎬 正在显示底部面板...")
            self.bottom_panel.show_panel()
    
    def show_main_window(self):
        """显示主窗口"""
        self.show()
        self.raise_()
        self.activateWindow()
        self.status_label.setText("🪟 主窗口已显示")
    
    def on_item_selected(self, item):
        """项目被选中"""
        self.status_label.setText(f"✅ 已选择: {item.content[:50]}...")
    
    def on_panel_closed(self):
        """面板关闭"""
        self.status_label.setText("🔒 底部面板已关闭 - 点击托盘图标重新唤醒")
    
    def closeEvent(self, event):
        """关闭事件"""
        # 如果系统托盘可用，最小化到托盘而不是关闭
        if self.system_tray.is_system_tray_available() and self.system_tray.is_visible():
            self.hide()
            event.ignore()
        else:
            event.accept()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("托盘功能演示")
    app.setApplicationVersion("1.0.0")
    
    # 设置应用程序图标
    from pathlib import Path
    app_icon_path = Path(__file__).parent / "resources" / "icons" / "app_icon.png"
    if app_icon_path.exists():
        from PyQt6.QtGui import QIcon
        app.setWindowIcon(QIcon(str(app_icon_path)))
        print(f"✅ 应用程序图标已设置: {app_icon_path}")
    
    window = TrayDemoWindow()
    window.show()
    
    print("托盘功能演示已启动！")
    print("功能说明：")
    print("1. 点击'添加测试数据'添加示例内容")
    print("2. 最小化窗口到系统托盘")
    print("3. 单击或双击托盘图标唤醒底部交互窗口")
    print("4. 右键托盘图标查看菜单选项")
    
    return app.exec()


if __name__ == "__main__":
    main() 