#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪贴板管理器 - 核心模块
负责监听和管理剪贴板内容
"""

import asyncio
import time
import hashlib
from datetime import datetime
from typing import Optional, Callable, Dict, Any, List
from dataclasses import dataclass, field

import win32clipboard
import win32con
import win32gui
import win32api
from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QThread
from PyQt6.QtWidgets import QApplication


@dataclass
class ClipboardItem:
    """剪贴板项目数据模型"""
    id: str
    content: str
    content_type: str = "text"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    is_favorite: bool = False
    tags: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.id:
            self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        content_hash = hashlib.md5(self.content.encode('utf-8')).hexdigest()
        timestamp = int(time.time() * 1000)
        return f"{content_hash}_{timestamp}"
    
    def update_access(self):
        """更新访问次数和时间"""
        self.access_count += 1
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'id': self.id,
            'content': self.content,
            'content_type': self.content_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'access_count': self.access_count,
            'is_favorite': self.is_favorite,
            'tags': self.tags,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClipboardItem':
        """从字典创建实例"""
        data = data.copy()
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)


class ClipboardListener(QObject):
    """剪贴板监听器 - 使用Windows消息机制"""
    
    # 信号定义
    clipboard_changed = pyqtSignal(ClipboardItem)  # 剪贴板内容变化
    clipboard_error = pyqtSignal(str)  # 错误信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_content = ""
        self._is_listening = False
        self._listener_thread = None
        self._hwnd = None
        self._clipboard_viewer_next = None
        
    def start_listening(self):
        """开始监听剪贴板"""
        if not self._is_listening:
            self._is_listening = True
            self._listener_thread = ClipboardListenerThread(self)
            self._listener_thread.clipboard_changed.connect(self._on_clipboard_changed)
            self._listener_thread.error_occurred.connect(self.clipboard_error.emit)
            self._listener_thread.start()
            print("剪贴板监听已启动（使用Windows消息机制）")
    
    def stop_listening(self):
        """停止监听剪贴板"""
        if self._is_listening:
            self._is_listening = False
            if self._listener_thread:
                self._listener_thread.stop()
                self._listener_thread.wait()
                self._listener_thread = None
            print("剪贴板监听已停止")
    
    def _on_clipboard_changed(self, content: str):
        """处理剪贴板变化"""
        if content and content != self._last_content:
            self._last_content = content
            self._process_clipboard_content(content)
    
    def _process_clipboard_content(self, content: str):
        """处理剪贴板内容"""
        try:
            # 创建剪贴板项目
            item = ClipboardItem(
                id="",  # 空字符串，会在 __post_init__ 中自动生成
                content=content,
                content_type=self._detect_content_type(content)
            )
            
            # 发送信号
            self.clipboard_changed.emit(item)
            
        except Exception as e:
            self.clipboard_error.emit(f"处理剪贴板内容错误: {str(e)}")
    
    def _detect_content_type(self, content: str) -> str:
        """检测内容类型"""
        if not content:
            return "empty"
        
        # 检测URL
        if content.startswith(('http://', 'https://', 'ftp://', 'file://')):
            return "link"
        
        # 检测文件路径
        if content.startswith(('C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\', 'H:\\', 'I:\\', 'J:\\', 'K:\\', 'L:\\', 'M:\\', 'N:\\', 'O:\\', 'P:\\', 'Q:\\', 'R:\\', 'S:\\', 'T:\\', 'U:\\', 'V:\\', 'W:\\', 'X:\\', 'Y:\\', 'Z:\\')):
            return "file"
        
        # 检测代码片段（简单检测）
        code_keywords = ['def ', 'class ', 'import ', 'from ', 'if __name__', 'function ', 'var ', 'let ', 'const ', 'public ', 'private ', 'protected ']
        if any(keyword in content for keyword in code_keywords):
            return "code"
        
        # 默认为文本
        return "text"
    
    def set_check_interval(self, interval: int):
        """设置检查间隔（兼容性方法，实际不使用）"""
        pass


class ClipboardListenerThread(QThread):
    """剪贴板监听线程 - 使用Windows消息机制"""
    
    # 信号定义
    clipboard_changed = pyqtSignal(str)  # 剪贴板内容变化
    error_occurred = pyqtSignal(str)  # 错误信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_running = False
        self._hwnd = None
        self._clipboard_viewer_next = None
        
    def run(self):
        """运行监听线程"""
        try:
            self._is_running = True
            
            # 创建隐藏窗口来接收剪贴板消息
            self._hwnd = win32gui.CreateWindowEx(
                0, "STATIC", "ClipboardListener",
                0, 0, 0, 0, 0, 0, 0, None
            )
            
            if not self._hwnd:
                self.error_occurred.emit("无法创建剪贴板监听窗口")
                return
            
            # 注册为剪贴板查看器
            self._clipboard_viewer_next = win32gui.SetClipboardViewer(self._hwnd)
            
            print("✅ 剪贴板监听窗口已创建，开始监听...")
            
            # 消息循环
            while self._is_running:
                try:
                    # 处理Windows消息
                    msg = win32gui.GetMessage(None, 0, 0)
                    
                    if msg[0] == 0:  # WM_QUIT
                        break
                    
                    if msg[0] == win32con.WM_CHANGECBCHAIN:
                        # 剪贴板查看器链变化
                        if msg[1] == self._hwnd:
                            self._clipboard_viewer_next = msg[2]
                        elif self._clipboard_viewer_next:
                            win32gui.SendMessage(self._clipboard_viewer_next, msg[0], msg[1], msg[2])
                    
                    elif msg[0] == win32con.WM_DRAWCLIPBOARD:
                        # 剪贴板内容变化
                        self._handle_clipboard_change()
                        
                        # 传递消息给下一个查看器
                        if self._clipboard_viewer_next:
                            win32gui.SendMessage(self._clipboard_viewer_next, msg[0], msg[1], msg[2])
                    
                    else:
                        # 其他消息
                        win32gui.TranslateMessage(msg)
                        win32gui.DispatchMessage(msg)
                        
                except Exception as e:
                    if self._is_running:
                        self.error_occurred.emit(f"消息处理错误: {str(e)}")
                    break
                    
        except Exception as e:
            self.error_occurred.emit(f"剪贴板监听线程错误: {str(e)}")
        finally:
            self._cleanup()
    
    def _handle_clipboard_change(self):
        """处理剪贴板变化"""
        try:
            # 延迟一下，确保剪贴板内容已更新
            time.sleep(0.05)
            
            # 获取剪贴板内容
            content = self._get_clipboard_content_safe()
            if content:
                self.clipboard_changed.emit(content)
                
        except Exception as e:
            if self._is_running:
                self.error_occurred.emit(f"处理剪贴板变化错误: {str(e)}")
    
    def _get_clipboard_content_safe(self) -> Optional[str]:
        """安全地获取剪贴板内容"""
        try:
            # 尝试打开剪贴板，如果失败则返回None
            if not win32clipboard.OpenClipboard():
                return None
            
            try:
                # 检查是否有文本内容
                if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                    content = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                elif win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT):
                    content = win32clipboard.GetClipboardData(win32con.CF_TEXT).decode('utf-8')
                else:
                    content = ""
                
                return content
                
            finally:
                # 确保关闭剪贴板
                try:
                    win32clipboard.CloseClipboard()
                except:
                    pass
                    
        except Exception:
            # 如果出现任何异常，返回None而不是抛出异常
            return None
    
    def stop(self):
        """停止监听"""
        self._is_running = False
        self._cleanup()
    
    def _cleanup(self):
        """清理资源"""
        try:
            if self._hwnd:
                # 从剪贴板查看器链中移除
                if self._clipboard_viewer_next:
                    win32gui.ChangeClipboardChain(self._hwnd, self._clipboard_viewer_next)
                
                # 销毁窗口
                win32gui.DestroyWindow(self._hwnd)
                self._hwnd = None
                self._clipboard_viewer_next = None
                
        except Exception as e:
            print(f"清理剪贴板监听资源时出错: {e}")


class ClipboardManager(QObject):
    """剪贴板管理器"""
    
    # 信号定义
    item_added = pyqtSignal(ClipboardItem)  # 新项目添加
    item_updated = pyqtSignal(ClipboardItem)  # 项目更新
    item_removed = pyqtSignal(str)  # 项目删除
    error_occurred = pyqtSignal(str)  # 错误信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._listener = ClipboardListener()
        self._items: Dict[str, ClipboardItem] = {}
        self._max_items = 1000  # 最大项目数
        self._is_enabled = False
        
        # 连接信号
        self._listener.clipboard_changed.connect(self._on_clipboard_changed)
        self._listener.clipboard_error.connect(self.error_occurred.emit)
    
    def start(self):
        """启动剪贴板管理器"""
        if not self._is_enabled:
            self._is_enabled = True
            self._listener.start_listening()
            print("剪贴板管理器已启动")
    
    def stop(self):
        """停止剪贴板管理器"""
        if self._is_enabled:
            self._is_enabled = False
            self._listener.stop_listening()
            print("剪贴板管理器已停止")
    
    def _on_clipboard_changed(self, item: ClipboardItem):
        """处理剪贴板变化"""
        try:
            # 检查是否已存在相同内容
            existing_item = self._find_item_by_content(item.content)
            
            if existing_item:
                # 更新现有项目
                existing_item.update_access()
                self.item_updated.emit(existing_item)
            else:
                # 添加新项目
                self._add_item(item)
                
        except Exception as e:
            self.error_occurred.emit(f"处理剪贴板变化错误: {str(e)}")
    
    def _add_item(self, item: ClipboardItem):
        """添加新项目"""
        # 检查是否超过最大项目数
        if len(self._items) >= self._max_items:
            self._remove_oldest_item()
        
        # 添加新项目
        self._items[item.id] = item
        self.item_added.emit(item)
    
    def _remove_oldest_item(self):
        """移除最旧的项目"""
        if not self._items:
            return
        
        # 找到最旧的项目
        oldest_item = min(self._items.values(), key=lambda x: x.created_at)
        del self._items[oldest_item.id]
        self.item_removed.emit(oldest_item.id)
    
    def _find_item_by_content(self, content: str) -> Optional[ClipboardItem]:
        """根据内容查找项目"""
        for item in self._items.values():
            if item.content == content:
                return item
        return None
    
    def get_item(self, item_id: str) -> Optional[ClipboardItem]:
        """根据ID获取项目"""
        return self._items.get(item_id)
    
    def get_all_items(self) -> list[ClipboardItem]:
        """获取所有项目"""
        return list(self._items.values())
    
    def get_recent_items(self, limit: int = 50) -> list[ClipboardItem]:
        """获取最近的项目"""
        sorted_items = sorted(self._items.values(), key=lambda x: x.created_at, reverse=True)
        return sorted_items[:limit]
    
    def remove_item(self, item_id: str) -> bool:
        """移除项目"""
        if item_id in self._items:
            del self._items[item_id]
            self.item_removed.emit(item_id)
            return True
        return False
    
    def clear_all(self):
        """清空所有项目"""
        item_ids = list(self._items.keys())
        self._items.clear()
        for item_id in item_ids:
            self.item_removed.emit(item_id)
    
    def set_max_items(self, max_items: int):
        """设置最大项目数"""
        self._max_items = max_items
        # 如果当前项目数超过新的最大值，移除多余的项目
        while len(self._items) > self._max_items:
            self._remove_oldest_item()
    
    def search_items(self, query: str, limit: int = 50) -> List[ClipboardItem]:
        """搜索项目"""
        if not query.strip():
            return self.get_recent_items(limit)
        
        query_lower = query.lower()
        results = []
        
        for item in self._items.values():
            if query_lower in item.content.lower():
                results.append(item)
                if len(results) >= limit:
                    break
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total_items = len(self._items)
        content_types = self._get_content_type_stats()
        
        return {
            'total_items': total_items,
            'content_types': content_types,
            'is_enabled': self._is_enabled
        }
    
    def _get_content_type_stats(self) -> Dict[str, int]:
        """获取内容类型统计"""
        stats = {}
        for item in self._items.values():
            content_type = item.content_type
            stats[content_type] = stats.get(content_type, 0) + 1
        return stats 