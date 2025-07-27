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
            # 文本类型内容
            "这是一个测试文本内容，用于演示滚动条功能",
            "重要的会议记录：明天下午2点开会，讨论项目进展",
            "购物清单：牛奶、面包、鸡蛋、水果、蔬菜",
            "项目进度：第一阶段已完成，开始第二阶段开发",
            "待办事项：1. 完成文档 2. 测试功能 3. 部署应用",
            "工作笔记：今天完成了主要功能的开发",
            "学习计划：本周学习Python高级特性",
            "健康提醒：记得多喝水，适当运动",
            "财务记录：本月收入5000元，支出3000元",
            "旅行计划：下个月去北京旅游",
            
            # 链接类型内容
            "https://www.example.com - 示例链接",
            "https://github.com/microsoft/vscode - VS Code",
            "https://www.python.org/downloads/ - Python下载",
            "https://docs.python.org/3/tutorial/ - Python教程",
            "https://stackoverflow.com/questions/tagged/python - Python问题",
            "https://www.w3schools.com/python/ - Python学习",
            "https://realpython.com/ - 高质量教程",
            "https://pypi.org/ - Python包索引",
            "https://www.jetbrains.com/pycharm/ - PyCharm",
            "https://code.visualstudio.com/ - VS Code",
            
            # 文件类型内容
            "C:\\Users\\Documents\\test.txt - 测试文件",
            "D:\\Projects\\paste-for-windows\\src\\main.py - 主文件",
            "E:\\工作\\项目报告.docx - 工作文档",
            "F:\\备份\\数据库备份.sql - 数据库备份",
            "G:\\下载\\重要文档.pdf - PDF文档",
            "H:\\图片\\工作截图.png - 截图",
            "I:\\音乐\\favorite_songs.mp3 - 音乐文件",
            "J:\\视频\\tutorial.mp4 - 教程视频",
            "K:\\代码\\web_project\\index.html - 网页文件",
            "L:\\文档\\技术手册.pdf - 技术文档",
            
            # 代码类型内容
            "def hello_world():\n    print('Hello, World!') - 基础函数",
            "class Calculator:\n    def add(self, a, b):\n        return a + b - 计算器类",
            "async def fetch_data(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as response:\n            return await response.text() - 异步函数",
            "def quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quick_sort(left) + middle + quick_sort(right) - 排序算法",
            "import os\nimport sys\n\ndef main():\n    print('Hello from Python!')\n    return 0\n\nif __name__ == '__main__':\n    main() - 主程序",
            "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2) - 斐波那契",
            "class Database:\n    def __init__(self, connection_string):\n        self.connection_string = connection_string\n    def connect(self):\n        pass - 数据库类",
            "def validate_email(email):\n    import re\n    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'\n    return re.match(pattern, email) is not None - 邮箱验证",
            "def read_file(file_path):\n    try:\n        with open(file_path, 'r', encoding='utf-8') as f:\n            return f.read()\n    except FileNotFoundError:\n        return None - 文件读取",
            "def send_email(to, subject, body):\n    import smtplib\n    from email.mime.text import MIMEText\n    msg = MIMEText(body)\n    msg['Subject'] = subject\n    msg['From'] = 'sender@example.com'\n    msg['To'] = to - 邮件发送",
            
            # 联系信息类型
            "电话号码：123-456-7890 - 联系人信息",
            "邮箱地址：test@example.com - 邮箱",
            "微信：wechat_id_123 - 微信",
            "QQ：123456789 - QQ号码",
            "地址：北京市朝阳区某某街道123号 - 地址",
            "公司电话：010-12345678 - 公司电话",
            "紧急联系人：张三 138-0000-0000 - 紧急联系",
            "客户邮箱：customer@company.com - 客户邮箱",
            "技术支持：support@tech.com - 技术支持",
            "招聘邮箱：hr@company.com - 招聘邮箱",
        ]
        
        for i, content in enumerate(test_items):
            item = ClipboardItem(id="", content=content)
            self.clipboard_manager._add_item(item)
        
        self.status_label.setText(f"✅ 已添加 {len(test_items)} 个测试项目 - 现在可以测试滚动条功能了")
    
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