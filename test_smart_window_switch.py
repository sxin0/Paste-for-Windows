#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能窗口切换功能测试脚本
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.auto_type import auto_type_manager


def test_window_enumeration():
    """测试窗口枚举功能"""
    print("🧪 测试窗口枚举功能...")
    print("=" * 50)
    
    # 获取所有可见窗口
    visible_windows = auto_type_manager.get_visible_windows()
    print(f"找到 {len(visible_windows)} 个可见窗口:")
    
    for i, window in enumerate(visible_windows[:10], 1):  # 只显示前10个
        title = window.get("title", "未知")
        class_name = window.get("class", "未知")
        print(f"  {i}. {title} ({class_name})")
    
    if len(visible_windows) > 10:
        print(f"  ... 还有 {len(visible_windows) - 10} 个窗口")
    
    print()


def test_smart_window_finding():
    """测试智能窗口查找功能"""
    print("🧪 测试智能窗口查找功能...")
    print("=" * 50)
    
    # 清空历史记录
    auto_type_manager.clear_window_history()
    
    # 获取当前窗口
    current_window = auto_type_manager.get_active_window_info()
    print(f"当前窗口: {current_window.get('title', '未知')} ({current_window.get('class', '未知')})")
    
    # 添加到历史记录
    auto_type_manager._add_to_window_history(current_window)
    
    # 查找最佳目标窗口
    target_window = auto_type_manager.find_best_target_window()
    
    if target_window:
        print(f"找到目标窗口: {target_window.get('title', '未知')} ({target_window.get('class', '未知')})")
    else:
        print("没有找到合适的目标窗口")
    
    print()


def test_window_history_management():
    """测试窗口历史记录管理"""
    print("🧪 测试窗口历史记录管理...")
    print("=" * 50)
    
    # 清空历史记录
    auto_type_manager.clear_window_history()
    
    # 模拟添加多个窗口到历史记录
    test_windows = [
        {"hwnd": 1, "title": "记事本", "class": "Notepad"},
        {"hwnd": 2, "title": "main.py - paste-for-windows - Cursor", "class": "Chrome_WidgetWin_1"},
        {"hwnd": 3, "title": "微信", "class": "WeChatMainWndForPC"},
        {"hwnd": 4, "title": "test.py - paste-for-windows - Cursor", "class": "Chrome_WidgetWin_1"},
        {"hwnd": 5, "title": "Chrome", "class": "Chrome_WidgetWin_1"},
    ]
    
    for window in test_windows:
        auto_type_manager._add_to_window_history(window)
    
    # 显示历史记录
    history = auto_type_manager.get_window_history()
    print(f"窗口历史记录 ({len(history)} 个):")
    for i, window in enumerate(history, 1):
        title = window.get("title", "未知")
        class_name = window.get("class", "未知")
        print(f"  {i}. {title} ({class_name})")
    
    # 测试智能查找
    print("\n测试智能窗口查找:")
    target_window = auto_type_manager.find_best_target_window()
    if target_window:
        print(f"找到目标窗口: {target_window.get('title', '未知')}")
    else:
        print("没有找到合适的目标窗口")
    
    print()


def test_auto_type_with_smart_switch():
    """测试带智能窗口切换的自动上屏"""
    print("🧪 测试带智能窗口切换的自动上屏...")
    print("=" * 50)
    
    print("请按照以下步骤操作：")
    print("1. 打开记事本或其他文本编辑器")
    print("2. 在编辑器中点击，确保有输入焦点")
    print("3. 按 Alt+Tab 切换到其他窗口（如浏览器）")
    print("4. 然后运行此测试")
    print()
    
    input("准备好后按回车键继续...")
    
    # 准备测试文本
    test_text = f"这是智能窗口切换测试！时间: {time.strftime('%H:%M:%S')}"
    print(f"测试文本: {test_text}")
    
    # 显示当前窗口信息
    current_window = auto_type_manager.get_active_window_info()
    print(f"当前窗口: {current_window.get('title', '未知')}")
    
    # 查找目标窗口
    target_window = auto_type_manager.find_best_target_window()
    if target_window:
        print(f"目标窗口: {target_window.get('title', '未知')}")
    else:
        print("没有找到目标窗口，将使用当前窗口")
    
    print()
    print("3秒后开始自动上屏测试...")
    
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    print("🚀 开始自动上屏...")
    
    # 执行自动上屏（带智能窗口切换）
    success = auto_type_manager.type_text(
        test_text, 
        method="clipboard", 
        switch_to_previous=True
    )
    
    if success:
        print("✅ 自动上屏成功！")
        print("📋 文本应该已经输入到目标窗口")
    else:
        print("❌ 自动上屏失败")
    
    print()


