# MarkItDown GUI

一个简单易用的可视化界面，用于将各种文件转换为 Markdown 格式。支持拖拽文件到窗口，自动完成转换并保存为 `.md` 文件。

## 功能特点

- **拖拽转换**: 直接拖拽文件到窗口即可完成转换
- **多格式支持**: PDF, Word, Excel, PowerPoint, HTML, CSV, JSON, XML, TXT, EPUB, ZIP, 图片, 音频等
- **批量转换**: 支持一次性转换多个文件
- **自定义输出**: 可选择输出目录
- **双击打开**: 转换完成后双击可直接打开生成的 Markdown 文件

## 安装

### 1. 克隆项目

```bash
git clone https://github.com/microsoft/markitdown.git
cd markitdown
```

### 2. 安装依赖

```bash
# 使用 pip 安装（推荐）
pip install -e "packages/markitdown[all]"

# 或者从本地安装
pip install -e .
```

### 3. 运行 GUI

```bash
python markitdown_gui.py
```

## 使用方法

1. **启动程序**: 运行 `python markitdown_gui.py`
2. **选择输出目录**: 点击"浏览"按钮选择转换后的 Markdown 文件保存位置
3. **添加文件**: 
   - 拖拽文件到窗口中间的拖拽区域
   - 或点击"选择文件"按钮
4. **开始转换**: 程序会自动开始转换，显示进度和状态
5. **查看结果**: 转换完成后双击结果列表中的文件可直接打开

## 支持的文件格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| PDF | .pdf | PDF 文档 |
| Word | .docx, .doc | Word 文档 |
| Excel | .xlsx, .xls | Excel 电子表格 |
| PowerPoint | .pptx, .ppt | 演示文稿 |
| HTML | .html, .htm | 网页 |
| CSV | .csv | 逗号分隔值 |
| JSON | .json | JSON 数据 |
| XML | .xml | XML 数据 |
| TXT | .txt | 纯文本 |
| EPUB | .epub | 电子书 |
| ZIP | .zip | ZIP 压缩包 |
| 图片 | .jpg, .jpeg, .png, .gif, .bmp | 图片（支持 OCR） |
| 音频 | .mp3, .wav | 音频（支持转录） |

## 界面预览

```
┌─────────────────────────────────────────────────────────┐
│  MarkItDown 文件转Markdown                              │
│  支持 PDF, Word, Excel, PPTX, 图片等格式                 │
├─────────────────────────────────────────────────────────┤
│  输出目录: [C:\Users\...\Desktop              ] [浏览] │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐│
│  │                                                     ││
│  │           📁 拖拽文件到这里                         ││
│  │                                                     ││
│  │              或点击选择文件                         ││
│  │                                                     ││
│  └─────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────┤
│  转换状态: [███████░░░░░░░░] 就绪             [清空历史]│
├─────────────────────────────────────────────────────────┤
│  转换结果:                                              │
│  ┌─────────────────┬────────┬────────────────────────┐ │
│  │ 文件名          │ 状态    │ 输出路径                │ │
│  ├─────────────────┼────────┼────────────────────────┤ │
│  │ document.pdf    │ ✓ 成功 │ C:\...\document.md     │ │
│  │ report.docx     │ ✓ 成功 │ C:\...\report.md       │ │
│  └─────────────────┴────────┴────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 常见问题

### 1. 启动时提示 "MarkItDown未正确安装"

请确保已正确安装 markitdown：

```bash
pip install -e "packages/markitdown[all]"
```

### 2. 拖拽功能不工作

- 确保使用 Python 3.10 或更高版本
- 在 Windows 上可能需要以管理员权限运行

### 3. 某些格式无法转换

某些格式需要额外的依赖。例如：

- PDF 转换: `pip install markitdown[pdf]`
- Word 转换: `pip install markitdown[docx]`
- Excel 转换: `pip install markitdown[xlsx]`
- 完整安装: `pip install markitdown[all]`

## 技术栈

- **GUI 框架**: tkinter (Python 内置)
- **核心库**: markitdown
- **Python 版本**: 3.10+

## 许可证

MIT License - 与 MarkItDown 项目相同
