# markitdown-paddleocr

智能 PDF/图片转 Markdown 插件，使用百度 PaddleOCR 云端 API 驱动的 OCR 识别。

## 特性

- 🔍 **智能检测**：自动识别每页内容类型（纯文本 vs 图片/表格）
- 📄 **默认解析**：纯文本页面使用 pdfplumber/pdfminer 提取，速度快、成本低
- 🤖 **AI 增强**：复杂页面（图片、表格）使用 PaddleOCR API 转换为 Markdown
- 🔄 **异步 Job 模型**：提交 OCR 任务 → 轮询状态 → 获取结果
- 📊 **结构化输出**：返回 Markdown（含表格、公式、图表等）

## 安装

```bash
pip install markitdown-paddleocr
```

## 配置

### 环境变量（推荐）

```bash
# 必需：百度 PaddleOCR Token
export BAIDU_PADDLE_TOKEN="your-paddle-token"

# 可选
export PADDLE_OCR_MODEL="PaddleOCR-VL-1.5"   # 模型名称
```

### 配置优先级

```
构造函数参数 > 环境变量 > 内置默认值
```

## 使用方法

### 命令行（推荐）

```bash
# 1. 设置 Token
export BAIDU_PADDLE_TOKEN="your-token"

# 2. 查看已安装插件
markitdown --list-plugins

# 3. 使用插件转换 PDF
markitdown -p document.pdf

# 4. 保存到文件
markitdown -p document.pdf -o output.md
```

### Python API

```python
from markitdown import MarkItDown
from markitdown_paddleocr import PaddleOcrConverter

# 方式1：自动从环境变量读取 BAIDU_PADDLE_TOKEN
converter = PaddleOcrConverter()
md = MarkItDown(enable_plugins=False)
md.register_converter(converter, priority=-1.0)
result = md.convert("document.pdf")
print(result.markdown)

# 方式2：手动传入 Token
converter = PaddleOcrConverter(token="your-token")
md = MarkItDown(enable_plugins=False)
md.register_converter(converter, priority=-1.0)
result = md.convert("document.pdf")
print(result.markdown)

# 方式3：强制所有页面使用 OCR
converter = PaddleOcrConverter(token="your-token", force_ai=True)
md = MarkItDown(enable_plugins=False)
md.register_converter(converter, priority=-1.0)
result = md.convert("document.pdf")
print(result.markdown)
```

### 直接使用 PaddleClient

```python
from markitdown_paddleocr import PaddleClient

client = PaddleClient(token="your-token")

# 本地文件
markdown = client.ocr(file_bytes=open("image.png", "rb").read(), filename="image.png")
print(markdown)

# URL 模式
markdown = client.ocr(file_url="https://example.com/document.pdf")
print(markdown)
```

## 配置选项

### PaddleOcrConverter 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `token` | str | 环境变量 `BAIDU_PADDLE_TOKEN` | PaddleOCR Token |
| `model` | str | `PaddleOCR-VL-1.5` | OCR 模型名称 |
| `poll_interval` | float | 2.0 | 轮询间隔（秒） |
| `poll_timeout` | float | 300.0 | 轮询超时（秒） |
| `force_ai` | bool | False | 强制所有页面使用 OCR |
| `use_doc_orientation_classify` | bool | False | 文档方向分类 |
| `use_doc_unwarping` | bool | False | 文档去扭曲 |
| `use_chart_recognition` | bool | False | 图表识别 |

### 环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `BAIDU_PADDLE_TOKEN` | Token（必需） | `7963b85a...` |
| `PADDLE_OCR_MODEL` | 模型名称 | `PaddleOCR-VL-1.5` |

## 工作原理

```
PDF/图片 输入
    │
    ▼
PaddleOcrConverter.convert()
    │
    ├─ 图片文件 ──► PaddleClient.ocr() ──► markdown
    │
    └─ PDF 文件 ──► 逐页分析内容类型
          │
          ├─ 纯文本页 ──► pdfplumber 提取文本
          │
          └─ 复杂页（图片/表格）
                │
                └─► 渲染为图片 ──► PaddleClient.ocr()
                      │
                      ├─ POST /api/v2/ocr/jobs  (提交 Job)
                      ├─ GET  /api/v2/ocr/jobs/{id}  (轮询状态)
                      └─ GET  jsonUrl  (获取 JSONL 结果)
    │
    ▼
合并输出完整 Markdown
```

## 依赖

- `markitdown>=0.1.0` - 基础框架
- `pdfplumber>=0.11.9` - PDF 解析和截图
- `pdfminer.six>=20251230` - 文本提取备用
- `Pillow>=9.0.0` - 图像处理
- `requests>=2.28.0` - HTTP 请求

## 发布到 PyPI

### 前置条件

- 确保已安装 `build` 和 `twine`：

```bash
pip install build twine
```

- 确保环境变量 `PyPI_API_Token` 已设置为你的 PyPI API Token：

```bash
export PyPI_API_Token="pypi-..."
```

### 发布步骤

```bash
# 1. 进入项目根目录（包含 pyproject.toml）
cd packages/markitdown-paddleocr

# 2. 构建分发包（生成 dist/ 目录下的 .tar.gz 和 .whl 文件）
python -m build

# 3. 检查包的元数据和内容
twine check dist/*

# 4. 上传到 PyPI（使用环境变量中的 Token 认证）
twine upload dist/* -u __token__ -p "$PyPI_API_Token"
```

### 发布到 TestPyPI（测试）

```bash
# 先上传到 TestPyPI 验证包是否正确
twine upload --repository testpypi dist/* -u __token__ -p "$PyPI_API_Token"

# 从 TestPyPI 安装验证
pip install --index-url https://test.pypi.org/simple/ markitdown-paddleocr
```

### 注意事项

- 发布前确保 `pyproject.toml` 中的版本号已更新
- 同一版本号不能重复上传，如需修正必须 bump 版本号
- `PyPI_API_Token` 环境变量切勿硬编码到脚本或提交到代码仓库

## 许可证

MIT
