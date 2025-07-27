#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 11 风格自动上屏功能测试脚本
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.auto_type import auto_type_manager


def test_windows11_style_auto_type():
    """测试Windows 11风格的自动上屏功能"""
    print("🧪 测试Windows 11风格的自动上屏功能...")
    print("=" * 60)
    
    print("请按照以下步骤操作：")
    print("1. 打开记事本或其他文本编辑器")
    print("2. 在编辑器中点击，确保有输入焦点")
    print("3. 保持记事本窗口激活状态")
    print("4. 然后运行此测试")
    print()
    
    input("准备好后按回车键继续...")
    
    # 获取当前激活窗口
    current_window = auto_type_manager.get_active_window_info()
    current_title = current_window.get("title", "未知")
    current_hwnd = current_window.get("hwnd")
    
    print(f"当前激活窗口: {current_title} (句柄: {current_hwnd})")
    
    # 测试文本
    test_text = "这是Windows 11风格的自动上屏测试内容！"
    print(f"测试文本: {test_text}")
    
    print("\n3秒后开始自动上屏测试...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    # 执行Windows 11风格的自动上屏
    print("🚀 开始自动上屏...")
    success = auto_type_manager.type_text(
        test_text,
        method="clipboard"
    )
    
    if success:
        print("✅ 自动上屏成功")
        print("📝 文本应该已经输入到当前激活的窗口中")
    else:
        print("❌ 自动上屏失败")
    
    print()


def test_direct_input_to_active_window():
    """测试直接输入到当前激活窗口"""
    print("🧪 测试直接输入到当前激活窗口...")
    print("=" * 60)
    
    print("请按照以下步骤操作：")
    print("1. 打开微信、QQ或其他聊天应用")
    print("2. 在聊天输入框中点击，确保有输入焦点")
    print("3. 保持聊天窗口激活状态")
    print("4. 然后运行此测试")
    print()
    
    input("准备好后按回车键继续...")
    
    # 获取当前激活窗口
    current_window = auto_type_manager.get_active_window_info()
    current_title = current_window.get("title", "未知")
    
    print(f"当前激活窗口: {current_title}")
    
    # 测试文本
    test_text = "Hello! 这是直接输入测试。"
    print(f"测试文本: {test_text}")
    
    print("\n3秒后开始直接输入测试...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    # 执行直接输入
    print("🚀 开始直接输入...")
    success = auto_type_manager.type_text(
        test_text,
        method="clipboard"
    )
    
    if success:
        print("✅ 直接输入成功")
        print("💬 文本应该已经输入到聊天输入框中")
    else:
        print("❌ 直接输入失败")
    
    print()


def test_no_window_switching():
    """测试不进行窗口切换的自动上屏"""
    print("🧪 测试不进行窗口切换的自动上屏...")
    print("=" * 60)
    
    print("请按照以下步骤操作：")
    print("1. 打开任意文本编辑器（如Word、记事本等）")
    print("2. 在编辑器中点击，确保有输入焦点")
    print("3. 保持编辑器窗口激活状态")
    print("4. 然后运行此测试")
    print()
    
    input("准备好后按回车键继续...")
    
    # 获取当前激活窗口
    current_window = auto_type_manager.get_active_window_info()
    current_title = current_window.get("title", "未知")
    
    print(f"当前激活窗口: {current_title}")
    
    # 测试文本
    test_text = "这是不进行窗口切换的测试内容。\n支持多行文本。\n就像Windows 11的剪贴板历史一样！"
    print(f"测试文本: {test_text}")
    
    print("\n3秒后开始测试...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    # 执行不进行窗口切换的自动上屏
    print("🚀 开始自动上屏（不切换窗口）...")
    success = auto_type_manager.type_text(
        test_text,
        method="clipboard"
    )
    
    if success:
        print("✅ 自动上屏成功")
        print("📝 文本应该已经直接输入到当前激活的窗口中")
        print("🔄 没有进行任何窗口切换操作")
    else:
        print("❌ 自动上屏失败")
    
    print()


def test_safety_check():
    """测试安全检查功能"""
    print("🧪 测试安全检查功能...")
    print("=" * 60)
    
    # 获取当前激活窗口
    current_window = auto_type_manager.get_active_window_info()
    current_title = current_window.get("title", "未知")
    
    print(f"当前激活窗口: {current_title}")
    
    # 检查是否安全
    is_safe = auto_type_manager.is_safe_to_type()
    print(f"安全检查结果: {'✅ 安全' if is_safe else '❌ 不安全'}")
    
    if not is_safe:
        print("⚠️ 当前窗口被认为不安全，不会进行自动上屏")
        print("安全窗口包括：聊天应用、文本编辑器、浏览器等")
        print("不安全窗口包括：任务管理器、命令提示符、系统工具等")
    else:
        print("✅ 当前窗口安全，可以进行自动上屏")
    
    print()


def test_clipboard_method():
    """测试剪贴板输入方法"""
    print("🧪 测试剪贴板输入方法...")
    print("=" * 60)
    
    print("请按照以下步骤操作：")
    print("1. 打开任意文本编辑器")
    print("2. 在编辑器中点击，确保有输入焦点")
    print("3. 保持编辑器窗口激活状态")
    print("4. 然后运行此测试")
    print()
    
    input("准备好后按回车键继续...")
    
    # 测试文本（包含特殊字符）
    test_text = "剪贴板方法测试：\n• 支持换行\n• 支持特殊字符：@#$%^&*()\n• 支持中文：你好世界！\n• 支持数字：1234567890"
    print(f"测试文本: {test_text}")
    
    print("\n3秒后开始剪贴板方法测试...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    # 执行剪贴板方法输入
    print("🚀 开始剪贴板方法输入...")
    success = auto_type_manager.type_text(
        test_text,
        method="clipboard"
    )
    
    if success:
        print("✅ 剪贴板方法输入成功")
        print("📋 文本应该已经通过剪贴板方式输入")
        print("💡 剪贴板方法的优点：速度快，支持特殊字符，不会触发输入法")
    else:
        print("❌ 剪贴板方法输入失败")
    
    print()


if __name__ == "__main__":
    print("🚀 Paste for Windows - Windows 11风格自动上屏功能测试")
    print()
    
    try:
        # 测试安全检查
        test_safety_check()
        
        # 测试Windows 11风格的自动上屏
        test_windows11_style_auto_type()
        
        # 测试直接输入到当前激活窗口
        test_direct_input_to_active_window()
        
        # 测试不进行窗口切换的自动上屏
        test_no_window_switching()
        
        # 测试剪贴板输入方法
        test_clipboard_method()
        
        print("🎉 所有测试完成！")
        print("\n📝 总结：")
        print("• Windows 11风格的自动上屏不需要窗口切换")
        print("• 直接在当前激活窗口输入内容")
        print("• 保持原窗口的激活状态和光标位置")
        print("• 使用剪贴板方法，速度快且稳定")
        
    except KeyboardInterrupt:
        print("\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc() 