#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统托盘模块
提供系统托盘功能和菜单
"""

from PyQt6.QtWidgets import (
    QSystemTrayIcon, QMenu, QWidget, QApplication
)
from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtGui import QIcon, QPixmap, QAction, QPainter, QPen, QBrush, QColor
from pathlib import Path

from ..core.clipboard_manager import ClipboardManager


class SystemTray(QObject):
    """系统托盘管理器"""
    
    # 信号定义
    show_window_requested = pyqtSignal()  # 显示窗口请求
    show_bottom_panel_requested = pyqtSignal()  # 显示底部面板请求
    toggle_bottom_panel_requested = pyqtSignal()  # 切换底部面板显示状态
    quit_requested = pyqtSignal()  # 退出请求
    
    def __init__(self, clipboard_manager: ClipboardManager, parent=None):
        super().__init__(parent)
        self.clipboard_manager = clipboard_manager
        self._setup_tray()
    
    def _setup_tray(self):
        """设置系统托盘"""
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon()
        
        # 设置图标（使用文本图标作为临时方案）
        self._create_icon()
        
        # 设置工具提示
        self.tray_icon.setToolTip("Paste for Windows\n剪贴板管理器")
        
        # 创建菜单
        self._create_menu()
        
        # 连接信号
        self.tray_icon.activated.connect(self._on_tray_activated)
    
    def _create_icon(self):
        """创建托盘图标"""
        # 尝试加载图标文件
        icon_path = Path(__file__).parent.parent.parent / "resources" / "icons" / "tray_icon.png"
        
        if icon_path.exists():
            # 使用实际的图标文件
            icon = QIcon(str(icon_path))
            self.tray_icon.setIcon(icon)
        else:
            # 如果图标文件不存在，创建一个简单的图标
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.GlobalColor.transparent)
            
            # 创建画家绘制简单图标
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # 绘制蓝色圆形背景
            painter.setPen(QPen(QColor("#0078d4"), 1))
            painter.setBrush(QBrush(QColor("#0078d4")))
            painter.drawEllipse(2, 2, 28, 28)
            
            # 绘制白色剪贴板
            painter.setPen(QPen(QColor("#ffffff"), 1))
            painter.setBrush(QBrush(QColor("#ffffff")))
            painter.drawRoundedRect(6, 8, 20, 16, 2, 2)
            
            painter.end()
            
            self.tray_icon.setIcon(QIcon(pixmap))
    
    def _create_menu(self):
        """创建托盘菜单"""
        menu = QMenu()
        
        # 显示底部面板
        show_panel_action = QAction("显示剪贴板历史", self)
        show_panel_action.triggered.connect(self.toggle_bottom_panel_requested.emit)
        menu.addAction(show_panel_action)
        
        # 显示主窗口
        show_window_action = QAction("显示主窗口", self)
        show_window_action.triggered.connect(self.show_window_requested.emit)
        menu.addAction(show_window_action)
        
        menu.addSeparator()
        
        # 启动/停止监听
        self.toggle_listening_action = QAction("停止监听", self)
        self.toggle_listening_action.triggered.connect(self._toggle_listening)
        menu.addAction(self.toggle_listening_action)
        
        # 清空历史
        clear_action = QAction("清空历史", self)
        clear_action.triggered.connect(self._clear_history)
        menu.addAction(clear_action)
        
        menu.addSeparator()
        
        # 设置
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self._show_settings)
        menu.addAction(settings_action)
        
        # 关于
        about_action = QAction("关于", self)
        about_action.triggered.connect(self._show_about)
        menu.addAction(about_action)
        
        menu.addSeparator()
        
        # 退出
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_requested.emit)
        menu.addAction(quit_action)
        
        # 设置菜单
        self.tray_icon.setContextMenu(menu)
    
    def _on_tray_activated(self, reason):
        """托盘图标激活事件"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            # 双击切换底部面板显示状态
            self.toggle_bottom_panel_requested.emit()
        elif reason == QSystemTrayIcon.ActivationReason.Trigger:
            # 单击切换底部面板显示状态 (PyQt6中使用Trigger而不是SingleClick)
            self.toggle_bottom_panel_requested.emit()
    
    def _toggle_listening(self):
        """切换监听状态"""
        if self.clipboard_manager._is_enabled:
            self.clipboard_manager.stop()
            self.toggle_listening_action.setText("开始监听")
        else:
            self.clipboard_manager.start()
            self.toggle_listening_action.setText("停止监听")
    
    def _clear_history(self):
        """清空历史"""
        self.clipboard_manager.clear_all()
        self.show_message("历史已清空", "剪贴板历史记录已全部清除")
    
    def _show_settings(self):
        """显示设置"""
        # TODO: 实现设置对话框
        self.show_message("设置", "设置功能开发中...")
    
    def _show_about(self):
        """显示关于"""
        self.show_message(
            "关于 Paste for Windows",
            "Paste for Windows v1.0.0\n\n"
            "专为 Windows 11 设计的现代化剪贴板管理器\n"
            "参考了 macOS 上优秀的 Paste 应用\n\n"
            "功能特性：\n"
            "• 实时剪贴板监听\n"
            "• 多格式内容支持\n"
            "• 智能搜索和过滤\n"
            "• 现代化界面设计\n"
            "• 系统托盘集成"
        )
    
    def show(self):
        """显示系统托盘"""
        self.tray_icon.show()
    
    def hide(self):
        """隐藏系统托盘"""
        self.tray_icon.hide()
    
    def show_message(self, title: str, message: str, duration: int = 3000):
        """显示托盘消息"""
        self.tray_icon.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information, duration)
    
    def update_tooltip(self, text: str):
        """更新工具提示"""
        self.tray_icon.setToolTip(text)
    
    def is_visible(self) -> bool:
        """检查是否可见"""
        return self.tray_icon.isVisible()
    
    def is_system_tray_available(self) -> bool:
        """检查系统托盘是否可用"""
        return QSystemTrayIcon.isSystemTrayAvailable() 