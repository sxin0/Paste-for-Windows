"""
实用工具函数模块
"""
import os
import sys
import threading
import winreg
from typing import Optional
import pystray
from PIL import Image, ImageDraw
import keyboard
from config import config, APP_NAME

class SystemTray:
    def __init__(self, main_app):
        self.main_app = main_app
        self.icon = None
        self.is_running = False
        # 保存app实例的引用以访问命令队列
        self.app_instance = None
    
    def set_app_instance(self, app_instance):
        """设置应用程序实例引用"""
        self.app_instance = app_instance
    
    def create_icon_image(self):
        """创建托盘图标"""
        # 创建一个简单的剪贴板图标
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # 绘制剪贴板形状
        draw.rectangle([10, 5, 54, 50], outline='black', width=2)
        draw.rectangle([20, 0, 44, 10], outline='black', width=2, fill='lightgray')
        draw.rectangle([15, 15, 49, 20], fill='lightblue')
        draw.rectangle([15, 25, 39, 30], fill='lightblue')
        draw.rectangle([15, 35, 44, 40], fill='lightblue')
        
        return image
    
    def start(self):
        """启动系统托盘"""
        if self.is_running:
            return
        
        self.is_running = True
        
        # 创建菜单
        menu = pystray.Menu(
            pystray.MenuItem("显示主窗口", self.show_main_window),
            pystray.MenuItem("设置", self.show_settings),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("统计信息", self.show_statistics),
            pystray.MenuItem("导出历史", self.export_history),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("退出", self.quit_application)
        )
        
        # 创建图标
        icon_image = self.create_icon_image()
        self.icon = pystray.Icon(APP_NAME, icon_image, APP_NAME, menu)
        
        # 启动托盘（在单独线程中）
        threading.Thread(target=self.icon.run, daemon=True).start()
    
    def stop(self):
        """停止系统托盘"""
        if self.icon:
            self.icon.stop()
        self.is_running = False
    
    def show_main_window(self, icon=None, item=None):
        """显示主窗口"""
        if self.app_instance:
            # 通过命令队列发送显示窗口命令
            self.app_instance.command_queue.put('toggle_window')
        elif hasattr(self.main_app, 'root') and self.main_app.root:
            # 备用方法：直接操作GUI（仅在主线程中安全）
            try:
                self.main_app.root.after(0, lambda: (
                    self.main_app.root.deiconify(),
                    self.main_app.root.lift(),
                    self.main_app.root.focus_force()
                ))
            except Exception as e:
                print(f"显示主窗口失败: {e}")
    
    def show_settings(self, icon=None, item=None):
        """显示设置"""
        if self.app_instance:
            # 确保主窗口存在
            if not hasattr(self.main_app, 'root') or not self.main_app.root:
                # 如果主窗口不存在，先显示主窗口，然后延迟打开设置
                self.app_instance.command_queue.put('toggle_window')
                # 使用线程延迟执行设置命令
                import threading
                import time
                def delayed_settings():
                    time.sleep(0.5)  # 等待主窗口创建
                    if self.app_instance:
                        self.app_instance.command_queue.put('open_settings')
                threading.Thread(target=delayed_settings, daemon=True).start()
            else:
                # 主窗口已存在，直接发送设置命令
                self.app_instance.command_queue.put('open_settings')
    
    def show_statistics(self, icon=None, item=None):
        """显示统计信息"""
        self.show_main_window()
        if hasattr(self.main_app, 'show_statistics'):
            # 延迟执行统计命令
            if self.app_instance:
                self.app_instance.command_queue.put('show_statistics')
    
    def export_history(self, icon=None, item=None):
        """导出历史"""
        self.show_main_window()
        if hasattr(self.main_app, 'export_history'):
            # 延迟执行导出命令
            if self.app_instance:
                self.app_instance.command_queue.put('export_history')
    
    def quit_application(self, icon=None, item=None):
        """退出应用程序"""
        if self.app_instance:
            self.app_instance.command_queue.put('quit')
        elif hasattr(self.main_app, 'on_closing'):
            self.main_app.on_closing()
        self.stop()

