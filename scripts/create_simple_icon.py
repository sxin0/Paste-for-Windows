#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单图标生成脚本
使用 PyQt6 绘制图标
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap, QPainter, QPen, QBrush, QColor, QIcon
from PyQt6.QtCore import Qt

def create_tray_icon():
    """创建托盘图标"""
    # 创建应用程序实例（如果还没有的话）
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # 创建图标目录
    icons_dir = project_root / "resources" / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)
    
    # 图标尺寸
    size = 32
    
    # 创建画布
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    # 创建画家
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # 设置背景圆形
    painter.setPen(QPen(QColor("#0078d4"), 1))
    painter.setBrush(QBrush(QColor("#0078d4")))
    painter.drawEllipse(2, 2, size-4, size-4)
    
    # 绘制剪贴板主体（白色矩形）
    painter.setPen(QPen(QColor("#ffffff"), 1))
    painter.setBrush(QBrush(QColor("#ffffff")))
    painter.drawRoundedRect(6, 8, 20, 16, 2, 2)
    
    # 绘制剪贴板顶部夹子
    painter.setPen(QPen(QColor("#c0c0c0"), 1))
    painter.setBrush(QBrush(QColor("#c0c0c0")))
    painter.drawRoundedRect(10, 6, 12, 4, 1, 1)
    
    # 绘制剪贴板内容线条
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QBrush(QColor("#0078d4")))
    
    # 四条内容线条
    painter.drawRoundedRect(8, 12, 16, 2, 1, 1)
    painter.drawRoundedRect(8, 16, 14, 2, 1, 1)
    painter.drawRoundedRect(8, 20, 12, 2, 1, 1)
    painter.drawRoundedRect(8, 24, 15, 2, 1, 1)
    
    painter.end()
    
    # 保存图标
    icon_path = icons_dir / "tray_icon.png"
    pixmap.save(str(icon_path))
    
    print(f"✅ 托盘图标已创建: {icon_path}")
    return icon_path

def create_app_icon():
    """创建应用程序图标（更大尺寸）"""
    # 创建应用程序实例（如果还没有的话）
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # 创建图标目录
    icons_dir = project_root / "resources" / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)
    
    # 图标尺寸
    size = 128
    
    # 创建画布
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    # 创建画家
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # 设置背景圆形
    painter.setPen(QPen(QColor("#0078d4"), 3))
    painter.setBrush(QBrush(QColor("#0078d4")))
    painter.drawEllipse(8, 8, size-16, size-16)
    
    # 绘制剪贴板主体（白色矩形）
    painter.setPen(QPen(QColor("#ffffff"), 2))
    painter.setBrush(QBrush(QColor("#ffffff")))
    painter.drawRoundedRect(24, 32, 80, 64, 8, 8)
    
    # 绘制剪贴板顶部夹子
    painter.setPen(QPen(QColor("#c0c0c0"), 2))
    painter.setBrush(QBrush(QColor("#c0c0c0")))
    painter.drawRoundedRect(40, 24, 48, 16, 4, 4)
    
    # 绘制剪贴板内容线条
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QBrush(QColor("#0078d4")))
    
    # 四条内容线条
    painter.drawRoundedRect(32, 48, 64, 4, 2, 2)
    painter.drawRoundedRect(32, 64, 56, 4, 2, 2)
    painter.drawRoundedRect(32, 80, 48, 4, 2, 2)
    painter.drawRoundedRect(32, 96, 60, 4, 2, 2)
    
    painter.end()
    
    # 保存图标
    icon_path = icons_dir / "app_icon.png"
    pixmap.save(str(icon_path))
    
    print(f"✅ 应用程序图标已创建: {icon_path}")
    return icon_path

if __name__ == "__main__":
    print("🚀 开始创建图标...")
    
    try:
        tray_icon = create_tray_icon()
        app_icon = create_app_icon()
        print("🎉 所有图标创建成功！")
    except Exception as e:
        print(f"❌ 图标创建失败: {e}")
        sys.exit(1) 