def test_manual_smart_switch():
    """手动测试智能窗口切换"""
    print("🧪 手动测试智能窗口切换...")
    print("=" * 50)
    
    print("这个测试将帮助您手动验证智能窗口切换功能")
    print()
    
    while True:
        print("请选择操作：")
        print("1. 显示当前窗口信息")
        print("2. 显示窗口历史记录")
        print("3. 显示所有可见窗口")
        print("4. 查找最佳目标窗口")
        print("5. 切换到最佳目标窗口")
        print("6. 清空窗口历史")
        print("7. 退出")
        
        choice = input("请输入选择 (1-7): ").strip()
        
        if choice == "1":
            window = auto_type_manager.get_active_window_info()
            print(f"当前窗口: {window.get('title', '未知')}")
            print(f"窗口类名: {window.get('class', '未知')}")
            print(f"窗口句柄: {window.get('hwnd', '未知')}")
            print()
            
        elif choice == "2":
            history = auto_type_manager.get_window_history()
            print(f"窗口历史记录 ({len(history)} 个):")
            for i, window in enumerate(history):
                print(f"  {i+1}. {window.get('title', '未知')} ({window.get('class', '未知')})")
            print()
            
        elif choice == "3":
            visible_windows = auto_type_manager.get_visible_windows()
            print(f"可见窗口 ({len(visible_windows)} 个):")
            for i, window in enumerate(visible_windows[:10], 1):
                print(f"  {i}. {window.get('title', '未知')} ({window.get('class', '未知')})")
            if len(visible_windows) > 10:
                print(f"  ... 还有 {len(visible_windows) - 10} 个窗口")
            print()
            
        elif choice == "4":
            target_window = auto_type_manager.find_best_target_window()
            if target_window:
                print(f"最佳目标窗口: {target_window.get('title', '未知')} ({target_window.get('class', '未知')})")
            else:
                print("没有找到合适的目标窗口")
            print()
            
        elif choice == "5":
            target_window = auto_type_manager.find_best_target_window()
            if target_window:
                print(f"尝试切换到: {target_window.get('title', '未知')}")
                success = auto_type_manager._switch_to_window(target_window)
                print(f"切换结果: {'✅ 成功' if success else '❌ 失败'}")
                
                if success:
                    # 验证切换结果
                    new_window = auto_type_manager.get_active_window_info()
                    print(f"切换后窗口: {new_window.get('title', '未知')}")
            else:
                print("没有找到合适的目标窗口")
            print()
            
        elif choice == "6":
            auto_type_manager.clear_window_history()
            print("已清空窗口历史记录")
            print()
            
        elif choice == "7":
            break
            
        else:
            print("无效选择，请重新输入")
            print()


if __name__ == "__main__":
    print("🚀 Paste for Windows - 智能窗口切换功能测试")
    print()
    
    try:
        # 测试窗口枚举
        test_window_enumeration()
        
        # 测试智能窗口查找
        test_smart_window_finding()
        
        # 测试窗口历史管理
        test_window_history_management()
        
        # 测试自动上屏
        test_auto_type_with_smart_switch()
        
        # 手动测试
        test_manual_smart_switch()
        
    except KeyboardInterrupt:
        print("\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc() 