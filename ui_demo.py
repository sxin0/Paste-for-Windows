#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paste for Windows - UI 演示示例
展示现代化界面的实现
"""

import sys
import os
from datetime import datetime
from typing import List, Dict, Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QListWidget, QListWidgetItem,
    QFrame, QScrollArea, QSplitter, QTabWidget, QComboBox,
    QSlider, QCheckBox, QSpinBox, QFormLayout, QDialog,
    QGraphicsDropShadowEffect, QSizePolicy
)
from PyQt6.QtCore import (
    QPropertyAnimation, QEasingCurve, QTimer, QSize,
    pyqtSignal, QThread, pyqtSlot
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (
    QPixmap, QPainter, QColor, QFont, QIcon, QPalette,
    QLinearGradient, QBrush, QPen
)

# 模拟数据
class ClipboardItem:
    """剪贴板项目数据模型"""
    
    def __init__(self, content: str, content_type: str = "text", 
                 created_at: Optional[datetime] = None, is_favorite: bool = False):
        self.id = f"item_{id(self)}"
        self.content = content
        self.content_type = content_type
        self.created_at = created_at or datetime.now()
        self.is_favorite = is_favorite
        self.preview = self._generate_preview()
    
    def _generate_preview(self) -> str:
        """生成预览内容"""
        if len(self.content) > 100:
            return self.content[:100] + "..."
        return self.content
    
    def get_type_icon(self) -> str:
        """获取类型图标"""
        icons = {
            "text": "📝",
            "image": "🖼️",
            "file": "📁",
            "link": "🔗",
            "code": "💻"
        }
        return icons.get(self.content_type, "📄")
    
    def format_time(self) -> str:
        """格式化时间"""
        now = datetime.now()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"{diff.days}天前"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}小时前"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60}分钟前"
        else:
            return "刚刚"

class ModernButton(QPushButton):
    """现代化按钮组件"""
    
    def __init__(self, text: str = "", icon: str = "", parent=None):
        super().__init__(text, parent)
        self.icon_text = icon
        self._setup_ui()
    
    def _setup_ui(self):
        """设置界面"""
        self.setMinimumHeight(36)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # 设置样式
        self.setStyleSheet("""
            ModernButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #0078d4,
                                          stop:1 #106ebe);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 500;
                font-size: 14px;
            }
            ModernButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #106ebe,
                                          stop:1 #005a9e);
            }
            ModernButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #005a9e,
                                          stop:1 #004578);
            }
        """)
    
    def paintEvent(self, event):
        """自定义绘制"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制背景
        rect = self.rect()
        gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        
        if self.isDown():
            gradient.setColorAt(0, QColor("#005a9e"))
            gradient.setColorAt(1, QColor("#004578"))
        elif self.underMouse():
            gradient.setColorAt(0, QColor("#106ebe"))
            gradient.setColorAt(1, QColor("#005a9e"))
        else:
            gradient.setColorAt(0, QColor("#0078d4"))
            gradient.setColorAt(1, QColor("#106ebe"))
        
        painter.fillRect(rect, gradient)
        
        # 绘制文本
        painter.setPen(QColor("white"))
        painter.setFont(self.font())
        
        # 如果有图标，绘制图标
        if self.icon_text:
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{self.icon_text} {self.text()}")
        else:
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())

class SearchBar(QWidget):
    """现代化搜索栏"""
    
    search_requested = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """设置界面"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(12)
        
        # 搜索输入框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索剪贴板内容...")
        self.search_input.setMinimumHeight(40)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 20px;
                padding: 8px 16px;
                font-size: 14px;
                background: rgba(255, 255, 255, 0.9);
                selection-background-color: #0078d4;
            }
            QLineEdit:focus {
                border-color: #0078d4;
                background: rgba(255, 255, 255, 0.95);
            }
        """)
        
        # 过滤按钮
        self.filter_btn = ModernButton("筛选", "🔽")
        self.filter_btn.setFixedWidth(80)
        
        # 添加到布局
        layout.addWidget(self.search_input, 1)
        layout.addWidget(self.filter_btn)
        
        # 连接信号
        self.search_input.textChanged.connect(self.search_requested.emit)

