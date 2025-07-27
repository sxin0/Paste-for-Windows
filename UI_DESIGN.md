# Paste for Windows - UI 设计文档

## 🎨 技术栈UI支持能力分析

### ✅ 当前技术栈优势

#### PyQt6 强大支持
- **现代化渲染引擎**: Qt6 提供最新的图形渲染技术
- **硬件加速**: 支持 GPU 加速渲染
- **高DPI支持**: 完美支持高分辨率显示器
- **跨平台一致性**: 在不同 Windows 版本上保持一致的外观

#### Windows 11 深度集成
- **Fluent Design**: 支持 Windows 11 设计语言
- **毛玻璃效果**: 原生支持 Acrylic 材质效果
- **系统主题**: 自动跟随系统主题切换
- **动画系统**: 流畅的界面动画

#### 图像处理能力
- **Pillow 支持**: 强大的图像处理和预览
- **多格式支持**: PNG, JPG, GIF, BMP, WebP 等
- **缩略图生成**: 自动生成高质量缩略图
- **图像压缩**: 智能图像压缩和优化

## 🎯 UI 设计理念

### 设计原则
1. **简洁优雅** - 遵循 Windows 11 Fluent Design 设计语言
2. **高效易用** - 直观的操作流程，减少学习成本
3. **响应迅速** - 流畅的动画和快速响应
4. **个性化** - 丰富的自定义选项
5. **无障碍** - 支持高对比度和屏幕阅读器

### 视觉风格
- **主色调**: 使用 Windows 11 系统色彩
- **字体**: Segoe UI 字体家族
- **图标**: Fluent Design 图标系统
- **间距**: 8px 网格系统
- **圆角**: 4px-8px 圆角设计

## 🏗️ 界面架构设计

### 主窗口布局
```
┌─────────────────────────────────────────────────────────────┐
│ 🎨 标题栏 (自定义标题栏)                                    │
├─────────────────────────────────────────────────────────────┤
│ 🔍 搜索栏 │ ⚙️ 设置 │ 🎨 主题 │ 📊 统计 │ 🚪 退出        │
├─────────────────────────────────────────────────────────────┤
│ 📁 侧边栏 │ 主内容区域                                      │
│ 收藏夹    │ ┌─────────────────────────────────────────────┐ │
│ 最近      │ │ 剪贴板项目列表                              │ │
│ 图片      │ │ • 项目1 (带预览)                            │ │
│ 文件      │ │ • 项目2 (带预览)                            │ │
│ 链接      │ │ • 项目3 (带预览)                            │ │
│ 标签      │ │ • 项目4 (带预览)                            │ │
│           │ └─────────────────────────────────────────────┘ │
│           │                                                 │
│           │ 📋 预览区域                                    │
│           │ ┌─────────────────────────────────────────────┐ │
│           │ │ 内容预览                                    │ │
│           │ │ 详细信息                                    │ │
│           │ │ 操作按钮                                    │ │
│           │ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 组件设计规范

#### 1. 搜索栏组件
```python
class SearchBarWidget(QWidget):
    """现代化搜索栏"""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        # 搜索输入框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索剪贴板内容...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 20px;
                padding: 8px 16px;
                font-size: 14px;
                background: rgba(255, 255, 255, 0.8);
                backdrop-filter: blur(10px);
            }
            QLineEdit:focus {
                border-color: #0078d4;
                background: rgba(255, 255, 255, 0.95);
            }
        """)
        
        # 搜索图标
        self.search_icon = QLabel()
        self.search_icon.setPixmap(QPixmap(":/icons/search.svg"))
        
        # 过滤按钮
        self.filter_btn = QPushButton("筛选")
        self.filter_btn.setStyleSheet("""
            QPushButton {
                background: #0078d4;
                color: white;
                border: none;
                border-radius: 16px;
                padding: 8px 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #106ebe;
            }
        """)
```

#### 2. 剪贴板列表组件
```python
class ClipboardListWidget(QListWidget):
    """现代化剪贴板列表"""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        # 设置样式
        self.setStyleSheet("""
            QListWidget {
                background: rgba(255, 255, 255, 0.8);
                border: none;
                border-radius: 8px;
                padding: 8px;
                backdrop-filter: blur(10px);
            }
            QListWidget::item {
                background: rgba(255, 255, 255, 0.6);
                border-radius: 6px;
                margin: 2px;
                padding: 12px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
            QListWidget::item:hover {
                background: rgba(0, 120, 212, 0.1);
                border-color: rgba(0, 120, 212, 0.3);
            }
            QListWidget::item:selected {
                background: rgba(0, 120, 212, 0.2);
                border-color: #0078d4;
            }
        """)
        
        # 设置动画
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(10)
```

#### 3. 预览面板组件
```python
class PreviewPanelWidget(QWidget):
    """内容预览面板"""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # 标题栏
        title_bar = QHBoxLayout()
        self.title_label = QLabel("预览")
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #323130;
            }
        """)
        
        # 操作按钮
        self.copy_btn = QPushButton("复制")
        self.favorite_btn = QPushButton("收藏")
        self.delete_btn = QPushButton("删除")
        
        # 按钮样式
        button_style = """
            QPushButton {
                background: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
                min-width: 60px;
            }
            QPushButton:hover {
                background: #106ebe;
            }
            QPushButton:pressed {
                background: #005a9e;
            }
        """
        
        self.copy_btn.setStyleSheet(button_style)
        self.favorite_btn.setStyleSheet(button_style.replace("#0078d4", "#107c10"))
        self.delete_btn.setStyleSheet(button_style.replace("#0078d4", "#d13438"))
