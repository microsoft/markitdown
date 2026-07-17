# MarkItDown

[![PyPI version](https://badge.fury.io/py/markitdown.svg)](https://badge.fury.io/py/markitdown)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/markitdown)](https://pypistats.org/packages/markitdown)
[![GitHub](https://img.shields.io/github/license/microsoft/markitdown)](https://github.com/microsoft/markitdown/blob/main/LICENSE)

**pypi** v0.1.6 下载量受上游服务限制 | 由 AutoGen 团队构建

> [!重要提示]
> MarkItDown 使用当前进程的权限执行 I/O 操作。与 `open()` 或 `requests.get()` 类似，它会访问进程本身能够访问的资源。在不受信任的环境中，请对输入进行安全检查，并尽可能使用范围最窄的 `convert_*` 函数（例如 `convert_stream()` 或 `convert_local()`）。更多信息请参阅文档中的[安全注意事项](#)。

MarkItDown 是一个轻量级的 Python 工具，用于将各种文件转换为 Markdown 格式，以便用于大语言模型（LLM）和相关的文本分析流水线。在这个用途上，它与 `textract` 最为相似，但更侧重于保留重要的文档结构和内容（包括标题、列表、表格、链接等）并以 Markdown 形式输出。虽然输出内容通常具有良好的可读性，但其主要设计目标是供文本分析工具使用——可能不适合需要高保真文档转换以供人直接阅读的场景。

## 支持的格式

MarkItDown 目前支持转换以下格式：

- PDF
- PowerPoint
- Word
- Excel
- 图像（EXIF 元数据和 OCR）
- 音频（EXIF 元数据和语音转录）
- HTML
- 基于文本的格式（CSV、JSON、XML）
- ZIP 文件（遍历其中的内容）
- YouTube 链接
- EPub
- ……更多格式正在持续添加中！

## 为什么选择 Markdown？

Markdown 与纯文本非常接近，只包含最少的标记和格式，同时仍能表达重要的文档结构。主流大语言模型（如 OpenAI 的 GPT-4o）原生支持 Markdown，并且经常在响应中不加提示地使用 Markdown 格式。这表明它们在大量 Markdown 格式的文本上进行了训练，并对其有很好的理解。另一个额外的好处是，Markdown 格式在 Token 效率上也相当高。

## 安装

```bash
pip install markitdown
```

安装所有可选依赖（包括 PDF、PowerPoint、Word、Excel、图像 OCR、语音转录等完整功能）：
```bash
pip install 'markitdown[all]'
```

## 使用示例

### 命令行界面

```bash
markitdown 文档.pdf -o 输出.md
```

### Python API

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("文档.pdf")
print(result.text_content)
```

转换网页内容：
```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("https://example.com")
print(result.text_content)
```

## 安全注意事项

MarkItDown 会以其运行进程的权限执行文件 I/O 操作。处理不受信任的输入时请注意：

- 使用 `convert_stream()` 处理来自不可信来源的字节流
- 不要直接转换来自不受信任来源的任意文件路径
- 注意音频转录会调用语音识别服务，可能存在隐私风险
- 对于生产环境，建议设置超时和资源限制

## 扩展开发

MarkItDown 采用可插拔的转换器架构。要添加对新格式的支持，可以继承 `Converter` 类并注册即可。

## 贡献

欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 致谢

MarkItDown 由 Microsoft AutoGen 团队开发和维护。感谢所有贡献者的支持。