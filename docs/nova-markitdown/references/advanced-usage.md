# 高级用法：Python SDK + 双 OCR 降级

当 markitdown 命令行无法满足需求时（如需要结构化 JSON 输出、按区域筛选、自定义处理流程、双 OCR 降级等），使用 Python 代码实现。

## 场景 0：DualOcrConverter — 双 OCR 自动降级（推荐）

`DualOcrConverter` 封装了 glmocr（主）→ paddleocr（备）的自动降级逻辑，是 PDF/图片处理的推荐方式。

```python
from markitdown import MarkItDown
from markitdown_glmocr import GlmOcrConverter
from markitdown_paddleocr import PaddleOcrConverter

class DualOcrConverter:
    """双 OCR 转换器：glmocr（主）→ paddleocr（备）自动降级。"""

    def __init__(self, glmocr_kwargs=None, paddleocr_kwargs=None):
        self.glmocr_kwargs = glmocr_kwargs or {}
        self.paddleocr_kwargs = paddleocr_kwargs or {}

    def convert(self, file_path: str) -> str:
        """转换文件，glmocr 失败自动降级到 paddleocr。"""
        # 第一步：尝试 glmocr
        try:
            md = MarkItDown(enable_plugins=False)
            md.register_converter(GlmOcrConverter(**self.glmocr_kwargs), priority=-1.0)
            result = md.convert(file_path)
            if result.markdown and result.markdown.strip():
                print("✓ glmocr 解析成功")
                return result.markdown
            raise Exception("glmocr returned empty result")
        except Exception as e:
            print(f"⚠ glmocr 失败: {e}")

        # 第二步：降级到 paddleocr
        try:
            md = MarkItDown(enable_plugins=False)
            md.register_converter(PaddleOcrConverter(**self.paddleocr_kwargs), priority=-1.0)
            result = md.convert(file_path)
            if result.markdown and result.markdown.strip():
                print("✓ paddleocr 解析成功（降级）")
                return result.markdown
            raise Exception("paddleocr returned empty result")
        except Exception as e:
            print(f"✗ paddleocr 也失败: {e}")
            raise RuntimeError(f"Both OCR engines failed. glmocr error preceded paddleocr fallback error.")

# 使用
converter = DualOcrConverter()
markdown = converter.convert("document.pdf")
```

### 自定义参数

```python
converter = DualOcrConverter(
    glmocr_kwargs={
        "api_key": "sk-xxx",
        "enable_layout": True,
        "force_ai": True,
    },
    paddleocr_kwargs={
        "token": "your-paddle-token",
        "model": "PaddleOCR-VL-1.5",
        "use_chart_recognition": True,
    }
)
markdown = converter.convert("complex_report.pdf")
```

### 批量处理 + 双 OCR

```python
from pathlib import Path

converter = DualOcrConverter()
pdf_dir = Path("./documents")
output_dir = pdf_dir / "output"
output_dir.mkdir(exist_ok=True)

for pdf_file in pdf_dir.glob("*.pdf"):
    try:
        markdown = converter.convert(str(pdf_file))
        (output_dir / f"{pdf_file.stem}.md").write_text(markdown, encoding="utf-8")
        print(f"✓ {pdf_file.name}")
    except RuntimeError:
        print(f"✗ {pdf_file.name} — both OCR engines failed")
```

## 场景 1：结构化 JSON 输出（glmocr 区域标签、边界框）

```python
import glmocr

# 一行调用完成 OCR
result = glmocr.parse("report.pdf")

# 获取 Markdown 文本
print(result.markdown_result)

# 获取结构化数据（按页分组，每页包含多个区域）
for page_idx, page_regions in enumerate(result.json_result):
    print(f"Page {page_idx + 1}: {len(page_regions)} regions")
    for region in page_regions:
        print(f"  [{region['label']}] {region['content'][:60]}")

# 按标签筛选特定类型内容
tables = [r for r in result.json_result[0] if r["label"] == "table"]
formulas = [r for r in result.json_result[0] if r["label"] == "formula"]
titles = [r for r in result.json_result[0] if r["label"] == "title"]

# 保存到磁盘（Markdown + JSON 同时保存）
result.save(output_dir="./output")
```

### 支持的区域标签

