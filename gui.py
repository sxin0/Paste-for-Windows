"""
剪贴板管理器GUI界面
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import datetime
from typing import List, Dict, Any
from clipboard_manager import ClipboardManager
from config import config, APP_NAME, APP_VERSION

class ClipboardGUI:
    def __init__(self):
        self.clipboard_manager = ClipboardManager()
        self.root = None
        self.search_var = None
        self.history_listbox = None
        self.detail_text = None
        self.status_label = None
        self.history_data = []
        
    def create_main_window(self):
        """创建主窗口"""
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry(f"{config.get('general', 'window_width', '800')}x{config.get('general', 'window_height', '600')}")
        self.root.configure(bg='#f0f0f0')
        
        # 设置图标
        try:
            self.root.iconbitmap(default='clipboard.ico')
        except:
            pass
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建主界面
        self.create_main_interface()
        
        # 绑定事件
        self.bind_events()
        
        # 加载历史记录
        self.load_history()
        
        # 添加剪贴板变化回调
        self.clipboard_manager.add_callback(self.on_clipboard_change)
        
        return self.root
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="导出历史记录...", command=self.export_history)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.on_closing)
        
        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="清空历史记录", command=self.clear_history)
        edit_menu.add_command(label="设置...", command=self.open_settings)
        
        # 查看菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="查看", menu=view_menu)
        view_menu.add_command(label="刷新", command=self.load_history)
        view_menu.add_command(label="统计信息", command=self.show_statistics)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)
    
    def create_main_interface(self):
        """创建主界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建搜索框架
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        search_entry.bind('<KeyRelease>', self.on_search)
        
        ttk.Button(search_frame, text="清除", command=self.clear_search).pack(side=tk.RIGHT)
        
        # 创建内容框架
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建左侧历史列表
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        ttk.Label(left_frame, text="剪贴板历史").pack(anchor=tk.W)
        
        # 创建历史列表
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # 历史列表
        self.history_listbox = tk.Listbox(list_frame, font=('Consolas', 10))
        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.history_listbox.yview)
        scrollbar_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.history_listbox.xview)
        
        self.history_listbox.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.history_listbox.bind('<Double-Button-1>', self.copy_selected_item)
        self.history_listbox.bind('<Button-3>', self.show_context_menu)
        self.history_listbox.bind('<<ListboxSelect>>', self.on_item_select)
        
        # 创建右侧详情面板
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(5, 0))
        right_frame.configure(width=300)
        
        ttk.Label(right_frame, text="详细信息").pack(anchor=tk.W)
        
        # 详细信息文本框
        detail_frame = ttk.Frame(right_frame)
        detail_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.detail_text = tk.Text(detail_frame, wrap=tk.WORD, font=('Consolas', 9), state=tk.DISABLED)
        detail_scrollbar = ttk.Scrollbar(detail_frame, orient=tk.VERTICAL, command=self.detail_text.yview)
        self.detail_text.configure(yscrollcommand=detail_scrollbar.set)
        
        self.detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        detail_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 操作按钮框架
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="复制", command=self.copy_selected_item).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(button_frame, text="收藏", command=self.toggle_favorite).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(button_frame, text="删除", command=self.delete_selected_item).pack(fill=tk.X)
        
        # 创建状态栏
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="就绪")
        self.status_label.pack(side=tk.LEFT)
        
        # 监听状态标签
        monitoring_label = ttk.Label(status_frame, text="● 监听中", foreground="green")
        monitoring_label.pack(side=tk.RIGHT)
    
    def bind_events(self):
        """绑定事件"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 绑定快捷键
        self.root.bind('<Control-f>', lambda e: self.search_var.get() and None)
        self.root.bind('<F5>', lambda e: self.load_history())
        self.root.bind('<Delete>', lambda e: self.delete_selected_item())
        self.root.bind('<Control-c>', lambda e: self.copy_selected_item())
    
    def load_history(self):
        """加载历史记录"""
        try:
            self.history_data = self.clipboard_manager.get_history()
            self.update_history_display()
            self.update_status(f"已加载 {len(self.history_data)} 条记录")
        except Exception as e:
            messagebox.showerror("错误", f"加载历史记录失败: {e}")
    
    def update_history_display(self, data=None):
        """更新历史记录显示"""
        if data is None:
            data = self.history_data
        
        self.history_listbox.delete(0, tk.END)
        
        for item in data:
            # 格式化显示文本
            content = item['content'][:100] + ('...' if len(item['content']) > 100 else '')
            content = content.replace('\n', ' ').replace('\t', ' ')
            
            # 添加类型和时间信息
            timestamp = datetime.datetime.fromisoformat(item['timestamp']).strftime('%H:%M')
            type_icon = self.get_type_icon(item['content_type'])
            favorite_icon = '★' if item['is_favorite'] else ''
            
            display_text = f"{type_icon} {timestamp} {favorite_icon} {content}"
            self.history_listbox.insert(tk.END, display_text)
    
    def get_type_icon(self, content_type):
        """获取类型图标"""
        icons = {
            'text': '📝',
            'image': '🖼️',
            'files': '📁',
            'url': '🔗'
        }
        return icons.get(content_type, '📄')
    
    def on_item_select(self, event):
        """选中项目时显示详细信息"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.history_data):
                item = self.history_data[index]
                self.show_item_details(item)
    
    def show_item_details(self, item):
        """显示项目详细信息"""
        self.detail_text.config(state=tk.NORMAL)
        self.detail_text.delete(1.0, tk.END)
        
        # 格式化详细信息
        details = f"类型: {item['content_type']}\n"
        details += f"时间: {datetime.datetime.fromisoformat(item['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}\n"
        details += f"大小: {item['size']} 字节\n"
        details += f"访问次数: {item['accessed_count']}\n"
        details += f"收藏: {'是' if item['is_favorite'] else '否'}\n"
        details += f"\n内容:\n{'-' * 20}\n{item['content']}"
        
        self.detail_text.insert(1.0, details)
        self.detail_text.config(state=tk.DISABLED)
    
    def on_search(self, event):
        """搜索处理"""
        keyword = self.search_var.get().strip()
        if keyword:
            # 在当前历史数据中搜索
            filtered_data = [
                item for item in self.history_data 
                if keyword.lower() in item['content'].lower()
            ]
            self.update_history_display(filtered_data)
            self.update_status(f"搜索到 {len(filtered_data)} 条记录")
        else:
            self.update_history_display()
            self.update_status(f"显示所有 {len(self.history_data)} 条记录")
    
    def clear_search(self):
        """清除搜索"""
        self.search_var.set('')
        self.update_history_display()
        self.update_status(f"显示所有 {len(self.history_data)} 条记录")
    
    def copy_selected_item(self, event=None):
        """复制选中的项目"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.history_data):
                item = self.history_data[index]
                self.clipboard_manager.copy_to_clipboard(item['content'])
                self.update_status(f"已复制: {item['content'][:50]}...")
    
    def delete_selected_item(self):
        """删除选中的项目"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.history_data):
                item = self.history_data[index]
                if messagebox.askyesno("确认删除", "确定要删除这个项目吗？"):
                    if self.clipboard_manager.delete_history_item(item['id']):
                        self.load_history()
                        self.update_status("项目已删除")
                    else:
                        messagebox.showerror("错误", "删除失败")
    
    def toggle_favorite(self):
        """切换收藏状态"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.history_data):
                item = self.history_data[index]
                if self.clipboard_manager.toggle_favorite(item['id']):
                    self.load_history()
                    status = "已收藏" if not item['is_favorite'] else "已取消收藏"
                    self.update_status(status)
                else:
                    messagebox.showerror("错误", "操作失败")
    
    def clear_history(self):
        """清空历史记录"""
        if messagebox.askyesno("确认清空", "确定要清空所有历史记录吗？此操作无法撤销。"):
            if self.clipboard_manager.clear_all_history():
                self.load_history()
                self.update_status("历史记录已清空")
            else:
                messagebox.showerror("错误", "清空失败")
    
    def export_history(self):
        """导出历史记录"""
        file_path = filedialog.asksaveasfilename(
            title="导出历史记录",
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if file_path:
            format_type = 'json' if file_path.endswith('.json') else 'txt'
            if self.clipboard_manager.export_history(file_path, format_type):
                messagebox.showinfo("成功", f"历史记录已导出到: {file_path}")
            else:
                messagebox.showerror("错误", "导出失败")
    
    def show_statistics(self):
        """显示统计信息"""
        stats = self.clipboard_manager.get_statistics()
        
        stats_text = f"""剪贴板统计信息
        
