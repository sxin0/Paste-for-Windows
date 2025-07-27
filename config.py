"""
Windows 剪贴板管理器配置文件
"""
import os
import configparser

# 应用程序基本信息
APP_NAME = "Paste for Windows"
APP_VERSION = "1.0.0"
APP_AUTHOR = "ClipboardManager"

# 文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.expanduser("~"), ".clipboardmanager")
DB_PATH = os.path.join(DATA_DIR, "clipboard_history.db")
CONFIG_PATH = os.path.join(DATA_DIR, "config.ini")

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

# 默认配置
DEFAULT_CONFIG = {
    "general": {
        "max_history_items": "100",
        "auto_start": "true",
        "show_notifications": "true",
        "hotkey": "win+v",
        "window_width": "600",
        "window_height": "400",
        "theme": "light"
    },
    "clipboard": {
        "monitor_interval": "0.5",
        "save_images": "true",
        "save_files": "true",
        "max_text_length": "10000"
    }
}

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(CONFIG_PATH):
            self.config.read(CONFIG_PATH, encoding='utf-8')
        else:
            # 如果配置文件不存在，创建默认配置
            self.create_default_config()
    
    def create_default_config(self):
        """创建默认配置文件"""
        for section, options in DEFAULT_CONFIG.items():
            self.config.add_section(section)
            for key, value in options.items():
                self.config.set(section, key, value)
        self.save_config()
    
    def save_config(self):
        """保存配置文件"""
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def get(self, section, key, fallback=None):
        """获取配置值"""
        return self.config.get(section, key, fallback=fallback)
    
    def getint(self, section, key, fallback=0):
        """获取整数配置值"""
        return self.config.getint(section, key, fallback=fallback)
    
    def getboolean(self, section, key, fallback=False):
        """获取布尔配置值"""
        return self.config.getboolean(section, key, fallback=fallback)
    
    def getfloat(self, section, key, fallback=0.0):
        """获取浮点数配置值"""
        return self.config.getfloat(section, key, fallback=fallback)
    
    def set(self, section, key, value):
        """设置配置值"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        self.save_config()

# 全局配置实例
config = Config() 