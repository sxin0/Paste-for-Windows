#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试滚轮滚动功能
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from src.gui.bottom_panel import BottomPanel
from src.core.clipboard_manager import ClipboardManager, ClipboardItem
from datetime import datetime, timedelta

class WheelScrollTestWindow(QMainWindow):
    """滚轮滚动测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("滚轮滚动功能测试")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # 创建剪贴板管理器
        self.clipboard_manager = ClipboardManager()
        
        # 创建底部面板
        self.bottom_panel = BottomPanel(self.clipboard_manager)
        
        # 设置UI
        self.setup_ui()
        
        # 连接信号
        self.bottom_panel.item_selected.connect(self.on_item_selected)
        self.bottom_panel.panel_closed.connect(self.on_panel_closed)
    
    def setup_ui(self):
        """设置UI"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title = QLabel("滚轮滚动功能测试")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            margin-bottom: 20px; 
            color: #333;
            text-align: center;
        """)
        main_layout.addWidget(title)
        
        # 说明文字
        description = QLabel("这个测试专门用于验证滚轮滚动功能。添加测试数据后，在底部面板中使用鼠标滚轮来横向滚动卡片。")
        description.setStyleSheet("""
            font-size: 14px; 
            color: #666; 
            margin-bottom: 30px;
            text-align: center;
        """)
        description.setWordWrap(True)
        main_layout.addWidget(description)
        
        # 功能说明
        features = QLabel("""
🎯 滚轮滚动功能特点：
• 向上滚动滚轮 → 向左移动卡片
• 向下滚动滚轮 → 向右移动卡片
• 滚动步长根据滚轮角度自动调整
• 支持在面板任何位置使用滚轮
• 只有在有水平滚动条时才生效
        """)
        features.setStyleSheet("""
            font-size: 12px; 
            color: #555; 
            margin-bottom: 20px;
            padding: 15px;
            background: #f5f5f5;
            border-radius: 8px;
            border-left: 4px solid #0078d4;
        """)
        main_layout.addWidget(features)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        # 添加测试数据按钮
        self.add_data_btn = QPushButton("添加测试数据 (30个)")
        self.add_data_btn.setMinimumHeight(50)
        self.add_data_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #4CAF50, stop:1 #45a049);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #45a049, stop:1 #3d8b40);
            }
        """)
        self.add_data_btn.clicked.connect(self.add_test_data)
        
        # 显示底部面板按钮
        self.show_panel_btn = QPushButton("显示底部面板")
        self.show_panel_btn.setMinimumHeight(50)
        self.show_panel_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #2196F3, stop:1 #1976D2);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #1976D2, stop:1 #1565C0);
            }
        """)
        self.show_panel_btn.clicked.connect(self.show_bottom_panel)
        
        # 清空数据按钮
        self.clear_data_btn = QPushButton("清空数据")
        self.clear_data_btn.setMinimumHeight(50)
        self.clear_data_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #F44336, stop:1 #D32F2F);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #D32F2F, stop:1 #C62828);
            }
        """)
        self.clear_data_btn.clicked.connect(self.clear_all_data)
        
        # 添加按钮到布局
        button_layout.addWidget(self.add_data_btn)
        button_layout.addWidget(self.show_panel_btn)
        button_layout.addWidget(self.clear_data_btn)
        
        main_layout.addLayout(button_layout)
        
        # 测试说明
        test_instructions = QLabel("""
🧪 测试步骤：
1. 点击"添加测试数据"按钮添加30个测试卡片
2. 点击"显示底部面板"按钮显示底部面板
3. 在底部面板中使用鼠标滚轮进行横向滚动
4. 观察滚动是否流畅，方向是否正确
5. 测试在不同位置使用滚轮的效果
        """)
        test_instructions.setStyleSheet("""
            font-size: 12px; 
            color: #666; 
            margin-top: 20px;
            padding: 15px;
            background: #fff3cd;
            border-radius: 8px;
            border-left: 4px solid #ffc107;
        """)
        main_layout.addWidget(test_instructions)
        
        # 状态标签
        self.status_label = QLabel("准备就绪 - 点击按钮开始测试滚轮滚动功能")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            color: #666; 
            font-size: 14px; 
            margin-top: 20px;
            padding: 10px;
            background: #f5f5f5;
            border-radius: 10px;
        """)
        main_layout.addWidget(self.status_label)
        
        # 添加弹性空间
        main_layout.addStretch()
        
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 rgba(255,255,255,0.95),
                                          stop:1 rgba(240,240,240,0.95));
            }
        """)
    
    def add_test_data(self):
        """添加测试数据"""
        # 清空现有数据
        self.clipboard_manager.clear_all()
        
        # 生成测试数据
        test_items = []
        for i in range(30):
            # 根据索引生成不同类型的内容
            item_type = i % 5  # 5种类型循环
            
            if item_type == 0:  # 文本类型
                content = f"文本内容 {i+1}：这是一个测试文本，用来验证滚轮滚动功能。这是第{i+1}个文本类型的卡片。"
                content_type = "text"
            elif item_type == 1:  # 链接类型
                content = f"https://example{i+1}.com - 这是第{i+1}个链接"
                content_type = "link"
            elif item_type == 2:  # 代码类型
                content = f"def test_function_{i+1}():\n    print('这是第{i+1}个代码片段')\n    return True"
                content_type = "code"
            elif item_type == 3:  # 文件类型
                content = f"C:\\Users\\Documents\\test_file_{i+1}.txt - 第{i+1}个文件"
                content_type = "file"
            else:  # 图片类型
                content = f"图片文件：test_image_{i+1}.png ({i+1}.{i%10}MB)"
                content_type = "image"
            
            # 创建时间，从最新到最旧
            timestamp = datetime.now() - timedelta(minutes=30-i)
            
            item = ClipboardItem(f"test_{i+1}", content, content_type, timestamp)
            test_items.append(item)
        
        # 添加测试项目到剪贴板管理器
        for item in test_items:
            self.clipboard_manager._add_item(item)
        
        self.status_label.setText("✅ 已添加 30 个测试数据 - 现在可以显示底部面板测试滚轮滚动功能")
    
    def show_bottom_panel(self):
        """显示底部面板"""
        self.status_label.setText("🎬 正在显示底部面板...")
        self.bottom_panel.show_panel()
    
    def clear_all_data(self):
        """清空所有数据"""
        self.clipboard_manager.clear_all()
        self.status_label.setText("🗑️ 已清空所有数据")
    
    def on_item_selected(self, item):
        """项目被选中"""
        self.status_label.setText(f"✅ 已选择: {item.content[:50]}...")
    
    def on_panel_closed(self):
        """面板关闭"""
        self.status_label.setText("🔒 底部面板已关闭")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("滚轮滚动功能测试")
    app.setApplicationVersion("1.0.0")
    
    window = WheelScrollTestWindow()
    window.show()
    
    print("🎯 滚轮滚动功能测试已启动！")
    print("📋 这个测试专门用于验证滚轮滚动功能")
    print("🔄 测试滚轮在底部面板中的横向滚动效果")
    print("")
    print("📝 测试步骤：")
    print("1. 点击'添加测试数据'按钮")
    print("2. 点击'显示底部面板'按钮")
    print("3. 在底部面板中使用鼠标滚轮")
    print("4. 观察横向滚动效果")
    print("5. 测试滚轮滚动的流畅度")
    
    return app.exec()


if __name__ == "__main__":
    main() 