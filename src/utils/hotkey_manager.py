#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全局快捷键管理器
负责注册和管理全局快捷键
"""

import threading
import time
from typing import Callable, Optional
from PyQt6.QtCore import QObject, pyqtSignal

try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("警告: keyboard 模块未安装，全局快捷键功能不可用")


class HotkeyManager(QObject):
    """全局快捷键管理器"""
    
    # 信号定义
    toggle_bottom_panel_requested = pyqtSignal()  # 切换底部面板
    
    def __init__(self):
        super().__init__()
        self._registered_hotkeys = {}
        self._is_running = False
        self._hotkey_thread = None
        
        # 默认快捷键配置
        self.default_hotkeys = {
            'toggle_bottom_panel': 'alt+v'
        }
    
    def start(self):
        """启动快捷键监听"""
        if not KEYBOARD_AVAILABLE:
            print("❌ keyboard 模块不可用，无法启动全局快捷键")
            return False
        
        if self._is_running:
            print("⚠️ 快捷键管理器已在运行")
            return True
        
        try:
            self._is_running = True
            self._hotkey_thread = threading.Thread(target=self._run_hotkey_listener, daemon=True)
            self._hotkey_thread.start()
            
            print("✅ 全局快捷键管理器已启动")
            return True
            
        except Exception as e:
            print(f"❌ 启动快捷键管理器失败: {e}")
            self._is_running = False
            return False
    
    def stop(self):
        """停止快捷键监听"""
        if not self._is_running:
            return
        
        try:
            self._is_running = False
            
            # 注销所有快捷键
            self._unregister_all_hotkeys()
            
            # 等待线程结束
            if self._hotkey_thread and self._hotkey_thread.is_alive():
                self._hotkey_thread.join(timeout=1.0)
            
            print("✅ 全局快捷键管理器已停止")
            
        except Exception as e:
            print(f"❌ 停止快捷键管理器失败: {e}")
    
    def _run_hotkey_listener(self):
        """运行快捷键监听线程"""
        try:
            # 注册快捷键
            self._register_default_hotkeys()
            
            # 保持线程运行
            while self._is_running:
                time.sleep(0.1)
                
        except Exception as e:
            print(f"❌ 快捷键监听线程异常: {e}")
        finally:
            self._unregister_all_hotkeys()
    
    def _register_default_hotkeys(self):
        """注册默认快捷键"""
        try:
            # 注册 Alt+V 切换底部面板
            keyboard.add_hotkey(
                self.default_hotkeys['toggle_bottom_panel'],
                self._on_toggle_bottom_panel_requested,
                suppress=True
            )
            self._registered_hotkeys['toggle_bottom_panel'] = self.default_hotkeys['toggle_bottom_panel']
            
            print(f"✅ 已注册快捷键:")
            print(f"   - {self.default_hotkeys['toggle_bottom_panel']} - 切换底部面板")
            
        except Exception as e:
            print(f"❌ 注册快捷键失败: {e}")
    
    def _unregister_all_hotkeys(self):
        """注销所有快捷键"""
        try:
            for hotkey_name, hotkey in self._registered_hotkeys.items():
                try:
                    keyboard.remove_hotkey(hotkey)
                    print(f"✅ 已注销快捷键: {hotkey}")
                except Exception as e:
                    print(f"⚠️ 注销快捷键 {hotkey} 失败: {e}")
            
            self._registered_hotkeys.clear()
            
        except Exception as e:
            print(f"❌ 注销快捷键失败: {e}")
    
    def _on_toggle_bottom_panel_requested(self):
        """Alt+V 快捷键回调 - 切换底部面板"""
        print("🎯 Alt+V 快捷键触发 - 切换底部面板")
        self.toggle_bottom_panel_requested.emit()
    
    def register_hotkey(self, hotkey: str, callback: Callable, name: str = None):
        """注册自定义快捷键"""
        if not KEYBOARD_AVAILABLE:
            print("❌ keyboard 模块不可用，无法注册快捷键")
            return False
        
        try:
            keyboard.add_hotkey(hotkey, callback, suppress=True)
            hotkey_name = name or f"custom_{len(self._registered_hotkeys)}"
            self._registered_hotkeys[hotkey_name] = hotkey
            print(f"✅ 已注册自定义快捷键: {hotkey}")
            return True
            
        except Exception as e:
            print(f"❌ 注册自定义快捷键失败: {e}")
            return False
    
    def unregister_hotkey(self, name: str):
        """注销指定快捷键"""
        if name in self._registered_hotkeys:
            try:
                hotkey = self._registered_hotkeys[name]
                keyboard.remove_hotkey(hotkey)
                del self._registered_hotkeys[name]
                print(f"✅ 已注销快捷键: {hotkey}")
                return True
                
            except Exception as e:
                print(f"❌ 注销快捷键失败: {e}")
                return False
        
        return False
    
    def get_registered_hotkeys(self):
        """获取已注册的快捷键列表"""
        return self._registered_hotkeys.copy()
    
    def is_running(self):
        """检查是否正在运行"""
        return self._is_running
    
    def is_available(self):
        """检查快捷键功能是否可用"""
        return KEYBOARD_AVAILABLE


# 全局快捷键管理器实例
hotkey_manager = HotkeyManager() 