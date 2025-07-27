#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Windows消息机制的剪贴板监听
验证 Ctrl+V 快捷键是否正常工作
"""

import sys
import time
import win32clipboard
import win32con
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.clipboard_manager import ClipboardManager


def test_message_based_clipboard():
    """测试基于消息的剪贴板监听"""
    print("🧪 开始测试Windows消息机制的剪贴板监听...")
    
    # 创建剪贴板管理器
    clipboard_manager = ClipboardManager()
    
    try:
        # 启动剪贴板监听
        print("📋 启动剪贴板监听（Windows消息机制）...")
        clipboard_manager.start()
        
        # 等待一下让监听器稳定
        time.sleep(2)
        
        print("\n🎯 测试阶段 1: 验证监听器正常工作")
        print("请复制一些文本内容，然后按回车继续...")
        input()
        
        # 检查是否有新项目
        items = clipboard_manager.get_recent_items(5)
        if items:
            print(f"✅ 监听器正常工作，捕获到 {len(items)} 个项目")
            for i, item in enumerate(items[:3]):
                print(f"   {i+1}. {item.content[:50]}{'...' if len(item.content) > 50 else ''}")
        else:
            print("⚠️ 监听器没有捕获到内容")
        
        print("\n🎯 测试阶段 2: 验证 Ctrl+V 功能")
        print("现在请尝试在其他应用程序中按 Ctrl+V，看看是否正常工作")
        print("如果 Ctrl+V 正常工作，说明冲突问题已彻底解决")
        
        # 设置一个测试内容
        test_content = f"测试内容 - {time.time()}"
        print(f"\n📝 设置测试内容: {test_content}")
        
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, test_content)
            win32clipboard.CloseClipboard()
            print("✅ 测试内容设置成功")
        except Exception as e:
            print(f"❌ 设置测试内容失败: {e}")
        
        print("\n💡 现在请尝试按 Ctrl+V 粘贴这个测试内容")
        print("如果粘贴成功，说明剪贴板访问冲突已解决")
        
        input("\n按回车键继续...")
        
        # 等待一下让监听器处理
        time.sleep(1)
        
        # 检查是否被监听器捕获
        items = clipboard_manager.get_recent_items(5)
        if items:
            latest_item = items[0]
            if test_content in latest_item.content:
                print("✅ 剪贴板内容被正确监听")
            else:
                print("⚠️ 剪贴板内容未被监听器捕获")
        else:
            print("⚠️ 监听器中没有项目")
        
        print("\n🎯 测试阶段 3: 连续测试")
        print("现在进行连续测试，验证稳定性...")
        
        for i in range(3):
            test_content = f"连续测试 {i+1} - {time.time()}"
            print(f"📝 设置内容 {i+1}: {test_content}")
            
            try:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, test_content)
                win32clipboard.CloseClipboard()
                print(f"✅ 内容 {i+1} 设置成功")
            except Exception as e:
                print(f"❌ 内容 {i+1} 设置失败: {e}")
            
            time.sleep(0.5)  # 等待一下
        
        # 等待监听器处理
        time.sleep(1)
        
        # 检查结果
        items = clipboard_manager.get_recent_items(10)
        print(f"\n📊 监听器捕获到 {len(items)} 个项目")
        
        print("\n🎯 测试完成！")
        print("💡 如果 Ctrl+V 在整个测试过程中都正常工作，说明问题已彻底解决")
        print("💡 如果仍然需要多次按 Ctrl+V，请检查是否有其他程序在干扰")
        
        # 保持运行一段时间供用户测试
        input("\n按回车键退出测试...")
        
    finally:
        # 停止剪贴板监听
        clipboard_manager.stop()
        print("✅ 剪贴板监听已停止")


def test_manual_clipboard_access():
    """手动测试剪贴板访问"""
    print("\n🔧 手动测试剪贴板访问...")
    
    for i in range(5):
        try:
            print(f"📋 第 {i+1} 次访问剪贴板...")
            
            # 尝试访问剪贴板
            win32clipboard.OpenClipboard()
            try:
                if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                    content = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                    print(f"✅ 第 {i+1} 次访问成功，内容长度: {len(content) if content else 0}")
                else:
                    print(f"✅ 第 {i+1} 次访问成功，无文本内容")
            finally:
                win32clipboard.CloseClipboard()
            
            time.sleep(0.2)  # 等待一下
            
        except Exception as e:
            print(f"❌ 第 {i+1} 次访问失败: {e}")


def test_clipboard_setting():
    """测试剪贴板设置"""
    print("\n📝 测试剪贴板设置功能...")
    
    test_content = "这是一个测试内容，用于验证剪贴板设置功能"
    print(f"📝 设置内容: {test_content}")
    
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, test_content)
        win32clipboard.CloseClipboard()
        
        print("✅ 剪贴板内容设置成功")
        print("💡 现在请按 Ctrl+V 粘贴内容，看看是否正常工作")
        
        input("按回车键继续...")
        
        # 读取剪贴板内容
        win32clipboard.OpenClipboard()
        try:
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                content = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                print(f"📋 当前剪贴板内容: {content}")
                if content == test_content:
                    print("✅ 剪贴板内容正确")
                else:
                    print("❌ 剪贴板内容不正确")
            else:
                print("📋 剪贴板中没有文本内容")
        finally:
            win32clipboard.CloseClipboard()
            
    except Exception as e:
        print(f"❌ 剪贴板设置测试失败: {e}")


if __name__ == "__main__":
    print("🚀 Windows消息机制剪贴板监听测试")
    print("=" * 60)
    
    # 运行测试
    test_message_based_clipboard()
    test_manual_clipboard_access()
    test_clipboard_setting()
    
    print("\n✅ 所有测试完成！")
    print("\n📋 测试总结:")
    print("1. 如果 Ctrl+V 在整个测试过程中都正常工作，说明问题已解决")
    print("2. 如果仍然需要多次按 Ctrl+V，可能是其他程序在干扰")
    print("3. 建议重启电脑，确保没有其他剪贴板管理器在运行") 