```

## 🎨 主题系统设计

### 主题配置
```python
class ThemeManager:
    """主题管理器"""
    
    def __init__(self):
        self.current_theme = "light"
        self.themes = {
            "light": {
                "background": "rgba(255, 255, 255, 0.9)",
                "surface": "rgba(255, 255, 255, 0.8)",
                "primary": "#0078d4",
                "secondary": "#605e5c",
                "text": "#323130",
                "text_secondary": "#605e5c",
                "border": "rgba(0, 0, 0, 0.1)",
                "shadow": "rgba(0, 0, 0, 0.1)",
            },
            "dark": {
                "background": "rgba(32, 32, 32, 0.9)",
                "surface": "rgba(50, 50, 50, 0.8)",
                "primary": "#60cdf8",
                "secondary": "#c8c6c4",
                "text": "#ffffff",
                "text_secondary": "#c8c6c4",
                "border": "rgba(255, 255, 255, 0.1)",
                "shadow": "rgba(0, 0, 0, 0.3)",
            }
        }
    
    def apply_theme(self, theme_name: str):
        """应用主题"""
        if theme_name not in self.themes:
            return
            
        self.current_theme = theme_name
        theme = self.themes[theme_name]
        
        # 应用全局样式
        app = QApplication.instance()
        app.setStyleSheet(self._generate_global_style(theme))
    
    def _generate_global_style(self, theme: dict) -> str:
        """生成全局样式"""
        return f"""
            QMainWindow {{
                background: {theme['background']};
                color: {theme['text']};
            }}
            
            QWidget {{
                background: transparent;
                color: {theme['text']};
            }}
            
            QPushButton {{
                background: {theme['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
            }}
            
            QPushButton:hover {{
                background: {self._adjust_color(theme['primary'], -10)};
            }}
            
            QLineEdit {{
                background: {theme['surface']};
                border: 2px solid {theme['border']};
                border-radius: 8px;
                padding: 8px 12px;
                color: {theme['text']};
            }}
            
            QLineEdit:focus {{
                border-color: {theme['primary']};
            }}
        """
