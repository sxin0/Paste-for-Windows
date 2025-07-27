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
    """剪贴板监听器"""
    
    # 信号定义
    clipboard_changed = pyqtSignal(ClipboardItem)  # 剪贴板内容变化
    clipboard_error = pyqtSignal(str)  # 错误信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_content = ""
        self._is_listening = False
        self._timer = QTimer()
        self._timer.timeout.connect(self._check_clipboard)
        self._check_interval = 100  # 检查间隔（毫秒）
        
    def start_listening(self):
        """开始监听剪贴板"""
        if not self._is_listening:
            self._is_listening = True
            self._timer.start(self._check_interval)
            print("剪贴板监听已启动")
    
    def stop_listening(self):
        """停止监听剪贴板"""
        if self._is_listening:
            self._is_listening = False
            self._timer.stop()
            print("剪贴板监听已停止")
    
    def _check_clipboard(self):
        """检查剪贴板内容"""
        try:
            # 打开剪贴板
            if not win32clipboard.OpenClipboard():
                return
            
            try:
                # 检查是否有文本内容
                if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                    content = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                elif win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT):
                    content = win32clipboard.GetClipboardData(win32con.CF_TEXT).decode('utf-8')
                else:
                    content = ""
                
                # 检查内容是否发生变化
                if content and content != self._last_content:
                    self._last_content = content
                    self._process_clipboard_content(content)
                    
            finally:
                # 确保关闭剪贴板
                try:
                    win32clipboard.CloseClipboard()
                except:
                    pass
                
        except Exception as e:
            # 减少错误日志频率，避免刷屏
            if not hasattr(self, '_last_error_time') or time.time() - self._last_error_time > 5:
                self.clipboard_error.emit(f"剪贴板访问错误: {str(e)}")
                self._last_error_time = time.time()
    
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
        """设置检查间隔"""
        self._check_interval = interval
        if self._is_listening:
            self._timer.setInterval(interval)


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
        try:
            # 检查项目数量限制
            if len(self._items) >= self._max_items:
                self._remove_oldest_item()
            
            # 添加项目
            self._items[item.id] = item
            self.item_added.emit(item)
            
        except Exception as e:
            self.error_occurred.emit(f"添加项目错误: {str(e)}")
    
    def _remove_oldest_item(self):
        """移除最旧的项目"""
        if not self._items:
            return
        
        # 找到最旧的项目
        oldest_item = min(self._items.values(), key=lambda x: x.created_at)
        self._items.pop(oldest_item.id)
        self.item_removed.emit(oldest_item.id)
    
    def _find_item_by_content(self, content: str) -> Optional[ClipboardItem]:
        """根据内容查找项目"""
        for item in self._items.values():
            if item.content == content:
                return item
        return None
    
    def get_item(self, item_id: str) -> Optional[ClipboardItem]:
        """获取指定项目"""
        return self._items.get(item_id)
    
    def get_all_items(self) -> list[ClipboardItem]:
        """获取所有项目"""
        return list(self._items.values())
    
    def get_recent_items(self, limit: int = 50) -> list[ClipboardItem]:
        """获取最近的项目"""
        items = sorted(self._items.values(), key=lambda x: x.updated_at, reverse=True)
        return items[:limit]
    
    def remove_item(self, item_id: str) -> bool:
        """删除指定项目"""
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
        # 如果当前项目数超过限制，移除多余的项目
        while len(self._items) > self._max_items:
            self._remove_oldest_item()
    
    def search_items(self, query: str, limit: int = 50) -> List[ClipboardItem]:
        """搜索项目"""
        results = []
        query_lower = query.lower()
        
        for item in self._items.values():
            if (query_lower in item.content.lower() or 
                query_lower in item.tags.lower()):
                results.append(item)
        
        # 按更新时间排序
        results.sort(key=lambda x: x.updated_at, reverse=True)
        return results[:limit]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'total_items': len(self._items),
            'max_items': self._max_items,
            'is_enabled': self._is_enabled,
            'content_types': self._get_content_type_stats()
        }
    
    def _get_content_type_stats(self) -> Dict[str, int]:
        """获取内容类型统计"""
        stats = {}
        for item in self._items.values():
            content_type = item.content_type
            stats[content_type] = stats.get(content_type, 0) + 1
        return stats 