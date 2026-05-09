# markitdown-glmocr

智能 PDF 转 Markdown 插件，使用 glm-ocr AI 驱动的图片和表格提取。

## 特性

- 🔍 **智能检测**：自动识别每页内容类型（纯文本 vs 图片/表格）
- 📄 **默认解析**：纯文本页面使用 pdfplumber/pdfminer 提取，速度快、成本低
- 🤖 **AI 增强**：复杂页面（图片、表格）使用 glm-ocr 转换为 Markdown
- ⚙️ **灵活配置**：支持配置文件、环境变量等多种配置方式

## 安装

```bash
# 基础安装
pip install markitdown-glmocr

# 安装 AI 功能
pip install markitdown-glmocr[zhipu]
```

## 配置

### 本地敏感配置（推荐）

项目根目录的 `.secrets.local` 文件存储敏感信息，此文件不会被提交到 Git：

```bash
# 创建 .secrets.local 文件
echo 'GLMOCR_API_KEY="your-api-key"' > .secrets.local

# 加载配置
source .secrets.local
```

### 环境变量

```bash
# 必需
export GLMOCR_API_KEY="your-zhipu-api-key"

# 可选
export GLMOCR_MODEL="glm-ocr"
export GLMOCR_DPI="150"
export GLMOCR_TIMEOUT="120"
```

### 配置文件

在 `pyproject.toml` 中配置默认值：

```toml
[tool.markitdown-glmocr]
model = "glm-ocr"
dpi = 150
timeout = 120
force_ai = false
```

## 使用方法

### 命令行（推荐）

```bash
# 1. 加载敏感配置
source .secrets.local

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

# 方式1：自动加载配置
md = MarkItDown(enable_plugins=True)
result = md.convert("document.pdf")
print(result.markdown)

# 方式2：手动配置
from markitdown_glmocr import GlmOcrConfig, AIService, GlmOcrPdfConverter

config = GlmOcrConfig.load()
ai_service = AIService(
    api_key="your-api-key",
    model="glm-ocr",
)

converter = GlmOcrPdfConverter(
    ai_service=ai_service,
    dpi=150,
)

md = MarkItDown(enable_plugins=False)
md.register_converter(converter, priority=-1.0)
result = md.convert("document.pdf")
```

## 配置选项

### GlmOcrConfig 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `api_key` | str | 环境变量 `GLMOCR_API_KEY` | 智谱 API Key |
| `model` | str | "glm-ocr" | 模型名称 |
| `dpi` | int | 150 | 截图分辨率 |
| `timeout` | int | 120 | 请求超时（秒） |
| `force_ai` | bool | False | 强制所有页面使用 AI |

### GlmOcrPdfConverter 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `ai_service` | AIService | None | AI 服务实例 |
| `dpi` | int | 150 | 截图分辨率 |
| `force_ai` | bool | False | 强制所有页面使用 AI |

## 工作原理

```
PDF 输入
    │
    ▼
逐页分析内容类型
    │
    ├─ 纯文本页面 ──► pdfplumber 提取文本
    │
    └─ 复杂页面（图片/表格）
          │
          ├─ 截图渲染 (150 DPI)
          │
          ├─ base64 编码
          │
          └─ 调用 glm-ocr API 转 Markdown
    │
    ▼
合并输出完整 Markdown
```

## 技术架构

- **zai-sdk**: 智谱 AI 官方 SDK
- **glm-ocr**: 智谱 OCR 模型，支持表格、图片识别
- **pdfplumber**: PDF 页面分析和截图
- **pdfminer**: 纯文本页面提取

## 依赖

- `markitdown>=0.1.0` - 基础框架
- `pdfplumber>=0.11.9` - PDF 解析和截图
- `pdfminer.six>=20251230` - 文本提取备用
- `Pillow>=9.0.0` - 图像处理
- `zai-sdk>=0.2.2` - 智谱 AI SDK（可选，AI 功能需要）

## 许可证

MIT
