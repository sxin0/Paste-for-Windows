#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光标位置管理功能测试脚本
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.auto_type import auto_type_manager


def test_cursor_position_management():
    """测试光标位置管理功能"""
    print("🧪 测试光标位置管理功能...")
    print("=" * 50)
    
    # 清空历史记录
    auto_type_manager.clear_window_history()
    
    # 获取当前光标位置
    current_pos = auto_type_manager.get_cursor_position()
    print(f"当前光标位置: {current_pos}")
    
    # 获取当前窗口
    current_window = auto_type_manager.get_active_window_info()
    hwnd = current_window.get("hwnd")
    print(f"当前窗口: {current_window.get('title', '未知')} (句柄: {hwnd})")
    
    # 保存光标位置
    if hwnd:
        success = auto_type_manager.save_cursor_position(hwnd)
        print(f"保存光标位置: {'✅ 成功' if success else '❌ 失败'}")
    
    # 移动光标到其他位置
    print("移动光标到新位置...")
    new_pos = (current_pos[0] + 100, current_pos[1] + 100)
    auto_type_manager.click_at_position(new_pos[0], new_pos[1])
    
    # 验证光标位置已改变
    new_current_pos = auto_type_manager.get_cursor_position()
    print(f"移动后光标位置: {new_current_pos}")
    
    # 恢复光标位置
    if hwnd:
        success = auto_type_manager.restore_cursor_position(hwnd)
        print(f"恢复光标位置: {'✅ 成功' if success else '❌ 失败'}")
        
        # 验证恢复结果
        restored_pos = auto_type_manager.get_cursor_position()
        print(f"恢复后光标位置: {restored_pos}")
        
        if restored_pos == current_pos:
            print("✅ 光标位置恢复成功")
        else:
            print("❌ 光标位置恢复失败")
    
    print()


def test_input_area_focus():
    """测试输入区域聚焦功能"""
    print("🧪 测试输入区域聚焦功能...")
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
    hwnd = current_window.get("hwnd")
    print(f"当前窗口: {current_window.get('title', '未知')}")
    
    # 添加到历史记录
    auto_type_manager._add_to_window_history(current_window)
    
    # 查找目标窗口
    target_window = auto_type_manager.find_best_target_window()
    if target_window:
        target_hwnd = target_window.get("hwnd")
        target_title = target_window.get("title", "未知")
        print(f"目标窗口: {target_title}")
        
        # 测试聚焦输入区域
        print("测试聚焦输入区域...")
        success = auto_type_manager.focus_input_area(target_hwnd)
        print(f"聚焦结果: {'✅ 成功' if success else '❌ 失败'}")
        
        if success:
            print("📝 光标应该已经聚焦到输入区域")
        else:
            print("⚠️ 聚焦失败，可能需要手动点击输入区域")
    else:
        print("没有找到目标窗口")
    
    print()


def test_window_switch_with_cursor():
    """测试带光标位置管理的窗口切换"""
    print("🧪 测试带光标位置管理的窗口切换...")
    print("=" * 50)
    
    print("请按照以下步骤操作：")
    print("1. 打开记事本或其他文本编辑器")
    print("2. 在编辑器中点击一个特定位置（记住这个位置）")
    print("3. 按 Alt+Tab 切换到其他窗口（如浏览器）")
    print("4. 然后运行此测试")
    print()
    
    input("准备好后按回车键继续...")
    
    # 获取当前光标位置
    current_pos = auto_type_manager.get_cursor_position()
    print(f"当前光标位置: {current_pos}")
    
    # 获取当前窗口
    current_window = auto_type_manager.get_active_window_info()
    hwnd = current_window.get("hwnd")
    print(f"当前窗口: {current_window.get('title', '未知')}")
    
    # 保存光标位置
    if hwnd:
        auto_type_manager.save_cursor_position(hwnd)
        print("已保存光标位置")
    
    # 添加到历史记录
    auto_type_manager._add_to_window_history(current_window)
    
    # 查找目标窗口
    target_window = auto_type_manager.find_best_target_window()
    if target_window:
        target_hwnd = target_window.get("hwnd")
        target_title = target_window.get("title", "未知")
        print(f"目标窗口: {target_title}")
        
        print("3秒后开始窗口切换测试...")
        for i in range(3, 0, -1):
            print(f"  {i}...")
            time.sleep(1)
        
        # 执行窗口切换
        print("🚀 开始窗口切换...")
        success = auto_type_manager._switch_to_window(target_window)
        
        if success:
            print("✅ 窗口切换成功")
            
            # 验证光标位置
            new_pos = auto_type_manager.get_cursor_position()
            print(f"切换后光标位置: {new_pos}")
            
            if new_pos == current_pos:
                print("✅ 光标位置已恢复")
            else:
                print("⚠️ 光标位置未恢复，可能需要手动聚焦")
        else:
            print("❌ 窗口切换失败")
    else:
        print("没有找到目标窗口")
    
    print()


def test_cursor_cache_management():
    """测试光标位置缓存管理"""
    print("🧪 测试光标位置缓存管理...")
    print("=" * 50)
    
    # 清空历史记录
    auto_type_manager.clear_window_history()
    
    # 模拟多个窗口的光标位置
    test_windows = [
        {"hwnd": 1001, "title": "记事本", "class": "Notepad"},
        {"hwnd": 1002, "title": "微信", "class": "WeChatMainWndForPC"},
        {"hwnd": 1003, "title": "Chrome", "class": "Chrome_WidgetWin_1"},
    ]
    
    # 模拟保存光标位置
    for i, window in enumerate(test_windows):
        hwnd = window["hwnd"]
        pos = (100 + i * 50, 100 + i * 50)
        auto_type_manager.cursor_positions[hwnd] = pos
        print(f"模拟保存窗口 {window['title']} 的光标位置: {pos}")
    
    # 显示缓存内容
    print(f"\n光标位置缓存数量: {len(auto_type_manager.cursor_positions)}")
    for hwnd, pos in auto_type_manager.cursor_positions.items():
        window_title = "未知"
        for window in test_windows:
            if window["hwnd"] == hwnd:
                window_title = window["title"]
                break
        print(f"  窗口 {window_title}: {pos}")
    
    # 测试恢复光标位置
    print("\n测试恢复光标位置:")
    for window in test_windows:
        hwnd = window["hwnd"]
        success = auto_type_manager.restore_cursor_position(hwnd)
        print(f"  恢复 {window['title']}: {'✅ 成功' if success else '❌ 失败'}")
    
    print()


if __name__ == "__main__":
    print("🚀 Paste for Windows - 光标位置管理功能测试")
    print()
    
    try:
        # 测试光标位置管理
        test_cursor_position_management()
        
        # 测试光标位置缓存管理
        test_cursor_cache_management()
        
        # 测试输入区域聚焦
        test_input_area_focus()
        
        # 测试带光标位置管理的窗口切换
        test_window_switch_with_cursor()
        
    except KeyboardInterrupt:
        print("\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc() 