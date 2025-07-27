#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
底部交互栏 - 从屏幕下方冒出来的界面
"""

import sys
import ctypes
from typing import List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QListWidget, QListWidgetItem, QFrame, QScrollArea,
    QGraphicsDropShadowEffect, QSizePolicy, QApplication
)
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QTimer, QRect, QPoint,
    pyqtSignal, QSize
)
from PyQt6.QtGui import (
    QPainter, QColor, QLinearGradient, QBrush, QPen, QFont,
    QPixmap, QIcon
)

from ..core.clipboard_manager import ClipboardItem, ClipboardManager


class BottomPanel(QWidget):
    """底部交互栏"""
    
    # 信号定义
    item_selected = pyqtSignal(ClipboardItem)  # 项目被选中
    panel_closed = pyqtSignal()  # 面板关闭
    
    def __init__(self, clipboard_manager: ClipboardManager, parent=None):
        super().__init__(parent)
        self.clipboard_manager = clipboard_manager
        self._setup_ui()
        self._setup_animations()
        self._load_items()
        
        # 连接信号
        self.clipboard_manager.item_added.connect(self._on_item_added)
        self.clipboard_manager.item_updated.connect(self._on_item_updated)
        self.clipboard_manager.item_removed.connect(self._on_item_removed)
    
    def _setup_ui(self):
        """设置界面"""
        # 设置窗口标志
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )
        
        # 设置属性
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建内容容器
        self.content_widget = QWidget()
        self.content_widget.setObjectName("contentWidget")
        self.content_widget.setStyleSheet("""
            QWidget#contentWidget {
                background: rgba(255, 255, 255, 0.8);
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)
        
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(12)
        
        # 标题栏
        title_layout = QHBoxLayout()
        
        # 标题
        self.title_label = QLabel("剪贴板历史")
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #000000;
            }
        """)
        
        # 关闭按钮
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-size: 20px;
                font-weight: bold;
                color: rgba(0, 0, 0, 0.6);
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 0.1);
                border-radius: 16px;
                color: #d13438;
            }
        """)
        self.close_btn.clicked.connect(self.hide_panel)
        
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.close_btn)
        
        # 搜索栏
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索剪贴板内容...")
        self.search_input.setMinimumHeight(36)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid rgba(0, 0, 0, 0.2);
                border-radius: 18px;
                padding: 8px 16px;
                font-size: 14px;
                background: rgba(255, 255, 255, 0.8);
                selection-background-color: rgba(0, 120, 212, 0.5);
                color: #000000;
            }
            QLineEdit:focus {
                border-color: #0078d4;
                background: rgba(255, 255, 255, 0.9);
            }
            QLineEdit::placeholder {
                color: rgba(0, 0, 0, 0.5);
            }
        """)
        self.search_input.textChanged.connect(self._on_search)
        
        # 创建横向滚动的卡片容器
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: rgba(255, 255, 255, 0.8);
                border: none;
                border-radius: 8px;
                outline: none;
            }
            QScrollBar:horizontal {
                background: rgba(0, 0, 0, 0.1);
                height: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 4px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background: rgba(0, 0, 0, 0.5);
            }
        """)
        
        # 创建卡片容器widget
        self.cards_container = QWidget()
        self.cards_layout = QHBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(16, 16, 16, 16)
        self.cards_layout.setSpacing(12)  # 恢复原来的卡片间距
        self.cards_layout.addStretch()  # 添加弹性空间
        
        self.scroll_area.setWidget(self.cards_container)
        
        # 添加到布局
        content_layout.addLayout(title_layout)
        content_layout.addWidget(self.search_input)
        content_layout.addWidget(self.scroll_area, 1)
        
        main_layout.addWidget(self.content_widget)
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, -5)
        self.content_widget.setGraphicsEffect(shadow)
    
    def _setup_animations(self):
        """设置动画"""
        # 显示动画
        self.show_animation = QPropertyAnimation(self, b"geometry")
        self.show_animation.setDuration(300)
        self.show_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # 隐藏动画
        self.hide_animation = QPropertyAnimation(self, b"geometry")
        self.hide_animation.setDuration(250)
        self.hide_animation.setEasingCurve(QEasingCurve.Type.InCubic)
        self.hide_animation.finished.connect(self._on_hide_finished)
    
    def _get_taskbar_height(self) -> int:
        """获取任务栏高度"""
        try:
            # 使用 Windows API 获取任务栏信息
            user32 = ctypes.windll.user32
            shell32 = ctypes.windll.shell32
            
            # 获取任务栏窗口句柄
            taskbar_hwnd = user32.FindWindowW("Shell_TrayWnd", None)
            if taskbar_hwnd:
                # 获取任务栏矩形
                rect = ctypes.wintypes.RECT()
                user32.GetWindowRect(taskbar_hwnd, ctypes.byref(rect))
                taskbar_height = rect.bottom - rect.top
                return max(taskbar_height, 0)  # 确保不为负数
        except Exception:
            pass
        
        # 如果无法获取，返回默认值
        return 50
    
    def _load_items(self):
        """加载剪贴板项目"""
        items = self.clipboard_manager.get_recent_items(20)
        for item in items:
            self._add_item_to_list(item)
    
    def _add_item_to_list(self, item: ClipboardItem):
        """添加项目到卡片容器"""
        widget = ClipboardItemWidget(item)
        
        # 将卡片插入到弹性空间之前
        self.cards_layout.insertWidget(self.cards_layout.count() - 1, widget)
        
        # 连接信号
        widget.item_clicked.connect(self.item_selected.emit)
        widget.item_clicked.connect(self.hide_panel)
    
    def _on_item_added(self, item: ClipboardItem):
        """新项目添加"""
        self._add_item_to_list(item)
        # 新项目会自动添加到最前面（因为insertWidget在弹性空间之前）
    
    def _on_item_updated(self, item: ClipboardItem):
        """项目更新"""
        # 这里可以更新列表中的项目显示
        pass
    
    def _on_item_removed(self, item_id: str):
        """项目删除"""
        # 从卡片容器中移除项目
        for i in range(self.cards_layout.count() - 1):  # 减1是因为最后一个是弹性空间
            widget = self.cards_layout.itemAt(i).widget()
            if widget and hasattr(widget, 'item') and widget.item.id == item_id:
                self.cards_layout.removeWidget(widget)
                widget.deleteLater()
                break
    
    def _on_search(self, query: str):
        """搜索处理"""
        # 清空卡片容器（保留弹性空间）
        while self.cards_layout.count() > 1:  # 保留最后的弹性空间
            widget = self.cards_layout.itemAt(0).widget()
            if widget:
                self.cards_layout.removeWidget(widget)
                widget.deleteLater()
        
        if query.strip():
            # 搜索项目
            items = self.clipboard_manager.search_items(query, 20)
        else:
            # 显示最近项目
            items = self.clipboard_manager.get_recent_items(20)
        
        # 添加搜索结果
        for item in items:
            self._add_item_to_list(item)
    
    def _on_item_clicked(self, item: QListWidgetItem):
        """项目点击（保留兼容性）"""
        pass
    
    def show_panel(self):
        """显示面板"""
        if not self.isVisible():
            # 计算显示位置
            screen = QApplication.primaryScreen().geometry()
            panel_width = screen.width()  # 铺满屏幕宽度
            panel_height = 400
            
            # 获取实际任务栏高度
            taskbar_height = self._get_taskbar_height()
            
            # 从屏幕底部开始
            start_rect = QRect(
                0,  # 从屏幕左边开始
                screen.height(),
                panel_width,
                panel_height
            )
            
            # 最终位置 - 考虑任务栏高度，留出一些间距
            end_y = screen.height() - panel_height - taskbar_height - 1  # 减去任务栏高度和1像素间距
            
            # 确保面板不会超出屏幕顶部边界
            end_y = max(end_y, 0)
            
            end_rect = QRect(
                0,  # 从屏幕左边开始
                end_y,
                panel_width,
                panel_height
            )
            
            # 设置初始位置
            self.setGeometry(start_rect)
            self.show()
            
            # 开始显示动画
            self.show_animation.setStartValue(start_rect)
            self.show_animation.setEndValue(end_rect)
            self.show_animation.start()
    
    def hide_panel(self):
        """隐藏面板"""
        if self.isVisible():
            # 计算隐藏位置
            current_rect = self.geometry()
            screen = QApplication.primaryScreen().geometry()
            
            # 隐藏到屏幕底部
            hide_rect = QRect(
                current_rect.x(),
                screen.height(),
                current_rect.width(),
                current_rect.height()
            )
            
            # 开始隐藏动画
            self.hide_animation.setStartValue(current_rect)
            self.hide_animation.setEndValue(hide_rect)
            self.hide_animation.start()
    
    def _on_hide_finished(self):
        """隐藏动画完成"""
        self.hide()
        self.panel_closed.emit()
    
    def keyPressEvent(self, event):
        """按键事件"""
        if event.key() == Qt.Key.Key_Escape:
            self.hide_panel()
        else:
            super().keyPressEvent(event)