| 标签 | 说明 |
|------|------|
| `title` | 标题 |
| `text` | 正文文本 |
| `table` | 表格 |
| `figure` | 图片 |
| `formula` | 公式 |
| `header` | 页眉 |
| `footer` | 页脚 |
| `page_number` | 页码 |
| `reference` | 参考文献 |
| `seal` | 印章 |

## 场景 2：单独使用 PaddleClient（paddleocr 直接调用）

```python
from markitdown_paddleocr import PaddleClient

client = PaddleClient(token="your-paddle-token")

# 本地文件 OCR
with open("image.png", "rb") as f:
    markdown = client.ocr(file_bytes=f.read(), filename="image.png")
print(markdown)

# URL 模式 OCR
markdown = client.ocr(file_url="https://example.com/document.pdf")
print(markdown)
```

## 场景 3：MarkItDown Python API + 单个 Converter

```python
from markitdown import MarkItDown
from markitdown_glmocr import GlmOcrConverter
# 或 from markitdown_paddleocr import PaddleOcrConverter

# glmocr
converter = GlmOcrConverter()
md = MarkItDown(enable_plugins=False)
md.register_converter(converter, priority=-1.0)
result = md.convert("document.pdf")
print(result.text_content)

# paddleocr
from markitdown_paddleocr import PaddleOcrConverter
converter = PaddleOcrConverter()
md = MarkItDown(enable_plugins=False)
md.register_converter(converter, priority=-1.0)
result = md.convert("document.pdf")
print(result.text_content)
```

## 场景 4：自定义转换器参数

```python
from markitdown import MarkItDown
from markitdown_glmocr import GlmOcrConverter
from markitdown_paddleocr import PaddleOcrConverter

# glmocr 自定义
glmocr_converter = GlmOcrConverter(
    api_key="sk-xxx",
    timeout=600,
    enable_layout=True,
    force_ai=True,
)

# paddleocr 自定义
paddleocr_converter = PaddleOcrConverter(
    token="your-token",
    model="PaddleOCR-VL-1.5",
    poll_interval=3.0,
    poll_timeout=600.0,
    force_ai=True,
    use_chart_recognition=True,
)

# 使用 DualOcrConverter 封装
converter = DualOcrConverter(
    glmocr_kwargs={"api_key": "sk-xxx", "enable_layout": True},
    paddleocr_kwargs={"token": "your-token", "use_chart_recognition": True},
)
markdown = converter.convert("complex_document.pdf")
```

## 场景 5：只处理图片（不经过 PDF）

```python
import glmocr

# glmocr 直接对图片 OCR
result = glmocr.parse("screenshot.png")
print(result.markdown_result)

# paddleocr 直接对图片 OCR
from markitdown_paddleocr import PaddleClient
client = PaddleClient(token="your-token")
with open("photo.jpg", "rb") as f:
    markdown = client.ocr(file_bytes=f.read(), filename="photo.jpg")
print(markdown)
```

## 场景 6：批量处理多个文件

```python
from pathlib import Path

# 使用 DualOcrConverter 批量处理（推荐）
converter = DualOcrConverter()

pdf_dir = Path("./documents")
for pdf_file in pdf_dir.glob("*.pdf"):
    try:
        markdown = converter.convert(str(pdf_file))
        output_path = pdf_dir / "output" / f"{pdf_file.stem}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        print(f"✓ {pdf_file.name}")
    except RuntimeError:
        print(f"✗ {pdf_file.name} — both OCR engines failed")
```

## OCR 引擎对比

| 维度 | glmocr | paddleocr |
|------|--------|-----------|
| API 风格 | 同步 SDK 调用 | 异步 Job 轮询（submit → poll → fetch） |
| 认证 | `ZHIPU_API_KEY` | `BAIDU_PADDLE_TOKEN` |
| 结果格式 | SDK 封装对象 | JSONL 流 |
| 结构化输出 | ✅ 区域标签 + 边界框 | ❌ 仅 Markdown |
| 表格识别 | ✅ HTML → Markdown | ✅ HTML 表格 |
| 公式识别 | ✅ LaTeX | ✅ LaTeX |
| 印章识别 | ✅ | ✅ |
| 响应速度 | 快（同步） | 较慢（需轮询，2-30s） |
| 适用场景 | 首选，结构化需求 | 降级备选，glmocr 不可用时 |
