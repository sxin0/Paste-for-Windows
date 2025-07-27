#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快捷键功能测试脚本
测试 Alt+V 快捷键唤起主窗口功能
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


class TestWindow(QMainWindow):
    """测试窗口"""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._setup_hotkey()
    
    def _setup_ui(self):
        """设置界面"""
        self.setWindowTitle("快捷键测试窗口")
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
        title_label = QLabel("快捷键功能测试")
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
            "快捷键测试说明：\n\n"
            "🎯 测试快捷键：\n"
            "• Alt+V - 显示/隐藏底部面板\n\n"
            "📋 测试步骤：\n"
            "1. 最小化此窗口\n"
            "2. 按 Alt+V 快捷键\n"
            "3. 观察底部面板是否切换\n\n"
            "⚠️ 注意事项：\n"
            "• 确保已安装 keyboard 模块\n"
            "• 某些应用可能会拦截快捷键\n"
            "• 如果快捷键不工作，请检查权限设置"
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
        
        # 测试按钮
        test_button = QPushButton("测试快捷键状态")
        test_button.setStyleSheet("""
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
        test_button.clicked.connect(self._test_hotkey_status)
        
        # 添加到布局
        layout.addWidget(title_label)
        layout.addWidget(self.status_label)
        layout.addWidget(info_label, 1)
        layout.addWidget(test_button)
        
        # 设置全局样式
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 rgb(255,255,255),
                                          stop:1 rgb(255,255,255));
            }
        """)
    
    def _setup_hotkey(self):
        """设置快捷键"""
        # 连接快捷键信号
        hotkey_manager.toggle_bottom_panel_requested.connect(self._on_toggle_bottom_panel)
        
        # 启动快捷键管理器
        if hotkey_manager.is_available():
            success = hotkey_manager.start()
            if success:
                self.status_label.setText("✅ 快捷键管理器已启动")
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
    
    def _on_toggle_bottom_panel(self):
        """Alt+V 快捷键回调"""
        print("🎯 Alt+V 快捷键触发 - 切换底部面板")
        self.status_label.setText("✅ Alt+V 快捷键工作正常！")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #107c10;
                text-align: center;
            }
        """)
        QTimer.singleShot(3000, self._reset_status)
    
    def _reset_status(self):
        """重置状态"""
        if hotkey_manager.is_running():
            self.status_label.setText("✅ 快捷键管理器运行中")
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
    
    def _test_hotkey_status(self):
        """测试快捷键状态"""
        if hotkey_manager.is_available():
            if hotkey_manager.is_running():
                hotkeys = hotkey_manager.get_registered_hotkeys()
                status_text = f"✅ 快捷键管理器运行中\n已注册快捷键：{len(hotkeys)} 个"
                for name, hotkey in hotkeys.items():
                    status_text += f"\n• {hotkey} - {name}"
            else:
                status_text = "❌ 快捷键管理器未运行"
        else:
            status_text = "❌ keyboard 模块不可用"
        
        self.status_label.setText(status_text)
    
    def closeEvent(self, event):
        """关闭事件"""
        hotkey_manager.stop()
        event.accept()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("快捷键测试")
    app.setApplicationVersion("1.0.0")
    
    # 创建测试窗口
    window = TestWindow()
    window.show()
    
    print("🚀 快捷键测试程序已启动")
    print("📋 测试快捷键：")
    print("   - Alt+V - 显示/隐藏底部面板")
    print("")
    print("💡 使用提示：")
    print("   1. 最小化窗口")
    print("   2. 按 Alt+V 测试切换功能")
    print("   3. 观察底部面板是否被正确切换")
    print("")
    
    # 运行应用程序
    exit_code = app.exec()
    
    # 清理资源
    hotkey_manager.stop()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main() 