# Paste for Windows - 技术架构文档

## 🏗️ 整体架构

### 架构概览
```
┌─────────────────────────────────────────────────────────────┐
│                    Paste for Windows                        │
├─────────────────────────────────────────────────────────────┤
│  🎨 表示层 (Presentation Layer)                            │
│  ├── GUI 界面 (PyQt6)                                      │
│  ├── 系统托盘 (System Tray)                                │
│  └── 全局热键 (Global Hotkeys)                             │
├─────────────────────────────────────────────────────────────┤
│  🧠 业务逻辑层 (Business Logic Layer)                      │
│  ├── 剪贴板管理器 (Clipboard Manager)                      │
│  ├── 数据处理器 (Data Processor)                           │
│  ├── 搜索引擎 (Search Engine)                              │
│  └── 配置管理器 (Config Manager)                           │
├─────────────────────────────────────────────────────────────┤
│  💾 数据访问层 (Data Access Layer)                         │
│  ├── SQLite 数据库                                         │
│  ├── 文件系统操作                                          │
│  └── 缓存管理                                              │
├─────────────────────────────────────────────────────────────┤
│  🔧 系统服务层 (System Service Layer)                      │
│  ├── Windows API 集成                                      │
│  ├── 系统通知                                              │
│  └── 权限管理                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📁 项目结构

```
paste-for-windows/
├── 📁 src/                          # 源代码目录
│   ├── 📁 core/                     # 核心模块
│   │   ├── __init__.py
│   │   ├── clipboard_manager.py     # 剪贴板管理核心
│   │   ├── data_processor.py        # 数据处理器
│   │   ├── search_engine.py         # 搜索引擎
│   │   └── config_manager.py        # 配置管理
│   ├── 📁 gui/                      # 图形界面
│   │   ├── __init__.py
│   │   ├── main_window.py           # 主窗口
│   │   ├── clipboard_list.py        # 剪贴板列表组件
│   │   ├── preview_panel.py         # 预览面板
│   │   ├── settings_dialog.py       # 设置对话框
│   │   ├── system_tray.py           # 系统托盘
│   │   └── styles/                  # 样式文件
│   │       ├── dark_theme.qss
│   │       └── light_theme.qss
│   ├── 📁 data/                     # 数据层
│   │   ├── __init__.py
│   │   ├── database.py              # 数据库操作
│   │   ├── models.py                # 数据模型
│   │   └── cache_manager.py         # 缓存管理
│   ├── 📁 utils/                    # 工具类
│   │   ├── __init__.py
│   │   ├── hotkey_manager.py        # 热键管理
│   │   ├── file_utils.py            # 文件工具
│   │   ├── image_utils.py           # 图像处理
│   │   └── system_utils.py          # 系统工具
│   └── 📁 services/                 # 服务层
│       ├── __init__.py
│       ├── windows_api.py           # Windows API 封装
│       ├── notification_service.py  # 通知服务
│       └── sync_service.py          # 同步服务
├── 📁 resources/                    # 资源文件
│   ├── 📁 icons/                    # 图标文件
│   ├── 📁 images/                   # 图片资源
│   └── 📁 locales/                  # 多语言文件
├── 📁 tests/                        # 测试文件
│   ├── 📁 unit/                     # 单元测试
│   ├── 📁 integration/              # 集成测试
│   └── 📁 fixtures/                 # 测试数据
├── 📁 docs/                         # 文档
│   ├── API.md                       # API 文档
│   ├── DEPLOYMENT.md                # 部署文档
│   └── CONTRIBUTING.md              # 贡献指南
├── 📁 scripts/                      # 脚本文件
│   ├── build.py                     # 构建脚本
│   ├── install.py                   # 安装脚本
│   └── deploy.py                    # 部署脚本
├── main.py                          # 程序入口
├── requirements.txt                 # 依赖列表
├── setup.py                         # 安装配置
├── pyproject.toml                   # 项目配置
└── README.md                        # 项目说明
```

## 🔧 技术栈选择

### 核心框架
- **Python 3.9+**: 主要开发语言
- **PyQt6**: GUI 框架，提供现代化界面
- **SQLite**: 轻量级数据库，本地存储
- **asyncio**: 异步编程，提高性能

### 关键依赖
```python
# GUI 框架
PyQt6>=6.4.0              # 现代化 GUI 框架
PyQt6-Qt6>=6.4.0          # Qt6 核心库

# 系统集成
pywin32>=305              # Windows API 访问
keyboard>=0.13.5          # 全局热键支持
pystray>=0.19.4           # 系统托盘支持

# 数据处理
pillow>=9.5.0             # 图像处理
python-magic>=0.4.27      # 文件类型检测
chardet>=5.1.0            # 字符编码检测

# 搜索功能
whoosh>=2.7.4             # 全文搜索引擎
jieba>=0.42.1             # 中文分词

# 配置管理
pydantic>=1.10.0          # 数据验证
toml>=0.10.2              # 配置文件格式

