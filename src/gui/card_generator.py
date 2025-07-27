#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卡片生成器 - 根据剪贴板内容生成对应的卡片
"""

from typing import Dict, Any, Optional
from datetime import datetime
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QPalette

from ..core.clipboard_manager import ClipboardItem


class CardGenerator:
    """卡片生成器"""
    
    # 内容类型配置
    CONTENT_TYPE_CONFIG = {
        "text": {
            "name": "文本",
            "color": "#0078d4",  # 蓝色
            "icon": "📝",
            "description": "普通文本内容"
        },
        "link": {
            "name": "链接",
            "color": "#107c10",  # 绿色
            "icon": "🔗",
            "description": "网址链接"
        },
        "code": {
            "name": "代码",
            "color": "#5c2d91",  # 紫色
            "icon": "💻",
            "description": "代码片段"
        },
        "file": {
            "name": "文件",
            "color": "#d13438",  # 红色
            "icon": "📁",
            "description": "文件路径"
        },
        "image": {
            "name": "图片",
            "color": "#ff8c00",  # 橙色
            "icon": "🖼️",
            "description": "图片文件"
        },
        "empty": {
            "name": "空内容",
            "color": "#605e5c",  # 灰色
            "icon": "⚪",
            "description": "空内容"
        }
    }
    
    @classmethod
    def get_type_config(cls, content_type: str) -> Dict[str, Any]:
        """获取内容类型配置"""
        return cls.CONTENT_TYPE_CONFIG.get(content_type, cls.CONTENT_TYPE_CONFIG["text"])
    
    @classmethod
    def generate_card_widget(cls, item: ClipboardItem, parent=None) -> 'ClipboardCardWidget':
        """生成卡片组件"""
        return ClipboardCardWidget(item, parent)
    
    @classmethod
    def get_card_preview(cls, item: ClipboardItem, max_length: int = 100) -> str:
        """获取卡片预览内容"""
        content = item.content.strip()
        
        if not content:
            return "空内容"
        
        # 根据内容类型生成不同的预览
        if item.content_type == "link":
            # 链接类型：显示域名
            try:
                from urllib.parse import urlparse
                parsed = urlparse(content)
                domain = parsed.netloc or parsed.path
                return f"🔗 {domain}"
            except:
                return f"🔗 {content[:max_length]}"
        
        elif item.content_type == "file":
            # 文件类型：显示文件名
            import os
            filename = os.path.basename(content)
            return f"📁 {filename}"
        
        elif item.content_type == "code":
            # 代码类型：显示第一行
            lines = content.split('\n')
            first_line = lines[0].strip()
            if len(first_line) > max_length:
                first_line = first_line[:max_length] + "..."
            return f"💻 {first_line}"
        
        else:
            # 文本类型：直接截取
            if len(content) > max_length:
                return content[:max_length] + "..."
            return content
    
    @classmethod
    def get_card_tooltip(cls, item: ClipboardItem) -> str:
        """获取卡片提示信息"""
        config = cls.get_type_config(item.content_type)
        
        tooltip = f"""
