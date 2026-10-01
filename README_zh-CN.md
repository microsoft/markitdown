# MarkItDown

[![PyPI](https://img.shields.io/pypi/v/markitdown.svg)](https://pypi.org/project/markitdown/)
![PyPI - Downloads](https://img.shields.io/pypi/dd/markitdown)
[![Built by AutoGen Team](https://img.shields.io/badge/Built%20by-AutoGen%20Team-blue)](https://github.com/microsoft/autogen)

> ⚠️ **重要提示**
> 
> MarkItDown 以当前进程的权限执行 I/O 操作。与 `open()` 或 `requests.get()` 类似，它会访问进程本身能够访问的资源。在不受信任的环境中使用时，请务必对输入进行安全清理，并根据您的使用场景调用最窄范围的 `convert_*` 函数（例如 `convert_stream()` 或 `convert_local()`）。更多信息请参阅[安全考虑](#安全考虑)部分。

## 项目简介

MarkItDown 是一个轻量级的 Python 工具，用于将各种文件格式转换为 Markdown，适用于大语言模型（LLM）和相关文本分析管道。

与 [textract](https://github.com/deanmalmgren/textract) 等工具相比，MarkItDown 更专注于保留重要的文档结构和内容为 Markdown 格式（包括：标题、列表、表格、链接等）。虽然输出通常具有良好的可读性且对人类友好，但它主要是为文本分析工具设计的 —— 对于需要高保真文档转换供人类阅读的场景，可能不是最佳选择。

## 为什么选择 Markdown？

Markdown 非常接近纯文本，只有最少的标记或格式，但仍然提供了一种表示重要文档结构的方式。主流的大语言模型，如 OpenAI 的 GPT-4o，原生"理解"Markdown，并且经常在未提示的情况下在响应中使用 Markdown。这表明它们在大量 Markdown 格式的文本上进行了训练，并且理解得很好。作为附带好处，Markdown 约定在 token 效率方面也非常高。

## 支持的格式

MarkItDown 目前支持从以下格式转换：

| 类别 | 格式 |
|------|------|
| 文档格式 | PDF, Word (DOCX), Excel (XLSX/XLS), PowerPoint (PPTX), EPUB |
| 网页格式 | HTML, Wikipedia, YouTube, Bing 搜索结果, RSS |
| 媒体格式 | 图片 (EXIF元数据+OCR), 音频 (EXIF元数据+语音转录) |
| 其他格式 | ZIP, CSV, JSON, XML, Jupyter Notebook, Outlook 消息 |
| 云端服务 | Azure Document Intelligence |

## 环境要求

MarkItDown 需要 Python 3.10 或更高版本。建议使用虚拟环境以避免依赖冲突。

### 使用标准 Python 创建虚拟环境

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

### 使用 uv 创建虚拟环境

```bash
uv venv --python=3.12 .venv
source .venv/bin/activate
# 注意：请使用 'uv pip install' 而不是直接使用 'pip install'
```

### 使用 Anaconda 创建虚拟环境

```bash
conda create -n markitdown python=3.12
conda activate markitdown
```

## 安装

### 从 PyPI 安装（推荐）

安装所有可选依赖（推荐）：

```bash
pip install 'markitdown[all]'
```

或者，从源码安装：

```bash
git clone git@github.com:microsoft/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[all]'
```

### 可选依赖分组

您可以根据需要选择性地安装依赖：

```bash
pip install 'markitdown[pdf, docx, pptx]'
```

可用的可选依赖分组：

| 分组 | 支持的格式 |
|------|-----------|
| `[all]` | 所有可选依赖（推荐） |
| `[pptx]` | PowerPoint 文件 |
| `[docx]` | Word 文件 |
| `[xlsx]` | Excel 文件 |
| `[xls]` | 旧版 Excel 文件 |
| `[pdf]` | PDF 文件 |
| `[outlook]` | Outlook 消息 |
| `[az-doc-intel]` | Azure Document Intelligence |
| `[audio-transcription]` | WAV 和 MP3 音频转录 |
| `[youtube-transcription]` | YouTube 视频字幕获取 |

## 使用方法

### 命令行使用

#### 基础转换

将文件转换为 Markdown 并输出到标准输出：

```bash
markitdown path-to-file.pdf
```

保存到文件（方式一）：

```bash
markitdown path-to-file.pdf > document.md
```

保存到文件（方式二）：

```bash
markitdown path-to-file.pdf -o document.md
```

#### 从标准输入读取

```bash
cat path-to-file.pdf | markitdown
```

或

```bash
markitdown < path-to-file.pdf
```

#### 提供文件类型提示

当从标准输入读取或文件扩展名不明确时，可以提供类型提示：

```bash
# 提供扩展名提示
markitdown -x .pdf

# 提供 MIME 类型提示
markitdown -m application/pdf

# 提供编码提示
markitdown -c utf-8
```

#### 使用插件

MarkItDown 支持第三方插件。插件默认禁用。

列出已安装的插件：

```bash
markitdown --list-plugins
```

启用插件进行转换：

```bash
markitdown --use-plugins path-to-file.pdf
```

要查找可用的插件，请在 GitHub 上搜索话题标签 `#markitdown-plugin`。

#### MarkItDown OCR 插件

`markitdown-ocr` 插件为 PDF、DOCX、PPTX 和 XLSX 转换器添加 OCR 支持，使用 LLM Vision 从嵌入的图像中提取文本 —— 使用与 MarkItDown 用于图像描述相同的 `llm_client` / `llm_model` 模式，无需新的 ML 库或二进制依赖。

**安装：**

```bash
pip install markitdown-ocr
pip install openai  # 或任何 OpenAI 兼容客户端
```

**命令行使用：**

```bash
markitdown document.pdf --use-plugins
```

**Python 使用：**

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

如果没有提供 `llm_client`，插件仍然会加载，但 OCR 会被静默跳过，转而使用标准的内置转换器。

更多详细信息请参阅 [`packages/markitdown-ocr/README.md`](packages/markitdown-ocr/README.md)。

#### 使用 Azure Document Intelligence

使用 Microsoft Document Intelligence 进行转换：

```bash
markitdown path-to-file.pdf -o document.md -d -e "<document_intelligence_endpoint>"
```

有关如何设置 Azure Document Intelligence 资源的更多信息，请参阅[官方文档](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/create-document-intelligence-resource?view=doc-intel-4.0.0)。

### Python API 使用

#### 基础用法

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)  # 设置为 True 以启用插件
result = md.convert("test.xlsx")
print(result.text_content)
```

#### 使用 Document Intelligence

```python
from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
result = md.convert("test.pdf")
print(result.text_content)
```

#### 使用大语言模型进行图像描述

要使用大语言模型进行图像描述（目前仅适用于 pptx 和图像文件），请提供 `llm_client` 和 `llm_model`：

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(
    llm_client=client, 
    llm_model="gpt-4o", 
    llm_prompt="可选的自定义提示词"
)
result = md.convert("example.jpg")
print(result.text_content)
```

#### 多种输入源

MarkItDown 支持多种输入源：

```python
from markitdown import MarkItDown
from pathlib import Path
import requests

md = MarkItDown()

# 本地文件路径 (字符串)
result = md.convert("/path/to/file.pdf")

# 本地文件路径 (Path 对象)
result = md.convert(Path("/path/to/file.pdf"))

# URL
result = md.convert("https://example.com/document.pdf")

# requests.Response 对象
response = requests.get("https://example.com/document.pdf")
result = md.convert(response)

# 二进制流
with open("/path/to/file.pdf", "rb") as f:
    result = md.convert(f)
```

#### 使用窄范围 API 进行更好的安全控制

```python
from markitdown import MarkItDown

md = MarkItDown()

# 只处理本地文件 (不处理 URL)
result = md.convert_local("/path/to/file.pdf")

# 只处理流
with open("/path/to/file.pdf", "rb") as f:
    result = md.convert_stream(f)

# 只处理 URI
result = md.convert_uri("https://example.com/document.pdf")
```

### Docker 使用

```sh
docker build -t markitdown:latest .
docker run --rm -i markitdown:latest < ~/your-file.pdf > output.md
```

## 安全考虑

MarkItDown 以当前进程的权限执行 I/O 操作。与 `open()` 或 `requests.get()` 类似，它会访问进程本身能够访问的资源。

### 输入安全

**清理您的输入：** 不要将不受信任的输入直接传递给 MarkItDown。如果输入的任何部分可能由不受信任的用户或系统控制（例如在托管或服务器端应用程序中），则必须在调用 MarkItDown 之前对其进行验证和限制。根据您的环境，这可能包括：
- 限制文件路径
- 限制 URI 方案和网络目标
- 阻止访问私有、回环、链路本地或元数据服务地址

### API 选择

**只调用您需要的转换方法：** 优先选择最适合您用例的最窄范围转换 API。

| API | 访问能力 | 推荐场景 |
|-----|----------|----------|
| `convert()` | 本地文件 + URL + 流 | 通用场景（最宽松） |
| `convert_local()` | 仅本地文件 | 只需要读取本地文件 |
| `convert_stream()` | 仅已打开的流 | 完全控制的场景 |
| `convert_response()` | 仅 requests.Response | 自己管理 HTTP 获取 |
| `convert_uri()` | URI 解析 | 需要 URI 处理时 |

## 贡献

本项目欢迎贡献和建议。大多数贡献要求您同意贡献者许可协议 (CLA)，声明您有权并实际授予我们使用您的贡献的权利。有关详细信息，请访问 https://cla.opensource.microsoft.com。

当您提交拉取请求时，CLA 机器人将自动确定您是否需要提供 CLA 并适当装饰 PR（例如状态检查、评论）。只需按照机器人提供的说明操作。您只需在使用我们的 CLA 的所有存储库中执行一次此操作。

本项目采用了 [Microsoft 开源行为准则](https://opensource.microsoft.com/codeofconduct/)。有关更多信息，请参阅[行为准则常见问题解答](https://opensource.microsoft.com/codeofconduct/faq/)，或联系 [opencode@microsoft.com](mailto:opencode@microsoft.com) 提出任何其他问题或意见。

### 如何贡献

您可以通过查看问题或帮助审查 PR 来提供帮助。任何问题或 PR 都是欢迎的，但我们也标记了一些为"open for contribution"和"open for reviewing"，以帮助促进社区贡献。这些当然只是建议，欢迎您以任何您喜欢的方式贡献。

| | 全部 | 特别需要社区帮助 |
|--|------|-----------------|
| **问题** | [所有问题](https://github.com/microsoft/markitdown/issues) | [开放贡献的问题](https://github.com/microsoft/markitdown/issues?q=is%3Aissue+is%3Aopen+label%3A%22open+for+contribution%22) |
| **PRs** | [所有 PR](https://github.com/microsoft/markitdown/pulls) | [开放审查的 PR](https://github.com/microsoft/markitdown/pulls?q=is%3Apr+is%3Aopen+label%3A%22open+for+reviewing%22) |

### 运行测试和检查

1. 导航到 MarkItDown 包目录：

```sh
cd packages/markitdown
```

2. 在您的环境中安装 `hatch` 并运行测试：

```sh
pip install hatch  # 其他安装 hatch 的方式：https://hatch.pypa.io/dev/install/
hatch shell
hatch test
```

或者使用 Devcontainer（已安装所有依赖）：

```sh
# 在 Devcontainer 中重新打开项目并运行：
hatch test
```

3. 在提交 PR 之前运行 pre-commit 检查：

```sh
pre-commit run --all-files
```

### 贡献第三方插件

您还可以通过创建和共享第三方插件来贡献。有关更多详细信息，请参阅 `packages/markitdown-sample-plugin`。

## 商标

本项目可能包含项目、产品或服务的商标或徽标。授权使用 Microsoft 商标或徽标必须遵守 [Microsoft 商标和品牌指南](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general)。在修改本项目中使用 Microsoft 商标或徽标时，不得引起混淆或暗示 Microsoft 赞助。任何第三方商标或徽标的使用均受这些第三方的政策约束。

## 许可证

本项目采用 MIT 许可证。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。
