#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快捷键演示脚本
演示 Alt+V 切换底部面板功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from src.utils.hotkey_manager import hotkey_manager
from src.gui.bottom_panel import BottomPanel


class DemoWindow(QMainWindow):
    """演示窗口"""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._setup_components()
        self._setup_hotkey()
    
    def _setup_ui(self):
        """设置界面"""
        self.setWindowTitle("快捷键演示 - Alt+V 切换底部面板")
        self.setMinimumSize(400, 300)
        self.resize(500, 400)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title_label = QLabel("Alt+V 快捷键演示")
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
        self.status_label = QLabel("正在启动快捷键管理器...")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #605e5c;
                text-align: center;
            }
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 说明信息
        info_label = QLabel(
            "演示说明：\n\n"
            "🎯 快捷键功能：\n"
            "• Alt+V - 显示/隐藏底部面板\n\n"
            "📋 测试步骤：\n"
            "1. 点击'显示底部面板'按钮\n"
            "2. 按 Alt+V 快捷键\n"
            "3. 观察底部面板的切换效果\n\n"
            "💡 提示：\n"
            "• 底部面板会从屏幕下方滑出\n"
            "• Alt+V 可以切换面板的显示状态\n"
            "• 也可以按 ESC 键关闭面板"
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
        
        # 按钮
        button_layout = QVBoxLayout()
        
        show_panel_button = QPushButton("显示底部面板")
        show_panel_button.setStyleSheet("""
            QPushButton {
                background: #0078d4;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #106ebe;
            }
            QPushButton:pressed {
                background: #005a9e;
            }
        """)
        show_panel_button.clicked.connect(self.show_bottom_panel)
        
        test_hotkey_button = QPushButton("测试 Alt+V 快捷键")
        test_hotkey_button.setStyleSheet("""
            QPushButton {
                background: #107c10;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #0e6e0e;
            }
            QPushButton:pressed {
                background: #0c5c0c;
            }
        """)
        test_hotkey_button.clicked.connect(self._test_hotkey)
        
        button_layout.addWidget(show_panel_button)
        button_layout.addWidget(test_hotkey_button)
        
        # 添加到布局
        layout.addWidget(title_label)
        layout.addWidget(self.status_label)
        layout.addWidget(info_label, 1)
        layout.addLayout(button_layout)
        
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
        # 创建底部面板
        self.bottom_panel = BottomPanel()
        
        # 连接底部面板信号
        self.bottom_panel.item_selected.connect(self._on_item_selected)
        self.bottom_panel.item_double_clicked.connect(self._on_item_double_clicked)
        self.bottom_panel.panel_closed.connect(self._on_panel_closed)
    
    def _setup_hotkey(self):
        """设置快捷键"""
        # 连接快捷键信号
        hotkey_manager.toggle_bottom_panel_requested.connect(self.toggle_bottom_panel)
        
        # 启动快捷键管理器
        if hotkey_manager.is_available():
            success = hotkey_manager.start()
            if success:
                self.status_label.setText("✅ 快捷键管理器已启动 - Alt+V 可用")
                self.status_label.setStyleSheet("""
                    QLabel {
                        font-size: 14px;
                        color: #107c10;
                        text-align: center;
                    }
                """)
            else:
                self.status_label.setText("❌ 快捷键管理器启动失败")
                self.status_label.setStyleSheet("""
                    QLabel {
                        font-size: 14px;
                        color: #d13438;
                        text-align: center;
                    }
                """)
        else:
            self.status_label.setText("❌ keyboard 模块不可用")
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #d13438;
                    text-align: center;
                }
            """)
    
    def show_bottom_panel(self):
        """显示底部面板"""
        print("🎯 显示底部面板")
        self.bottom_panel.show_panel()
        
        # 更新状态
        self.status_label.setText("✅ 底部面板已显示")
        QTimer.singleShot(2000, self._reset_status)
    
    def toggle_bottom_panel(self):
        """切换底部面板"""
        print("🎯 Alt+V 快捷键触发 - 切换底部面板")
        if self.bottom_panel.isVisible():
            self.bottom_panel.hide_panel()
            self.status_label.setText("✅ Alt+V 快捷键工作正常 - 隐藏面板")
        else:
            self.bottom_panel.show_panel()
            self.status_label.setText("✅ Alt+V 快捷键工作正常 - 显示面板")
        
        QTimer.singleShot(3000, self._reset_status)
    
    def _test_hotkey(self):
        """测试快捷键"""
        if hotkey_manager.is_available() and hotkey_manager.is_running():
            hotkeys = hotkey_manager.get_registered_hotkeys()
            status_text = f"✅ 快捷键管理器运行正常\n已注册快捷键：{len(hotkeys)} 个"
            for name, hotkey in hotkeys.items():
                status_text += f"\n• {hotkey} - {name}"
        else:
            status_text = "❌ 快捷键管理器未运行"
        
        self.status_label.setText(status_text)
        QTimer.singleShot(5000, self._reset_status)
    
    def _reset_status(self):
        """重置状态"""
        if hotkey_manager.is_running():
            self.status_label.setText("✅ 快捷键管理器运行中 - Alt+V 可用")
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #107c10;
                    text-align: center;
                }
            """)
        else:
            self.status_label.setText("❌ 快捷键管理器未运行")
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #d13438;
                    text-align: center;
                }
            """)
    
    def _on_item_selected(self, item):
        """项目被选中"""
        print(f"选中项目: {item.content[:50]}...")
    
    def _on_item_double_clicked(self, item):
        """项目双击"""
        print(f"双击项目: {item.content[:50]}...")
    
    def _on_panel_closed(self):
        """面板关闭"""
        print("底部面板已关闭")
    
    def closeEvent(self, event):
        """关闭事件"""
        hotkey_manager.stop()
        event.accept()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("快捷键演示")
    app.setApplicationVersion("1.0.0")
    
    # 创建演示窗口
    window = DemoWindow()
    window.show()
    
    print("🚀 Alt+V 快捷键演示程序已启动")
    print("📋 快捷键功能：")
    print("   - Alt+V - 显示/隐藏底部面板")
    print("")
    print("💡 使用提示：")
    print("   1. 点击'显示底部面板'按钮")
    print("   2. 按 Alt+V 测试切换功能")
    print("   3. 观察底部面板的切换效果")
    print("")
    
    # 运行应用程序
    exit_code = app.exec()
    
    # 清理资源
    hotkey_manager.stop()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main() 