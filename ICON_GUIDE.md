# 托盘图标使用指南

## 概述

已为 Paste for Windows 创建了完整的图标系统，包括托盘图标和应用程序图标。

## 图标文件

### 托盘图标
- **文件位置**: `resources/icons/tray_icon.png`
- **尺寸**: 32x32 像素
- **设计**: 蓝色圆形背景，白色剪贴板图标
- **用途**: 系统托盘显示

### 应用程序图标
- **文件位置**: `resources/icons/app_icon.png`
- **尺寸**: 128x128 像素
- **设计**: 大尺寸版本，适合窗口标题栏和任务栏
- **用途**: 应用程序窗口图标

### SVG 源文件
- **文件位置**: `resources/icons/tray_icon.svg`
- **用途**: 矢量格式源文件，可用于生成其他尺寸

## 图标生成

### 自动生成脚本
```bash
python scripts/create_simple_icon.py
```

这个脚本会：
1. 使用 PyQt6 绘制图标
2. 生成托盘图标 (32x32)
3. 生成应用程序图标 (128x128)
4. 保存到 `resources/icons/` 目录

### 手动生成（如果需要其他尺寸）
```bash
python scripts/create_icons.py
```

需要安装额外的依赖：
```bash
pip install cairosvg
```

## 代码集成

### 托盘图标使用
在 `src/gui/system_tray.py` 中：

```python
def _create_icon(self):
    """创建托盘图标"""
    # 尝试加载图标文件
    icon_path = Path(__file__).parent.parent.parent / "resources" / "icons" / "tray_icon.png"
    
    if icon_path.exists():
        # 使用实际的图标文件
        icon = QIcon(str(icon_path))
        self.tray_icon.setIcon(icon)
    else:
        # 备用方案：动态绘制图标
        # ... 绘制代码 ...
```

### 应用程序图标使用
在主程序中：

```python
from pathlib import Path
from PyQt6.QtGui import QIcon

app_icon_path = Path("resources/icons/app_icon.png")
if app_icon_path.exists():
    app.setWindowIcon(QIcon(str(app_icon_path)))
```

## 图标设计说明

### 托盘图标设计
- **背景**: 蓝色圆形 (#0078d4)，符合 Windows 11 设计语言
- **主体**: 白色剪贴板，简洁明了
- **顶部**: 灰色夹子，增加真实感
- **内容**: 蓝色线条，表示剪贴板内容

### 颜色方案
- **主色**: #0078d4 (Windows 蓝色)
- **背景**: #ffffff (白色)
- **夹子**: #c0c0c0 (灰色)
- **边框**: #d0d0d0 (浅灰色)

## 测试

### 托盘图标测试
```bash
python tray_demo.py
```

### 图标文件检查
```bash
python test_icon.py
```

## 故障排除

### 图标不显示
1. 检查图标文件是否存在
2. 确认文件路径正确
3. 验证文件权限

### 图标模糊
1. 确保使用正确尺寸的图标
2. 检查图标文件质量
3. 考虑重新生成更高分辨率的图标

### 备用方案
如果图标文件不存在，系统会自动生成一个简单的图标作为备用方案。

## 自定义

### 修改图标颜色
编辑 `scripts/create_simple_icon.py` 中的颜色值：

```python
# 修改主色
painter.setBrush(QBrush(QColor("#your_color_here")))
```

### 修改图标设计
1. 编辑 SVG 源文件
2. 或修改 Python 绘制代码
3. 重新运行生成脚本

## 注意事项

1. 图标文件应放在 `resources/icons/` 目录下
2. 托盘图标建议使用 32x32 像素
3. 应用程序图标建议使用 128x128 像素或更大
4. 确保图标文件格式为 PNG（推荐）或 ICO
5. 图标文件应具有透明背景以支持不同主题 