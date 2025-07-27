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
            # 文本类型内容
            "托盘图标功能演示 - 这是一个测试文本，用于验证滚动条功能",
            "重要提醒：点击托盘图标可以快速唤醒底部交互窗口",
            "购物清单：苹果、香蕉、橙子、葡萄、草莓、蓝莓、猕猴桃",
            "联系方式：demo@example.com - 演示邮箱",
            "项目进度：托盘功能开发完成，正在测试滚动条效果",
            "待办事项：1. 测试托盘功能 2. 优化用户体验 3. 完善滚动条",
            "使用技巧：单击或双击托盘图标都可以唤醒底部窗口",
            "工作笔记：今天完成了托盘功能的开发，明天测试滚动条",
            "学习计划：本周学习PyQt6高级特性，下周开始学习系统托盘",
            "健康提醒：记得多喝水，适当运动，保持良好作息",
            "财务记录：本月收入6000元，支出3500元，结余2500元",
            "旅行计划：下个月去上海旅游，需要提前订票和酒店",
            
            # 链接类型内容
            "https://www.example.com - 示例链接",
            "https://github.com/microsoft/vscode - VS Code官方仓库",
            "https://www.python.org/downloads/ - Python官方下载页面",
            "https://docs.python.org/3/tutorial/ - Python官方教程",
            "https://stackoverflow.com/questions/tagged/python - Python相关问题",
            "https://www.w3schools.com/python/ - Python学习网站",
            "https://realpython.com/ - 高质量Python教程",
            "https://pypi.org/ - Python包索引",
            "https://www.jetbrains.com/pycharm/ - PyCharm IDE",
            "https://code.visualstudio.com/ - Visual Studio Code",
            
            # 文件类型内容
            "C:\\Users\\Documents\\demo.txt - 示例文件路径",
            "D:\\Projects\\paste-for-windows\\src\\main.py - 项目主文件",
            "E:\\工作\\项目报告.docx - 工作文档",
            "F:\\备份\\数据库备份.sql - 数据库备份文件",
            "G:\\下载\\重要文档.pdf - 下载的PDF文档",
            "H:\\图片\\工作截图.png - 工作截图",
            "I:\\音乐\\favorite_songs.mp3 - 音乐文件",
            "J:\\视频\\tutorial.mp4 - 教程视频",
            "K:\\代码\\web_project\\index.html - 网页文件",
            "L:\\文档\\技术手册.pdf - 技术文档",
            
            # 代码类型内容
            "def tray_demo():\n    print('托盘功能演示')\n    return True - 示例代码",
            "class TrayManager:\n    def __init__(self):\n        self.tray_icon = None\n    def show_tray(self):\n        # 显示托盘图标\n        pass - 托盘管理类",
            "async def tray_click_handler():\n    await show_notification('托盘被点击了')\n    return True - 异步点击处理",
            "def create_tray_menu():\n    menu = QMenu()\n    menu.addAction('显示窗口')\n    menu.addAction('退出')\n    return menu - 创建托盘菜单",
            "import os\nimport sys\n\ndef main():\n    print('托盘应用启动')\n    return 0\n\nif __name__ == '__main__':\n    main() - 主程序入口",
            "def show_notification(title, message):\n    from PyQt6.QtWidgets import QSystemTrayIcon\n    tray = QSystemTrayIcon()\n    tray.showMessage(title, message) - 显示通知",
            "class SystemTray:\n    def __init__(self, parent=None):\n        self.parent = parent\n        self.setup_tray()\n    def setup_tray(self):\n        # 设置托盘\n        pass - 系统托盘类",
            "def handle_tray_activation(reason):\n    if reason == QSystemTrayIcon.ActivationReason.Trigger:\n        show_main_window()\n    elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:\n        show_bottom_panel() - 托盘激活处理",
            "def create_context_menu():\n    context_menu = QMenu()\n    context_menu.addAction('设置')\n    context_menu.addSeparator()\n    context_menu.addAction('关于')\n    context_menu.addAction('退出')\n    return context_menu - 创建上下文菜单",
            "def tray_icon_clicked():\n    if main_window.isVisible():\n        main_window.hide()\n    else:\n        main_window.show()\n        main_window.raise_()\n        main_window.activateWindow() - 托盘图标点击处理",
            
            # 联系信息类型
            "电话号码：123-456-7890 - 联系人信息",
            "邮箱地址：demo@example.com - 演示邮箱",
            "微信：demo_wechat_123 - 微信联系方式",
            "QQ：987654321 - QQ号码",
            "地址：北京市朝阳区某某街道456号 - 联系地址",
            "公司电话：010-87654321 - 公司联系方式",
            "紧急联系人：李四 139-0000-0000 - 紧急联系信息",
            "客户邮箱：client@demo.com - 客户联系方式",
            "技术支持：support@demo.com - 技术支持邮箱",
            "招聘邮箱：hr@demo.com - 人力资源邮箱",
        ]
        
        for i, content in enumerate(test_items):
            item = ClipboardItem(id="", content=content)
            self.clipboard_manager._add_item(item)
        
        self.status_label.setText(f"✅ 已添加 {len(test_items)} 个测试项目 - 现在可以点击托盘图标测试滚动条功能")
    
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