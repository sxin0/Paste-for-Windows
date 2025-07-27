#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动上屏工具 - 模拟键盘输入将内容直接输入到当前激活的应用程序
"""

import time
import threading
from typing import Optional
import pyautogui
import win32api
import win32con
import win32gui
import win32clipboard


class AutoTypeManager:
    """自动上屏管理器"""
    
    def __init__(self):
        # 设置pyautogui的安全设置
        pyautogui.FAILSAFE = True  # 鼠标移动到屏幕左上角时停止
        pyautogui.PAUSE = 0.01  # 每个操作之间的暂停时间
        
        # 输入延迟设置
        self.type_delay = 0.01  # 每个字符之间的延迟
        self.line_delay = 0.1   # 换行符的额外延迟
        
        # 窗口历史记录
        self.window_history = []
        self.max_history = 10
        
    def type_text(self, text: str, method: str = "clipboard", switch_to_previous: bool = True) -> bool:
        """
        将文本输入到应用程序
        
        Args:
            text: 要输入的文本
            method: 输入方法 ("clipboard" 或 "keyboard")
            switch_to_previous: 是否切换到上一个窗口
        
        Returns:
            bool: 是否成功
        """
        try:
            # 记录当前窗口
            current_window = self.get_active_window_info()
            if current_window.get("hwnd"):
                self._add_to_window_history(current_window)
            
            # 如果需要切换到上一个窗口
            if switch_to_previous:
                # 查找最佳目标窗口
                target_window = self.find_best_target_window()
                if target_window:
                    print(f"切换到目标窗口: {target_window.get('title', '未知')}")
                    if self._switch_to_window(target_window):
                        # 等待窗口激活
                        time.sleep(0.1)
                    else:
                        print("切换到目标窗口失败，使用当前窗口")
                else:
                    print("没有找到合适的目标窗口，使用当前窗口")
            
            # 执行输入
            if method == "clipboard":
                return self._type_via_clipboard(text)
            elif method == "keyboard":
                return self._type_via_keyboard(text)
            else:
                print(f"不支持的输入方法: {method}")
                return False
                
        except Exception as e:
            print(f"自动上屏失败: {e}")
            return False
    
    def _type_via_clipboard(self, text: str) -> bool:
        """
        通过剪贴板方式输入文本（推荐）
        优点：速度快，支持特殊字符，不会触发输入法
        """
        try:
            # 保存当前剪贴板内容
            original_clipboard = self._get_clipboard_content()
            
            # 将文本复制到剪贴板
            self._set_clipboard_content(text)
            
            # 等待一下确保剪贴板内容已更新
            time.sleep(0.05)
            
            # 模拟 Ctrl+V 粘贴
            pyautogui.hotkey('ctrl', 'v')
            
            # 恢复原始剪贴板内容
            if original_clipboard is not None:
                time.sleep(0.1)  # 等待粘贴完成
                self._set_clipboard_content(original_clipboard)
            
            return True
            
        except Exception as e:
            print(f"剪贴板方式输入失败: {e}")
            return False
    
    def _type_via_keyboard(self, text: str) -> bool:
        """
        通过键盘模拟方式输入文本
        优点：不依赖剪贴板，更直接
        缺点：速度较慢，可能触发输入法
        """
        try:
            # 确保目标窗口处于激活状态
            self._ensure_window_active()
            
            # 逐字符输入
            for char in text:
                if char == '\n':
                    # 换行符
                    pyautogui.press('enter')
                    time.sleep(self.line_delay)
                elif char == '\t':
                    # 制表符
                    pyautogui.press('tab')
                    time.sleep(self.type_delay)
                else:
                    # 普通字符
                    pyautogui.typewrite(char)
                    time.sleep(self.type_delay)
            
            return True
            
        except Exception as e:
            print(f"键盘方式输入失败: {e}")
            return False
    
    def _get_clipboard_content(self) -> Optional[str]:
        """获取剪贴板内容"""
        try:
            win32clipboard.OpenClipboard()
            try:
                data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                return data
            except:
                return None
            finally:
                win32clipboard.CloseClipboard()
        except:
            return None
    
    def _set_clipboard_content(self, text: str) -> bool:
        """设置剪贴板内容"""
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
            win32clipboard.CloseClipboard()
            return True
        except Exception as e:
            print(f"设置剪贴板失败: {e}")
            return False
    
    def _add_to_window_history(self, window_info: dict):
        """添加窗口到历史记录"""
        if not window_info.get("hwnd"):
            return
        
        # 检查是否是当前应用的窗口
        window_class = window_info.get("class", "")
        window_title = window_info.get("title", "")
        
        # 定义当前应用的窗口类名
        current_app_classes = [
            "Chrome_WidgetWin_1",  # Cursor/Chrome 相关
            "Qt6QWindowIcon",      # PyQt6 应用
            "QWidget",             # PyQt6 窗口
            "PasteForWindows",     # 我们的应用
        ]
        
        # 检查是否是当前应用
        is_current_app = (
            window_class in current_app_classes or
            "paste-for-windows" in window_title.lower() or
            "cursor" in window_title.lower() or
            "chrome" in window_title.lower()
        )
        
        # 如果是当前应用，检查是否已经存在相同的应用窗口
        if is_current_app:
            for existing in self.window_history:
                existing_class = existing.get("class", "")
                existing_title = existing.get("title", "")
                existing_is_current_app = (
                    existing_class in current_app_classes or
                    "paste-for-windows" in existing_title.lower() or
                    "cursor" in existing_title.lower() or
                    "chrome" in existing_title.lower()
                )
                
                if existing_is_current_app:
                    # 如果已存在当前应用窗口，移除旧记录
                    self.window_history.remove(existing)
                    break
        else:
            # 如果不是当前应用，检查是否已经存在相同的窗口
            for existing in self.window_history:
                if existing.get("hwnd") == window_info.get("hwnd"):
                    # 如果已存在，移除旧记录
                    self.window_history.remove(existing)
                    break
        
        # 添加到历史记录开头
        self.window_history.insert(0, window_info.copy())
        
        # 限制历史记录数量
        if len(self.window_history) > self.max_history:
            self.window_history = self.window_history[:self.max_history]
    
    def _get_previous_window(self) -> Optional[dict]:
        """获取上一个窗口（智能跳过当前应用）"""
        if len(self.window_history) <= 1:
            return None
        
        current_window = self.window_history[0] if self.window_history else None
        current_class = current_window.get("class", "") if current_window else ""
        
        # 定义当前应用的窗口类名
        current_app_classes = [
            "Chrome_WidgetWin_1",  # Cursor/Chrome 相关
            "Qt6QWindowIcon",      # PyQt6 应用
            "QWidget",             # PyQt6 窗口
            "PasteForWindows",     # 我们的应用
        ]
        
        # 从历史记录中查找第一个不是当前应用的窗口
        for i, window in enumerate(self.window_history[1:], 1):
            window_class = window.get("class", "")
            window_title = window.get("title", "")
            
            # 检查是否是当前应用
            is_current_app = (
                window_class in current_app_classes or
                "paste-for-windows" in window_title.lower() or
                "cursor" in window_title.lower() or
                "chrome" in window_title.lower()
            )
            
            # 如果不是当前应用，返回这个窗口
            if not is_current_app:
                print(f"找到目标窗口: {window_title} ({window_class})")
                return window
        
        # 如果所有窗口都是当前应用，返回None
        print("所有历史窗口都是当前应用，无法找到合适的目标窗口")
        return None
    
    def _switch_to_window(self, window_info: dict) -> bool:
        """切换到指定窗口"""
        try:
            hwnd = window_info.get("hwnd")
            if not hwnd:
                print("窗口句柄为空")
                return False
            
            # 检查窗口是否仍然存在
            if not win32gui.IsWindow(hwnd):
                print("窗口不存在")
                return False
            
            # 检查窗口是否可见
            if not win32gui.IsWindowVisible(hwnd):
                print("窗口不可见")
                return False
            
            # 检查窗口是否最小化
            if win32gui.IsIconic(hwnd):
                print("窗口已最小化，尝试恢复")
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                time.sleep(0.1)
            
            # 激活窗口
            win32gui.SetForegroundWindow(hwnd)
            
            # 等待窗口激活
            time.sleep(0.1)
            
            # 验证窗口是否真的激活了
            active_hwnd = win32gui.GetForegroundWindow()
            if active_hwnd == hwnd:
                print("窗口切换成功")
                return True
            else:
                print(f"窗口切换失败，期望: {hwnd}, 实际: {active_hwnd}")
                return False
            
        except Exception as e:
            print(f"切换窗口失败: {e}")
            return False
    
    def verify_window_exists(self, window_info: dict) -> bool:
        """验证窗口是否仍然存在"""
        try:
            hwnd = window_info.get("hwnd")
            if not hwnd:
                return False
            
            # 检查窗口是否仍然存在
            if not win32gui.IsWindow(hwnd):
                return False
            
            # 检查窗口是否可见
            if not win32gui.IsWindowVisible(hwnd):
                return False
            
            return True
            
        except Exception as e:
            print(f"验证窗口存在性失败: {e}")
            return False
    
    def _ensure_window_active(self):
        """确保当前窗口处于激活状态"""
        try:
            # 获取当前鼠标位置下的窗口
            cursor_pos = win32api.GetCursorPos()
            hwnd = win32gui.WindowFromPoint(cursor_pos)
            
            # 激活窗口
            if hwnd and win32gui.IsWindow(hwnd):
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.05)  # 等待窗口激活
                
        except Exception as e:
            print(f"激活窗口失败: {e}")
    
    def get_window_history(self) -> list:
        """获取窗口历史记录"""
        return self.window_history.copy()
    
    def clear_window_history(self):
        """清空窗口历史记录"""
        self.window_history.clear()
    
    def get_visible_windows(self) -> list:
        """获取所有可见的窗口"""
        windows = []
        
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                try:
                    title = win32gui.GetWindowText(hwnd)
                    class_name = win32gui.GetClassName(hwnd)
                    
                    # 过滤掉一些系统窗口
                    if (title and 
                        class_name and 
                        not title.startswith("Program Manager") and
                        not title.startswith("Microsoft Text Input") and
                        not title.startswith("Default IME") and
                        len(title) > 0):
                        
                        windows.append({
                            "hwnd": hwnd,
                            "title": title,
                            "class": class_name
                        })
                except:
                    pass
            return True
        
        try:
            win32gui.EnumWindows(enum_windows_callback, windows)
        except Exception as e:
            print(f"枚举窗口失败: {e}")
        
        return windows
    
    def find_best_target_window(self) -> Optional[dict]:
        """查找最佳目标窗口"""
        # 首先尝试从历史记录中查找
        previous_window = self._get_previous_window()
        if previous_window:
            # 验证窗口是否仍然存在
            if self.verify_window_exists(previous_window):
                print(f"从历史记录中找到有效窗口: {previous_window.get('title', '未知')}")
                return previous_window
            else:
                print(f"历史记录中的窗口已不存在: {previous_window.get('title', '未知')}")
                # 从历史记录中移除无效窗口
                self._remove_invalid_windows()
        
        # 如果没有历史记录或历史记录中的窗口都无效，查找所有可见窗口
        visible_windows = self.get_visible_windows()
        
        # 定义当前应用的窗口类名
        current_app_classes = [
            "Chrome_WidgetWin_1",  # Cursor/Chrome 相关
            "Qt6QWindowIcon",      # PyQt6 应用
            "QWidget",             # PyQt6 窗口
            "PasteForWindows",     # 我们的应用
        ]
        
        # 查找第一个不是当前应用的窗口
        for window in visible_windows:
            window_class = window.get("class", "")
            window_title = window.get("title", "")
            
            # 检查是否是当前应用
            is_current_app = (
                window_class in current_app_classes or
                "paste-for-windows" in window_title.lower() or
                "cursor" in window_title.lower() or
                "chrome" in window_title.lower()
            )
            
            # 如果不是当前应用，返回这个窗口
            if not is_current_app:
                print(f"从可见窗口中找到目标窗口: {window_title} ({window_class})")
                return window
        
        print("没有找到合适的目标窗口")
        return None
    
    def _remove_invalid_windows(self):
        """从历史记录中移除无效窗口"""
        valid_windows = []
        for window in self.window_history:
            if self.verify_window_exists(window):
                valid_windows.append(window)
            else:
                print(f"移除无效窗口: {window.get('title', '未知')}")
        
        self.window_history = valid_windows
    
    def get_active_window_info(self) -> dict:
        """获取当前激活窗口的信息"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd:
                window_text = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)
                return {
                    "hwnd": hwnd,
                    "title": window_text,
                    "class": class_name
                }
        except Exception as e:
            print(f"获取窗口信息失败: {e}")
        
        return {}
    
    def is_safe_to_type(self) -> bool:
        """检查是否安全进行自动输入"""
        try:
            # 获取当前激活窗口
            window_info = self.get_active_window_info()
            
            # 检查是否是系统关键窗口
            dangerous_classes = [
                "TaskManagerWindow",  # 任务管理器
                "ConsoleWindowClass",  # 命令提示符
                "CabinetWClass",      # 文件资源管理器
                "Notepad",            # 记事本
                "WordPadClass",       # 写字板
            ]
            
            if window_info.get("class") in dangerous_classes:
                return False
            
            # 检查窗口标题是否包含危险关键词
            dangerous_keywords = [
                "管理员", "Administrator", "系统", "System",
                "命令", "Command", "PowerShell", "cmd"
            ]
            
            title = window_info.get("title", "").lower()
            for keyword in dangerous_keywords:
                if keyword.lower() in title:
                    return False
            
            return True
            
        except Exception as e:
            print(f"安全检查失败: {e}")
            return False


# 全局实例
auto_type_manager = AutoTypeManager() 