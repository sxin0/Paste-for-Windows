"""
Windows 剪贴板管理器主程序
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
        sys.stdout.flush()
        self.command_queue.put('toggle_window')
    
    def process_commands(self):
        """处理命令队列（在主线程中运行）"""
        try:
            queue_size = self.command_queue.qsize()
            print(f"开始处理命令队列，队列大小: {queue_size}")
            sys.stdout.flush()
            
            if queue_size == 0:
                print("队列为空，跳过处理")
                sys.stdout.flush()
            else:
                while True:
                    try:
                        command = self.command_queue.get_nowait()
                        print(f"处理命令: {command}")
                        sys.stdout.flush()
                        
                        if command == 'toggle_window':
                            print("执行toggle_window命令")
                            sys.stdout.flush()
                            self.toggle_main_window()
                        elif command == 'open_settings':
                            print("处理open_settings命令")
                            sys.stdout.flush()
                            
                            # 确保主窗口可见
                            if hasattr(self.gui, 'root') and self.gui.root:
                                try:
                                    if not self.gui.root.winfo_viewable():
                                        print("主窗口不可见，先显示主窗口")
                                        self.gui.root.deiconify()
                                        self.gui.root.lift()
                                        self.gui.root.focus_force()
                                        self.window_visible = True
                                except Exception as e:
                                    print(f"显示主窗口时出错: {e}")
                            
                            # 打开设置窗口
                            if hasattr(self.gui, 'open_settings'):
                                print("调用gui.open_settings()")
                                sys.stdout.flush()
                                self.gui.open_settings()
                                print("gui.open_settings()调用完成")
                                sys.stdout.flush()
                            else:
                                print("❌ gui对象没有open_settings方法")
                                sys.stdout.flush()
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
                        print("命令队列处理完毕")
                        sys.stdout.flush()
                        break
        except Exception as e:
            print(f"处理命令时出错: {e}")
            import traceback
            traceback.print_exc()
        
        # 继续处理命令 - 确保在主线程中运行
        if self.is_running and hasattr(self.gui, 'root') and self.gui.root:
            try:
                print("安排下次命令处理")
                sys.stdout.flush()
                self.gui.root.after(100, self.process_commands)
            except Exception as e:
                print(f"安排下次命令处理时出错: {e}")
        else:
            print("无法安排下次命令处理：程序未运行或主窗口不存在")
            sys.stdout.flush()
    
    def toggle_main_window(self):
        """切换主窗口显示状态"""
        print("toggle_main_window 被调用")
        sys.stdout.flush()
        
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
            
            print("开始切换窗口状态...")
            sys.stdout.flush()
            
            # 检查窗口当前状态
            try:
                current_state = self.gui.root.state()
                is_visible = self.gui.root.winfo_viewable()
                print(f"当前窗口状态: {current_state}, 可见: {is_visible}")
            except Exception as e:
                print(f"获取窗口状态失败: {e}")
                current_state = 'unknown'
                is_visible = False
            
            # 简化逻辑：如果窗口不可见，就显示它
            if not is_visible or current_state != 'normal':
                print("显示主窗口")
                sys.stdout.flush()
                
                # 确保窗口可见
                try:
                    # 强制显示窗口
                    self.gui.root.deiconify()
                    self.gui.root.state('normal')
                    
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
                    
                    # 强制更新
                    self.gui.root.update_idletasks()
                    
                    self.window_visible = True
                    print("主窗口已显示")
                    
                    # 验证窗口状态
                    try:
                        final_state = self.gui.root.state()
                        final_visible = self.gui.root.winfo_viewable()
                        print(f"显示后窗口状态: {final_state}, 可见: {final_visible}")
                    except Exception as e:
                        print(f"验证窗口状态失败: {e}")
                    
                except Exception as e:
                    print(f"显示窗口时出错: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("隐藏主窗口")
                sys.stdout.flush()
                try:
                    self.gui.root.withdraw()
                    self.window_visible = False
                    print("主窗口已隐藏")
                except Exception as e:
                    print(f"隐藏窗口时出错: {e}")
            
            print(f"切换完成 - 窗口状态: {self.gui.root.state()}, 可见: {self.gui.root.winfo_viewable()}")
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
            # 创建主窗口（在启动其他组件之前）
            print("正在创建主窗口...")
            sys.stdout.flush()
            root = self.gui.create_main_window()
            print(f"主窗口已创建，初始状态: {root.state()}")
            sys.stdout.flush()
            
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
            
            # 默认显示主窗口（除非明确指定后台模式）
            # 默认显示主窗口（除非明确指定后台模式）
            if show_window:
                # 显示主窗口
                self.window_visible = True
                print("主窗口设置为可见状态")
                sys.stdout.flush()
                
                # 确保窗口实际显示
                try:
                    root.deiconify()
                    root.lift()
                    root.focus_force()
                    print(f"主窗口已显示，状态: {root.state()}, 可见: {root.winfo_viewable()}")
                except Exception as e:
                    print(f"显示主窗口时出错: {e}")
            else:
                # 后台模式：隐藏主窗口
                root.withdraw()
                self.window_visible = False
                print(f"程序在后台运行，主窗口已隐藏，当前状态: {root.state()}")
                sys.stdout.flush()
            
            # 开始处理命令队列 - 确保在主线程中运行
            print("开始处理命令队列...")
            sys.stdout.flush()
            
            # 立即处理一次命令队列，然后安排定期处理
            try:
                print("调用初始命令处理...")
                sys.stdout.flush()
                self.process_commands()
                print("初始命令处理完成")
                sys.stdout.flush()
            except Exception as e:
                print(f"初始命令处理失败: {e}")
                import traceback
                traceback.print_exc()
            
            # 安排定期处理
            root.after(100, self.process_commands)
            
            # 绑定窗口关闭事件
            root.protocol("WM_DELETE_WINDOW", self.on_window_close)
            
            print("准备运行主循环...")
            sys.stdout.flush()
            
            # 运行主循环
            root.mainloop()
                
        except Exception as e:
            print(f"启动失败: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("启动错误", f"应用程序启动失败:\n{e}")
            sys.exit(1)
    
    def on_window_close(self):
        """窗口关闭事件处理"""
        # 隐藏窗口而不是退出程序
        if hasattr(self.gui, 'root') and self.gui.root:
            self.gui.root.withdraw()
            self.window_visible = False
    
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
    
    try:
        # 创建应用程序实例
        app = ClipboardApp()
        app.initialize()
        
        # 启动应用程序 - 默认显示主窗口，除非明确指定后台模式
        show_window = not args.background
        print(f"启动模式: {'前台' if show_window else '后台'}")
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
        try:
            locale.setlocale(locale.LC_ALL, 'chinese')
        except:
            pass
        
        # 设置控制台编码
        try:
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
        except:
            pass
    
    main() 