class HotkeyManager:
    def __init__(self, callback):
        self.callback = callback
        self.hotkey = None
        self.is_registered = False
    
    def register_hotkey(self, hotkey_str: str = None):
        """注册热键"""
        if hotkey_str is None:
            hotkey_str = config.get('general', 'hotkey', 'win+v')
        
        try:
            # 取消之前的热键
            self.unregister_hotkey()
            
            # 注册新热键
            keyboard.add_hotkey(hotkey_str, self.callback)
            self.hotkey = hotkey_str
            self.is_registered = True
            print(f"热键已注册: {hotkey_str}")
            return True
        except Exception as e:
            print(f"注册热键失败: {e}")
            return False
    
    def unregister_hotkey(self):
        """取消热键注册"""
        if self.is_registered and self.hotkey:
            try:
                keyboard.remove_hotkey(self.hotkey)
                self.is_registered = False
                print(f"热键已取消: {self.hotkey}")
            except Exception as e:
                print(f"取消热键失败: {e}")

class AutoStartManager:
    @staticmethod
    def get_app_path():
        """获取应用程序路径"""
        if getattr(sys, 'frozen', False):
            # 打包后的exe文件
            return sys.executable
        else:
            # 开发环境
            return sys.executable + ' "' + os.path.abspath(__file__) + '"'
    
    @staticmethod
    def is_auto_start_enabled():
        """检查是否已启用开机自启"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Run", 
                               0, winreg.KEY_READ)
            try:
                winreg.QueryValueEx(key, APP_NAME)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception:
            return False
    
    @staticmethod
    def enable_auto_start():
        """启用开机自启"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Run", 
                               0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, AutoStartManager.get_app_path())
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"启用开机自启失败: {e}")
            return False
    
    @staticmethod
    def disable_auto_start():
        """禁用开机自启"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Run", 
                               0, winreg.KEY_SET_VALUE)
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"禁用开机自启失败: {e}")
            return False
    
    @staticmethod
    def toggle_auto_start():
        """切换开机自启状态"""
        if AutoStartManager.is_auto_start_enabled():
            return AutoStartManager.disable_auto_start()
        else:
            return AutoStartManager.enable_auto_start()

class NotificationManager:
    @staticmethod
    def show_notification(title: str, message: str, duration: int = 3000):
        """显示系统通知"""
        if not config.getboolean('general', 'show_notifications', True):
            return
        
        try:
            import win10toast
            toaster = win10toast.ToastNotifier()
            toaster.show_toast(title, message, duration=duration)
        except ImportError:
            # 如果没有安装win10toast，使用系统调用
            try:
                import subprocess
                subprocess.run([
                    'powershell', '-Command',
                    f"Add-Type -AssemblyName System.Windows.Forms; "
                    f"[System.Windows.Forms.MessageBox]::Show('{message}', '{title}')"
                ], shell=True, capture_output=True)
            except Exception as e:
                print(f"显示通知失败: {e}")

def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def format_time_ago(timestamp_str: str) -> str:
    """格式化时间差显示"""
    import datetime
    
    try:
        timestamp = datetime.datetime.fromisoformat(timestamp_str)
        now = datetime.datetime.now()
        diff = now - timestamp
        
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return "刚刚"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"{minutes} 分钟前"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"{hours} 小时前"
        elif seconds < 604800:
            days = int(seconds // 86400)
            return f"{days} 天前"
        else:
            return timestamp.strftime("%Y-%m-%d")
    except Exception:
        return "未知时间"

def sanitize_filename(filename: str) -> str:
    """清理文件名，移除非法字符"""
    import re
    # 移除Windows文件名中的非法字符
    illegal_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(illegal_chars, '_', filename)
    # 移除前后空格并限制长度
    sanitized = sanitized.strip()[:255]
    return sanitized

def get_clipboard_text_preview(text: str, max_length: int = 100) -> str:
    """获取剪贴板文本预览"""
    if not text:
        return ""
    
    # 替换换行符和制表符
    preview = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    
    # 移除多余空格
    import re
    preview = re.sub(r'\s+', ' ', preview).strip()
    
    # 截断长度
    if len(preview) > max_length:
        preview = preview[:max_length] + "..."
    
    return preview

class PerformanceMonitor:
    """性能监控工具"""
    
    def __init__(self):
        self.start_time = None
        self.timers = {}
    
    def start_timer(self, name: str):
        """开始计时"""
        import time
        self.timers[name] = time.time()
    
    def end_timer(self, name: str) -> float:
        """结束计时并返回耗时"""
        import time
        if name in self.timers:
            elapsed = time.time() - self.timers[name]
            del self.timers[name]
            return elapsed
        return 0.0
    
    def get_memory_usage(self) -> dict:
        """获取内存使用情况"""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            return {
                'rss': memory_info.rss,  # 常驻内存
                'vms': memory_info.vms,  # 虚拟内存
                'percent': process.memory_percent()
            }
        except ImportError:
            return {}

# 全局实例
performance_monitor = PerformanceMonitor() 