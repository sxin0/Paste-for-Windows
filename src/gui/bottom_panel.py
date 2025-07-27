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
    QPixmap, QIcon, QPalette
)

from ..core.clipboard_manager import ClipboardItem, ClipboardManager


class BottomPanel(QWidget):
    """底部交互栏"""
    
    # 信号定义
    item_selected = pyqtSignal(ClipboardItem)  # 项目被选中
    item_double_clicked = pyqtSignal(ClipboardItem)  # 项目双击上屏
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
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建内容容器
        self.content_widget = QWidget()
        self.content_widget.setObjectName("contentWidget")
        self.content_widget.setStyleSheet("""
            QWidget#contentWidget {
                background: rgb(255, 255, 255);
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                border: 1px solid rgba(0, 0, 0, 0.1);
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
                background: rgb(255, 255, 255);
                selection-background-color: rgba(0, 120, 212, 0.5);
                color: #000000;
            }
            QLineEdit:focus {
                border-color: #0078d4;
                background: rgb(255, 255, 255);
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
                background: rgb(255, 255, 255);
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
        
        # 为滚动区域添加滚轮事件支持
        self.scroll_area.wheelEvent = self._scroll_area_wheel_event
        
        # 创建卡片容器widget
        self.cards_container = QWidget()
        self.cards_layout = QHBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(20, 20, 20, 20)  # 增加容器边距
        self.cards_layout.setSpacing(8)  # 减少卡片间距，让卡片更紧凑
        self.cards_layout.addStretch()  # 添加弹性空间
        
        # 为卡片容器添加滚轮事件支持
        self.cards_container.wheelEvent = self._cards_container_wheel_event
        
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
        widget.item_clicked.connect(self._on_item_clicked)
        widget.item_double_clicked.connect(self._on_item_double_clicked)
    
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
    
    def _on_item_clicked(self, item: ClipboardItem):
        """项目单击事件 - 选中项目"""
        # 清除其他卡片的选中状态
        self._clear_selection()
        
        # 找到对应的widget并设置选中状态
        for i in range(self.cards_layout.count() - 1):  # 减1是因为最后一个是弹性空间
            widget = self.cards_layout.itemAt(i).widget()
            if widget and hasattr(widget, 'item') and widget.item.id == item.id:
                widget.set_selected(True)
                break
        
        # 发送选中信号
        self.item_selected.emit(item)
    
    def _on_item_double_clicked(self, item: ClipboardItem):
        """项目双击事件 - 内容上屏"""
        # 发送双击信号
        self.item_double_clicked.emit(item)
        
        # 隐藏面板
        self.hide_panel()
    
    def _clear_selection(self):
        """清除所有卡片的选中状态"""
        for i in range(self.cards_layout.count() - 1):  # 减1是因为最后一个是弹性空间
            widget = self.cards_layout.itemAt(i).widget()
            if widget and hasattr(widget, 'set_selected'):
                widget.set_selected(False)
    
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
    
    def wheelEvent(self, event):
        """滚轮事件 - 支持横向滚动"""
        # 获取滚轮滚动的角度
        delta = event.angleDelta().y()
        
        # 获取水平滚动条
        horizontal_scrollbar = self.scroll_area.horizontalScrollBar()
        
        if horizontal_scrollbar.isVisible():
            # 计算滚动步长（基于卡片宽度和滚动速度）
            scroll_step = self._calculate_scroll_step(delta)
            
            # 根据滚轮方向决定滚动方向
            if delta > 0:
                # 向上滚动，向左移动
                new_value = horizontal_scrollbar.value() - scroll_step
            else:
                # 向下滚动，向右移动
                new_value = horizontal_scrollbar.value() + scroll_step
            
            # 设置新的滚动位置
            horizontal_scrollbar.setValue(new_value)
            
            # 阻止事件继续传播
            event.accept()
        else:
            # 如果没有水平滚动条，让事件继续传播
            super().wheelEvent(event)
    
    def _calculate_scroll_step(self, delta: int) -> int:
        """计算滚动步长（基于卡片宽度和滚动速度）"""
        # 卡片宽度（包括间距）
        card_width = 220  # 卡片固定宽度
        card_spacing = 8   # 卡片间距
        total_card_width = card_width + card_spacing
        
        # 根据滚动速度调整步长
        # 快速滚动时滚动更多卡片，慢速滚动时滚动更少卡片
        speed_factor = abs(delta) / 120.0  # 标准化滚动速度
        
        # 基础滚动：1个卡片宽度
        # 快速滚动：最多3个卡片宽度
        # 慢速滚动：最少0.5个卡片宽度
        if speed_factor >= 2.0:
            # 快速滚动：滚动2-3个卡片
            cards_to_scroll = min(3, 2 + speed_factor - 2.0)
        elif speed_factor >= 1.0:
            # 中等速度：滚动1-2个卡片
            cards_to_scroll = 1 + (speed_factor - 1.0)
        else:
            # 慢速滚动：滚动0.5-1个卡片
            cards_to_scroll = 0.5 + speed_factor * 0.5
        
        # 计算最终滚动步长
        scroll_step = int(total_card_width * cards_to_scroll)
        
        return scroll_step
    
    def _scroll_area_wheel_event(self, event):
        """滚动区域的滚轮事件处理"""
        # 获取滚轮滚动的角度
        delta = event.angleDelta().y()
        
        # 获取水平滚动条
        horizontal_scrollbar = self.scroll_area.horizontalScrollBar()
        
        if horizontal_scrollbar.isVisible():
            # 计算滚动步长（基于卡片宽度和滚动速度）
            scroll_step = self._calculate_scroll_step(delta)
            
            # 根据滚轮方向决定滚动方向
            if delta > 0:
                # 向上滚动，向左移动
                new_value = horizontal_scrollbar.value() - scroll_step
            else:
                # 向下滚动，向右移动
                new_value = horizontal_scrollbar.value() + scroll_step
            
            # 设置新的滚动位置
            horizontal_scrollbar.setValue(new_value)
            
            # 阻止事件继续传播
            event.accept()
        else:
            # 如果没有水平滚动条，让事件继续传播
            event.ignore()
    
    def _cards_container_wheel_event(self, event):
        """卡片容器的滚轮事件处理"""
        # 获取滚轮滚动的角度
        delta = event.angleDelta().y()
        
        # 获取水平滚动条
        horizontal_scrollbar = self.scroll_area.horizontalScrollBar()
        
        if horizontal_scrollbar.isVisible():
            # 计算滚动步长（基于卡片宽度和滚动速度）
            scroll_step = self._calculate_scroll_step(delta)
            
            # 根据滚轮方向决定滚动方向
            if delta > 0:
                # 向上滚动，向左移动
                new_value = horizontal_scrollbar.value() - scroll_step
            else:
                # 向下滚动，向右移动
                new_value = horizontal_scrollbar.value() + scroll_step
            
            # 设置新的滚动位置
            horizontal_scrollbar.setValue(new_value)
            
            # 阻止事件继续传播
            event.accept()
        else:
            # 如果没有水平滚动条，让事件继续传播
            event.ignore()


class ClipboardItemWidget(QWidget):
    """剪贴板项目组件"""
    
    item_clicked = pyqtSignal(ClipboardItem)  # 单击选中
    item_double_clicked = pyqtSignal(ClipboardItem)  # 双击上屏
    
    def __init__(self, item: ClipboardItem, parent=None):
        super().__init__(parent)
        self.item = item
        self.is_selected = False  # 选中状态
        self._setup_ui()
    
    def _setup_ui(self):
        """设置界面"""
        # 设置对象名称以便样式表选择器工作
        self.setObjectName("ClipboardItemWidget")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)  # 增加内边距
        layout.setSpacing(10)  # 增加内部元素间距
        
        # 类型图标
        self.type_icon = QLabel(self._get_type_icon())
        self.type_icon.setFixedSize(32, 32)
        self.type_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.type_icon.setStyleSheet("""
            QLabel {
                font-size: 20px;
                background: rgb(240, 248, 255);
                border-radius: 16px;
                padding: 6px;
                border: none;
            }
        """)
        
        # 内容预览
        self.content_label = QLabel(self._get_preview())
        self.content_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #000000;
                line-height: 1.4;
                background: transparent;
                border: none;
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
                background: transparent;
                border: none;
            }
        """)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        # 添加到布局
        layout.addWidget(self.type_icon, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.content_label, 1)
        layout.addWidget(self.time_label, 0, Qt.AlignmentFlag.AlignCenter)
        
        # 设置固定宽度，适合卡片显示
        self.setFixedWidth(220)  # 增加宽度以适应新的内边距
        self.setMinimumHeight(140)  # 增加高度以适应新的内边距
        
        # 设置整体样式（边框颜色将在_set_border_color中设置）
        self._set_border_color()
        
        # 添加阴影效果 - 移到样式设置之后
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        # 设置鼠标事件
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        # 启用双击事件
        self.setMouseTracking(True)
    
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
    
    def _set_border_color(self):
        """根据内容类型设置背景颜色和边框"""
        # 现在背景和边框都在 paintEvent 中处理
        # 只需要触发重绘
        self.update()
    
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
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 单击选中
            self.set_selected(True)
            self.item_clicked.emit(self.item)
        super().mousePressEvent(event)
    
    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 双击上屏
            self.item_double_clicked.emit(self.item)
        super().mouseDoubleClickEvent(event)
    
    def set_selected(self, selected: bool):
        """设置选中状态"""
        self.is_selected = selected
        self.update()  # 触发重绘以显示选中效果
    
    def paintEvent(self, event):
        """重写绘制事件来手动绘制背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 定义每种类型的背景色和边框色
        type_styles = {
            "text": {"bg": "#E3F2FD", "border": "#2196F3"},      # 浅蓝色 - 文本
            "link": {"bg": "#E8F5E8", "border": "#4CAF50"},      # 浅绿色 - 链接
            "file": {"bg": "#FFEBEE", "border": "#F44336"},      # 浅红色 - 文件
            "code": {"bg": "#F3E5F5", "border": "#9C27B0"},      # 浅紫色 - 代码
            "image": {"bg": "#FFF3E0", "border": "#FF9800"}      # 浅橙色 - 图片
        }
        
        # 获取当前类型的样式
        style = type_styles.get(self.item.content_type, {"bg": "#F5F5F5", "border": "#9E9E9E"})
        
        # 根据选中状态调整样式
        if self.is_selected:
            # 选中状态：更深的背景色和更粗的边框
            bg_color = QColor(style['bg'])
            bg_color.setAlpha(200)  # 增加不透明度
            border_color = QColor(style['border'])
            border_width = 3
        else:
            # 正常状态
            bg_color = QColor(style['bg'])
            border_color = QColor(style['border'])
            border_width = 2
        
        # 绘制背景
        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(border_color, border_width))
        painter.drawRoundedRect(self.rect(), 8, 8)
        
        # 如果选中，绘制选中指示器
        if self.is_selected:
            # 在右上角绘制选中指示器
            indicator_rect = QRect(self.width() - 20, 5, 15, 15)
            painter.setBrush(QBrush(QColor("#4CAF50")))
            painter.setPen(QPen(QColor("#4CAF50"), 1))
            painter.drawEllipse(indicator_rect)
            
            # 绘制白色勾号
            painter.setPen(QPen(QColor("white"), 2))
            painter.drawLine(indicator_rect.center().x() - 3, indicator_rect.center().y(), 
                           indicator_rect.center().x() - 1, indicator_rect.center().y() + 2)
            painter.drawLine(indicator_rect.center().x() - 1, indicator_rect.center().y() + 2,
                           indicator_rect.center().x() + 3, indicator_rect.center().y() - 2)
        
        # 调用父类的绘制事件
        super().paintEvent(event) 