总项目数: {stats.get('total_items', 0)}
收藏项目: {stats.get('favorite_items', 0)}
今日新增: {stats.get('today_items', 0)}

类型分布:"""
        
        for type_name, count in stats.get('type_statistics', {}).items():
            stats_text += f"\n  {type_name}: {count}"
        
        messagebox.showinfo("统计信息", stats_text)
    
    def open_settings(self):
        """打开设置窗口"""
        try:
            # 确保主窗口存在
            if not hasattr(self, 'root') or not self.root:
                print("主窗口不存在，无法打开设置")
                return
            
            # 确保主窗口可见
            if self.root.state() == 'withdrawn':
                self.root.deiconify()
                self.root.lift()
                self.root.focus_force()
            
            settings_window = SettingsWindow(self.root, config)
            settings_window.show()
            print("设置窗口已打开")  # 调试信息
        except Exception as e:
            print(f"设置窗口错误: {e}")  # 调试信息
            import traceback
            traceback.print_exc()
            if hasattr(self, 'root') and self.root:
                messagebox.showerror("错误", f"打开设置窗口失败: {e}")
            else:
                print("无法显示错误对话框，主窗口不存在")
    
    def show_about(self):
        """显示关于信息"""
        about_text = f"""{APP_NAME} v{APP_VERSION}

