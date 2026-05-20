# markitdown-paddleocr 方案设计

## 概述

基于百度 PaddleOCR 云端 API 实现的 markitdown OCR 插件，参考 markitdown-glmocr 架构。

## 与 glmocr 的核心差异

| 维度 | glmocr | paddleocr |
|------|--------|-----------|
| API 风格 | 同步 SDK 调用 | 异步 Job 轮询（submit → poll → fetch result） |
| 认证 | `ZHIPU_API_KEY` | `BAIDU_PADDLE_TOKEN` (bearer token) |
| 结果格式 | SDK 封装对象 | JSONL 流（逐行 JSON，含 layoutParsingResults） |
| 图片处理 | SDK 内置 base64 编码 | 需手动上传文件或传 fileUrl |
| 模型 | glm-ocr | PaddleOCR-VL-1.5 |

## 架构

```
markitdown-paddleocr/
├── pyproject.toml
├── README.md
└── src/markitdown_paddleocr/
    ├── __init__.py          # 导出 + __plugin_interface_version__
    ├── __about__.py         # __version__
    ├── _config.py           # PaddleOcrConfig dataclass
    ├── _paddle_client.py    # PaddleOCR API 客户端（submit/poll/fetch）
    ├── _converter.py        # PaddleOcrConverter(DocumentConverter)
    └── _plugin.py           # register_converters 入口
```

## 核心流程

```
文件输入 (PDF/图片)
    │
    ▼
PaddleOcrConverter.convert()
    │
    ├─ 图片文件 ──► _convert_image() ──► PaddleClient.ocr() ──► markdown
    │
    └─ PDF 文件 ──► _convert_pdf()
          │
          ├─ 逐页分析 (pdfplumber)
          ├─ 纯文本页 ──► pdfplumber 提取
          └─ 复杂页 ──► 渲染为图片 ──► PaddleClient.ocr() ──► markdown
```

## PaddleClient 核心逻辑

```python
class PaddleClient:
    JOB_URL = "https://paddleocr.aistudio-app.com/api/v2/ocr/jobs"

    def ocr(self, file_bytes, filename=None, file_url=None) -> str:
        # 1. 提交 Job（本地文件用 multipart，URL 用 JSON）
        job_id = self._submit(file_bytes, filename, file_url)
        # 2. 轮询 Job 状态（pending → running → done）
        result_url = self._poll(job_id)
        # 3. 获取 JSONL 结果，拼接 markdown
        return self._fetch_markdown(result_url)
```

## 关键设计决策

1. **异步轮询间隔**: 默认 2s，可配置，最大等待 300s
2. **PDF 处理策略**: 与 glmocr 一致，纯文本页用 pdfplumber，复杂页用 OCR
3. **图片上传**: 使用 multipart/form-data 上传本地文件；支持 fileUrl 模式
4. **结果解析**: 从 JSONL 的 `layoutParsingResults[].markdown.text` 提取 markdown
5. **环境变量**: `BAIDU_PADDLE_TOKEN`（必需），`PADDLE_OCR_MODEL`（默认 PaddleOCR-VL-1.5）
6. **可选参数**: `useDocOrientationClassify`, `useDocUnwarping`, `useChartRecognition`

## 依赖

```
markitdown>=0.1.0
pdfminer.six>=20251230
pdfplumber>=0.11.9
Pillow>=9.0.0
requests>=2.28.0
```

## 入口点

```toml
[project.entry-points."markitdown.plugin"]
markitdown_paddleocr = "markitdown_paddleocr"
```

## 使用方式

```bash
# 环境变量
export BAIDU_PADDLE_TOKEN="your-token"

# CLI
markitdown -p document.pdf

# Python
from markitdown_paddleocr import PaddleOcrConverter
converter = PaddleOcrConverter(token="your-token")
```