# 开发工具
pytest>=7.3.1             # 测试框架
black>=23.3.0             # 代码格式化
mypy>=1.3.0               # 类型检查
```

## 🧠 核心模块设计

### 1. 剪贴板管理器 (ClipboardManager)

```python
class ClipboardManager:
    """剪贴板管理器核心类"""
    
    def __init__(self):
        self._listeners = []
        self._processor = DataProcessor()
        self._running = False
    
    async def start_monitoring(self):
        """开始监听剪贴板变化"""
        
    async def stop_monitoring(self):
        """停止监听"""
        
    def add_listener(self, listener):
        """添加监听器"""
        
    def remove_listener(self, listener):
        """移除监听器"""
        
    async def _monitor_clipboard(self):
        """剪贴板监听循环"""
        
    def _process_clipboard_data(self, data):
        """处理剪贴板数据"""
```

**职责**:
- 实时监听剪贴板变化
- 数据格式识别和处理
- 通知相关组件更新
- 管理监听器生命周期

### 2. 数据处理器 (DataProcessor)

```python
class DataProcessor:
    """数据处理器"""
    
    def process_text(self, text: str) -> ClipboardItem:
        """处理文本数据"""
        
    def process_image(self, image_data: bytes) -> ClipboardItem:
        """处理图片数据"""
        
    def process_files(self, file_paths: List[str]) -> ClipboardItem:
        """处理文件数据"""
        
    def process_html(self, html: str) -> ClipboardItem:
        """处理富文本数据"""
        
    def detect_content_type(self, data) -> ContentType:
        """检测内容类型"""
        
    def generate_preview(self, item: ClipboardItem) -> str:
        """生成预览内容"""
```

**职责**:
- 内容类型自动识别
- 数据格式转换
- 预览内容生成
- 数据清理和优化

### 3. 搜索引擎 (SearchEngine)

```python
class SearchEngine:
    """搜索引擎"""
    
    def __init__(self, index_path: str):
        self._index = self._create_index(index_path)
        
    def search(self, query: str, filters: Dict = None) -> List[ClipboardItem]:
        """执行搜索"""
        
    def index_item(self, item: ClipboardItem):
        """索引项目"""
        
    def remove_from_index(self, item_id: str):
        """从索引中移除"""
        
    def update_index(self, item: ClipboardItem):
        """更新索引"""
        
    def _create_index(self, path: str) -> Index:
        """创建搜索索引"""
```

**职责**:
- 全文搜索
- 模糊匹配
- 搜索结果排序
- 索引管理

### 4. 数据库管理器 (DatabaseManager)

```python
class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._connection = None
        
    async def connect(self):
        """连接数据库"""
        
    async def disconnect(self):
        """断开连接"""
        
    async def save_item(self, item: ClipboardItem) -> str:
        """保存项目"""
        
    async def get_item(self, item_id: str) -> ClipboardItem:
        """获取项目"""
        
    async def get_items(self, limit: int = 100, offset: int = 0) -> List[ClipboardItem]:
        """获取项目列表"""
        
    async def delete_item(self, item_id: str):
        """删除项目"""
        
    async def update_item(self, item: ClipboardItem):
        """更新项目"""
        
    async def search_items(self, query: str) -> List[ClipboardItem]:
        """搜索项目"""
```

**数据库模式**:
```sql
-- 剪贴板项目表
CREATE TABLE clipboard_items (
    id TEXT PRIMARY KEY,
    content_type TEXT NOT NULL,
    content TEXT,
    preview TEXT,
    file_path TEXT,
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    access_count INTEGER DEFAULT 0,
    is_favorite BOOLEAN DEFAULT FALSE,
    tags TEXT,
    metadata TEXT
);

-- 标签表
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    color TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 项目标签关联表
CREATE TABLE item_tags (
    item_id TEXT,
    tag_id INTEGER,
    FOREIGN KEY (item_id) REFERENCES clipboard_items(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id),
    PRIMARY KEY (item_id, tag_id)
);

-- 使用统计表
CREATE TABLE usage_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    copy_count INTEGER DEFAULT 0,
    paste_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🎨 GUI 架构

### 主窗口设计

```python
class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self._clipboard_manager = None
        self._search_engine = None
        self._setup_ui()
        self._setup_connections()
        
    def _setup_ui(self):
        """设置界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QHBoxLayout(central_widget)
        
        # 侧边栏
        self._sidebar = SidebarWidget()
        layout.addWidget(self._sidebar, 1)
        
        # 主内容区域
        main_content = QVBoxLayout()
        
        # 搜索栏
        self._search_bar = SearchBarWidget()
        main_content.addWidget(self._search_bar)
        
        # 剪贴板列表
        self._clipboard_list = ClipboardListWidget()
        main_content.addWidget(self._clipboard_list, 1)
        
        # 预览面板
        self._preview_panel = PreviewPanelWidget()
        main_content.addWidget(self._preview_panel)
        
        layout.addLayout(main_content, 3)
        
    def _setup_connections(self):
        """设置信号连接"""
        self._search_bar.search_requested.connect(self._on_search)
        self._clipboard_list.item_selected.connect(self._on_item_selected)
        self._sidebar.category_changed.connect(self._on_category_changed)
```

