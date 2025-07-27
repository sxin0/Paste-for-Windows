 # Paste for Windows

一个功能强大的Windows剪贴板管理器，灵感来源于macOS的Paste应用。自动监听剪贴板变化，智能管理历史记录，让您的工作更加高效。

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%2011-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## ✨ 主要特性

- 🔄 **自动监听剪贴板变化** - 实时捕获并保存剪贴板内容
- 📝 **多格式支持** - 支持文本、图片、文件路径等多种格式
- 🔍 **智能搜索** - 快速查找历史记录中的内容
- ⭐ **收藏功能** - 标记重要内容，永久保存
- 💾 **数据持久化** - 使用SQLite数据库安全存储历史记录
- 🎯 **全局快捷键** - `Ctrl+Shift+V` 快速呼出主窗口
- 🔔 **系统托盘集成** - 最小化到系统托盘，不占用任务栏空间
- 🚀 **开机自启动** - 可选择开机自动启动，无需手动启动
- 🎨 **现代化界面** - 简洁美观的用户界面，操作直观
- 📊 **统计信息** - 详细的使用统计和数据分析

## 🖼️ 界面预览

### 主界面
- 左侧：剪贴板历史列表，显示时间、类型和内容预览
- 右侧：详细信息面板，显示完整内容和元数据
- 顶部：搜索框，支持实时搜索过滤

### 系统托盘
- 显示主窗口
- 快速设置
- 统计信息
- 导出历史记录
- 退出程序

## 🚀 快速开始

### 系统要求

- Windows 10/11
- Python 3.7 或更高版本
- 4GB 内存（推荐）
- 100MB 可用磁盘空间

### 自动安装（推荐）

1. 下载项目文件到本地目录
2. 运行安装脚本：
   ```bash
   python install.py
   ```
3. 安装脚本会自动：
   - 检查Python版本
   - 安装所需依赖
   - 创建桌面快捷方式
   - 创建开始菜单项
   - 设置开机自启动

### 手动安装

1. 克隆或下载项目：
   ```bash
   git clone https://github.com/your-username/paste-for-windows.git
   cd paste-for-windows
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行程序：
   ```bash
   python main.py
   ```

## 📖 使用说明

### 基本操作

1. **启动程序**
   - 双击桌面快捷方式
   - 或运行 `python main.py`

2. **快捷键**
   - `Ctrl+Shift+V`: 打开/关闭主窗口
   - `F5`: 刷新历史记录
   - `Delete`: 删除选中项目
   - `Ctrl+C`: 复制选中项目到剪贴板

3. **基本操作**
   - 双击列表项：复制到剪贴板
   - 右键菜单：复制、收藏、删除
   - 搜索框：输入关键词实时搜索

### 高级功能

#### 内容类型识别
- 📝 **文本内容**：自动识别URL、邮箱、电话号码
- 🖼️ **图片内容**：支持剪贴板中的图片
- 📁 **文件路径**：复制文件时自动记录路径

#### 搜索和过滤
- 支持内容搜索
- 按类型过滤
- 收藏项目筛选

#### 数据管理
- 历史记录自动清理
- 支持导出为JSON或TXT格式
- 数据备份和恢复

## ⚙️ 配置选项

程序支持多种配置选项，可通过设置窗口修改：

### 常规设置
- **最大历史项目数**：控制保存的历史记录数量（默认100）
- **开机自启动**：是否随系统启动（默认开启）
- **显示通知**：是否显示系统通知（默认开启）
- **全局快捷键**：自定义快捷键组合（默认Ctrl+Shift+V）

### 剪贴板设置
- **监听间隔**：剪贴板检查频率（默认0.5秒）
- **保存图片**：是否保存图片内容（默认开启）
- **保存文件路径**：是否保存文件路径（默认开启）
- **最大文本长度**：单个文本项目的最大长度（默认10000字符）

### 外观设置
- **主题**：浅色/深色主题
- **窗口大小**：自定义窗口尺寸

配置文件位置：`%USERPROFILE%\.clipboardmanager\config.ini`

## 🗂️ 项目结构

```
paste-for-windows/
├── main.py              # 主程序入口
├── gui.py               # GUI界面模块
├── clipboard_manager.py # 剪贴板管理核心
├── database.py          # 数据库操作
├── utils.py             # 工具函数
├── config.py            # 配置管理
├── install.py           # 安装脚本
├── requirements.txt     # Python依赖
├── README.md            # 项目说明
└── clipboard.ico        # 应用程序图标
```

## 🔧 开发说明

### 核心模块说明

- **main.py**: 应用程序入口，负责初始化和协调各个模块
- **clipboard_manager.py**: 剪贴板监听和内容处理的核心逻辑
- **database.py**: SQLite数据库操作，负责数据持久化
- **gui.py**: Tkinter图形界面，包含主窗口和设置窗口
- **utils.py**: 工具类，包含系统托盘、热键管理、自启动等功能
- **config.py**: 配置文件管理

### 添加新功能

1. 在相应模块中添加功能函数
2. 在GUI中添加对应的界面元素
3. 在配置文件中添加相关设置项
4. 更新数据库结构（如需要）

### 打包为可执行文件

使用PyInstaller打包：

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=clipboard.ico main.py
```

## 🚨 常见问题

### Q: 程序启动后没有反应
A: 检查系统托盘，程序可能已最小化到托盘。使用快捷键Ctrl+Shift+V可以呼出主窗口。

### Q: 快捷键不起作用
A: 
1. 检查是否有其他程序占用了相同快捷键
2. 尝试以管理员权限运行程序
3. 在设置中更换快捷键组合

### Q: 剪贴板内容没有被自动记录
A: 
1. 确认程序正在运行（检查系统托盘）
2. 检查设置中的监听间隔配置
3. 重启程序尝试

### Q: 数据库文件在哪里？
A: 数据库和配置文件保存在 `%USERPROFILE%\.clipboardmanager\` 目录下。

### Q: 如何备份数据？
A: 可以通过以下方式备份：
1. 使用程序内的导出功能
2. 直接复制 `%USERPROFILE%\.clipboardmanager\` 目录

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork本项目
2. 创建feature分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 提交Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢macOS Paste应用的设计灵感
- 感谢所有开源库的贡献者
- 感谢Python社区的支持

## 📞 联系方式

如果您有任何问题或建议，请通过以下方式联系：

- 提交Issue：[GitHub Issues](https://github.com/your-username/paste-for-windows/issues)
- 邮箱：your-email@example.com

---

**享受高效的剪贴板管理体验！** 🚀