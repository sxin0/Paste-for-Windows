#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图标生成脚本
将SVG图标转换为PNG格式
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from cairosvg import svg2png
    print("✅ 使用 cairosvg 库转换图标...")
except ImportError:
    print("❌ 未安装 cairosvg 库，尝试使用其他方法...")
    try:
        # 尝试使用 rsvg-convert (如果安装了 librsvg)
        import subprocess
        def svg_to_png_svg2png(svg_path, png_path, size=32):
            """使用 rsvg-convert 转换 SVG 到 PNG"""
            try:
                subprocess.run([
                    'rsvg-convert', 
                    '-w', str(size), 
                    '-h', str(size),
                    '-f', 'png',
                    '-o', str(png_path),
                    str(svg_path)
                ], check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False
        
        svg2png = None
        print("⚠️  使用 rsvg-convert 转换图标...")
    except ImportError:
        print("❌ 无法找到可用的SVG转换工具")
        print("请安装以下任一工具：")
        print("  pip install cairosvg")
        print("  或安装 librsvg (Windows: choco install librsvg)")
        sys.exit(1)

def create_icons():
    """创建图标文件"""
    icons_dir = project_root / "resources" / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)
    
    # 图标尺寸列表
    sizes = [16, 24, 32, 48, 64, 128, 256]
    
    svg_path = icons_dir / "tray_icon.svg"
    if not svg_path.exists():
        print(f"❌ SVG 文件不存在: {svg_path}")
        return False
    
    print(f"📁 图标目录: {icons_dir}")
    print(f"🎨 源SVG文件: {svg_path}")
    
    success_count = 0
    
    for size in sizes:
        png_path = icons_dir / f"tray_icon_{size}x{size}.png"
        
        try:
            if svg2png:
                # 使用 cairosvg
                with open(svg_path, 'rb') as svg_file:
                    svg2png(
                        file_obj=svg_file,
                        write_to=str(png_path),
                        output_width=size,
                        output_height=size
                    )
            else:
                # 使用 rsvg-convert
                if svg_to_png_svg2png(svg_path, png_path, size):
                    pass
                else:
                    print(f"❌ 转换失败: {size}x{size}")
                    continue
            
            print(f"✅ 创建图标: {png_path.name}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 转换 {size}x{size} 失败: {e}")
    
    # 创建默认图标（32x32）
    default_png = icons_dir / "tray_icon.png"
    if (icons_dir / "tray_icon_32x32.png").exists():
        import shutil
        shutil.copy2(icons_dir / "tray_icon_32x32.png", default_png)
        print(f"✅ 创建默认图标: {default_png.name}")
        success_count += 1
    
    print(f"\n🎉 图标创建完成！成功创建 {success_count} 个图标文件")
    return success_count > 0

if __name__ == "__main__":
    print("🚀 开始创建图标...")
    if create_icons():
        print("✅ 图标创建成功！")
    else:
        print("❌ 图标创建失败！")
        sys.exit(1) 