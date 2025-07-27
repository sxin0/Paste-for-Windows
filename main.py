"""
Windows 剪贴板管理器主程序
类似于 macOS Paste 的功能
"""
import sys
import os
import threading
import tkinter as tk
from tkinter import messagebox
import argparse
import queue
import time

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import ClipboardGUI
from utils import SystemTray, HotkeyManager, AutoStartManager, NotificationManager
from config import config, APP_NAME, APP_VERSION

class ClipboardApp:
    def __init__(self):
        self.gui = None
        self.tray = None
        self.hotkey_manager = None
        self.is_running = False
        self.command_queue = queue.Queue()
        self.window_visible = False
        
    def initialize(self):
        """初始化应用程序"""
        print(f"正在启动 {APP_NAME} v{APP_VERSION}...")
        sys.stdout.flush()
        
        # 创建GUI实例
        self.gui = ClipboardGUI()
        print("GUI 实例已创建")
        sys.stdout.flush()
        
        # 创建系统托盘
        self.tray = SystemTray(self.gui)
        self.tray.set_app_instance(self)
        print("系统托盘已创建")
        sys.stdout.flush()
        
        # 创建热键管理器
        self.hotkey_manager = HotkeyManager(self.on_hotkey_pressed)
        print("热键管理器已创建")
        sys.stdout.flush()
        
        # 设置开机自启
        self.setup_auto_start()
        
        print("应用程序初始化完成")
        sys.stdout.flush()
    
    def setup_auto_start(self):
        """设置开机自启"""
        if config.getboolean('general', 'auto_start', True):
            if not AutoStartManager.is_auto_start_enabled():
                AutoStartManager.enable_auto_start()
                print("已启用开机自启")
        else:
            if AutoStartManager.is_auto_start_enabled():
                AutoStartManager.disable_auto_start()
                print("已禁用开机自启")
    
    def on_hotkey_pressed(self):
        """热键回调 - 将命令放入队列"""
        print("🎉 Win+V 热键被触发！")
        sys.stdout.flush()  # 强制刷新输出
        self.command_queue.put('toggle_window')
    
    def process_commands(self):
        """处理命令队列（在主线程中运行）"""
        try:
            while True:
                try:
                    command = self.command_queue.get_nowait()
                    print(f"处理命令: {command}")
                    sys.stdout.flush()
                    if command == 'toggle_window':
                        self.toggle_main_window()
                    elif command == 'open_settings':
                        if hasattr(self.gui, 'open_settings'):
                            self.gui.open_settings()
                    elif command == 'show_statistics':
                        if hasattr(self.gui, 'show_statistics'):
                            self.gui.show_statistics()
                    elif command == 'export_history':
                        if hasattr(self.gui, 'export_history'):
                            self.gui.export_history()
                    elif command == 'quit':
                        self.stop()
                        break
                except queue.Empty:
                    break
        except Exception as e:
            print(f"处理命令时出错: {e}")
        
        # 继续处理命令
        if self.is_running and hasattr(self.gui, 'root') and self.gui.root:
            self.gui.root.after(100, self.process_commands)
    
    def toggle_main_window(self):
        """切换主窗口显示状态"""
        # 确保此方法在主线程中执行
        if hasattr(self.gui, 'root') and self.gui.root:
            # 使用 after 方法确保在主线程中执行
            self.gui.root.after(0, self._do_toggle_window)
        else:
            print("主窗口不存在，无法切换")
    
    def _do_toggle_window(self):
        """实际执行窗口切换的方法（在主线程中）"""
        try:
            if not hasattr(self.gui, 'root') or not self.gui.root:
                print("主窗口不存在，无法切换")
                return
            
            current_state = self.gui.root.state()
            is_visible = self.gui.root.winfo_viewable()
            
            print(f"切换前 - 窗口状态: {current_state}, 可见: {is_visible}, window_visible标志: {self.window_visible}")
            sys.stdout.flush()
            
            # 更简单的逻辑：如果窗口当前是正常显示状态，就隐藏；否则就显示
            if current_state == 'normal' and is_visible:
                # 窗口当前可见，隐藏它
                print("隐藏主窗口")
                sys.stdout.flush()
                self.gui.root.withdraw()
                self.window_visible = False
            else:
                # 窗口当前隐藏或最小化，显示它
                print("显示主窗口")
                sys.stdout.flush()
                
                # 先取消隐藏状态
                self.gui.root.deiconify()
                # 确保窗口正常显示
                self.gui.root.state('normal')
                
                # 确保窗口大小和位置正确
                window_width = config.get('general', 'window_width', '800')
                window_height = config.get('general', 'window_height', '600')
                
                # 获取屏幕尺寸
                screen_width = self.gui.root.winfo_screenwidth()
                screen_height = self.gui.root.winfo_screenheight()
                
                # 计算居中位置
                x = (screen_width - int(window_width)) // 2
                y = (screen_height - int(window_height)) // 2
                
                # 设置窗口位置和大小
                self.gui.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
                
                # 强制更新窗口
                self.gui.root.update()
                
                # 提升窗口到前台
                self.gui.root.lift()
                self.gui.root.focus_force()
                
                # 临时置顶确保用户能看到
                self.gui.root.attributes('-topmost', True)
                def remove_topmost():
                    try:
                        self.gui.root.attributes('-topmost', False)
                    except:
                        pass
                self.gui.root.after(300, remove_topmost)
                
                # 更新内部状态
                self.window_visible = True
                
            print(f"切换后 - 窗口状态: {self.gui.root.state()}, 可见: {self.gui.root.winfo_viewable()}, window_visible标志: {self.window_visible}")
            sys.stdout.flush()
            
        except Exception as e:
            print(f"切换窗口显示状态失败: {e}")
            sys.stdout.flush()
            import traceback
            traceback.print_exc()
    
    def show_main_window(self):
        """显示主窗口"""
        self.command_queue.put('toggle_window')
    
    def start(self, show_window=True):
        """启动应用程序"""
        if self.is_running:
            return
        
        self.is_running = True
        
        try:
            # 启动系统托盘
            print("正在启动系统托盘...")
            sys.stdout.flush()
            self.tray.start()
            print("系统托盘已启动")
            sys.stdout.flush()
            
            # 注册热键
            print("正在注册热键...")
            sys.stdout.flush()
            hotkey_result = self.hotkey_manager.register_hotkey()
            if hotkey_result:
                print("✅ 热键注册成功")
                print(f"热键: {self.hotkey_manager.hotkey}")
                sys.stdout.flush()
            else:
                print("❌ 热键注册失败")
                print("请检查是否需要管理员权限或热键是否被其他程序占用")
                sys.stdout.flush()
            
            # 显示通知
            if config.getboolean('general', 'show_notifications', True):
                NotificationManager.show_notification(
                    APP_NAME, 
                    "剪贴板管理器已启动，使用 Win+V 打开主窗口"
                )
            
            # 启动剪贴板监听
            print("正在启动剪贴板监听...")
            sys.stdout.flush()
            self.gui.clipboard_manager.start_monitoring()
            print("剪贴板监听已启动")
            sys.stdout.flush()
            
            # 始终创建主窗口（确保tkinter主循环可用）
            print("正在创建主窗口...")
            sys.stdout.flush()
            root = self.gui.create_main_window()
            print(f"主窗口已创建，初始状态: {root.state()}")
            sys.stdout.flush()
            
            if show_window:
                # 显示主窗口
                self.window_visible = True
                print("主窗口设置为可见状态")
                sys.stdout.flush()
            else:
                # 后台模式：隐藏主窗口
                root.withdraw()
                self.window_visible = False
                print(f"程序在后台运行，主窗口已隐藏，当前状态: {root.state()}")
                sys.stdout.flush()
            
            # 开始处理命令队列
            root.after(100, self.process_commands)
            
            # 绑定窗口关闭事件
            root.protocol("WM_DELETE_WINDOW", self.on_window_close)
            
            # 运行主循环
            root.mainloop()
                
        except Exception as e:
            print(f"启动失败: {e}")
            messagebox.showerror("启动错误", f"应用程序启动失败:\n{e}")
            sys.exit(1)
    
    def on_window_close(self):
        """窗口关闭事件处理"""
        # 隐藏窗口而不是退出程序
        if hasattr(self.gui, 'root') and self.gui.root:
            self.gui.root.withdraw()
            self.window_visible = False
    
    def run_background(self):
        """在后台运行"""
        try:
            import signal
            
            def signal_handler(signum, frame):
                print("接收到退出信号，正在关闭...")
                self.stop()
                sys.exit(0)
            
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            
            print("应用程序正在后台运行...")
            print("按 Ctrl+C 退出")
            
            # 保持程序运行
            while self.is_running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n用户取消，正在退出...")
            self.stop()
    
    def stop(self):
        """停止应用程序"""
        if not self.is_running:
            return
        
        print("正在停止应用程序...")
        self.is_running = False
        
        try:
            # 停止剪贴板监听
            if self.gui and self.gui.clipboard_manager:
                self.gui.clipboard_manager.stop_monitoring()
            
            # 取消热键注册
            if self.hotkey_manager:
                self.hotkey_manager.unregister_hotkey()
            
            # 停止系统托盘
            if self.tray:
                self.tray.stop()
            
            # 关闭主窗口
            if self.gui and hasattr(self.gui, 'root') and self.gui.root:
                self.gui.root.quit()
                self.gui.root.destroy()
            
            print("应用程序已停止")
            
        except Exception as e:
            print(f"停止应用程序时出错: {e}")

