#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动上屏功能测试脚本
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.auto_type import auto_type_manager


def test_auto_type():
    """测试自动上屏功能"""
    print("🧪 开始测试自动上屏功能...")
    print("=" * 50)
    
    # 测试1：获取当前窗口信息
    print("1. 获取当前窗口信息...")
    window_info = auto_type_manager.get_active_window_info()
    print(f"   当前窗口: {window_info.get('title', '未知')}")
    print(f"   窗口类名: {window_info.get('class', '未知')}")
    print()
    
    # 测试2：安全检查
    print("2. 安全检查...")
    is_safe = auto_type_manager.is_safe_to_type()
    print(f"   是否安全: {'✅ 安全' if is_safe else '❌ 不安全'}")
    print()
    
    if not is_safe:
        print("⚠️  当前窗口不安全，建议切换到安全的应用程序（如记事本、微信等）")
        print("   然后重新运行测试")
        return
    
    # 测试3：准备测试文本
    test_text = "Hello, 这是自动上屏测试！\n当前时间: " + time.strftime("%H:%M:%S")
    print(f"3. 准备测试文本: {test_text}")
    print()
    
    # 测试4：执行自动上屏
    print("4. 执行自动上屏...")
    print("   ⚠️  请确保当前窗口有输入焦点（如记事本、微信对话框等）")
    print("   📝 3秒后开始输入...")
    
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("   🚀 开始输入...")
    success = auto_type_manager.type_text(test_text, method="clipboard")
    
    if success:
        print("   ✅ 自动上屏成功！")
        print("   📋 文本应该已经输入到当前窗口")
    else:
        print("   ❌ 自动上屏失败")
        print("   🔄 尝试键盘方式...")
        
        success = auto_type_manager.type_text(test_text, method="keyboard")
        if success:
            print("   ✅ 键盘方式成功！")
        else:
            print("   ❌ 键盘方式也失败了")
    
    print()
    print("=" * 50)
    print("🎉 测试完成！")


def test_clipboard_method():
    """测试剪贴板方式"""
    print("🧪 测试剪贴板方式...")
    print("=" * 30)
    
    test_text = "剪贴板测试文本 " + time.strftime("%H:%M:%S")
    print(f"测试文本: {test_text}")
    
    # 保存原始剪贴板
    original = auto_type_manager._get_clipboard_content()
    print(f"原始剪贴板: {original[:50] if original else '空'}")
    
    # 设置新内容
    success = auto_type_manager._set_clipboard_content(test_text)
    print(f"设置剪贴板: {'✅ 成功' if success else '❌ 失败'}")
    
    # 读取验证
    new_content = auto_type_manager._get_clipboard_content()
    print(f"读取剪贴板: {new_content}")
    
    # 恢复原始内容
    if original is not None:
        auto_type_manager._set_clipboard_content(original)
        print("已恢复原始剪贴板内容")
    
    print("=" * 30)


if __name__ == "__main__":
    print("🚀 Paste for Windows - 自动上屏功能测试")
    print()
    
    try:
        # 测试剪贴板功能
        test_clipboard_method()
        print()
        
        # 测试自动上屏
        test_auto_type()
        
    except KeyboardInterrupt:
        print("\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc() 