---
name: nova-markitdown
description:
  Convert various file formats (PDF, Word, Excel, PPT, images, HTML, audio, video) to Markdown using markitdown CLI with dual OCR fallback:glmocr (primary) → paddleocr (fallback). Activate when users need file-to-markdown conversion, OCR recognition, content extraction, structured data from documents, or batch document processing. Keywords:PDF to markdown, image OCR, document conversion, markitdown, glmocr, paddleocr, file extraction.
compatibility:
  Python 3.10+, pip packages:markitdown[all], markitdown-glmocr[glmocr], markitdown-paddleocr.  Requires ZHIPU_API_KEY for glmocr, BAIDU_PADDLE_TOKEN for paddleocr fallback.  Network access to Zhipu AI API and Baidu PaddleOCR API.
metadata:
  author: hankl
  version: "2.0.0"
---

# nova-markitdown

使用 markitdown 命令行工具将各种文件格式转换为 Markdown，**双 OCR 引擎自动降级**：glmocr（主）→ paddleocr（备）。

## 触发条件

当用户需要以下操作时激活此技能：

- 将文件（PDF、Word、Excel、PPT、图片、HTML、音频、视频等）转换为 Markdown 文本
- 提取文件中的文本内容、表格、图片描述等
- 对 PDF 或图片进行 OCR 识别和结构化提取
- 批量转换多个文件为 Markdown

## 环境设置

### 安装依赖

```bash
# 基础 markitdown（支持大部分文件格式）
pip install 'markitdown'

# markitdown-glmocr 插件（主 OCR，智谱 GLM-OCR）
pip install 'markitdown-glmocr[glmocr]'

# markitdown-paddleocr 插件（备 OCR，百度 PaddleOCR）
pip install 'markitdown-paddleocr'
```

### 环境变量

```bash
# 主 OCR：智谱 API Key（glmocr）
export ZHIPU_API_KEY="your-zhipu-api-key"

# 备 OCR：百度 PaddleOCR Token（paddleocr，glmocr 失败时自动切换）
export BAIDU_PADDLE_TOKEN="your-paddle-token"

# 可选配置
export GLMOCR_MODEL="glm-ocr"          # glmocr 模型名称
export GLMOCR_TIMEOUT="600"             # glmocr 请求超时秒数
export PADDLE_OCR_MODEL="PaddleOCR-VL-1.5"  # paddleocr 模型名称
```

> **重要**：`ZHIPU_API_KEY` 用于 glmocr（主），`BAIDU_PADDLE_TOKEN` 用于 paddleocr（备）。两者都设置可实现自动降级。

### 验证安装

```bash
markitdown --version
markitdown --list-plugins  # 输出中应包含 markitdown_glmocr 和 markitdown_paddleocr
```

## 核心规则

1. **优先使用 markitdown 命令行**：所有文件转换优先通过 `markitdown` CLI 完成。
2. **PDF 和图片使用双 OCR 降级策略**：
   - **第一步**：使用 `markitdown -p`（glmocr 插件）尝试解析
   - **第二步**：若 glmocr 报错（API 错误、超时、Key 失效等），自动切换到 paddleocr 插件重试
   - **实现方式**：通过 Python 脚本封装，捕获异常后切换
3. **其他文件类型不使用 `-p`**：Word、Excel、PPT、HTML、音频等使用不带 `-p` 的 markitdown 命令。
4. **复杂场景回退到 Python SDK**：需要结构化 JSON 输出、按区域筛选、自定义处理流程时，使用 Python 代码。详见 [advanced-usage.md](references/advanced-usage.md)。

## 快速参考

