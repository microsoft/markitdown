# markitdown-glmocr

智能 PDF 转 Markdown 插件，使用 glmocr SDK（智谱 GLM-OCR）驱动的图片和表格提取。

## 特性

- 🔍 **智能检测**：自动识别每页内容类型（纯文本 vs 图片/表格）
- 📄 **默认解析**：纯文本页面使用 pdfplumber/pdfminer 提取，速度快、成本低
- 🤖 **AI 增强**：复杂页面（图片、表格）使用 glmocr SDK 转换为 Markdown
- ⚡ **一行调用**：`glmocr.parse("document.pdf")` 完成 OCR，无需手动截图编码
- 📊 **结构化输出**：返回 Markdown + JSON 结构（含区域标签、边界框）

## 安装

```bash
# 基础安装
pip install markitdown-glmocr

# 安装 AI 功能
pip install markitdown-glmocr[glmocr]
```

## 配置

### 环境变量（推荐）

```bash
# 必需：智谱 API Key
export ZHIPU_API_KEY="your-zhipu-api-key"

# 可选
export GLMOCR_MODEL="glm-ocr"          # 模型名称
export GLMOCR_TIMEOUT="600"             # 请求超时（秒）
export GLMOCR_ENABLE_LAYOUT="true"      # 启用布局检测
export GLMOCR_LOG_LEVEL="INFO"          # 日志级别
```

### 配置优先级

```
构造函数参数 > 环境变量 > .env 文件 > config.yaml > 内置默认值
```

### 本地敏感配置

```bash
# 创建 .env 文件（自动读取）
echo "ZHIPU_API_KEY=your-api-key" > .env
```

## 使用方法

### 命令行（推荐）

```bash
# 1. 设置 API Key
export ZHIPU_API_KEY="sk-xxx"

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
from markitdown_glmocr import GlmOcrConverter

# 方式1：自动从环境变量读取 ZHIPU_API_KEY
converter = GlmOcrConverter()
md = MarkItDown(enable_plugins=False)
md.register_converter(converter, priority=-1.0)
result = md.convert("document.pdf")
print(result.markdown)

# 方式2：手动传入 API Key
converter = GlmOcrConverter(api_key="sk-xxx")
md = MarkItDown(enable_plugins=False)
md.register_converter(converter, priority=-1.0)
result = md.convert("document.pdf")
print(result.markdown)

# 方式3：直接使用 glmocr SDK（更简单）
import glmocr
result = glmocr.parse("document.pdf")
print(result.markdown_result)  # Markdown 输出
print(result.json_result)      # 结构化 JSON（区域标签、边界框）
```

### 处理结果

```python
import glmocr

result = glmocr.parse("report.pdf")

# 获取 Markdown
print(result.markdown_result)

# 获取结构化数据（按页分组）
for page_idx, page_regions in enumerate(result.json_result):
    print(f"Page {page_idx + 1}: {len(page_regions)} regions")
    for region in page_regions:
        print(f"  [{region['label']}] {region['content'][:60]}")

# 按标签筛选
tables = [r for r in result.json_result[0] if r["label"] == "table"]
formulas = [r for r in result.json_result[0] if r["label"] == "formula"]

# 保存到磁盘
result.save(output_dir="./output")
```

## 配置选项

### GlmOcrConverter 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `api_key` | str | 环境变量 `ZHIPU_API_KEY` | 智谱 API Key |
| `timeout` | int | 1800 | 请求超时（秒） |
| `enable_layout` | bool | False | 启用布局检测 |
| `force_ai` | bool | False | 强制所有页面使用 AI |

### 环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `ZHIPU_API_KEY` | API Key（必需） | `sk-abc123` |
| `GLMOCR_MODEL` | 模型名称 | `glm-ocr` |
| `GLMOCR_TIMEOUT` | 请求超时（秒） | `600` |
| `GLMOCR_ENABLE_LAYOUT` | 布局检测 | `true` |
| `GLMOCR_LOG_LEVEL` | 日志级别 | `INFO` |

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
          └─► glmocr.parse() 一行调用
                │
                ├─ 内置截图渲染
                ├─ 内置 base64 编码
                └─ 内置 OCR 识别
    │
    ▼
合并输出完整 Markdown
```

## 区域标签（json_result）

glmocr SDK 返回的结构化数据支持以下标签：

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

## 技术架构

- **glmocr**: 智谱 OCR SDK，一行代码完成 PDF/图片解析
- **pdfplumber**: PDF 页面分析和纯文本提取
- **pdfminer**: 纯文本页面提取备用

## 依赖

- `markitdown>=0.1.0` - 基础框架
- `pdfplumber>=0.11.9` - PDF 解析和截图
- `pdfminer.six>=20251230` - 文本提取备用
- `Pillow>=9.0.0` - 图像处理
- `glmocr` - 智谱 OCR SDK（可选，AI 功能需要）

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
cd packages/markitdown-glmocr

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
pip install --index-url https://test.pypi.org/simple/ markitdown-glmocr
```

### 注意事项

- 发布前确保 `pyproject.toml` 中的版本号已更新
- 同一版本号不能重复上传，如需修正必须 bump 版本号
- `PyPI_API_Token` 环境变量切勿硬编码到脚本或提交到代码仓库

## 许可证

MIT