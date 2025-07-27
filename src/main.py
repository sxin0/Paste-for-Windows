#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paste for Windows - 主应用程序
第一阶段：基础功能实现
"""

import sys
import os
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.clipboard_manager import ClipboardManager
from src.core.config_manager import ConfigManager
from src.data.database import DatabaseManager
from src.gui.bottom_panel import BottomPanel
from src.gui.system_tray import SystemTray


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._setup_components()
        self._connect_signals()
    
    def _setup_ui(self):
        """设置界面"""
        self.setWindowTitle("Paste for Windows")
        self.setMinimumSize(400, 300)
        self.resize(600, 400)
        
        # 设置窗口标志
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinMaxButtonsHint)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title_label = QLabel("Paste for Windows")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #0078d4;
                text-align: center;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 状态信息
        self.status_label = QLabel("正在启动...")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #605e5c;
                text-align: center;
            }
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 提示信息
        info_label = QLabel(
            "剪贴板管理器已启动\n\n"
            "使用说明：\n"
            "• 按 Win+V 显示剪贴板历史\n"
            "• 双击系统托盘图标显示主窗口\n"
            "• 右键系统托盘图标查看更多选项\n\n"
            "当前功能：\n"
            "• 实时剪贴板监听\n"
            "• 文本内容存储\n"
            "• 基础搜索功能\n"
            "• 系统托盘集成\n"
            "• 颜色分类卡片边框\n\n"
            "🎨 卡片效果：\n"
            "• 文本：蓝色边框\n"
            "• 链接：绿色边框\n"
            "• 代码：紫色边框\n"
            "• 文件：红色边框\n"
            "• 图片：橙色边框"
        )
        info_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #323130;
                line-height: 1.5;
                padding: 20px;
                background: rgb(255, 255, 255);
                border-radius: 8px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
        """)
        info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        info_label.setWordWrap(True)
        
        # 添加到布局
        layout.addWidget(title_label)
        layout.addWidget(self.status_label)
        layout.addWidget(info_label, 1)
        
        # 设置全局样式
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 rgb(255,255,255),
                                          stop:1 rgb(255,255,255));
            }
        """)
    
    def _setup_components(self):
        """设置组件"""
        # 配置管理器
        self.config_manager = ConfigManager()
        
        # 数据库管理器
        self.database_manager = DatabaseManager()
        
        # 剪贴板管理器
        self.clipboard_manager = ClipboardManager()
        
        # 系统托盘
        self.system_tray = SystemTray(self.clipboard_manager)
        
        # 底部面板
        self.bottom_panel = BottomPanel(self.clipboard_manager)
        
        # 启动剪贴板监听
        self.clipboard_manager.start()
        
        # 显示系统托盘
        if self.system_tray.is_system_tray_available():
            self.system_tray.show()
        
        # 更新状态
        self._update_status()
        
        # 添加测试卡片（仅在开发模式下）
        self._add_test_cards()
    
    def _connect_signals(self):
        """连接信号"""
        # 系统托盘信号
        self.system_tray.show_window_requested.connect(self.show_main_window)
        self.system_tray.show_bottom_panel_requested.connect(self.show_bottom_panel)
        self.system_tray.toggle_bottom_panel_requested.connect(self.toggle_bottom_panel)
        self.system_tray.quit_requested.connect(self.quit_application)
        
        # 底部面板信号
        self.bottom_panel.item_selected.connect(self._on_item_selected)
        
        # 剪贴板管理器信号
        self.clipboard_manager.item_added.connect(self._on_item_added)
        self.clipboard_manager.error_occurred.connect(self._on_error)
    
    def _update_status(self):
        """更新状态信息"""
        stats = self.clipboard_manager.get_stats()
        status_text = f"已监听 {stats['total_items']} 个项目"
        
        if self.clipboard_manager._is_enabled:
            status_text += " | 监听中"
        else:
            status_text += " | 已停止"
        
        self.status_label.setText(status_text)
    
    def _on_item_added(self, item):
        """新项目添加"""
        self._update_status()
        # 可以在这里添加通知或其他反馈
    
    def _on_item_selected(self, item):
        """项目被选中"""
        # 将选中的内容复制到剪贴板
        import win32clipboard
        import win32con
        
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, item.content)
            win32clipboard.CloseClipboard()
            
            # 显示通知
            self.system_tray.show_message(
                "内容已复制",
                f"已复制到剪贴板：{item.content[:50]}{'...' if len(item.content) > 50 else ''}"
            )
            
        except Exception as e:
            print(f"复制到剪贴板失败: {e}")
    
    def _on_error(self, error_message: str):
        """错误处理"""
        print(f"错误: {error_message}")
        self.system_tray.show_message("错误", error_message)
    
    def _add_test_cards(self):
        """添加测试卡片"""
        from datetime import datetime, timedelta
        from src.core.clipboard_manager import ClipboardItem
        
        # 创建测试数据
        test_items = [
            # 基础测试卡片
            ClipboardItem(
                "test_text_1", 
                "这是一段测试文本内容，用来展示文本类型卡片的边框效果。文本类型使用蓝色边框。", 
                "text", 
                datetime.now() - timedelta(minutes=25)
            ),
            ClipboardItem(
                "test_link_1", 
                "https://www.example.com", 
                "link", 
                datetime.now() - timedelta(minutes=24)
            ),
            ClipboardItem(
                "test_code_1", 
                "print('Hello, World!')\ndef main():\n    print('这是一个代码示例')", 
                "code", 
                datetime.now() - timedelta(minutes=23)
            ),
            ClipboardItem(
                "test_file_1", 
                "C:\\Users\\Documents\\important_document.txt", 
                "file", 
                datetime.now() - timedelta(minutes=22)
            ),
            ClipboardItem(
                "test_image_1", 
                "图片文件：screenshot.png (2.5MB)", 
                "image", 
                datetime.now() - timedelta(minutes=21)
            ),
            
            # 更多文本类型卡片
            ClipboardItem(
                "test_text_2", 
                "这是另一个文本类型的卡片，用来测试多个相同类型卡片的显示效果。", 
                "text", 
                datetime.now() - timedelta(minutes=20)
            ),
            ClipboardItem(
                "test_text_3", 
                "会议记录：明天下午2点开会，讨论项目进展和下一步计划。", 
                "text", 
                datetime.now() - timedelta(minutes=19)
            ),
            ClipboardItem(
                "test_text_4", 
                "购物清单：牛奶、面包、鸡蛋、水果、蔬菜、肉类、调味品等日常用品。", 
                "text", 
                datetime.now() - timedelta(minutes=18)
            ),
            ClipboardItem(
                "test_text_5", 
                "重要提醒：记得备份重要文件，检查系统更新，整理桌面文件。", 
                "text", 
                datetime.now() - timedelta(minutes=17)
            ),
            
            # 更多链接类型卡片
            ClipboardItem(
                "test_link_2", 
                "https://github.com/microsoft/vscode", 
                "link", 
                datetime.now() - timedelta(minutes=16)
            ),
            ClipboardItem(
                "test_link_3", 
                "https://www.python.org/downloads/", 
                "link", 
                datetime.now() - timedelta(minutes=15)
            ),
            ClipboardItem(
                "test_link_4", 
                "https://docs.python.org/3/tutorial/", 
                "link", 
                datetime.now() - timedelta(minutes=14)
            ),
            ClipboardItem(
                "test_link_5", 
                "https://stackoverflow.com/questions/tagged/python", 
                "link", 
                datetime.now() - timedelta(minutes=13)
            ),
            
            # 更多代码类型卡片
            ClipboardItem(
                "test_code_2", 
                "import os\nimport sys\n\ndef hello_world():\n    print('Hello, World!')\n    return True", 
                "code", 
                datetime.now() - timedelta(minutes=12)
            ),
            ClipboardItem(
                "test_code_3", 
                "class Calculator:\n    def add(self, a, b):\n        return a + b\n    \n    def multiply(self, a, b):\n        return a * b", 
                "code", 
                datetime.now() - timedelta(minutes=11)
            ),
            ClipboardItem(
                "test_code_4", 
                "async def fetch_data(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as response:\n            return await response.text()", 
                "code", 
                datetime.now() - timedelta(minutes=10)
            ),
            ClipboardItem(
                "test_code_5", 
                "def quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quick_sort(left) + middle + quick_sort(right)", 
                "code", 
                datetime.now() - timedelta(minutes=9)
            ),
            
            # 更多文件类型卡片
            ClipboardItem(
                "test_file_2", 
                "D:\\Projects\\paste-for-windows\\src\\main.py", 
                "file", 
                datetime.now() - timedelta(minutes=8)
            ),
            ClipboardItem(
                "test_file_3", 
                "C:\\Users\\Documents\\工作\\项目报告.docx", 
                "file", 
                datetime.now() - timedelta(minutes=7)
            ),
            ClipboardItem(
                "test_file_4", 
                "E:\\Downloads\\重要文档.pdf", 
                "file", 
                datetime.now() - timedelta(minutes=6)
            ),
            ClipboardItem(
                "test_file_5", 
                "F:\\备份\\数据库备份.sql", 
                "file", 
                datetime.now() - timedelta(minutes=5)
            ),
            
            # 更多图片类型卡片
            ClipboardItem(
                "test_image_2", 
                "图片文件：工作截图.png (1.8MB)", 
                "image", 
                datetime.now() - timedelta(minutes=4)
            ),
            ClipboardItem(
                "test_image_3", 
                "图片文件：会议照片.jpg (3.2MB)", 
                "image", 
                datetime.now() - timedelta(minutes=3)
            ),
            ClipboardItem(
                "test_image_4", 
                "图片文件：设计稿.psd (15.7MB)", 
                "image", 
                datetime.now() - timedelta(minutes=2)
            ),
            ClipboardItem(
                "test_image_5", 
                "图片文件：图标集.svg (256KB)", 
                "image", 
                datetime.now() - timedelta(minutes=1)
            ),
            
            # 最后几个测试卡片
            ClipboardItem(
                "test_mixed_1", 
                "这是一个混合内容的测试：包含文本、链接 https://example.com 和代码片段 print('test')", 
                "text", 
                datetime.now()
            ),
        ]
        
        # 添加测试项目到剪贴板管理器
        for item in test_items:
            self.clipboard_manager._add_item(item)
        
        print("✅ 已添加测试卡片，包含以下类型：")
        print("   - 文本类型（蓝色边框）")
        print("   - 链接类型（绿色边框）")
        print("   - 代码类型（紫色边框）")
        print("   - 文件类型（红色边框）")
        print("   - 图片类型（橙色边框）")
        print(f"   📊 总计 {len(test_items)} 个测试卡片")
        print("   🔄 现在可以测试滚动条功能了")
        print("   按 Win+V 或点击托盘图标查看卡片效果")
    
    def show_main_window(self):
        """显示主窗口"""
        self.show()
        self.raise_()
        self.activateWindow()
    
    def show_bottom_panel(self):
        """显示底部面板"""
        self.bottom_panel.show_panel()
    
    def toggle_bottom_panel(self):
        """切换底部面板显示状态"""
        if self.bottom_panel.isVisible():
            self.bottom_panel.hide_panel()
        else:
            self.bottom_panel.show_panel()
    
    def quit_application(self):
        """退出应用程序"""
        # 显示确认对话框
        from PyQt6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self,
            "确认退出",
            "确定要退出 Paste for Windows 吗？\n\n退出后剪贴板监听将停止。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 清理资源
            self.clipboard_manager.stop()
            self.database_manager.close()
            self.system_tray.hide()
            
            # 退出应用程序
            QApplication.quit()
    
    def closeEvent(self, event):
        """关闭事件"""
        # 如果系统托盘可用，最小化到托盘而不是关闭
        if self.system_tray.is_system_tray_available() and self.system_tray.is_visible():
            self.hide()
            event.ignore()
        else:
            # 清理资源
            self.clipboard_manager.stop()
            self.database_manager.close()
            event.accept()


class PasteForWindowsApp:
    """Paste for Windows 应用程序"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = None
        
        # 设置应用程序信息
        self.app.setApplicationName("Paste for Windows")
        self.app.setApplicationVersion("1.0.0")
        self.app.setOrganizationName("PasteForWindows")
        
        # 设置应用程序图标
        # self.app.setWindowIcon(QIcon("resources/icons/app_icon.png"))
    
    def run(self):
        """运行应用程序"""
        try:
            # 创建主窗口
            self.main_window = MainWindow()
            
            # 显示主窗口
            self.main_window.show()
            
            # 运行应用程序
            return self.app.exec()
            
        except Exception as e:
            print(f"应用程序启动失败: {e}")
            return 1
    
    def cleanup(self):
        """清理资源"""
        if self.main_window:
            self.main_window.clipboard_manager.stop()
            self.main_window.database_manager.close()


def main():
    """主函数"""
    app = PasteForWindowsApp()
    
    try:
        exit_code = app.run()
    except KeyboardInterrupt:
        print("应用程序被用户中断")
        exit_code = 0
    except Exception as e:
        print(f"应用程序异常退出: {e}")
        exit_code = 1
    finally:
        app.cleanup()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main() 