类型: {config['name']}
创建时间: {item.created_at.strftime('%Y-%m-%d %H:%M:%S')}
访问次数: {item.access_count}
内容长度: {len(item.content)} 字符
        """.strip()
        
        if item.tags:
            tooltip += f"\n标签: {item.tags}"
        
        return tooltip


class ClipboardCardWidget(QFrame):
    """剪贴板卡片组件"""
    
    # 信号定义
    clicked = pyqtSignal(ClipboardItem)
    double_clicked = pyqtSignal(ClipboardItem)
    
    def __init__(self, item: ClipboardItem, parent=None):
        super().__init__(parent)
        self.item = item
        self._is_selected = False
        self._setup_ui()
        self._setup_style()
    
    def _setup_ui(self):
        """设置界面"""
        # 设置固定大小
        self.setFixedSize(300, 120)
        
        # 设置鼠标样式
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # 头部信息
        header_layout = QHBoxLayout()
        
        # 类型图标和名称
        config = CardGenerator.get_type_config(self.item.content_type)
        type_label = QLabel(f"{config['icon']} {config['name']}")
        type_label.setFont(QFont("Microsoft YaHei", 9, QFont.Weight.Bold))
        type_label.setStyleSheet(f"color: {config['color']};")
        
        # 时间信息
        time_label = QLabel(self.item.created_at.strftime("%H:%M"))
        time_label.setFont(QFont("Microsoft YaHei", 8))
        time_label.setStyleSheet("color: #605e5c;")
        
        header_layout.addWidget(type_label)
        header_layout.addStretch()
        header_layout.addWidget(time_label)
        
        # 内容预览
        content_preview = CardGenerator.get_card_preview(self.item, 80)
        content_label = QLabel(content_preview)
        content_label.setFont(QFont("Microsoft YaHei", 10))
        content_label.setWordWrap(True)
        content_label.setStyleSheet("color: #323130; line-height: 1.4;")
        
        # 底部信息
        footer_layout = QHBoxLayout()
        
        # 访问次数
        access_label = QLabel(f"访问: {self.item.access_count}")
        access_label.setFont(QFont("Microsoft YaHei", 8))
        access_label.setStyleSheet("color: #605e5c;")
        
        # 收藏状态
        if self.item.is_favorite:
            favorite_label = QLabel("⭐")
            favorite_label.setFont(QFont("Microsoft YaHei", 10))
        else:
            favorite_label = QLabel("")
        
        footer_layout.addWidget(access_label)
        footer_layout.addStretch()
        footer_layout.addWidget(favorite_label)
        
        # 添加到主布局
        layout.addLayout(header_layout)
        layout.addWidget(content_label, 1)
        layout.addLayout(footer_layout)
        
        # 设置工具提示
        self.setToolTip(CardGenerator.get_card_tooltip(self.item))
    
    def _setup_style(self):
        """设置样式"""
        config = CardGenerator.get_type_config(self.item.content_type)
        border_color = config['color']
        
        self.setStyleSheet(f"""
            ClipboardCardWidget {{
                background: rgb(255, 255, 255);
                border: 2px solid {border_color};
                border-radius: 8px;
                margin: 4px;
            }}
            
            ClipboardCardWidget:hover {{
                background: rgb(248, 248, 248);
                border-color: {border_color};
                transform: translateY(-2px);
            }}
            
            ClipboardCardWidget[selected="true"] {{
                background: rgb(240, 248, 255);
                border-color: {border_color};
                border-width: 3px;
            }}
        """)
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.item)
    
    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit(self.item)
    
    def set_selected(self, selected: bool):
        """设置选中状态"""
        self._is_selected = selected
        if selected:
            self.setProperty("selected", "true")
        else:
            self.setProperty("selected", "false")
        self.setStyle(self.style())  # 重新应用样式
    
    def update_item(self, item: ClipboardItem):
        """更新项目数据"""
        self.item = item
        # 重新设置工具提示
        self.setToolTip(CardGenerator.get_card_tooltip(self.item))
        
        # 更新显示内容（这里可以添加更多更新逻辑）
        # 例如更新访问次数、时间等


class CardContainer(QWidget):
    """卡片容器"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """设置界面"""
        from PyQt6.QtWidgets import QGridLayout
        
        # 网格布局
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(8)
        self.grid_layout.setContentsMargins(8, 8, 8, 8)
        
        # 设置样式
        self.setStyleSheet("""
            CardContainer {
                background: transparent;
            }
        """)
    
    def add_card(self, card_widget: ClipboardCardWidget, row: int, col: int):
        """添加卡片"""
        self.grid_layout.addWidget(card_widget, row, col)
    
    def clear_cards(self):
        """清空所有卡片"""
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def get_card_count(self) -> int:
        """获取卡片数量"""
        return self.grid_layout.count() 