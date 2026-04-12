# MarkItDown

[![PyPI](https://img.shields.io/pypi/v/markitdown.svg)](https://pypi.org/project/markitdown/)
![PyPI - Downloads](https://img.shields.io/pypi/dd/markitdown)
[![Built by AutoGen Team](https://img.shields.io/badge/Built%20by-AutoGen%20Team-blue)](https://github.com/microsoft/autogen)

> [!TIP]
> MarkItDown 现已提供 MCP（Model Context Protocol）服务器，可与 Claude Desktop 等 LLM 应用集成。更多信息请参阅 [markitdown-mcp](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp)。

> [!IMPORTANT]
> 0.0.1 到 0.1.0 之间的破坏性变更：
> * 依赖项现按可选功能组组织（详见下文）。使用 `pip install 'markitdown[all]'` 可获得与旧版兼容的行为。
> * `convert_stream()` 现在需要类二进制文件对象（例如以二进制模式打开的文件，或 `io.BytesIO` 对象）。这与上一版本不兼容：此前也接受类文本文件对象（如 `io.StringIO`）。
> * `DocumentConverter` 类接口已改为从类文件流读取，而非文件路径。*不再创建临时文件*。如果你是插件或自定义 `DocumentConverter` 的维护者，很可能需要更新代码。若仅使用 `MarkItDown` 类或 CLI（如下文示例），通常无需改动。

MarkItDown 是一款轻量级 Python 工具，用于将各类文件转换为 Markdown，供 LLM 及相关文本分析流水线使用。在这方面它与 [textract](https://github.com/deanmalmgren/textract) 较为接近，但更侧重于在 Markdown 中保留重要的文档结构与内容（包括：标题、列表、表格、链接等）。虽然输出通常可读性尚可，但其主要面向文本分析工具消费——未必适合需要高保真、面向人工阅读的文档转换。

MarkItDown 目前支持从以下类型转换：

- PDF
- PowerPoint
- Word
- Excel
- 图片（EXIF 元数据与 OCR）
- 音频（EXIF 元数据与语音转写）
- HTML
- 基于文本的格式（CSV、JSON、XML）
- ZIP 文件（遍历其内容）
- YouTube 链接
- EPub
- ……还有更多！

## 为什么选择 Markdown？

Markdown 非常接近纯文本，标记与格式极少，但仍能表达重要的文档结构。主流 LLM（如 OpenAI 的 GPT-4o）原生「会说」Markdown，且常在未明确要求时就在回复中使用 Markdown。这表明模型在大量 Markdown 文本上接受过训练，理解较好。附带好处是，Markdown 在 token 使用上也较为高效。

## 环境要求

MarkItDown 需要 **Python 3.10 或更高版本**。建议使用虚拟环境以避免依赖冲突。

使用标准 Python 安装时，可用以下命令创建并激活虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate
```

若使用 `uv`，可这样创建虚拟环境：

```bash
uv venv --python=3.12 .venv
source .venv/bin/activate
# 注意：请使用 `uv pip install` 而非单独的 `pip install`，以便将包装入该虚拟环境
```

若使用 Anaconda，可这样创建虚拟环境：

```bash
conda create -n markitdown python=3.12
conda activate markitdown
```

## 安装

使用 pip 安装 MarkItDown：`pip install 'markitdown[all]'`。也可从源码安装：

```bash
git clone git@github.com:microsoft/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[all]'
```

## 用法

### 命令行

```bash
markitdown path-to-file.pdf > document.md
```

或使用 `-o` 指定输出文件：

```bash
markitdown path-to-file.pdf -o document.md
```

也可通过管道传入内容：

```bash
cat path-to-file.pdf | markitdown
```

### 可选依赖

MarkItDown 针对不同文件格式有可选依赖。前文使用 `[all]` 安装了全部可选依赖。你也可以按需单独安装以精细控制。例如：

```bash
pip install 'markitdown[pdf, docx, pptx]'
```

将仅安装 PDF、DOCX、PPTX 所需的依赖。

当前可用的可选依赖包括：

* `[all]` 安装全部可选依赖
* `[pptx]` PowerPoint 文件
* `[docx]` Word 文件
* `[xlsx]` Excel 文件
* `[xls]` 旧版 Excel 文件
* `[pdf]` PDF 文件
* `[outlook]` Outlook 邮件
* `[az-doc-intel]` Azure 文档智能（Document Intelligence）
* `[audio-transcription]` wav、mp3 等音频转写
* `[youtube-transcription]` 获取 YouTube 视频字幕/转写

### 插件

MarkItDown 支持第三方插件。插件默认关闭。列出已安装插件：

```bash
markitdown --list-plugins
```

启用插件：

```bash
markitdown --use-plugins path-to-file.pdf
```

在 GitHub 上搜索话题标签 `#markitdown-plugin` 可发现可用插件。开发插件请参阅 `packages/markitdown-sample-plugin`。

#### markitdown-ocr 插件

`markitdown-ocr` 插件为 PDF、DOCX、PPTX、XLSX 转换器增加 OCR 支持，使用 LLM 视觉能力从嵌入图片中提取文字——与 MarkItDown 用于图片描述的 `llm_client` / `llm_model` 模式相同。无需新增 ML 库或二进制依赖。

**安装：**

```bash
pip install markitdown-ocr
pip install openai  # 或任意兼容 OpenAI API 的客户端
```

**用法：**

传入与图片描述相同的 `llm_client` 和 `llm_model`：

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

若未提供 `llm_client`，插件仍会加载，但会静默跳过 OCR，改用内置标准转换器。

详细文档见 [`packages/markitdown-ocr/README.md`](packages/markitdown-ocr/README.md)。

### Azure 文档智能（Document Intelligence）

使用 Microsoft 文档智能进行转换：

```bash
markitdown path-to-file.pdf -o document.md -d -e "<document_intelligence_endpoint>"
```

如何创建 Azure 文档智能资源，请参阅[此处](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/create-document-intelligence-resource?view=doc-intel-4.0.0)。

### Python API

基本用法：

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False) # 设为 True 以启用插件
result = md.convert("test.xlsx")
print(result.text_content)
```

在 Python 中使用文档智能转换：

```python
from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
result = md.convert("test.pdf")
print(result.text_content)
```

若要对图片生成描述使用大语言模型（目前仅支持 pptx 与图片文件），请提供 `llm_client` 与 `llm_model`：

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(llm_client=client, llm_model="gpt-4o", llm_prompt="optional custom prompt")
result = md.convert("example.jpg")
print(result.text_content)
```

### Docker

```sh
docker build -t markitdown:latest .
docker run --rm -i markitdown:latest < ~/your-file.pdf > output.md
```

## 参与贡献

欢迎提交贡献与建议。多数贡献需要签署贡献者许可协议（CLA），声明你有权且确实授予我们使用你贡献的权利。详情请访问 https://cla.opensource.microsoft.com。

提交拉取请求时，CLA 机器人会自动判断你是否需要签署 CLA，并为 PR 添加相应标记（如状态检查、评论）。按机器人说明操作即可。在我们使用同一 CLA 的所有仓库中，你只需签署一次。

本项目采用 [Microsoft 开源行为准则](https://opensource.microsoft.com/codeofconduct/)。更多信息见[行为准则常见问题](https://opensource.microsoft.com/codeofconduct/faq/)，或发邮件至 [opencode@microsoft.com](mailto:opencode@microsoft.com) 咨询。

### 如何参与

你可以通过查看 issue、协助评审 PR 等方式参与。任何 issue 或 PR 都欢迎；我们也用标签标出了「欢迎贡献」和「欢迎评审」以方便社区参与。这些只是建议，你可以用任何方式贡献。

<div align="center">

|            | 全部                                                          | 特别需要社区协助                                                                                                      |
| ---------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Issues** | [全部 Issues](https://github.com/microsoft/markitdown/issues) | [欢迎贡献的 Issues](https://github.com/microsoft/markitdown/issues?q=is%3Aissue+is%3Aopen+label%3A%22open+for+contribution%22) |
| **PRs**    | [全部 PRs](https://github.com/microsoft/markitdown/pulls)     | [欢迎评审的 PRs](https://github.com/microsoft/markitdown/pulls?q=is%3Apr+is%3Aopen+label%3A%22open+for+reviewing%22)              |

</div>

### 运行测试与检查

- 进入 MarkItDown 包目录：

  ```sh
  cd packages/markitdown
  ```

- 在环境中安装 `hatch` 并运行测试：

  ```sh
  pip install hatch  # 其他安装方式：https://hatch.pypa.io/dev/install/
  hatch shell
  hatch test
  ```

  （备选）使用已装好依赖的 Devcontainer：

  ```sh
  # 在 Devcontainer 中重新打开项目后执行：
  hatch test
  ```

- 提交 PR 前运行 pre-commit：`pre-commit run --all-files`

### 贡献第三方插件

你也可以通过创建并分享第三方插件来贡献。详见 `packages/markitdown-sample-plugin`。

## 商标

本项目可能包含项目、产品或服务的商标或徽标。使用 Microsoft 商标或徽标须遵守并遵循 [Microsoft 商标与品牌使用准则](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general)。在本项目的修改版本中使用 Microsoft 商标或徽标不得造成混淆或暗示 Microsoft 赞助。第三方商标或徽标的使用须遵守相应第三方的政策。
