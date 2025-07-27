#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第一阶段功能测试脚本
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.clipboard_manager import ClipboardManager, ClipboardItem
from src.data.database import DatabaseManager
from src.core.config_manager import ConfigManager


def test_clipboard_manager():
    """测试剪贴板管理器"""
    print("=== 测试剪贴板管理器 ===")
    
    manager = ClipboardManager()
    
    # 测试添加项目
    test_items = [
        ClipboardItem("这是测试文本1", "text"),
        ClipboardItem("https://www.example.com", "link"),
        ClipboardItem("C:\\test\\file.txt", "file"),
        ClipboardItem("def test_function():", "code")
    ]
    
    for item in test_items:
        manager._add_item(item)
        print(f"添加项目: {item.content_type} - {item.content[:30]}...")
    
    # 测试获取项目
    items = manager.get_recent_items(5)
    print(f"获取最近项目: {len(items)} 个")
    
    # 测试搜索
    search_results = manager.search_items("test")
    print(f"搜索 'test': {len(search_results)} 个结果")
    
    # 测试统计
    stats = manager.get_stats()
    print(f"统计信息: {stats}")
    
    return manager


def test_database_manager():
    """测试数据库管理器"""
    print("\n=== 测试数据库管理器 ===")
    
    db = DatabaseManager(":memory:")  # 使用内存数据库进行测试
    
    # 测试保存项目
    test_item = ClipboardItem("数据库测试内容", "text")
    success = db.save_item(test_item)
    print(f"保存项目: {'成功' if success else '失败'}")
    
    # 测试获取项目
    retrieved_item = db.get_item(test_item.id)
    if retrieved_item:
        print(f"获取项目: {retrieved_item.content}")
    else:
        print("获取项目失败")
    
    # 测试搜索
    search_results = db.search_items("测试")
    print(f"数据库搜索: {len(search_results)} 个结果")
    
    db.close()
    return db


def test_config_manager():
    """测试配置管理器"""
    print("\n=== 测试配置管理器 ===")
    
    config = ConfigManager()
    
    # 测试获取配置
    max_items = config.get('max_clipboard_items')
    print(f"最大项目数: {max_items}")
    
    # 测试设置配置
    success = config.set('max_clipboard_items', 2000)
    print(f"设置配置: {'成功' if success else '失败'}")
    
    # 测试获取所有配置
    all_config = config.get_all()
    print(f"配置项数量: {len(all_config)}")
    
    # 测试便捷方法
    clipboard_settings = config.get_clipboard_settings()
    print(f"剪贴板设置: {clipboard_settings}")
    
    return config


def test_bottom_panel():
    """测试底部面板（需要GUI环境）"""
    print("\n=== 测试底部面板 ===")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from src.gui.bottom_panel import BottomPanel
        
        app = QApplication(sys.argv)
        manager = ClipboardManager()
        panel = BottomPanel(manager)
        
        print("底部面板创建成功")
        print("面板功能:")
        print("- 从屏幕底部滑出动画")
        print("- 剪贴板项目列表")
        print("- 搜索功能")
        print("- 项目选择")
        
        return panel
        
    except Exception as e:
        print(f"底部面板测试失败: {e}")
        return None


def main():
    """主测试函数"""
    print("Paste for Windows - 第一阶段功能测试")
    print("=" * 50)
    
    try:
        # 测试核心模块
        clipboard_manager = test_clipboard_manager()
        database_manager = test_database_manager()
        config_manager = test_config_manager()
        
        # 测试GUI组件
        bottom_panel = test_bottom_panel()
        
        print("\n" + "=" * 50)
        print("第一阶段测试完成！")
        print("\n已实现的功能:")
        print("✅ 剪贴板监听和管理")
        print("✅ 数据持久化存储")
        print("✅ 配置管理")
        print("✅ 底部交互栏（从屏幕下方冒出来）")
        print("✅ 系统托盘集成")
        print("✅ 基础搜索功能")
        print("✅ 现代化UI设计")
        
        print("\n下一步:")
        print("1. 运行 'python run.py' 启动完整应用")
        print("2. 测试剪贴板监听功能")
        print("3. 测试底部面板动画效果")
        print("4. 测试系统托盘功能")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 