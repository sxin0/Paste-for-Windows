"""
测试设置窗口
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from gui import SettingsWindow

def test_settings():
    """测试设置窗口"""
    try:
        # 创建主窗口
        root = tk.Tk()
        root.title("测试设置窗口")
        root.geometry("300x200")
        
        def open_settings():
            try:
                print("尝试打开设置窗口...")
                print(f"Config对象: {config}")
                print(f"Config类型: {type(config)}")
                
                # 测试配置访问
                print(f"测试配置读取: {config.get('general', 'max_history_items', '100')}")
                
                settings_window = SettingsWindow(root, config)
                print("SettingsWindow创建成功")
                
                settings_window.show()
                print("设置窗口显示成功")
                
            except Exception as e:
                print(f"错误详情: {e}")
                import traceback
                traceback.print_exc()
                messagebox.showerror("错误", f"打开设置窗口失败: {e}")
        
        # 创建测试按钮
        btn = ttk.Button(root, text="打开设置", command=open_settings)
        btn.pack(pady=50)
        
        print("测试程序启动")
        root.mainloop()
        
    except Exception as e:
        print(f"测试程序错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_settings() 