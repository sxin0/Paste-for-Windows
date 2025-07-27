"""
简化测试 - 只测试 GUI 核心功能
"""
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from clipboard_manager import ClipboardManager
from gui import ClipboardGUI

def test_simplified():
    """简化测试"""
    try:
        print("创建 ClipboardGUI 实例...")
        app = ClipboardGUI()
        
        print("创建主窗口...")
        root = app.create_main_window()
        
        def test_settings():
            print("点击设置按钮...")
            app.open_settings()
        
        # 添加测试按钮到状态栏
        test_btn = ttk.Button(root, text="测试设置", command=test_settings)
        test_btn.pack(side=tk.BOTTOM, pady=5)
        
        print("程序启动成功，请点击菜单中的设置...")
        root.mainloop()
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simplified() 