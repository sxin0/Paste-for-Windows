#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动上屏工具 - 模拟键盘输入将内容直接输入到当前激活的应用程序
"""

import time
import threading
from typing import Optional, Tuple
import pyautogui
import win32api
import win32con
import win32gui
import win32clipboard
import win32process


class AutoTypeManager:
    """自动上屏管理器"""
    
    def __init__(self):
        # 设置pyautogui的安全设置
        pyautogui.FAILSAFE = True  # 鼠标移动到屏幕左上角时停止
        pyautogui.PAUSE = 0.01  # 每个操作之间的暂停时间
        
        # 输入延迟设置
        self.type_delay = 0.01  # 每个字符之间的延迟
        self.line_delay = 0.1   # 换行符的额外延迟
        
    def type_text(self, text: str, method: str = "clipboard", target_window: dict = None) -> bool:
        """
        将文本直接输入到指定窗口或当前激活窗口
        
        Args:
            text: 要输入的文本
            method: 输入方法 ("clipboard" 或 "keyboard")
            target_window: 目标窗口信息，如果为None则使用当前激活窗口
        
        Returns:
            bool: 是否成功
        """
        try:
            # 如果指定了目标窗口，先切换到该窗口
            if target_window:
                print(f"切换到目标窗口: {target_window.get('title', '未知')}")
                if not self._switch_to_window(target_window):
                    print("切换到目标窗口失败")
                    return False
                # 等待窗口激活
                time.sleep(0.1)
            else:
                # 使用当前激活窗口，确保窗口处于激活状态
                self._ensure_window_active()
            
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
    
    def _ensure_window_active(self):
        """确保当前窗口处于激活状态"""
        try:
            # 获取当前激活窗口
            active_hwnd = win32gui.GetForegroundWindow()
            
            # 如果当前窗口不是激活窗口，尝试激活它
            if active_hwnd:
                win32gui.SetForegroundWindow(active_hwnd)
                time.sleep(0.05)
                
        except Exception as e:
            print(f"激活窗口失败: {e}")
    
    def get_active_window_info(self) -> dict:
        """获取当前激活窗口信息"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd:
                title = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)
                return {
                    "hwnd": hwnd,
                    "title": title,
                    "class": class_name
                }
            else:
                return {"hwnd": None, "title": "未知", "class": "未知"}
                
        except Exception as e:
            print(f"获取窗口信息失败: {e}")
            return {"hwnd": None, "title": "未知", "class": "未知"}
    
    def is_safe_to_type(self) -> bool:
        """检查当前窗口是否安全进行自动输入"""
        try:
            window_info = self.get_active_window_info()
            title = window_info.get("title", "").lower()
            class_name = window_info.get("class", "").lower()
            
            # 不安全的窗口关键词
            unsafe_keywords = [
                "task manager", "任务管理器",
                "command prompt", "cmd", "命令提示符",
                "powershell",
                "file explorer", "文件资源管理器",
                "control panel", "控制面板",
                "administrator", "管理员",
                "system", "系统",
                "security", "安全"
            ]
            
            # 检查标题和类名是否包含不安全关键词
            for keyword in unsafe_keywords:
                if keyword in title or keyword in class_name:
                    print(f"检测到不安全窗口: {window_info.get('title')} ({window_info.get('class')})")
                    return False
            
            return True
            
        except Exception as e:
            print(f"安全检查失败: {e}")
            return False


# 创建全局实例
auto_type_manager = AutoTypeManager() 