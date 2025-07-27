"""
在主程序环境下测试设置功能
"""
import sys
import os
import tkinter as tk
from tkinter import ttk

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ClipboardApp

def test_main_settings():
    """在主程序环境下测试设置功能"""
    try:
        print("创建 ClipboardApp 实例...")
        app = ClipboardApp()
        app.initialize()
        
        print("创建主窗口...")
        root = app.gui.create_main_window()
        
        def test_open_settings():
            print("测试打开设置...")
            try:
                app.gui.open_settings()
                print("设置窗口打开成功")
            except Exception as e:
                print(f"设置窗口打开失败: {e}")
                import traceback
                traceback.print_exc()
        
        # 添加测试按钮
        test_frame = ttk.Frame(root)
        test_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        test_btn = ttk.Button(test_frame, text="测试设置", command=test_open_settings)
        test_btn.pack(side=tk.LEFT)
        
        print("启动主循环...")
        root.mainloop()
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_main_settings() 