class ClipboardItemWidget(QWidget):
    """剪贴板项目组件"""
    
    item_clicked = pyqtSignal(ClipboardItem)
    
    def __init__(self, item: ClipboardItem, parent=None):
        super().__init__(parent)
        self.item = item
        self._setup_ui()
    
    def _setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # 类型图标
        self.type_icon = QLabel(self._get_type_icon())
        self.type_icon.setFixedSize(32, 32)
        self.type_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.type_icon.setStyleSheet("""
            QLabel {
                font-size: 20px;
                background: rgba(0, 120, 212, 0.1);
                border-radius: 16px;
                padding: 6px;
            }
        """)
        
        # 内容预览
        self.content_label = QLabel(self._get_preview())
        self.content_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #000000;
                line-height: 1.4;
            }
        """)
        self.content_label.setWordWrap(True)
        self.content_label.setMaximumHeight(60)
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # 时间标签
        self.time_label = QLabel(self._format_time())
        self.time_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: rgba(0, 0, 0, 0.6);
            }
        """)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        # 添加到布局
        layout.addWidget(self.type_icon, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.content_label, 1)
        layout.addWidget(self.time_label, 0, Qt.AlignmentFlag.AlignCenter)
        
        # 设置固定宽度，适合卡片显示
        self.setFixedWidth(200)
        self.setMinimumHeight(120)
        
        # 设置整体样式
        self.setStyleSheet("""
            ClipboardItemWidget {
                background: rgba(255, 255, 255, 0.6);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                margin: 4px;
            }
            ClipboardItemWidget:hover {
                background: rgba(255, 255, 255, 0.8);
                border-color: rgba(0, 120, 212, 0.3);
            }
        """)
        
        # 设置鼠标事件
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mousePressEvent = self._on_click
    
    def _get_type_icon(self) -> str:
        """获取类型图标"""
        icons = {
            "text": "📝",
            "link": "🔗",
            "file": "📁",
            "code": "💻",
            "image": "🖼️"
        }
        return icons.get(self.item.content_type, "📄")
    
    def _get_preview(self) -> str:
        """获取预览内容"""
        content = self.item.content
        if len(content) > 60:
            return content[:60] + "..."
        return content
    
    def _format_time(self) -> str:
        """格式化时间"""
        from datetime import datetime
        now = datetime.now()
        diff = now - self.item.created_at
        
        if diff.days > 0:
            return f"{diff.days}天前"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}小时前"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60}分钟前"
        else:
            return "刚刚"
    
    def _on_click(self, event):
        """点击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.item_clicked.emit(self.item) 