def check_single_instance():
    """检查是否已有实例在运行"""
    import tempfile
    import fcntl
    
    lock_file_path = os.path.join(tempfile.gettempdir(), f"{APP_NAME}.lock")
    
    try:
        lock_file = open(lock_file_path, 'w')
        fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True, lock_file
    except:
        return False, None

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description=f"{APP_NAME} - Windows 剪贴板管理器")
    parser.add_argument('--background', '-b', action='store_true', 
                       help='在后台运行，不显示主窗口')
    parser.add_argument('--show', '-s', action='store_true', 
                       help='显示主窗口（如果程序正在运行）')
    parser.add_argument('--version', '-v', action='version', 
                       version=f'{APP_NAME} v{APP_VERSION}')
    
    args = parser.parse_args()
    
    # 检查是否已有实例运行
    if os.name == 'posix':  # Linux/Mac
        is_single, lock_file = check_single_instance()
        if not is_single:
            print("应用程序已在运行中")
            if args.show:
                # 尝试发送信号显示窗口
                print("尝试显示现有窗口...")
            return
    
    try:
        # 创建应用程序实例
        app = ClipboardApp()
        app.initialize()
        
        # 启动应用程序
        show_window = not args.background
        app.start(show_window=show_window)
        
    except KeyboardInterrupt:
        print("\n用户取消启动")
    except Exception as e:
        print(f"应用程序异常: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理资源
        if 'app' in locals():
            app.stop()

if __name__ == "__main__":
    # 确保在Windows上正确处理中文
    if sys.platform.startswith('win'):
        import locale
        locale.setlocale(locale.LC_ALL, 'chinese')
        
        # 设置控制台编码
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    
    main() 