```

## 🌟 现代化特效

### 1. 毛玻璃效果
```python
class BlurWidget(QWidget):
    """毛玻璃效果组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 创建毛玻璃效果
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(20)
        
        # 绘制背景
        rect = self.rect()
        painter.fillRect(rect, QColor(255, 255, 255, 30))
```

### 2. 动画系统
```python
class AnimationManager:
    """动画管理器"""
    
    def __init__(self):
        self.animations = {}
    
    def fade_in(self, widget: QWidget, duration: int = 300):
        """淡入动画"""
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()
    
    def slide_in(self, widget: QWidget, direction: str = "right", duration: int = 300):
        """滑入动画"""
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        
        # 设置起始和结束位置
        start_rect = widget.geometry()
        end_rect = widget.geometry()
        
        if direction == "right":
            start_rect.setX(start_rect.x() + start_rect.width())
        elif direction == "left":
            start_rect.setX(start_rect.x() - start_rect.width())
        elif direction == "up":
            start_rect.setY(start_rect.y() - start_rect.height())
        elif direction == "down":
            start_rect.setY(start_rect.y() + start_rect.height())
        
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()
```

### 3. 响应式布局
```python
class ResponsiveLayout(QVBoxLayout):
    """响应式布局"""
    
    def __init__(self):
        super().__init__()
        self.setSpacing(8)
        self.setContentsMargins(16, 16, 16, 16)
    
    def resizeEvent(self, event):
        """响应窗口大小变化"""
        width = event.size().width()
        
        # 根据窗口宽度调整布局
        if width < 600:
            # 小屏幕：垂直布局
            self.setDirection(QBoxLayout.TopToBottom)
        elif width < 1000:
            # 中等屏幕：混合布局
            self.setDirection(QBoxLayout.LeftToRight)
        else:
            # 大屏幕：水平布局
            self.setDirection(QBoxLayout.LeftToRight)
```

## 🎯 界面组件设计

### 1. 剪贴板项目卡片
```python
class ClipboardItemWidget(QWidget):
    """剪贴板项目卡片"""
    
    def __init__(self, item: ClipboardItem):
        super().__init__()
        self.item = item
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)
        
        # 类型图标
        self.type_icon = QLabel()
        self.type_icon.setFixedSize(24, 24)
        self.type_icon.setPixmap(self._get_type_icon())
        
        # 内容预览
        self.preview_label = QLabel(self.item.preview)
        self.preview_label.setWordWrap(True)
        self.preview_label.setMaximumHeight(60)
        
        # 时间标签
        self.time_label = QLabel(self._format_time())
        self.time_label.setStyleSheet("color: #605e5c; font-size: 12px;")
        
        # 收藏按钮
        self.favorite_btn = QPushButton()
        self.favorite_btn.setFixedSize(24, 24)
        self.favorite_btn.setIcon(self._get_favorite_icon())
        self.favorite_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                background: rgba(0, 120, 212, 0.1);
                border-radius: 12px;
            }
        """)
        
        # 添加到布局
        layout.addWidget(self.type_icon)
        layout.addWidget(self.preview_label, 1)
        layout.addWidget(self.time_label)
        layout.addWidget(self.favorite_btn)