一个功能强大的Windows剪贴板管理器，类似于macOS的Paste应用。

特性:
• 自动监听剪贴板变化
• 支持文本、图片、文件等多种格式
• 智能搜索和过滤
• 收藏和历史记录管理
• 数据持久化存储
• 系统托盘集成

快捷键:
• Win+V: 打开主窗口
• F5: 刷新历史记录
• Delete: 删除选中项目
• Ctrl+C: 复制选中项目"""
        
        messagebox.showinfo("关于", about_text)
    
    def show_context_menu(self, event):
        """显示右键菜单"""
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="复制", command=self.copy_selected_item)
        context_menu.add_command(label="收藏/取消收藏", command=self.toggle_favorite)
        context_menu.add_separator()
        context_menu.add_command(label="删除", command=self.delete_selected_item)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def on_clipboard_change(self, content, content_type, metadata):
        """剪贴板变化回调"""
        # 在主线程中更新界面
        if self.root:
            self.root.after(0, self.load_history)
    
    def update_status(self, message):
        """更新状态栏"""
        if self.status_label:
            self.status_label.config(text=message)
    
    def on_closing(self):
        """窗口关闭处理"""
        self.clipboard_manager.stop_monitoring()
        self.root.destroy()
    
    def start(self):
        """启动GUI"""
        self.create_main_window()
        self.clipboard_manager.start_monitoring()
        self.root.mainloop()

class SettingsWindow:
    def __init__(self, parent, config_obj):
        self.parent = parent
        self.config = config_obj
        self.window = None
    
    def show(self):
        """显示设置窗口"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("设置")
        self.window.geometry("400x500")
        self.window.transient(self.parent)
        
        # 尝试获取焦点，如果失败则忽略
        try:
            self.window.grab_set()
        except tk.TclError as e:
            print(f"无法获取窗口焦点，忽略: {e}")
        
        # 确保窗口显示在前面
        self.window.lift()
        self.window.focus_force()
        
        # 创建设置界面
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 常规设置
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="常规")
        self.create_general_settings(general_frame)
        
        # 剪贴板设置
        clipboard_frame = ttk.Frame(notebook)
        notebook.add(clipboard_frame, text="剪贴板")
        self.create_clipboard_settings(clipboard_frame)
        
        # 外观设置
        appearance_frame = ttk.Frame(notebook)
        notebook.add(appearance_frame, text="外观")
        self.create_appearance_settings(appearance_frame)
        
        # 按钮框架
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(button_frame, text="确定", command=self.save_settings).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="取消", command=self.window.destroy).pack(side=tk.RIGHT)
    
    def create_general_settings(self, parent):
        """创建常规设置"""
        # 最大历史项目数
        ttk.Label(parent, text="最大历史项目数:").pack(anchor=tk.W, pady=(10, 5))
        self.max_items_var = tk.StringVar(value=self.config.get('general', 'max_history_items', '100'))
        ttk.Entry(parent, textvariable=self.max_items_var).pack(fill=tk.X, pady=(0, 10))
        
        # 自动启动
        self.auto_start_var = tk.BooleanVar(value=self.config.getboolean('general', 'auto_start', True))
        ttk.Checkbutton(parent, text="开机自动启动", variable=self.auto_start_var).pack(anchor=tk.W, pady=(0, 10))
        
        # 显示通知
        self.show_notifications_var = tk.BooleanVar(value=self.config.getboolean('general', 'show_notifications', True))
        ttk.Checkbutton(parent, text="显示通知", variable=self.show_notifications_var).pack(anchor=tk.W, pady=(0, 10))
        
        # 热键设置
        ttk.Label(parent, text="快捷键:").pack(anchor=tk.W, pady=(10, 5))
        self.hotkey_var = tk.StringVar(value=self.config.get('general', 'hotkey', 'win+v'))
        ttk.Entry(parent, textvariable=self.hotkey_var).pack(fill=tk.X)
    
    def create_clipboard_settings(self, parent):
        """创建剪贴板设置"""
        # 监听间隔
        ttk.Label(parent, text="监听间隔(秒):").pack(anchor=tk.W, pady=(10, 5))
        self.monitor_interval_var = tk.StringVar(value=self.config.get('clipboard', 'monitor_interval', '0.5'))
        ttk.Entry(parent, textvariable=self.monitor_interval_var).pack(fill=tk.X, pady=(0, 10))
        
        # 保存图片
        self.save_images_var = tk.BooleanVar(value=self.config.getboolean('clipboard', 'save_images', True))
        ttk.Checkbutton(parent, text="保存图片", variable=self.save_images_var).pack(anchor=tk.W, pady=(0, 10))
        
        # 保存文件
        self.save_files_var = tk.BooleanVar(value=self.config.getboolean('clipboard', 'save_files', True))
        ttk.Checkbutton(parent, text="保存文件路径", variable=self.save_files_var).pack(anchor=tk.W, pady=(0, 10))
        
        # 最大文本长度
        ttk.Label(parent, text="最大文本长度:").pack(anchor=tk.W, pady=(10, 5))
        self.max_text_length_var = tk.StringVar(value=self.config.get('clipboard', 'max_text_length', '10000'))
        ttk.Entry(parent, textvariable=self.max_text_length_var).pack(fill=tk.X)
    
    def create_appearance_settings(self, parent):
        """创建外观设置"""
        # 主题
        ttk.Label(parent, text="主题:").pack(anchor=tk.W, pady=(10, 5))
        self.theme_var = tk.StringVar(value=self.config.get('general', 'theme', 'light'))
        theme_combo = ttk.Combobox(parent, textvariable=self.theme_var, values=['light', 'dark'])
        theme_combo.pack(fill=tk.X, pady=(0, 10))
        theme_combo.state(['readonly'])
        
        # 窗口大小
        ttk.Label(parent, text="窗口宽度:").pack(anchor=tk.W, pady=(10, 5))
        self.window_width_var = tk.StringVar(value=self.config.get('general', 'window_width', '800'))
        ttk.Entry(parent, textvariable=self.window_width_var).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(parent, text="窗口高度:").pack(anchor=tk.W, pady=(10, 5))
        self.window_height_var = tk.StringVar(value=self.config.get('general', 'window_height', '600'))
        ttk.Entry(parent, textvariable=self.window_height_var).pack(fill=tk.X)
    
    def save_settings(self):
        """保存设置"""
        try:
            # 保存常规设置
            self.config.set('general', 'max_history_items', self.max_items_var.get())
            self.config.set('general', 'auto_start', str(self.auto_start_var.get()))
            self.config.set('general', 'show_notifications', str(self.show_notifications_var.get()))
            self.config.set('general', 'hotkey', self.hotkey_var.get())
            self.config.set('general', 'theme', self.theme_var.get())
            self.config.set('general', 'window_width', self.window_width_var.get())
            self.config.set('general', 'window_height', self.window_height_var.get())
            
            # 保存剪贴板设置
            self.config.set('clipboard', 'monitor_interval', self.monitor_interval_var.get())
            self.config.set('clipboard', 'save_images', str(self.save_images_var.get()))
            self.config.set('clipboard', 'save_files', str(self.save_files_var.get()))
            self.config.set('clipboard', 'max_text_length', self.max_text_length_var.get())
            
            messagebox.showinfo("成功", "设置已保存！重启应用程序以使所有设置生效。")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"保存设置失败: {e}")

if __name__ == "__main__":
    app = ClipboardGUI()
    app.start() 