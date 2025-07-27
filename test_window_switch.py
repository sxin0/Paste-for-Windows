#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
窗口切换和自动上屏功能测试脚本
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.auto_type import auto_type_manager


def test_window_history():
    """测试窗口历史记录功能"""
    print("🧪 测试窗口历史记录功能...")
    print("=" * 50)
    
    # 清空历史记录
    auto_type_manager.clear_window_history()
    print("已清空窗口历史记录")
    
    # 获取当前窗口
    current_window = auto_type_manager.get_active_window_info()
    print(f"当前窗口: {current_window.get('title', '未知')}")
    
    # 模拟添加窗口到历史记录
    auto_type_manager._add_to_window_history(current_window)
    
    # 查看历史记录
    history = auto_type_manager.get_window_history()
    print(f"历史记录数量: {len(history)}")
    
    for i, window in enumerate(history):
        print(f"  {i+1}. {window.get('title', '未知')} ({window.get('class', '未知')})")
    
    print()


def test_window_switch():
    """测试窗口切换功能"""
    print("🧪 测试窗口切换功能...")
    print("=" * 50)
    
    print("请按照以下步骤操作：")
    print("1. 打开记事本或其他文本编辑器")
    print("2. 在编辑器中点击，确保有输入焦点")
    print("3. 按 Alt+Tab 切换到其他窗口（如浏览器）")
    print("4. 然后运行此测试")
    print()
    
    input("准备好后按回车键继续...")
    
    # 获取当前窗口
    current_window = auto_type_manager.get_active_window_info()
    print(f"当前窗口: {current_window.get('title', '未知')}")
    
    # 添加到历史记录
    auto_type_manager._add_to_window_history(current_window)
    
    # 获取上一个窗口
    previous_window = auto_type_manager._get_previous_window()
    if previous_window:
        print(f"上一个窗口: {previous_window.get('title', '未知')}")
        
        # 尝试切换
        print("尝试切换到上一个窗口...")
        success = auto_type_manager._switch_to_window(previous_window)
        
        if success:
            print("✅ 窗口切换成功！")
            
            # 验证切换结果
            new_window = auto_type_manager.get_active_window_info()
            print(f"切换后窗口: {new_window.get('title', '未知')}")
        else:
            print("❌ 窗口切换失败")
    else:
        print("没有找到上一个窗口")
    
    print()


def test_auto_type_with_switch():
    """测试带窗口切换的自动上屏"""
    print("🧪 测试带窗口切换的自动上屏...")
    print("=" * 50)
    
    print("请按照以下步骤操作：")
    print("1. 打开记事本或其他文本编辑器")
    print("2. 在编辑器中点击，确保有输入焦点")
    print("3. 按 Alt+Tab 切换到其他窗口（如浏览器）")
    print("4. 然后运行此测试")
    print()
    
    input("准备好后按回车键继续...")
    
    # 准备测试文本
    test_text = f"这是窗口切换测试！时间: {time.strftime('%H:%M:%S')}"
    print(f"测试文本: {test_text}")
    
    # 显示当前窗口历史
    history = auto_type_manager.get_window_history()
    print(f"当前窗口历史数量: {len(history)}")
    
    for i, window in enumerate(history[:3]):  # 只显示前3个
        print(f"  {i+1}. {window.get('title', '未知')}")
    
    print()
    print("3秒后开始自动上屏测试...")
    
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    print("🚀 开始自动上屏...")
    
    # 执行自动上屏（带窗口切换）
    success = auto_type_manager.type_text(
        test_text, 
        method="clipboard", 
        switch_to_previous=True
    )
    
    if success:
        print("✅ 自动上屏成功！")
        
        # 显示结果
        history = auto_type_manager.get_window_history()
        if len(history) > 1:
            target_window = history[1]
            print(f"目标窗口: {target_window.get('title', '未知')}")
        
        print("📋 文本应该已经输入到目标窗口")
    else:
        print("❌ 自动上屏失败")
    
    print()


def test_manual_window_switch():
    """手动测试窗口切换"""
    print("🧪 手动测试窗口切换...")
    print("=" * 50)
    
    print("这个测试将帮助您手动验证窗口切换功能")
    print()
    
    while True:
        print("请选择操作：")
        print("1. 显示当前窗口信息")
        print("2. 显示窗口历史记录")
        print("3. 切换到上一个窗口")
        print("4. 清空窗口历史")
        print("5. 退出")
        
        choice = input("请输入选择 (1-5): ").strip()
        
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
            previous = auto_type_manager._get_previous_window()
            if previous:
                print(f"尝试切换到: {previous.get('title', '未知')}")
                success = auto_type_manager._switch_to_window(previous)
                print(f"切换结果: {'✅ 成功' if success else '❌ 失败'}")
            else:
                print("没有找到上一个窗口")
            print()
            
        elif choice == "4":
            auto_type_manager.clear_window_history()
            print("已清空窗口历史记录")
            print()
            
        elif choice == "5":
            break
            
        else:
            print("无效选择，请重新输入")
            print()


if __name__ == "__main__":
    print("🚀 Paste for Windows - 窗口切换功能测试")
    print()
    
    try:
        # 测试窗口历史记录
        test_window_history()
        
        # 测试窗口切换
        test_window_switch()
        
        # 测试自动上屏
        test_auto_type_with_switch()
        
        # 手动测试
        test_manual_window_switch()
        
    except KeyboardInterrupt:
        print("\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc() 