```

### 2. 设置对话框
```python
class SettingsDialog(QDialog):
    """设置对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setFixedSize(600, 500)
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 标签页
        self.tab_widget = QTabWidget()
        
        # 常规设置
        general_tab = QWidget()
        general_layout = QFormLayout(general_tab)
        
        self.autostart_cb = QCheckBox("开机自启动")
        self.notification_cb = QCheckBox("显示通知")
        self.minimize_tray_cb = QCheckBox("最小化到系统托盘")
        
        general_layout.addRow("启动设置:", self.autostart_cb)
        general_layout.addRow("通知设置:", self.notification_cb)
        general_layout.addRow("窗口行为:", self.minimize_tray_cb)
        
        # 剪贴板设置
        clipboard_tab = QWidget()
        clipboard_layout = QFormLayout(clipboard_tab)
        
        self.max_history_spin = QSpinBox()
        self.max_history_spin.setRange(100, 10000)
        self.max_history_spin.setValue(1000)
        
        self.auto_clean_cb = QCheckBox("自动清理过期数据")
        self.clean_days_spin = QSpinBox()
        self.clean_days_spin.setRange(1, 365)
        self.clean_days_spin.setValue(30)
        
        clipboard_layout.addRow("最大历史记录:", self.max_history_spin)
        clipboard_layout.addRow("自动清理:", self.auto_clean_cb)
        clipboard_layout.addRow("清理天数:", self.clean_days_spin)
        
        # 外观设置
        appearance_tab = QWidget()
        appearance_layout = QFormLayout(appearance_tab)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["跟随系统", "浅色主题", "深色主题"])
        
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(50, 100)
        self.opacity_slider.setValue(90)
        
        appearance_layout.addRow("主题:", self.theme_combo)
        appearance_layout.addRow("透明度:", self.opacity_slider)
        
        # 添加快捷键设置
        hotkey_tab = QWidget()
        hotkey_layout = QFormLayout(hotkey_tab)
        
        self.show_window_hotkey = QLineEdit("Win+V")
        self.quick_paste_hotkey = QLineEdit("Win+Shift+V")
        
        hotkey_layout.addRow("显示窗口:", self.show_window_hotkey)
        hotkey_layout.addRow("快速粘贴:", self.quick_paste_hotkey)
        
        # 添加标签页
        self.tab_widget.addTab(general_tab, "常规")
        self.tab_widget.addTab(clipboard_tab, "剪贴板")
        self.tab_widget.addTab(appearance_tab, "外观")
        self.tab_widget.addTab(hotkey_tab, "快捷键")
        
        layout.addWidget(self.tab_widget)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("确定")
        self.cancel_btn = QPushButton("取消")
        self.apply_btn = QPushButton("应用")
        
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.apply_btn)
        
        layout.addLayout(button_layout)
```

## 🎨 样式表系统

### 全局样式表
```css
/* 全局样式 */
* {
    font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
}

QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                               stop:0 rgba(255,255,255,0.95),
                               stop:1 rgba(255,255,255,0.85));
    border-radius: 12px;
}

QWidget {
    background: transparent;
}

/* 按钮样式 */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                               stop:0 #0078d4,
                               stop:1 #106ebe);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
    font-size: 14px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                               stop:0 #106ebe,
                               stop:1 #005a9e);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                               stop:0 #005a9e,
                               stop:1 #004578);
}

/* 输入框样式 */
QLineEdit {
    background: rgba(255, 255, 255, 0.8);
    border: 2px solid rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 14px;
    selection-background-color: #0078d4;
}

QLineEdit:focus {
    border-color: #0078d4;
    background: rgba(255, 255, 255, 0.95);
}

/* 列表样式 */
QListWidget {
    background: rgba(255, 255, 255, 0.6);
    border: none;
    border-radius: 8px;
    padding: 8px;
    outline: none;
}

QListWidget::item {
    background: rgba(255, 255, 255, 0.8);
    border-radius: 6px;
    margin: 2px;
    padding: 12px;
    border: 1px solid rgba(0, 0, 0, 0.1);
}

QListWidget::item:hover {
    background: rgba(0, 120, 212, 0.1);
    border-color: rgba(0, 120, 212, 0.3);
}

QListWidget::item:selected {
    background: rgba(0, 120, 212, 0.2);
    border-color: #0078d4;
}

/* 滚动条样式 */
QScrollBar:vertical {
    background: rgba(0, 0, 0, 0.1);
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(0, 0, 0, 0.5);
}

/* 标签页样式 */
QTabWidget::pane {
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.8);
}

QTabBar::tab {
    background: rgba(255, 255, 255, 0.6);
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    padding: 8px 16px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background: rgba(255, 255, 255, 0.9);
    border-color: rgba(0, 120, 212, 0.3);
}
```

## 🚀 性能优化

### 1. 渲染优化
```python
class OptimizedWidget(QWidget):
    """优化渲染的组件"""
    
    def __init__(self):
        super().__init__()
        # 启用硬件加速
        self.setAttribute(Qt.WA_PaintOnScreen, False)
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)
        
        # 设置渲染提示
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.TextAntialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
```

### 2. 内存优化
```python
class MemoryOptimizedList(QListWidget):
    """内存优化的列表"""
    
    def __init__(self):
        super().__init__()
        self._item_cache = {}
        self._max_cache_size = 100
        
    def add_item(self, item: ClipboardItem):
        """添加项目时进行内存优化"""
        # 限制缓存大小
        if len(self._item_cache) > self._max_cache_size:
            # 清理最旧的缓存
            oldest_key = next(iter(self._item_cache))
            del self._item_cache[oldest_key]
        
        # 创建列表项
        list_item = QListWidgetItem()
        widget = ClipboardItemWidget(item)
        list_item.setSizeHint(widget.sizeHint())
        
        self.addItem(list_item)
        self.setItemWidget(list_item, widget)
        
        # 缓存项目
        self._item_cache[item.id] = widget
```

## 📱 响应式设计

### 1. 断点系统
```python
class ResponsiveDesign:
    """响应式设计管理器"""
    
    BREAKPOINTS = {
        "mobile": 480,
        "tablet": 768,
        "desktop": 1024,
        "large": 1440
    }
    
    def __init__(self, window: QMainWindow):
        self.window = window
        self.current_breakpoint = "desktop"
        
    def update_layout(self, width: int):
        """根据宽度更新布局"""
        new_breakpoint = self._get_breakpoint(width)
        
        if new_breakpoint != self.current_breakpoint:
            self.current_breakpoint = new_breakpoint
            self._apply_layout(new_breakpoint)
    
    def _get_breakpoint(self, width: int) -> str:
        """获取断点"""
        for breakpoint, min_width in self.BREAKPOINTS.items():
            if width >= min_width:
                return breakpoint
        return "mobile"
    
    def _apply_layout(self, breakpoint: str):
        """应用布局"""
        if breakpoint == "mobile":
            self._apply_mobile_layout()
        elif breakpoint == "tablet":
            self._apply_tablet_layout()
        elif breakpoint == "desktop":
            self._apply_desktop_layout()
        elif breakpoint == "large":
            self._apply_large_layout()
```

## 🎯 总结

### ✅ 技术栈完全支持现代化UI

你的技术栈 **PyQt6 + Windows 11** 完全支持创建现代化、美观的UI界面：

1. **PyQt6 优势**:
   - 最新的 Qt6 渲染引擎
   - 硬件加速支持
   - 丰富的动画系统
   - 强大的样式表支持

2. **Windows 11 集成**:
   - Fluent Design 设计语言
   - 毛玻璃效果支持
   - 系统主题集成
   - 原生动画效果

3. **性能优化**:
   - GPU 加速渲染
   - 内存优化
   - 响应式设计
   - 异步处理

### 🎨 设计建议

1. **遵循 Fluent Design** - 使用 Windows 11 设计语言
2. **毛玻璃效果** - 利用 Acrylic 材质效果
3. **流畅动画** - 添加适当的过渡动画
4. **响应式布局** - 支持不同屏幕尺寸
5. **主题系统** - 支持深色/浅色主题切换

### 🚀 实现优先级

1. **第一阶段**: 基础界面和主题系统
2. **第二阶段**: 动画效果和毛玻璃
3. **第三阶段**: 响应式设计和优化
4. **第四阶段**: 高级特效和个性化

你的技术栈完全可以实现媲美甚至超越 Paste for Mac 的现代化UI界面！ 