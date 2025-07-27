#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试剪贴板冲突修复
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


def test_clipboard_access():
    """测试剪贴板访问"""
    print("🧪 开始测试剪贴板访问...")
    
    # 创建剪贴板管理器
    clipboard_manager = ClipboardManager()
    
    try:
        # 启动剪贴板监听
        print("📋 启动剪贴板监听...")
        clipboard_manager.start()
        
        # 等待一下让监听器稳定
        time.sleep(1)
        
        # 测试多次剪贴板访问
        print("🔄 测试剪贴板访问...")
        for i in range(5):
            try:
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
        
        # 测试设置剪贴板内容
        print("📝 测试设置剪贴板内容...")
        test_content = f"测试内容 - {time.time()}"
        
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, test_content)
            win32clipboard.CloseClipboard()
            print("✅ 设置剪贴板内容成功")
        except Exception as e:
            print(f"❌ 设置剪贴板内容失败: {e}")
        
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
        
        print("\n🎯 测试完成！")
        print("💡 现在请尝试在其他应用程序中按 Ctrl+V，看看是否正常工作")
        print("💡 如果 Ctrl+V 正常工作，说明冲突问题已修复")
        
        # 保持运行一段时间供用户测试
        input("\n按回车键退出测试...")
        
    finally:
        # 停止剪贴板监听
        clipboard_manager.stop()
        print("✅ 剪贴板监听已停止")


def test_manual_clipboard():
    """手动测试剪贴板功能"""
    print("\n🔧 手动测试剪贴板功能...")
    
    try:
        # 设置测试内容
        test_content = "这是一个测试内容，用于验证剪贴板功能"
        print(f"📝 设置剪贴板内容: {test_content}")
        
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
            else:
                print("📋 剪贴板中没有文本内容")
        finally:
            win32clipboard.CloseClipboard()
            
    except Exception as e:
        print(f"❌ 手动测试失败: {e}")


if __name__ == "__main__":
    print("🚀 剪贴板冲突修复测试")
    print("=" * 50)
    
    # 运行测试
    test_clipboard_access()
    test_manual_clipboard()
    
    print("\n✅ 测试完成！") 