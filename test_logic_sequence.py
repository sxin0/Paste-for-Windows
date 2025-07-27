#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
逻辑顺序测试脚本
测试：双击卡片 -> 关闭自身窗口 -> 查找上个窗口(确认窗口是否还存在)
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.auto_type import auto_type_manager


def test_logic_sequence():
    """测试逻辑顺序"""
    print("🧪 测试逻辑顺序：双击卡片 -> 关闭自身窗口 -> 查找上个窗口")
    print("=" * 60)
    
    # 清空历史记录
    auto_type_manager.clear_window_history()
    print("已清空窗口历史记录")
    
    # 模拟添加一些窗口到历史记录
    test_windows = [
        {"hwnd": 1, "title": "记事本", "class": "Notepad"},
        {"hwnd": 2, "title": "微信", "class": "WeChatMainWndForPC"},
        {"hwnd": 3, "title": "Chrome", "class": "Chrome_WidgetWin_1"},
    ]
    
    for window in test_windows:
        auto_type_manager._add_to_window_history(window)
    
    print("模拟窗口历史记录:")
    history = auto_type_manager.get_window_history()
    for i, window in enumerate(history, 1):
        print(f"  {i}. {window.get('title', '未知')} ({window.get('class', '未知')})")
    
    print()
    print("请按照以下步骤操作：")
    print("1. 打开记事本或其他文本编辑器")
    print("2. 在编辑器中点击，确保有输入焦点")
    print("3. 按 Alt+Tab 切换到其他窗口（如浏览器）")
    print("4. 然后运行此测试")
    print()
    
    input("准备好后按回车键继续...")
    
    # 获取当前窗口（模拟剪贴板历史窗口）
    current_window = auto_type_manager.get_active_window_info()
    print(f"当前窗口（剪贴板历史）: {current_window.get('title', '未知')}")
    
    # 添加到历史记录
    auto_type_manager._add_to_window_history(current_window)
    
    print()
    print("🔄 开始逻辑顺序测试...")
    print()
    
    # 步骤1：查找目标窗口（确认窗口是否还存在）
    print("步骤1: 查找目标窗口（确认窗口是否还存在）")
    target_window = auto_type_manager.find_best_target_window()
    
    if target_window:
        print(f"✅ 找到目标窗口: {target_window.get('title', '未知')}")
        
        # 验证窗口存在性
        if auto_type_manager.verify_window_exists(target_window):
            print("✅ 窗口存在性验证通过")
        else:
            print("❌ 窗口存在性验证失败")
            return
    else:
        print("❌ 没有找到合适的目标窗口")
        return
    
    print()
    
    # 步骤2：准备测试文本
    test_text = f"逻辑顺序测试！时间: {time.strftime('%H:%M:%S')}"
    print(f"步骤2: 准备测试文本: {test_text}")
    print()
    
    # 步骤3：执行自动上屏（模拟关闭自身窗口后的操作）
    print("步骤3: 执行自动上屏（模拟关闭自身窗口后的操作）")
    print("3秒后开始...")
    
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    print("🚀 开始自动上屏...")
    
    # 执行自动上屏
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
    print("=" * 60)
    print("🎉 逻辑顺序测试完成！")


def test_window_verification():
    """测试窗口验证功能"""
    print("🧪 测试窗口验证功能...")
    print("=" * 50)
    
    # 获取当前窗口
    current_window = auto_type_manager.get_active_window_info()
    print(f"当前窗口: {current_window.get('title', '未知')}")
    
    # 验证窗口存在性
    exists = auto_type_manager.verify_window_exists(current_window)
    print(f"窗口存在性: {'✅ 存在' if exists else '❌ 不存在'}")
    
    # 测试无效窗口
    invalid_window = {"hwnd": 999999, "title": "无效窗口", "class": "Invalid"}
    exists = auto_type_manager.verify_window_exists(invalid_window)
    print(f"无效窗口存在性: {'✅ 存在' if exists else '❌ 不存在'}")
    
    print()


def test_window_switching():
    """测试窗口切换功能"""
    print("🧪 测试窗口切换功能...")
    print("=" * 50)
    
    # 获取所有可见窗口
    visible_windows = auto_type_manager.get_visible_windows()
    print(f"找到 {len(visible_windows)} 个可见窗口")
    
    # 查找目标窗口
    target_window = auto_type_manager.find_best_target_window()
    if target_window:
        print(f"目标窗口: {target_window.get('title', '未知')}")
        
        # 尝试切换
        print("尝试切换到目标窗口...")
        success = auto_type_manager._switch_to_window(target_window)
        
        if success:
            print("✅ 窗口切换成功")
            
            # 验证切换结果
            new_window = auto_type_manager.get_active_window_info()
            print(f"切换后窗口: {new_window.get('title', '未知')}")
        else:
            print("❌ 窗口切换失败")
    else:
        print("没有找到目标窗口")
    
    print()


if __name__ == "__main__":
    print("🚀 Paste for Windows - 逻辑顺序测试")
    print()
    
    try:
        # 测试窗口验证
        test_window_verification()
        
        # 测试窗口切换
        test_window_switching()
        
        # 测试逻辑顺序
        test_logic_sequence()
        
    except KeyboardInterrupt:
        print("\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc() 