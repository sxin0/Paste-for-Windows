#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alt+V 快捷键测试脚本
测试 Alt+V 显示/隐藏底部面板功能
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


class AltVTestWindow(QMainWindow):
    """Alt+V 测试窗口"""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._setup_components()
        self._setup_hotkey()
    
    def _setup_ui(self):
        """设置界面"""
        self.setWindowTitle("Alt+V 快捷键测试")
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
        title_label = QLabel("Alt+V 快捷键测试")
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
            "测试说明：\n\n"
            "🎯 Alt+V 快捷键功能：\n"
            "• 第一次按 Alt+V - 显示底部面板\n"
            "• 再次按 Alt+V - 隐藏底部面板\n"
            "• 按 ESC 键 - 关闭面板\n\n"
            "📋 测试步骤：\n"
            "1. 点击'显示底部面板'按钮\n"
            "2. 按 Alt+V 快捷键\n"
            "3. 观察面板的显示/隐藏效果\n"
            "4. 再次按 Alt+V 测试隐藏功能\n\n"
            "💡 预期效果：\n"
            "• Alt+V 应该能够切换面板状态\n"
            "• 面板应该有流畅的滑入/滑出动画\n"
            "• 状态栏应该显示当前操作结果"
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
        
        test_alt_v_button = QPushButton("测试 Alt+V 快捷键")
        test_alt_v_button.setStyleSheet("""
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
        test_alt_v_button.clicked.connect(self._test_alt_v)
        
        button_layout.addWidget(show_panel_button)
        button_layout.addWidget(test_alt_v_button)
        
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
            self.status_label.setText("✅ Alt+V 工作正常 - 隐藏面板")
        else:
            self.bottom_panel.show_panel()
            self.status_label.setText("✅ Alt+V 工作正常 - 显示面板")
        
        QTimer.singleShot(3000, self._reset_status)
    
    def _test_alt_v(self):
        """测试 Alt+V 快捷键"""
        if hotkey_manager.is_available() and hotkey_manager.is_running():
            hotkeys = hotkey_manager.get_registered_hotkeys()
            status_text = f"✅ Alt+V 快捷键已注册\n当前快捷键："
            for name, hotkey in hotkeys.items():
                status_text += f"\n• {hotkey} - {name}"
            status_text += "\n\n💡 现在可以按 Alt+V 测试功能"
        else:
            status_text = "❌ Alt+V 快捷键未注册"
        
        self.status_label.setText(status_text)
        QTimer.singleShot(5000, self._reset_status)
    
    def _reset_status(self):
        """重置状态"""
        if hotkey_manager.is_running():
            panel_status = "显示中" if self.bottom_panel.isVisible() else "隐藏中"
            self.status_label.setText(f"✅ 快捷键管理器运行中 - Alt+V 可用 (面板状态: {panel_status})")
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
    app.setApplicationName("Alt+V 测试")
    app.setApplicationVersion("1.0.0")
    
    # 创建测试窗口
    window = AltVTestWindow()
    window.show()
    
    print("🚀 Alt+V 快捷键测试程序已启动")
    print("📋 测试功能：")
    print("   - Alt+V - 显示/隐藏底部面板")
    print("")
    print("💡 测试步骤：")
    print("   1. 点击'显示底部面板'按钮")
    print("   2. 按 Alt+V 测试切换功能")
    print("   3. 观察面板的显示/隐藏效果")
    print("   4. 再次按 Alt+V 测试隐藏功能")
    print("")
    
    # 运行应用程序
    exit_code = app.exec()
    
    # 清理资源
    hotkey_manager.stop()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main() 