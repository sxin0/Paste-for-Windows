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
            # 文本类型内容
            "这是一个测试文本内容，用于演示搜索功能和滚动条效果",
            "重要的会议记录：明天下午2点开会，讨论项目进展和下一步计划",
            "购物清单：牛奶、面包、鸡蛋、水果、蔬菜、肉类、调味品等日常用品",
            "项目进度：第一阶段已完成，开始第二阶段开发，预计下周完成",
            "待办事项：1. 完成文档 2. 测试功能 3. 部署应用 4. 用户培训",
            "工作笔记：今天完成了主要功能的开发，明天需要测试和优化",
            "学习计划：本周学习Python高级特性，下周开始学习Web开发",
            "健康提醒：记得多喝水，适当运动，保持良好作息",
            "财务记录：本月收入5000元，支出3000元，结余2000元",
            "旅行计划：下个月去北京旅游，需要提前订票和酒店",
            
            # 链接类型内容
            "https://www.example.com - 这是一个示例链接",
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
            "C:\\Users\\Documents\\important_file.txt - 重要文件路径",
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
            "def hello_world():\n    print('Hello, World!')\n    return True - 代码片段",
            "class Calculator:\n    def add(self, a, b):\n        return a + b\n    def multiply(self, a, b):\n        return a * b - 计算器类",
            "async def fetch_data(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as response:\n            return await response.text() - 异步函数",
            "def quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quick_sort(left) + middle + quick_sort(right) - 快速排序算法",
            "import os\nimport sys\n\ndef main():\n    print('Hello from Python!')\n    return 0\n\nif __name__ == '__main__':\n    main() - 主程序入口",
            "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2) - 斐波那契数列",
            "class Database:\n    def __init__(self, connection_string):\n        self.connection_string = connection_string\n    def connect(self):\n        # 连接数据库\n        pass - 数据库类",
            "def validate_email(email):\n    import re\n    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'\n    return re.match(pattern, email) is not None - 邮箱验证函数",
            "def read_file(file_path):\n    try:\n        with open(file_path, 'r', encoding='utf-8') as f:\n            return f.read()\n    except FileNotFoundError:\n        return None - 文件读取函数",
            "def send_email(to, subject, body):\n    import smtplib\n    from email.mime.text import MIMEText\n    msg = MIMEText(body)\n    msg['Subject'] = subject\n    msg['From'] = 'sender@example.com'\n    msg['To'] = to - 邮件发送函数",
            
            # 联系信息类型
            "电话号码：123-456-7890 - 联系人信息",
            "邮箱地址：test@example.com - 邮箱",
            "微信：wechat_id_123 - 微信联系方式",
            "QQ：123456789 - QQ号码",
            "地址：北京市朝阳区某某街道123号 - 联系地址",
            "公司电话：010-12345678 - 公司联系方式",
            "紧急联系人：张三 138-0000-0000 - 紧急联系信息",
            "客户邮箱：customer@company.com - 客户联系方式",
            "技术支持：support@tech.com - 技术支持邮箱",
            "招聘邮箱：hr@company.com - 人力资源邮箱",
        ]
        
        for i, content in enumerate(test_items):
            item = ClipboardItem(id="", content=content)
            self.clipboard_manager._add_item(item)
        
        self.status_label.setText(f"✅ 已添加 {len(test_items)} 个测试项目 - 现在可以测试滚动条功能了")
    
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