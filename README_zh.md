# MarkItDown - 中文README

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/markitdown.svg)](https://pypi.org/project/markitdown/)
![PyPI - Downloads](https://img.shields.io/pypi/dd/markitdown)
[![Built by AutoGen Team](https://img.shields.io/badge/Built%20by-AutoGen%20Team-blue)](https://github.com/microsoft/autogen)

**将各种文档格式转换为 Markdown 的轻量级 Python 工具**

</div>

---

## ⚠️ 重要安全提示

> MarkItDown 执行 I/O 操作时具有当前进程的权限。类似于 `open()` 或 `requests.get()`，它将访问进程本身可以访问的资源。
>
> **请在不受信任的环境中对输入进行消毒处理，并调用最窄的 `convert_*` 函数以满足您的使用场景（例如 `convert_stream()` 或 `convert_local()`）。**

详见 [安全考虑](#安全考虑) 部分。

---

## 简介

MarkItDown 是微软开源的轻量级 Python 工具，用于将各种文件格式转换为 Markdown，专为与大语言模型（LLM）和相关文本分析管道配合使用而设计。

### 为什么选择 Markdown？

Markdown 极其接近纯文本，标记最少，但仍能表示重要的文档结构。主流 LLM（如 OpenAI 的 GPT-4o）原生"理解"Markdown，并且经常在回复中不加提示地使用 Markdown。这表明它们在大量 Markdown 格式的文本上进行了训练，并且理解得很好。此外，Markdown 约定也是高度 token 高效的。

### 支持的格式

MarkItDown 目前支持从以下格式转换：

| 类别 | 支持的格式 |
|------|-----------|
| **办公文档** | PDF, Word (DOCX), PowerPoint (PPTX), Excel (XLSX/XLS) |
| **网页** | HTML, Wikipedia, YouTube (字幕), Bing 搜索结果 |
| **媒体** | 图片 (EXIF 元数据 + OCR), 音频 (EXIF 元数据 + 语音转录) |
| **文本格式** | CSV, JSON, XML, Jupyter Notebook (IPYNB) |
| **其他** | ZIP 文件 (遍历内容), EPUB 电子书, Outlook 消息 (MSG), RSS 订阅 |

---

## 前置要求

MarkItDown 需要 Python 3.10 或更高版本。建议使用虚拟环境以避免依赖冲突。

### 创建虚拟环境

**标准 Python 安装：**
```bash
python -m venv .venv
source .venv/bin/activate
```

**使用 uv：**
```bash
uv venv --python=3.12 .venv
source .venv/bin/activate
# 注意：在此虚拟环境中安装包时请使用 'uv pip install' 而非 'pip install'
```

**使用 Anaconda：**
```bash
conda create -n markitdown python=3.12
conda activate markitdown
```

---

## 安装

### 从 PyPI 安装

安装所有可选依赖（推荐）：
```bash
pip install 'markitdown[all]'
```

或仅安装特定格式的依赖：
```bash
pip install 'markitdown[pdf, docx, pptx]'
```

### 从源码安装

```bash
git clone git@github.com:microsoft/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[all]'
```

---

## 使用方法

### 命令行使用

#### 基本转换

```bash
# 转换文件并输出到 stdout
markitdown path-to-file.pdf

# 转换文件并保存到指定文件
markitdown path-to-file.pdf -o document.md

# 使用重定向
markitdown path-to-file.pdf > document.md

# 从 stdin 读取
cat path-to-file.pdf | markitdown
```

#### 命令行选项

```bash
# 查看版本
markitdown --version

# 查看帮助
markitdown --help

# 提供文件扩展名提示（当从 stdin 读取时）
markitdown --extension .pdf

# 提供 MIME 类型提示
markitdown --mime-type "application/pdf"

# 提供字符编码提示
markitdown --charset UTF-8

# 保留 data URI（如 base64 编码的图片）
markitdown --keep-data-uris path-to-file.docx
```

#### 使用 Azure 文档智能

```bash
# 使用 Azure Document Intelligence 进行更精确的转换
markitdown path-to-file.pdf -o document.md -d -e "<document_intelligence_endpoint>"
```

#### 插件管理

```bash
# 列出已安装的插件
markitdown --list-plugins

# 使用插件进行转换
markitdown --use-plugins path-to-file.pdf
```

### Python API 使用

#### 基本用法

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)  # 设置为 True 以启用插件
result = md.convert("test.xlsx")
print(result.text_content)
```

#### 转换结果对象

```python
result = md.convert("document.pdf")

# 获取转换后的 Markdown 内容
print(result.markdown)       # 推荐使用
print(result.text_content)   # 已弃用的别名

# 获取文档标题（如果有）
print(result.title)
```

#### 多种输入源

```python
from markitdown import MarkItDown, StreamInfo
import io
import requests

md = MarkItDown()

# 1. 本地文件路径
result = md.convert("/path/to/document.pdf")
result = md.convert_local("/path/to/document.pdf")

# 2. URL
result = md.convert("https://example.com/document.pdf")
result = md.convert_uri("https://example.com/document.pdf")

# 3. 文件 URI
result = md.convert("file:///path/to/document.pdf")

# 4. Data URI
data_uri = "data:text/plain;base64,SGVsbG8sIFdvcmxkIQ=="
result = md.convert(data_uri)

# 5. requests.Response 对象
response = requests.get("https://example.com/document.pdf")
result = md.convert(response)
result = md.convert_response(response)

# 6. 二进制流
with open("document.pdf", "rb") as f:
    result = md.convert_stream(f)
    
# 或使用 BytesIO
pdf_data = io.BytesIO(...)
result = md.convert_stream(
    pdf_data,
    stream_info=StreamInfo(extension=".pdf")
)
```

#### 使用 LLM 进行图像描述

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(
    llm_client=client,
    llm_model="gpt-4o",
    llm_prompt="自定义提示词（可选）"
)

# 转换包含图片的文件，LLM 将生成图片描述
result = md.convert("example.pptx")
print(result.text_content)

# 转换图片文件
result = md.convert("example.jpg")
print(result.text_content)
```

#### 使用 Azure 文档智能

```python
from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
result = md.convert("test.pdf")
print(result.text_content)
```

---

## 可选依赖详解

MarkItDown 使用可选依赖来激活各种文件格式支持。

### 可用的依赖组

| 依赖组 | 包含的功能 |
|--------|-----------|
| `[all]` | 所有可选依赖（推荐） |
| `[pptx]` | PowerPoint 文件支持 |
| `[docx]` | Word 文件支持 |
| `[xlsx]` | Excel 2007+ 文件支持 |
| `[xls]` | 旧版 Excel 文件支持 |
| `[pdf]` | PDF 文件支持 |
| `[outlook]` | Outlook 消息 (.msg) 支持 |
| `[audio-transcription]` | WAV/MP3 音频转录 |
| `[youtube-transcription]` | YouTube 字幕获取 |
| `[az-doc-intel]` | Azure 文档智能支持 |

### 安装示例

```bash
# 仅安装 PDF 和 Word 支持
pip install 'markitdown[pdf, docx]'

# 安装所有依赖
pip install 'markitdown[all]'
```

---

## 插件系统

### 什么是插件

MarkItDown 支持第三方插件扩展其功能。插件通过 Python 的 `entry_points` 机制自动发现。

### markitdown-ocr 插件

`markitdown-ocr` 插件为 PDF、DOCX、PPTX 和 XLSX 转换器添加 OCR 支持，使用 LLM Vision 从嵌入图片中提取文本。

#### 安装

```bash
pip install markitdown-ocr
pip install openai  # 或任何 OpenAI 兼容的客户端
```

#### 使用

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(
    enable_plugins=True,
    llm_client=OpenAI(),
    llm_model="gpt-4o",
)
result = md.convert("document_with_images.pdf")
print(result.text_content)
```

> 如果未提供 `llm_client`，插件仍会加载，但 OCR 会被静默跳过，转而使用标准的内置转换器。

### 查找和开发插件

- 在 GitHub 上搜索标签 `#markitdown-plugin` 查找可用插件
- 参考 `packages/markitdown-sample-plugin` 开发自己的插件

---

## Docker 使用

### 构建镜像

```bash
docker build -t markitdown:latest .
```

### 运行容器

```bash
# 转换本地文件
docker run --rm -i markitdown:latest < ~/your-file.pdf > output.md
```

---

## 安全考虑

### 输入消毒

**不要直接将不受信任的输入传递给 MarkItDown。** 如果输入的任何部分可能由不受信任的用户或系统控制（例如在托管或服务器端应用程序中），则必须在调用 MarkItDown 之前对其进行验证和限制。

根据您的环境，这可能包括：
- 限制文件路径范围
- 限制 URI 方案和网络目标
- 阻止访问私有、回环、链路本地或元数据服务地址

### 使用合适的 API

优先选择最符合您使用场景的狭窄转换 API：

| API | 用途 | 安全性 |
|-----|------|--------|
| `convert()` | 最宽泛，接受本地文件、远程 URL、流 | ⚠️ 最宽泛 |
| `convert_local()` | 仅本地文件 | ⚠️ 仍需路径验证 |
| `convert_stream()` | 仅二进制流 | ✅ 最可控 |
| `convert_response()` | 仅 requests.Response | ✅ 您控制请求 |

**示例：**
```python
# ❌ 危险：用户输入可能是恶意路径或 URL
md = MarkItDown()
result = md.convert(user_input)

# ✅ 安全：使用狭窄的 API 并自己控制获取
import requests

# 对于 HTTP 资源
response = requests.get(
    url,
    timeout=10,
    allow_redirects=False  # 控制重定向
)
result = md.convert_response(response)

# 对于本地文件（先验证路径）
import os

# 确保路径在允许的目录内
allowed_dir = "/allowed/directory"
full_path = os.path.abspath(os.path.join(allowed_dir, user_input))

if not full_path.startswith(allowed_dir):
    raise ValueError("Invalid path")

result = md.convert_local(full_path)
```

---

## 故障排除

### 常见问题

**Q: 转换 PDF 时出现 `MissingDependencyException`？**

A: 确保安装了 PDF 依赖：
```bash
pip install 'markitdown[pdf]'
# 或
pip install 'markitdown[all]'
```

**Q: 转换 DOCX 时数学公式不显示？**

A: MarkItDown 支持将 OMML（Office Math Markup Language）转换为 LaTeX 格式。确保安装了完整依赖：
```bash
pip install 'markitdown[docx]'
```

**Q: 如何处理深度嵌套的 HTML？**

A: MarkItDown 会自动处理。当 HTML 嵌套过深导致 `RecursionError` 时，它会回退到纯文本提取模式，并发出警告。

**Q: 如何保留图片的 base64 编码？**

A: 使用 `keep_data_uris=True` 参数：
```python
# Python API
result = md.convert("document.docx", keep_data_uris=True)

# 命令行
markitdown --keep-data-uris document.docx
```

---

## 项目结构

```
markitdown/
├── packages/
│   ├── markitdown/              # 核心包
│   │   ├── src/markitdown/
│   │   │   ├── _markitdown.py   # 核心 MarkItDown 类
│   │   │   ├── _base_converter.py  # 转换器基类
│   │   │   ├── converters/      # 各种格式转换器
│   │   │   └── ...
│   │   └── tests/               # 测试文件
│   ├── markitdown-ocr/          # OCR 插件
│   ├── markitdown-sample-plugin/ # 示例插件
│   └── markitdown-mcp/          # MCP 支持
└── README.md
```

---

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 商标

本项目可能包含项目、产品或服务的商标或徽标。Microsoft 商标或徽标的授权使用必须遵守 [Microsoft 商标和品牌指南](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general)。使用第三方商标或徽标需遵守这些第三方的政策。