class ClipboardItemWidget(QWidget):
    """剪贴板项目卡片"""
    
    item_clicked = pyqtSignal(ClipboardItem)
    favorite_toggled = pyqtSignal(ClipboardItem, bool)
    
    def __init__(self, item: ClipboardItem, parent=None):
        super().__init__(parent)
        self.item = item
        self._setup_ui()
    
    def _setup_ui(self):
        """设置界面"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)
        
        # 类型图标
        self.type_icon = QLabel(self.item.get_type_icon())
        self.type_icon.setFixedSize(32, 32)
        self.type_icon.setStyleSheet("""
            QLabel {
                font-size: 20px;
                background: rgba(0, 120, 212, 0.1);
                border-radius: 16px;
                padding: 6px;
            }
        """)
        
        # 内容区域
        content_layout = QVBoxLayout()
        content_layout.setSpacing(4)
        
        # 预览文本
        self.preview_label = QLabel(self.item.preview)
        self.preview_label.setWordWrap(True)
        self.preview_label.setMaximumHeight(40)
        self.preview_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #323130;
                line-height: 1.4;
            }
        """)
        
        # 时间标签
        self.time_label = QLabel(self.item.format_time())
        self.time_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #605e5c;
            }
        """)
        
        content_layout.addWidget(self.preview_label)
        content_layout.addWidget(self.time_label)
        
        # 收藏按钮
        self.favorite_btn = QPushButton("⭐" if self.item.is_favorite else "☆")
        self.favorite_btn.setFixedSize(32, 32)
        self.favorite_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                font-size: 16px;
                color: #ff6b35;
            }
            QPushButton:hover {
                background: rgba(255, 107, 53, 0.1);
                border-radius: 16px;
            }
        """)
        self.favorite_btn.clicked.connect(self._toggle_favorite)
        
        # 添加到布局
        layout.addWidget(self.type_icon)
        layout.addLayout(content_layout, 1)
        layout.addWidget(self.favorite_btn)
        
        # 设置整体样式
        self.setStyleSheet("""
            ClipboardItemWidget {
                background: rgba(255, 255, 255, 0.8);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                margin: 2px;
            }
            ClipboardItemWidget:hover {
                background: rgba(0, 120, 212, 0.1);
                border-color: rgba(0, 120, 212, 0.3);
            }
        """)
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        # 设置鼠标事件
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mousePressEvent = self._on_click
    
    def _toggle_favorite(self):
        """切换收藏状态"""
        self.item.is_favorite = not self.item.is_favorite
        self.favorite_btn.setText("⭐" if self.item.is_favorite else "☆")
        self.favorite_toggled.emit(self.item, self.item.is_favorite)
    
    def _on_click(self, event):
        """点击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.item_clicked.emit(self.item)

class ClipboardListWidget(QListWidget):
    """现代化剪贴板列表"""
    
    item_selected = pyqtSignal(ClipboardItem)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._items: List[ClipboardItem] = []
    
    def _setup_ui(self):
        """设置界面"""
        self.setStyleSheet("""
            QListWidget {
                background: rgba(255, 255, 255, 0.6);
                border: none;
                border-radius: 8px;
                padding: 8px;
                outline: none;
            }
            QListWidget::item {
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }
            QListWidget::item:selected {
                background: transparent;
            }
        """)
        
        # 设置滚动模式
        self.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(10)
        
        # 设置选择模式
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
    
    def add_item(self, item: ClipboardItem):
        """添加项目"""
        self._items.append(item)
        
        # 创建列表项
        list_item = QListWidgetItem()
        widget = ClipboardItemWidget(item)
        
        # 设置大小
        list_item.setSizeHint(widget.sizeHint())
        
        # 添加到列表
        self.addItem(list_item)
        self.setItemWidget(list_item, widget)
        
        # 连接信号
        widget.item_clicked.connect(self.item_selected.emit)
        widget.favorite_toggled.connect(self._on_favorite_toggled)
    
    def _on_favorite_toggled(self, item: ClipboardItem, is_favorite: bool):
        """收藏状态改变"""
        print(f"项目 {item.id} 收藏状态: {is_favorite}")
    
    def clear_items(self):
        """清空项目"""
        self.clear()
        self._items.clear()

class PreviewPanel(QWidget):
    """预览面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self.current_item: Optional[ClipboardItem] = None
    
    def _setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # 标题栏
        title_layout = QHBoxLayout()
        self.title_label = QLabel("预览")
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #323130;
            }
        """)
        
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        
        # 操作按钮
        self.copy_btn = ModernButton("复制", "📋")
        self.favorite_btn = ModernButton("收藏", "⭐")
        self.delete_btn = ModernButton("删除", "🗑️")
        
        # 设置按钮颜色
        self.favorite_btn.setStyleSheet(self.favorite_btn.styleSheet().replace("#0078d4", "#107c10"))
        self.delete_btn.setStyleSheet(self.delete_btn.styleSheet().replace("#0078d4", "#d13438"))
        
        title_layout.addWidget(self.copy_btn)
        title_layout.addWidget(self.favorite_btn)
        title_layout.addWidget(self.delete_btn)
        
        # 内容区域
        self.content_label = QLabel("选择一个项目进行预览")
        self.content_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #605e5c;
                padding: 20px;
                background: rgba(255, 255, 255, 0.5);
                border-radius: 8px;
                border: 2px dashed rgba(0, 0, 0, 0.1);
            }
        """)
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_label.setWordWrap(True)
        
        # 添加到布局
        layout.addLayout(title_layout)
        layout.addWidget(self.content_label, 1)
        
        # 设置整体样式
        self.setStyleSheet("""
            PreviewPanel {
                background: rgba(255, 255, 255, 0.8);
                border-radius: 8px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
        """)
    
    def show_item(self, item: ClipboardItem):
        """显示项目预览"""
        self.current_item = item
        self.title_label.setText(f"预览 - {item.get_type_icon()}")
        self.content_label.setText(item.content)
        self.content_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #323130;
                padding: 20px;
                background: rgba(255, 255, 255, 0.8);
                border-radius: 8px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                line-height: 1.6;
            }
        """)

class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._load_demo_data()
    
    def _setup_ui(self):
        """设置界面"""
        self.setWindowTitle("Paste for Windows - 演示")
        self.setMinimumSize(800, 600)
        self.resize(1000, 700)
        
        # 设置窗口标志
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowMinMaxButtonsHint)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 搜索栏
        self.search_bar = SearchBar()
        main_layout.addWidget(self.search_bar)
        
        # 内容区域
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 剪贴板列表
        self.clipboard_list = ClipboardListWidget()
        content_splitter.addWidget(self.clipboard_list)
        
        # 预览面板
        self.preview_panel = PreviewPanel()
        content_splitter.addWidget(self.preview_panel)
        
        # 设置分割器比例
        content_splitter.setSizes([600, 400])
        
        main_layout.addWidget(content_splitter, 1)
        
        # 连接信号
        self.search_bar.search_requested.connect(self._on_search)
        self.clipboard_list.item_selected.connect(self.preview_panel.show_item)
        
        # 设置全局样式
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 rgba(255,255,255,0.95),
                                          stop:1 rgba(255,255,255,0.85));
            }
        """)
    
    def _load_demo_data(self):
        """加载演示数据"""
        demo_items = [
            ClipboardItem("这是一个文本内容的示例，展示了剪贴板管理器的基本功能。", "text"),
            ClipboardItem("https://github.com/your-username/paste-for-windows", "link"),
            ClipboardItem("print('Hello, World!')\nfor i in range(10):\n    print(i)", "code"),
            ClipboardItem("C:\\Users\\Username\\Documents\\example.txt", "file"),
            ClipboardItem("这是一段很长的文本内容，用来测试文本截断和预览功能。当文本内容超过一定长度时，应该自动截断并显示省略号。", "text"),
            ClipboardItem("https://www.microsoft.com/zh-cn/windows", "link"),
            ClipboardItem("import os\nimport sys\n\ndef main():\n    print('Hello from Python!')\n\nif __name__ == '__main__':\n    main()", "code"),
            ClipboardItem("D:\\Projects\\paste-for-windows\\src\\main.py", "file"),
        ]
        
        for item in demo_items:
            self.clipboard_list.add_item(item)
    
    def _on_search(self, query: str):
        """搜索处理"""
        print(f"搜索: {query}")
        # 这里可以实现实际的搜索逻辑

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("Paste for Windows")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Your Organization")
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 