#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
负责管理应用程序的各种设置
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, field, asdict
from PyQt6.QtCore import QObject, pyqtSignal


@dataclass
class AppConfig:
    """应用程序配置"""
    
    # 基础设置
    app_name: str = "Paste for Windows"
    app_version: str = "1.0.0"
    
    # 剪贴板设置
    max_clipboard_items: int = 1000
    clipboard_check_interval: int = 100  # 毫秒
    auto_clean_days: int = 30
    
    # 界面设置
    window_width: int = 800
    window_height: int = 600
    window_x: int = -1  # -1 表示居中
    window_y: int = -1  # -1 表示居中
    theme: str = "auto"  # auto, light, dark
    opacity: float = 1.0
    
    # 快捷键设置
    show_window_hotkey: str = "Win+V"
    quick_paste_hotkey: str = "Win+Shift+V"
    
    # 系统集成设置
    auto_start: bool = False
    minimize_to_tray: bool = True
    show_notifications: bool = True
    start_minimized: bool = False
    
    # 搜索设置
    search_history_limit: int = 20
    fuzzy_search: bool = True
    
    # 数据设置
    backup_enabled: bool = True
    backup_interval_days: int = 7
    backup_keep_count: int = 5
    
    # 高级设置
    debug_mode: bool = False
    log_level: str = "INFO"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AppConfig':
        """从字典创建配置"""
        return cls(**data)


class ConfigManager(QObject):
    """配置管理器"""
    
    # 信号定义
    config_changed = pyqtSignal(str, object)  # 配置项名称, 新值
    config_loaded = pyqtSignal()
    config_saved = pyqtSignal()
    
    def __init__(self, config_file: str = None):
        super().__init__()
        
        if config_file is None:
            # 默认配置文件路径
            app_data_dir = Path.home() / "AppData" / "Local" / "PasteForWindows"
            app_data_dir.mkdir(parents=True, exist_ok=True)
            config_file = app_data_dir / "config.json"
        
        self.config_file = Path(config_file)
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 默认配置
        self._config = AppConfig()
        
        # 加载配置
        self.load_config()
    
    def load_config(self) -> bool:
        """加载配置文件"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._config = AppConfig.from_dict(data)
                    print(f"配置加载成功: {self.config_file}")
            else:
                # 创建默认配置文件
                self.save_config()
                print(f"创建默认配置文件: {self.config_file}")
            
            self.config_loaded.emit()
            return True
            
        except Exception as e:
            print(f"配置加载失败: {e}")
            return False
    
    def save_config(self) -> bool:
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config.to_dict(), f, indent=2, ensure_ascii=False)
            
            print(f"配置保存成功: {self.config_file}")
            self.config_saved.emit()
            return True
            
        except Exception as e:
            print(f"配置保存失败: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return getattr(self._config, key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """设置配置值"""
        try:
            if hasattr(self._config, key):
                old_value = getattr(self._config, key)
                setattr(self._config, key, value)
                
                # 发送配置变化信号
                self.config_changed.emit(key, value)
                
                # 自动保存配置
                self.save_config()
                
                print(f"配置更新: {key} = {value}")
                return True
            else:
                print(f"配置项不存在: {key}")
                return False
                
        except Exception as e:
            print(f"设置配置失败: {e}")
            return False
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self._config.to_dict()
    
    def reset_to_defaults(self) -> bool:
        """重置为默认配置"""
        try:
            self._config = AppConfig()
            self.save_config()
            print("配置已重置为默认值")
            return True
            
        except Exception as e:
            print(f"重置配置失败: {e}")
            return False
    
    def export_config(self, export_path: str) -> bool:
        """导出配置"""
        try:
            export_file = Path(export_path)
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(self._config.to_dict(), f, indent=2, ensure_ascii=False)
            
            print(f"配置导出成功: {export_file}")
            return True
            
        except Exception as e:
            print(f"配置导出失败: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """导入配置"""
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                print(f"配置文件不存在: {import_file}")
                return False
            
            with open(import_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._config = AppConfig.from_dict(data)
            
            self.save_config()
            print(f"配置导入成功: {import_file}")
            return True
            
        except Exception as e:
            print(f"配置导入失败: {e}")
            return False
    
    # 便捷方法
    def get_clipboard_settings(self) -> Dict[str, Any]:
        """获取剪贴板相关设置"""
        return {
            'max_items': self.get('max_clipboard_items'),
            'check_interval': self.get('clipboard_check_interval'),
            'auto_clean_days': self.get('auto_clean_days')
        }
    
    def get_ui_settings(self) -> Dict[str, Any]:
        """获取界面相关设置"""
        return {
            'window_width': self.get('window_width'),
            'window_height': self.get('window_height'),
            'window_x': self.get('window_x'),
            'window_y': self.get('window_y'),
            'theme': self.get('theme'),
            'opacity': self.get('opacity')
        }
    
    def get_hotkey_settings(self) -> Dict[str, Any]:
        """获取快捷键设置"""
        return {
            'show_window': self.get('show_window_hotkey'),
            'quick_paste': self.get('quick_paste_hotkey')
        }
    
    def get_system_settings(self) -> Dict[str, Any]:
        """获取系统集成设置"""
        return {
            'auto_start': self.get('auto_start'),
            'minimize_to_tray': self.get('minimize_to_tray'),
            'show_notifications': self.get('show_notifications'),
            'start_minimized': self.get('start_minimized')
        } 