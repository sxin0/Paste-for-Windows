"""
Windows 剪贴板管理器安装脚本
"""
import subprocess
import sys
import os
import shutil
from pathlib import Path

def install_requirements():
    """安装Python依赖"""
    print("正在安装Python依赖...")
    
    # 基础依赖包
    packages = [
        'pyperclip==1.8.2',
        'pystray==0.19.4',
        'pillow==10.0.1',
        'keyboard==0.13.5',
        'configparser==6.0.0',
    ]
    
    # Windows特定依赖
    if sys.platform.startswith('win'):
        packages.extend([
            'pywin32',  # Windows API支持
            'win10toast',  # Windows 10 通知支持
        ])
    
    for package in packages:
        try:
            print(f"安装 {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"✗ {package} 安装失败: {e}")
            return False
    
    print("所有依赖安装完成！")
    return True

def create_desktop_shortcut():
    """创建桌面快捷方式"""
    try:
        import win32com.client
        
        desktop = Path.home() / "Desktop"
        shortcut_path = desktop / "Paste for Windows.lnk"
        
        # 获取当前脚本目录
        current_dir = Path(__file__).parent.absolute()
        target_path = current_dir / "main.py"
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target_path}"'
        shortcut.WorkingDirectory = str(current_dir)
        shortcut.IconLocation = str(current_dir / "clipboard.ico") if (current_dir / "clipboard.ico").exists() else ""
        shortcut.Description = "Windows 剪贴板管理器"
        shortcut.save()
        
        print(f"✓ 桌面快捷方式已创建: {shortcut_path}")
        return True
    except Exception as e:
        print(f"✗ 创建桌面快捷方式失败: {e}")
        return False

def create_start_menu_entry():
    """创建开始菜单项"""
    try:
        import win32com.client
        
        start_menu = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
        start_menu.mkdir(parents=True, exist_ok=True)
        
        shortcut_path = start_menu / "Paste for Windows.lnk"
        
        # 获取当前脚本目录
        current_dir = Path(__file__).parent.absolute()
        target_path = current_dir / "main.py"
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target_path}"'
        shortcut.WorkingDirectory = str(current_dir)
        shortcut.IconLocation = str(current_dir / "clipboard.ico") if (current_dir / "clipboard.ico").exists() else ""
        shortcut.Description = "Windows 剪贴板管理器"
        shortcut.save()
        
        print(f"✓ 开始菜单项已创建: {shortcut_path}")
        return True
    except Exception as e:
        print(f"✗ 创建开始菜单项失败: {e}")
        return False

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("✗ 需要Python 3.7或更高版本")
        print(f"当前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✓ Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
    return True

def create_icon_file():
    """创建应用程序图标"""
    try:
        from PIL import Image, ImageDraw
        
        # 创建一个简单的剪贴板图标
        size = 64
        image = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # 绘制剪贴板
        clipboard_color = (70, 130, 180)  # 钢蓝色
        clip_color = (105, 105, 105)      # 暗灰色
        
        # 主剪贴板区域
        draw.rectangle([8, 12, 56, 56], fill=clipboard_color, outline=(0, 0, 0), width=2)
        
        # 夹子
        draw.rectangle([20, 8, 44, 16], fill=clip_color, outline=(0, 0, 0), width=1)
        draw.rectangle([24, 4, 40, 12], fill=clip_color, outline=(0, 0, 0), width=1)
        
        # 文档线条
        for i, y in enumerate([22, 28, 34, 40]):
            width = 32 - (i * 2)
            draw.rectangle([16, y, 16 + width, y + 2], fill=(255, 255, 255))
        
        # 保存为ICO文件
        icon_path = Path(__file__).parent / "clipboard.ico"
        image.save(icon_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
        
        print(f"✓ 应用程序图标已创建: {icon_path}")
        return True
    except Exception as e:
        print(f"✗ 创建图标失败: {e}")
        return False

def setup_auto_start():
    """设置开机自启动"""
    try:
        from utils import AutoStartManager
        
        if AutoStartManager.enable_auto_start():
            print("✓ 开机自启动已设置")
            return True
        else:
            print("✗ 设置开机自启动失败")
            return False
    except Exception as e:
        print(f"✗ 设置开机自启动失败: {e}")
        return False

def main():
    """主安装函数"""
    print("=" * 60)
    print("    Windows 剪贴板管理器 - 安装程序")
    print("=" * 60)
    print()
    
    # 检查Python版本
    if not check_python_version():
        return False
    
    print()
    
    # 安装依赖
    if not install_requirements():
        print("依赖安装失败，安装中止")
        return False
    
    print()
    
    # 创建图标
    create_icon_file()
    
    # 创建快捷方式
    print("正在创建快捷方式...")
    create_desktop_shortcut()
    create_start_menu_entry()
    
    print()
    
    # 设置开机自启动
    setup_auto_start()
    
    print()
    print("=" * 60)
    print("安装完成！")
    print()
    print("使用方法:")
    print("1. 双击桌面快捷方式启动程序")
    print("2. 程序会在系统托盘中运行")
    print("3. 使用 Ctrl+Shift+V 快捷键打开主窗口")
    print("4. 程序会自动监听剪贴板变化并保存历史记录")
    print()
    print("功能特性:")
    print("• 自动监听剪贴板变化")
    print("• 支持文本、图片、文件等多种格式")
    print("• 智能搜索和过滤")
    print("• 收藏和历史记录管理")
    print("• 数据持久化存储")
    print("• 系统托盘集成")
    print("• 全局快捷键支持")
    print("=" * 60)
    
    # 询问是否立即启动
    try:
        choice = input("\n是否立即启动应用程序？(y/n): ").lower().strip()
        if choice in ['y', 'yes', '是']:
            print("正在启动应用程序...")
            current_dir = Path(__file__).parent
            main_script = current_dir / "main.py"
            subprocess.Popen([sys.executable, str(main_script)])
            print("应用程序已启动！")
    except KeyboardInterrupt:
        print("\n用户取消")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n安装被用户取消")
    except Exception as e:
        print(f"\n安装过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n按回车键退出...")