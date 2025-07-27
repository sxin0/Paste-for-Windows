"""
剪贴板管理器核心模块
"""
import pyperclip
import threading
import time
import os
from typing import Optional, Callable, List, Dict, Any
from PIL import Image
import io
import tkinter as tk
from database import ClipboardDatabase
from config import config

class ClipboardManager:
    def __init__(self):
        self.db = ClipboardDatabase()
        self.is_monitoring = False
        self.monitor_thread = None
        self.last_clipboard_content = ""
        self.callbacks = []
        
        # 支持的内容类型
        self.content_types = {
            'text': self._handle_text,
            'image': self._handle_image,
            'files': self._handle_files
        }
        
    def start_monitoring(self):
        """开始监听剪贴板"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_clipboard, daemon=True)
            self.monitor_thread.start()
            print("剪贴板监听已启动")
    
    def stop_monitoring(self):
        """停止监听剪贴板"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("剪贴板监听已停止")
    
    def add_callback(self, callback: Callable):
        """添加剪贴板变化回调函数"""
        self.callbacks.append(callback)
    
    def remove_callback(self, callback: Callable):
        """移除剪贴板变化回调函数"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def _monitor_clipboard(self):
        """监听剪贴板变化的主循环"""
        interval = config.getfloat("clipboard", "monitor_interval", 0.5)
        
        while self.is_monitoring:
            try:
                current_content = self._get_clipboard_content()
                
                if current_content and current_content != self.last_clipboard_content:
                    self.last_clipboard_content = current_content
                    self._process_clipboard_change(current_content)
                
                time.sleep(interval)
            except Exception as e:
                print(f"剪贴板监听错误: {e}")
                time.sleep(1)
    
    def _get_clipboard_content(self) -> Optional[str]:
        """获取当前剪贴板内容"""
        try:
            # 首先尝试获取文本内容
            text_content = pyperclip.paste()
            if text_content:
                return text_content
            
            # 尝试获取其他类型的内容（Windows特定）
            try:
                import win32clipboard
                win32clipboard.OpenClipboard()
                
                # 检查是否有文件
                if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_HDROP):
                    files = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
                    win32clipboard.CloseClipboard()
                    return f"FILES:{';'.join(files)}"
                
                # 检查是否有图片
                if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
                    win32clipboard.CloseClipboard()
                    return "IMAGE:clipboard_image"
                
                win32clipboard.CloseClipboard()
            except ImportError:
                # 如果没有安装win32clipboard，只处理文本
                pass
            
            return None
        except Exception as e:
            print(f"获取剪贴板内容失败: {e}")
            return None
    
    def _process_clipboard_change(self, content: str):
        """处理剪贴板内容变化"""
        try:
            content_type, processed_content, metadata = self._detect_content_type(content)
            
            # 检查内容长度限制
            max_length = config.getint("clipboard", "max_text_length", 10000)
            if content_type == 'text' and len(content) > max_length:
                processed_content = content[:max_length] + "... (内容已截断)"
                metadata['truncated'] = True
                metadata['original_length'] = len(content)
            
            # 保存到数据库
            success = self.db.add_clipboard_item(processed_content, content_type, metadata)
            
            if success:
                # 通知所有回调函数
                for callback in self.callbacks:
                    try:
                        callback(processed_content, content_type, metadata)
                    except Exception as e:
                        print(f"回调函数执行失败: {e}")
        except Exception as e:
            print(f"处理剪贴板变化失败: {e}")
    
    def _detect_content_type(self, content: str) -> tuple:
        """检测内容类型"""
        metadata = {}
        
        if content.startswith("FILES:"):
            # 文件类型
            files = content[6:].split(';')
            metadata['file_count'] = len(files)
            metadata['files'] = files
            return 'files', f"文件 ({len(files)} 个)", metadata
        
        elif content.startswith("IMAGE:"):
            # 图片类型
            metadata['image_source'] = 'clipboard'
            return 'image', "图片内容", metadata
        
        else:
            # 文本类型
            lines = content.split('\n')
            metadata['line_count'] = len(lines)
            metadata['char_count'] = len(content)
            metadata['word_count'] = len(content.split())
            
            # 检测特殊文本类型
            if content.startswith('http://') or content.startswith('https://'):
                metadata['text_type'] = 'url'
            elif '@' in content and '.' in content and len(content.split()) == 1:
                metadata['text_type'] = 'email'
            elif content.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').isdigit():
                metadata['text_type'] = 'phone'
            else:
                metadata['text_type'] = 'general'
            
            return 'text', content, metadata
    
    def _handle_text(self, content: str) -> str:
        """处理文本内容"""
        return content.strip()
    
    def _handle_image(self, content: str) -> str:
        """处理图片内容"""
        # 这里可以添加图片处理逻辑
        return "图片内容"
    
    def _handle_files(self, content: str) -> str:
        """处理文件内容"""
        if content.startswith("FILES:"):
            files = content[6:].split(';')
            return f"文件列表: {', '.join([os.path.basename(f) for f in files])}"
        return content
    
    def copy_to_clipboard(self, content: str):
        """将内容复制到剪贴板"""
        try:
            pyperclip.copy(content)
            print(f"已复制到剪贴板: {content[:50]}...")
        except Exception as e:
            print(f"复制到剪贴板失败: {e}")
    
    def get_history(self, limit: int = None, content_type: str = None) -> List[Dict[str, Any]]:
        """获取剪贴板历史"""
        return self.db.get_clipboard_history(limit, content_type)
    
    def search_history(self, keyword: str, limit: int = 50) -> List[Dict[str, Any]]:
        """搜索剪贴板历史"""
        return self.db.search_clipboard_history(keyword, limit)
    
    def delete_history_item(self, item_id: int) -> bool:
        """删除历史项目"""
        return self.db.delete_clipboard_item(item_id)
    
    def clear_all_history(self) -> bool:
        """清空所有历史"""
        return self.db.clear_all_history()
    
    def toggle_favorite(self, item_id: int) -> bool:
        """切换收藏状态"""
        return self.db.toggle_favorite(item_id)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self.db.get_statistics()
    
    def export_history(self, file_path: str, format_type: str = 'json') -> bool:
        """导出历史记录"""
        try:
            import json
            
            history = self.get_history()
            
            if format_type.lower() == 'json':
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(history, f, ensure_ascii=False, indent=2)
            elif format_type.lower() == 'txt':
                with open(file_path, 'w', encoding='utf-8') as f:
                    for item in history:
                        f.write(f"时间: {item['timestamp']}\n")
                        f.write(f"类型: {item['content_type']}\n")
                        f.write(f"内容: {item['content']}\n")
                        f.write("-" * 50 + "\n")
            
            return True
        except Exception as e:
            print(f"导出历史记录失败: {e}")
            return False 