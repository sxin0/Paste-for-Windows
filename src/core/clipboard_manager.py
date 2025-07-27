#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪贴板管理器 - 核心模块
负责监听和管理剪贴板内容
"""

import asyncio
import time
import hashlib
import ctypes
import os
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
            print("✅ 剪贴板监听已启动（使用Windows消息机制）")
    
    def stop_listening(self):
        """停止监听剪贴板"""
        if self._is_listening:
            self._is_listening = False
            if self._listener_thread:
                self._listener_thread.stop()
                self._listener_thread.wait()
                self._listener_thread = None
            print("✅ 剪贴板监听已停止")
    
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
            
            print(f"📋 监听到新的剪贴板内容: {content[:50]}{'...' if len(content) > 50 else ''}")
            
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
    """剪贴板监听线程 - 使用轮询方式（稳定版）"""
    
    # 信号定义
    clipboard_changed = pyqtSignal(str)  # 剪贴板内容变化
    error_occurred = pyqtSignal(str)  # 错误信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_running = False
        self._last_content = ""
        self._poll_interval = 0.5  # 改为0.5秒轮询间隔
        self._consecutive_failures = 0
        self._max_consecutive_failures = 5  # 减少连续失败次数限制
        self._log_file = "clipboard_changes.log"  # 记录文件
        
    def run(self):
        """运行监听线程"""
        try:
            self._is_running = True
            self._consecutive_failures = 0
            print("🔄 开始剪贴板监听（轮询方式）...")
            print(f"📊 轮询间隔: {self._poll_interval} 秒")
            print(f"🔄 最大连续失败次数: {self._max_consecutive_failures}")
            
            # 获取初始剪贴板内容
            initial_content = self._get_clipboard_content()
            if initial_content:
                self._last_content = initial_content
                print(f"📋 初始剪贴板内容: {initial_content[:50]}{'...' if len(initial_content) > 50 else ''}")
            else:
                print("📋 初始剪贴板为空或无法访问")
            
            print("💡 现在请复制一些文本内容进行测试")
            
            # 轮询循环
            while self._is_running:
                try:
                    # 获取当前剪贴板内容
                    current_content = self._get_clipboard_content()
                    
                    # 检查内容是否发生变化
                    if current_content and current_content != self._last_content:
                        print(f"🆕 检测到剪贴板变化: {current_content[:50]}{'...' if len(current_content) > 50 else ''}")
                        
                        # 写入记录
                        content_type = "文本"
                        if current_content.startswith("[图片数据"):
                            content_type = "图片"
                        elif current_content.startswith("[文件列表"):
                            content_type = "文件列表"
                        elif current_content.startswith("[未知格式"):
                            content_type = "未知"
                        elif current_content.startswith("获取剪贴板失败"):
                            content_type = "错误"
                        
                        self._write_to_log(current_content, content_type)
                        
                        self._last_content = current_content
                        self.clipboard_changed.emit(current_content)
                        self._consecutive_failures = 0  # 重置失败计数
                    
                    # 等待下一次轮询
                    time.sleep(self._poll_interval)
                    
                except Exception as e:
                    self._consecutive_failures += 1
                    error_msg = f"轮询过程中出现错误: {e}"
                    print(f"❌ {error_msg} (第{self._consecutive_failures}次)")
                    
                    if self._consecutive_failures >= self._max_consecutive_failures:
                        print(f"❌ 连续失败次数过多({self._consecutive_failures})，停止监听")
                        self.error_occurred.emit(f"连续失败次数过多，停止监听: {error_msg}")
                        break
                    else:
                        self.error_occurred.emit(f"轮询错误 (第{self._consecutive_failures}次): {str(e)}")
                        # 短暂等待后继续
                        time.sleep(0.2)
                    
        except Exception as e:
            print(f"❌ 监听线程错误: {e}")
            self.error_occurred.emit(f"监听线程错误: {str(e)}")
        finally:
            print("🔄 监听线程已退出")
    
    def _get_clipboard_content(self):
        """获取剪贴板内容（改进版）"""
        try:
            win32clipboard.OpenClipboard()
            
            # 尝试获取文本内容
            try:
                content = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                content_type = "文本"
            except:
                # 如果不是文本，尝试获取其他格式
                try:
                    content = win32clipboard.GetClipboardData(win32con.CF_TEXT)
                    content_type = "文本(ANSI)"
                except:
                    # 检查是否有图片
                    try:
                        content = win32clipboard.GetClipboardData(win32con.CF_DIB)
                        content_type = "图片"
                    except:
                        # 检查是否有文件列表
                        try:
                            content = win32clipboard.GetClipboardData(win32con.CF_HDROP)
                            content_type = "文件列表"
                        except:
                            content = "未知格式"
                            content_type = "未知"
            
            win32clipboard.CloseClipboard()
            
            # 处理不同类型的内容
            if content_type == "文本(ANSI)" and isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')
            elif content_type == "图片":
                content = f"[图片数据 - {len(content)} 字节]"
            elif content_type == "文件列表":
                content = f"[文件列表 - {len(content)} 字节]"
            elif content_type == "未知":
                content = "[未知格式内容]"
            
            return content
            
        except Exception as e:
            return f"获取剪贴板失败: {str(e)}"
    
    def _write_to_log(self, content: str, content_type: str = "文本"):
        """写入记录到日志文件"""
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 限制内容长度，避免日志文件过大
            if len(content) > 200:
                display_content = content[:200] + "..."
                content_length = len(content)
            else:
                display_content = content
                content_length = len(content)
            
            log_entry = f"[{current_time}] 剪贴板内容变化 ({content_type}): {display_content}"
            if len(content) > 200:
                log_entry += f" (总长度: {content_length} 字符)"
            
            # 写入日志文件
            with open(self._log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
                f.write("-" * 80 + "\n")
            
            print(f"📝 已记录到日志: {self._log_file}")
            
        except Exception as e:
            print(f"❌ 写入日志失败: {e}")
    
    def stop(self):
        """停止监听"""
        print("🛑 停止剪贴板监听...")
        self._is_running = False
    
    def set_poll_interval(self, interval):
        """设置轮询间隔"""
        self._poll_interval = interval
        print(f"📊 轮询间隔已设置为: {interval} 秒")


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
        self._database_manager = None  # 数据库管理器
        
        # 连接信号
        self._listener.clipboard_changed.connect(self._on_clipboard_changed)
        self._listener.clipboard_error.connect(self.error_occurred.emit)
    
    def set_database_manager(self, database_manager):
        """设置数据库管理器"""
        self._database_manager = database_manager
    
    def start(self):
        """启动剪贴板管理器"""
        if not self._is_enabled:
            self._is_enabled = True
            self._listener.start_listening()
            print("✅ 剪贴板管理器已启动")
    
    def stop(self):
        """停止剪贴板管理器"""
        if self._is_enabled:
            self._is_enabled = False
            self._listener.stop_listening()
            print("✅ 剪贴板管理器已停止")
    
    def _on_clipboard_changed(self, item: ClipboardItem):
        """处理剪贴板变化"""
        try:
            # 检查是否已存在相同内容
            existing_item = self._find_item_by_content(item.content)
            
            if existing_item:
                # 更新现有项目
                existing_item.update_access()
                self.item_updated.emit(existing_item)
                
                # 保存到数据库
                if self._database_manager:
                    self._database_manager.save_item(existing_item)
                    
                print(f"🔄 更新现有剪贴板项目: {item.content[:30]}{'...' if len(item.content) > 30 else ''}")
            else:
                # 添加新项目
                self._add_item(item)
                
                # 保存到数据库
                if self._database_manager:
                    self._database_manager.save_item(item)
                    
                print(f"📝 新增剪贴板项目: {item.content[:30]}{'...' if len(item.content) > 30 else ''}")
                
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
        
        print(f"✅ 剪贴板项目已添加到内存: {item.content_type} 类型")
    
    def _remove_oldest_item(self):
        """移除最旧的项目"""
        if not self._items:
            return
        
        # 找到最旧的项目
        oldest_item = min(self._items.values(), key=lambda x: x.created_at)
        del self._items[oldest_item.id]
        self.item_removed.emit(oldest_item.id)
        
        # 从数据库中也删除
        if self._database_manager:
            self._database_manager.delete_item(oldest_item.id)
    
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
            
            # 从数据库中也删除
            if self._database_manager:
                self._database_manager.delete_item(item_id)
                
            return True
        return False
    
    def clear_all(self):
        """清空所有项目"""
        item_ids = list(self._items.keys())
        self._items.clear()
        for item_id in item_ids:
            self.item_removed.emit(item_id)
        
        # 清空数据库
        if self._database_manager:
            self._database_manager.clear_all_items()
    
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
    
    def load_from_database(self):
        """从数据库加载项目"""
        if not self._database_manager:
            return
        
        try:
            # 从数据库获取最近的项目
            db_items = self._database_manager.get_recent_items(self._max_items)
            
            # 清空当前内存中的项目
            self._items.clear()
            
            # 加载数据库中的项目
            for item in db_items:
                self._items[item.id] = item
            
            print(f"✅ 从数据库加载了 {len(db_items)} 个剪贴板项目")
            
        except Exception as e:
            print(f"❌ 从数据库加载项目失败: {e}")
            self.error_occurred.emit(f"从数据库加载项目失败: {str(e)}") 