| 文件类型 | 命令 | `-p` | 说明 |
|----------|------|:---:|------|
| PDF | `markitdown -p file.pdf -o out.md` | Yes | glmocr AI OCR |
| 图片 (.jpg/.png) | `markitdown -p image.png -o out.md` | Yes | glmocr AI OCR |
| Word (.docx) | `markitdown file.docx -o out.md` | No | 内置转换器 |
| Excel (.xlsx/.xls) | `markitdown file.xlsx -o out.md` | No | 内置转换器 |
| PPT (.pptx) | `markitdown file.pptx -o out.md` | No | 内置转换器 |
| HTML | `markitdown file.html -o out.md` | No | 内置转换器 |
| CSV/JSON/XML | `markitdown file.csv -o out.md` | No | 内置转换器 |
| 音频 | `markitdown audio.mp3 -o out.md` | No | 内置转换器 |
| ZIP | `markitdown archive.zip -o out.md` | No | 自动遍历 |
| YouTube | `markitdown "https://youtube.com/..." -o out.md` | No | 视频转录 |

## 使用指南

### PDF 转换（双 OCR 降级）

```bash
# 方式1：CLI 直接调用（仅 glmocr，无降级）
markitdown -p document.pdf -o output.md

# 方式2：Python 双 OCR 降级（推荐，glmocr 失败自动切 paddleocr）
python -c "
from markitdown import MarkItDown
from markitdown_glmocr import GlmOcrConverter
from markitdown_paddleocr import PaddleOcrConverter

md = MarkItDown(enable_plugins=False)
try:
    md.register_converter(GlmOcrConverter(), priority=-1.0)
    result = md.convert('document.pdf')
    if not result.markdown.strip():
        raise Exception('Empty result')
except Exception as e:
    print(f'glmocr failed: {e}, falling back to paddleocr...')
    md = MarkItDown(enable_plugins=False)
    md.register_converter(PaddleOcrConverter(), priority=-1.0)
    result = md.convert('document.pdf')
print(result.markdown)
"
```

工作原理：纯文本页面使用 pdfplumber/pdfminer 快速提取；复杂页面（含图片、表格、公式）自动使用 AI OCR。glmocr 失败时自动降级到 paddleocr。

### 图片转换（双 OCR 降级）

```bash
# CLI 直接调用（仅 glmocr）
markitdown -p photo.jpg -o photo.md

# Python 双 OCR 降级（推荐）
python -c "
from markitdown import MarkItDown
from markitdown_glmocr import GlmOcrConverter
from markitdown_paddleocr import PaddleOcrConverter

md = MarkItDown(enable_plugins=False)
try:
    md.register_converter(GlmOcrConverter(), priority=-1.0)
    result = md.convert('photo.jpg')
    if not result.markdown.strip():
        raise Exception('Empty result')
except Exception as e:
    print(f'glmocr failed: {e}, falling back to paddleocr...')
    md = MarkItDown(enable_plugins=False)
    md.register_converter(PaddleOcrConverter(), priority=-1.0)
    result = md.convert('photo.jpg')
print(result.markdown)
"
```

### 其他文件格式

```bash
markitdown document.docx -o document.md     # Word
markitdown spreadsheet.xlsx -o data.md      # Excel
markitdown presentation.pptx -o slides.md   # PPT
markitdown webpage.html -o webpage.md       # HTML
markitdown data.csv -o data.md              # CSV
markitdown config.json -o config.md         # JSON
markitdown archive.zip -o archive.md        # ZIP
```

## 故障排查

**插件未发现**：运行 `markitdown --list-plugins`，若无 glmocr 则 `pip install 'markitdown-glmocr[glmocr]'`，若无 paddleocr 则 `pip install markitdown-paddleocr`。

**glmocr API Key 错误**：检查 `echo $ZHIPU_API_KEY`，或在 `.env` 中设置。glmocr 失败时会自动降级到 paddleocr。

**paddleocr Token 错误**：检查 `echo $BAIDU_PADDLE_TOKEN`，或在 `.env` 中设置。

**PDF 输出为空或质量差**：确保使用 `-p` 参数，检查 API Key/Token，可设置 `GLMOCR_ENABLE_LAYOUT=true` 提升结构化输出。

**两个 OCR 都失败**：检查网络连接，确认两个 API Key/Token 都有效。

## 高级用法

需要结构化 JSON 输出、按区域筛选、批量处理、自定义参数、**双 OCR 降级封装**等高级场景，请参考 [advanced-usage.md](references/advanced-usage.md)，包含 Python SDK 的完整示例和 `DualOcrConverter` 统一封装。