### 组件设计

#### 1. 剪贴板列表组件
```python
class ClipboardListWidget(QListWidget):
    """剪贴板列表组件"""
    
    item_selected = pyqtSignal(ClipboardItem)
    item_double_clicked = pyqtSignal(ClipboardItem)
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._setup_context_menu()
        
    def _setup_ui(self):
        """设置界面"""
        self.setAlternatingRowColors(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        
    def _setup_context_menu(self):
        """设置右键菜单"""
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        
    def add_item(self, item: ClipboardItem):
        """添加项目"""
        list_item = ClipboardListItem(item)
        self.addItem(list_item)
        
    def clear_items(self):
        """清空项目"""
        self.clear()
```

#### 2. 预览面板组件
```python
class PreviewPanelWidget(QWidget):
    """预览面板组件"""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        
        # 标题栏
        title_bar = QHBoxLayout()
        self._title_label = QLabel("预览")
        title_bar.addWidget(self._title_label)
        title_bar.addStretch()
        
        # 操作按钮
        self._copy_btn = QPushButton("复制")
        self._favorite_btn = QPushButton("收藏")
        title_bar.addWidget(self._copy_btn)
        title_bar.addWidget(self._favorite_btn)
        
        layout.addLayout(title_bar)
        
        # 预览内容
        self._preview_widget = QStackedWidget()
        self._text_preview = TextPreviewWidget()
        self._image_preview = ImagePreviewWidget()
        self._file_preview = FilePreviewWidget()
        
        self._preview_widget.addWidget(self._text_preview)
        self._preview_widget.addWidget(self._image_preview)
        self._preview_widget.addWidget(self._file_preview)
        
        layout.addWidget(self._preview_widget)
        
    def show_item(self, item: ClipboardItem):
        """显示项目预览"""
        if item.content_type == ContentType.TEXT:
            self._preview_widget.setCurrentWidget(self._text_preview)
            self._text_preview.show_content(item.content)
        elif item.content_type == ContentType.IMAGE:
            self._preview_widget.setCurrentWidget(self._image_preview)
            self._image_preview.show_content(item.file_path)
        elif item.content_type == ContentType.FILE:
            self._preview_widget.setCurrentWidget(self._file_preview)
            self._file_preview.show_content(item.file_path)
```

## 🔄 数据流设计

### 剪贴板数据流
```
用户复制内容
    ↓
Windows 剪贴板
    ↓
ClipboardManager 监听
    ↓
DataProcessor 处理
    ↓
DatabaseManager 存储
    ↓
SearchEngine 索引
    ↓
GUI 更新显示
```

### 搜索数据流
```
用户输入搜索关键词
    ↓
SearchBarWidget 发送信号
    ↓
MainWindow 处理搜索请求
    ↓
SearchEngine 执行搜索
    ↓
DatabaseManager 获取结果
    ↓
ClipboardListWidget 更新显示
```

### 配置数据流
```
用户修改设置
    ↓
SettingsDialog 收集配置
    ↓
ConfigManager 验证和保存
    ↓
配置文件持久化
    ↓
相关组件应用新配置
```

## 🚀 性能优化

### 1. 异步处理
- 使用 `asyncio` 进行异步编程
- 剪贴板监听使用异步循环
- 数据库操作异步化
- GUI 更新使用信号槽机制

### 2. 缓存策略
- 内存缓存常用数据
- 图片缩略图缓存
- 搜索结果缓存
- 配置缓存

### 3. 数据库优化
- 索引优化
- 连接池管理
- 批量操作
- 定期清理

### 4. 内存管理
- 图片数据压缩
- 大文件处理优化
- 垃圾回收优化
- 内存使用监控

## 🔒 安全设计

### 1. 数据安全
- 本地存储，不上传云端
- 敏感数据加密
- 访问权限控制
- 数据备份机制

### 2. 系统安全
- 最小权限原则
- UAC 兼容性
- Windows Defender 认证
- 安全更新机制

### 3. 隐私保护
- 不收集用户隐私数据
- 本地化处理
- 数据清理选项
- 隐私模式支持

## 🧪 测试策略

### 1. 单元测试
- 核心模块测试
- 工具函数测试
- 数据模型测试
- 配置管理测试

### 2. 集成测试
- GUI 组件测试
- 数据库操作测试
- 系统集成测试
- 性能测试

### 3. 端到端测试
- 用户场景测试
- 跨应用测试
- 系统兼容性测试
- 压力测试

## 📦 部署架构

### 1. 开发环境
- Python 虚拟环境
- 开发依赖管理
- 代码质量检查
- 自动化测试

### 2. 构建系统
- PyInstaller 打包
- 依赖自动检测
- 资源文件打包
- 签名和验证

### 3. 分发方式
- Microsoft Store
- 独立安装包
- 便携版
- 包管理器

---

*本文档描述了 Paste for Windows 的完整技术架构，为开发团队提供技术指导。* 