# Nova-PDF 插件技术方案

## 1. 概述

### 1.1 目标
开发一个智能 PDF 解析插件 `nova-pdf`，实现：
- 自动检测 PDF 每页内容类型（纯文本 vs 包含图片/表格）
- 对纯文本页面使用默认解析能力（pdfminer/pdfplumber）
- 对包含图片/表格的页面截图后调用 AI 接口转 Markdown

### 1.2 核心价值
- **提升复杂 PDF 解析质量**：图表、扫描件等传统方法效果差的内容
- **降低成本**：纯文本页面不调用 AI，节省 API 费用
- **灵活配置**：支持自定义 AI 模型、分辨率、提示词等

---

## 2. 架构设计

### 2.1 插件结构
```
packages/nova-pdf/
├── src/
│   └── nova_pdf/
│       ├── __init__.py           # 导出和版本信息
│       ├── __about__.py          # 版本号
│       ├── _plugin.py            # 插件注册入口
│       ├── _converter.py         # PDF 转换器核心实现
│       ├── _page_analyzer.py     # 页面内容分析器
│       ├── _page_renderer.py     # 页面截图渲染器
│       └── _ai_service.py        # AI 接口封装
├── tests/
│   ├── __init__.py
│   ├── test_converter.py
│   ├── test_analyzer.py
│   └── fixtures/
│       ├── text_only.pdf
│       ├── with_images.pdf
│       └── mixed_content.pdf
├── pyproject.toml
└── README.md
```

### 2.2 组件职责

| 组件 | 职责 |
|------|------|
| `_plugin.py` | 实现 `register_converters` 入口，注册转换器 |
| `_converter.py` | 继承 `DocumentConverter`，协调整体流程 |
| `_page_analyzer.py` | 分析页面是否包含图片/表格 |
| `_page_renderer.py` | 将 PDF 页面渲染为图片 |
| `_ai_service.py` | 调用 AI Vision API 转换图片为 Markdown |

### 2.3 流程图

```
┌──────────────────────────────────────────────────────────────────┐
│                        PDF 文件输入                                │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                     逐页分析 (PageAnalyzer)                        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  对每一页:                                                   │  │
│  │  1. 检测是否包含图片 (images)                                │  │
│  │  2. 检测是否包含表格 (tables)                                 │  │
│  │  3. 标记页面类型: PLAIN_TEXT / COMPLEX                       │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                                │
          ┌─────────────────────┴─────────────────────┐
          ▼                                           ▼
┌─────────────────────┐                    ┌─────────────────────┐
│   PLAIN_TEXT 页面    │                    │    COMPLEX 页面      │
│                     │                    │                     │
│  使用默认解析:        │                    │  1. 截图渲染         │
│  - pdfplumber 提取   │                    │  2. 调用 AI 接口     │
│  - pdfminer 备用     │                    │  3. 转换为 Markdown   │
└─────────────────────┘                    └─────────────────────┘
          │                                           │
          └─────────────────────┬─────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                    合并所有页面结果                                │
│                    输出完整 Markdown                               │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. 核心算法设计

### 3.1 页面内容检测 (PageAnalyzer)

#### 检测策略
```python
class PageType(Enum):
    PLAIN_TEXT = "plain_text"      # 纯文本，使用默认解析
    HAS_IMAGES = "has_images"      # 包含图片
    HAS_TABLES = "has_tables"      # 包含表格
    COMPLEX = "complex"            # 复杂内容（图片+表格+混合）
```

#### 图片检测方法
使用 **pdfplumber** 的页面对象检测：

```python
def detect_images(page) -> bool:
    """检测页面是否包含图片"""
    # 方法1: 直接检测 page.images
    if hasattr(page, 'images') and len(page.images) > 0:
        return True

    # 方法2: 检测页面对象中的图像资源
    if hasattr(page, 'objects'):
        if 'image' in page.objects and len(page.objects['image']) > 0:
            return True
        # 检测 XObject (可能包含内嵌图像)
        if 'xobject' in page.objects and len(page.objects['xobject']) > 0:
            for obj in page.objects['xobject']:
                if obj.get('subtype') == 'Image':
                    return True

    # 方法3: 检测页面资源字典
    try:
        if hasattr(page.page, 'get_resources'):
            resources = page.page.get_resources()
            if resources and 'XObject' in resources:
                return True
    except Exception:
        pass

    return False
```

#### 表格检测方法
```python
def detect_tables(page) -> bool:
    """检测页面是否包含表格"""
    # 方法1: 使用 pdfplumber 的 extract_tables
    tables = page.extract_tables()
    if tables and len(tables) > 0:
        # 过滤空表格
        for table in tables:
            if table and any(any(cell for cell in row) for row in table):
                return True

    # 方法2: 检测表格线（边框线）
    if hasattr(page, 'objects') and 'line' in page.objects:
        lines = page.objects['line']
        if len(lines) > 10:  # 大量线条可能构成表格
            # 分析线条是否形成网格结构
            h_lines = [l for l in lines if l.get('height', 1) < 2]
            v_lines = [l for l in lines if l.get('width', 1) < 2]
            if len(h_lines) > 2 and len(v_lines) > 2:
                return True

    return False
```

#### 综合判断
```python
def analyze_page(page) -> PageType:
    """分析页面类型"""
    has_images = detect_images(page)
    has_tables = detect_tables(page)

    if has_images and has_tables:
        return PageType.COMPLEX
    elif has_images:
        return PageType.HAS_IMAGES
    elif has_tables:
        return PageType.HAS_TABLES
    else:
        return PageType.PLAIN_TEXT
```

### 3.2 页面截图渲染 (PageRenderer)

#### 技术选型

使用 **pdfplumber.to_image**，理由：
- 已是项目依赖，无需额外安装
- 实现简单，代码量少
- 底层使用 PIL，满足需求

#### 实现方案
```python
import io

def render_page_to_image(page, dpi: int = 150) -> io.BytesIO:
    """
    将 PDF 页面渲染为图片

    Args:
        page: pdfplumber 页面对象
        dpi: 渲染分辨率，默认 150（平衡质量和速度）

    Returns:
        BytesIO: PNG 图片流
    """
    # 使用 pdfplumber 的 to_image 方法
    page_image = page.to_image(resolution=dpi)

    # 转换为 BytesIO
    img_stream = io.BytesIO()
    page_image.original.save(img_stream, format="PNG")
    img_stream.seek(0)

    return img_stream
```

#### DPI 推荐值
```python
DPI_SETTINGS = {
    "low": 72,      # 快速预览，文件小
    "medium": 150,  # 平衡质量和速度（默认）
    "high": 300,   # 高质量，适合复杂图表
}
```

### 3.3 AI 接口调用 (AIService)

#### 复用 markitdown 的 LLM 客户端机制
```python
from markitdown.converters._llm_caption import llm_caption

class AIService:
    """AI Vision 服务封装"""

    def __init__(
        self,
        client,                    # OpenAI 兼容客户端
        model: str = "gpt-4o",     # 模型名称
        prompt: str | None = None, # 自定义提示词
    ):
        self.client = client
        self.model = model
        self.prompt = prompt or self._default_prompt()

    def _default_prompt(self) -> str:
        return """请将这张图片的内容转换为 Markdown 格式。

要求：
1. 保持原有的文档结构（标题、段落、列表等）
2. 表格使用 Markdown 表格语法
3. 图片中的文字清晰转写
4. 数学公式使用 LaTeX 语法
5. 如有图表，用文字描述其内容
6. 不要添加任何额外的解释或评论"""

    def image_to_markdown(
        self,
        image_stream: io.BytesIO,
        stream_info: StreamInfo,
    ) -> str:
        """调用 AI 将图片转为 Markdown"""
        result = llm_caption(
            image_stream,
            stream_info,
            client=self.client,
            model=self.model,
            prompt=self.prompt,
        )
        return result or ""
```

---

## 4. 转换器实现 (_converter.py)

### 4.1 核心流程
```python
class NovaPdfConverter(DocumentConverter):
    """智能 PDF 转换器"""

    def __init__(
        self,
        ai_service: AIService | None = None,
        dpi: int = 150,
        force_ai: bool = False,  # 强制所有页面使用 AI
    ):
        self.ai_service = ai_service
        self.dpi = dpi
        self.force_ai = force_ai

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        # 读取 PDF
        pdf_stream = io.BytesIO(file_stream.read())

        markdown_parts = []

        with pdfplumber.open(pdf_stream) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # 分析页面类型
                page_type = analyze_page(page)

                # 根据类型选择处理方式
                if self.force_ai or page_type != PageType.PLAIN_TEXT:
                    # 复杂内容：截图 + AI
                    if self.ai_service:
                        img = render_page_to_image(page, self.dpi)
                        md = self.ai_service.image_to_markdown(img, StreamInfo())
                    else:
                        # 无 AI 服务，回退到默认解析
                        md = page.extract_text() or ""
                else:
                    # 纯文本：默认解析
                    md = page.extract_text() or ""

                if md.strip():
                    markdown_parts.append(f"## Page {page_num + 1}\n\n{md}")

        return DocumentConverterResult(
            markdown="\n\n".join(markdown_parts),
        )
```

---

## 5. 配置选项

### 5.1 初始化参数
```python
class NovaPdfConfig:
    """nova-pdf 配置"""

    # AI 服务配置
    llm_client: Any = None           # OpenAI 兼容客户端（必需）
    llm_model: str = "gpt-4o"        # 模型名称
    llm_prompt: str | None = None   # 自定义提示词

    # 渲染配置
    dpi: int = 150                   # 截图分辨率
    image_format: str = "png"       # 图片格式

    # 处理策略
    force_ai: bool = False          # 强制所有页面使用 AI
    skip_tables: bool = False       # 跳过表格检测（表格用默认解析）
    skip_images: bool = False       # 跳过图片检测（图片用默认解析）

    # 性能配置
    max_concurrent: int = 5          # 并发请求数
    timeout: int = 60                # 单页 AI 调用超时（秒）
```

### 5.2 使用示例
```python
from openai import OpenAI
from markitdown import MarkItDown

# 初始化 LLM 客户端
client = OpenAI(api_key="your-api-key")

# 创建 MarkItDown 实例并启用 nova-pdf 插件
md = MarkItDown(
    enable_plugins=True,
    llm_client=client,
    llm_model="gpt-4o",
)

# 转换 PDF
result = md.convert("complex_document.pdf")
print(result.markdown)
```

---

## 6. 依赖管理

### 6.1 pyproject.toml
```toml
[project]
name = "nova-pdf"
dependencies = [
    "markitdown>=0.1.0",
    "pdfminer.six>=20251230",
    "pdfplumber>=0.11.9",   # 页面解析和截图渲染
    "Pillow>=9.0.0",        # 图像处理（pdfplumber.to_image 底层依赖）
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
]

# 插件入口点
[project.entry-points."markitdown.plugin"]
nova_pdf = "nova_pdf"
```

---

## 7. 错误处理

### 7.1 降级策略
```python
def convert_with_fallback(
    self,
    pdf_bytes: bytes,
    page_num: int,
    page_type: PageType,
) -> str:
    """带降级的转换"""

    # 尝试 AI 转换
    if self.ai_service and page_type != PageType.PLAIN_TEXT:
        try:
            img = render_page_to_image(pdf_bytes, page_num, self.dpi)
            result = self.ai_service.image_to_markdown(img, StreamInfo())
            if result.strip():
                return result
        except AIServiceError as e:
            logger.warning(f"AI 转换失败，降级到默认解析: {e}")

    # 降级到默认解析
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        page = pdf.pages[page_num]
        text = page.extract_text() or ""

        # 尝试提取表格
        tables = page.extract_tables()
        if tables:
            for table in tables:
                text += "\n\n" + self._table_to_markdown(table)

        return text
```

---

## 8. 性能优化

### 8.1 异步处理
```python
import asyncio
from typing import List

async def convert_pages_async(
    self,
    pdf_bytes: bytes,
    pages: List[PageInfo],
) -> List[str]:
    """异步并发处理多页"""

    async def process_page(page_info: PageInfo) -> str:
        if page_info.type == PageType.PLAIN_TEXT:
            return self._extract_text(pdf_bytes, page_info.num)
        else:
            return await self._ai_convert_async(pdf_bytes, page_info.num)

    # 使用信号量限制并发
    semaphore = asyncio.Semaphore(self.max_concurrent)

    async def limited_process(page_info):
        async with semaphore:
            return await process_page(page_info)

    tasks = [limited_process(p) for p in pages]
    return await asyncio.gather(*tasks)
```

### 8.2 缓存机制
```python
from functools import lru_cache
import hashlib

class CachedAIService(AIService):
    """带缓存的 AI 服务"""

    @lru_cache(maxsize=100)
    def _get_cache_key(self, image_hash: str) -> str | None:
        """获取缓存结果"""
        # 可接入 Redis 等
        pass

    def image_to_markdown(self, image_stream: io.BytesIO, ...) -> str:
        # 计算图片哈希
        image_hash = hashlib.md5(image_stream.read()).hexdigest()
        image_stream.seek(0)

        # 检查缓存
        cached = self._get_cache_key(image_hash)
        if cached:
            return cached

        # 调用 AI
        result = super().image_to_markdown(image_stream, ...)

        # 存入缓存
        self._cache_result(image_hash, result)
        return result
```

---

## 9. 测试策略

### 9.1 测试用例设计
```python
class TestNovaPdfConverter:
    """nova-pdf 转换器测试"""

    def test_plain_text_pdf(self):
        """纯文本 PDF 应使用默认解析"""
        pass

    def test_pdf_with_images(self):
        """包含图片的 PDF 应调用 AI"""
        pass

    def test_pdf_with_tables(self):
        """包含表格的 PDF 应调用 AI"""
        pass

    def test_mixed_content_pdf(self):
        """混合内容应正确区分处理"""
        pass

    def test_ai_service_fallback(self):
        """AI 服务失败时应降级"""
        pass

    def test_dpi_settings(self):
        """不同 DPI 设置的渲染质量"""
        pass

    def test_concurrent_processing(self):
        """并发处理性能测试"""
        pass
```

---

## 10. 扩展性设计

### 10.1 自定义页面分析器
```python
class PageAnalyzerPlugin(ABC):
    """页面分析器插件接口"""

    @abstractmethod
    def analyze(self, page) -> PageType:
        """分析页面类型"""
        pass

# 允许用户注入自定义分析器
class NovaPdfConverter(DocumentConverter):
    def __init__(
        self,
        page_analyzer: PageAnalyzerPlugin | None = None,
        ...
    ):
        self.page_analyzer = page_analyzer or DefaultPageAnalyzer()
```

### 10.2 自定义 AI 提示词模板
```python
PROMPT_TEMPLATES = {
    "default": "...",
    "academic": "学术论文模板...",
    "financial": "财务报表模板...",
    "legal": "法律文档模板...",
}

class AIService:
    def __init__(self, prompt_template: str = "default", ...):
        self.prompt = PROMPT_TEMPLATES.get(prompt_template, PROMPT_TEMPLATES["default"])
```

---

## 11. 风险与缓解措施

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| AI API 调用失败 | 转换中断 | 实现降级策略，回退到默认解析 |
| 大文件内存溢出 | 程序崩溃 | 分页处理，控制内存占用 |
| AI 响应慢 | 用户体验差 | 异步处理、进度反馈、超时控制 |
| 解析质量不稳定 | 输出错误 | 多模型对比、人工审核机制 |
| API 费用过高 | 成本失控 | 智能跳过纯文本页面、缓存机制 |

---

## 12. 实施计划

### ✅ Phase 1: 基础框架（已完成）
- [x] 创建项目结构
- [x] 实现插件注册入口
- [x] 实现基础转换器框架

### ✅ Phase 2: 核心功能（已完成）
- [x] 实现页面内容检测 (`_page_analyzer.py`)
- [x] 实现页面截图渲染 (`_page_renderer.py`)
- [x] 实现 AI 服务接口 (`_ai_service.py`)
- [x] 实现完整转换流程 (`_converter.py`)

### ⏳ Phase 3: 测试与优化（待进行）
- [ ] 运行单元测试
- [ ] 添加测试 PDF 样本
- [ ] 性能测试和优化

### ⏳ Phase 4: 文档与发布（待进行）
- [x] 编写 README 和使用文档
- [x] 准备示例代码
- [ ] 打包发布

---

## 代码结构

```
packages/nova-pdf/
├── src/nova_pdf/
│   ├── __about__.py          # 版本号 (0.1.0)
│   ├── __init__.py           # 导出 register_converters
│   ├── _plugin.py            # 插件注册入口
│   ├── _converter.py         # PDF 转换器核心
│   ├── _page_analyzer.py     # 图片/表格检测
│   ├── _page_renderer.py     # 页面截图 (pdfplumber.to_image)
│   └── _ai_service.py        # AI 接口封装（两步上传）
├── tests/
│   ├── test_analyzer.py      # 分析器测试
│   ├── test_converter.py     # 转换器测试
│   └── test_ai_service.py    # AI 服务测试
├── pyproject.toml            # 项目配置 + nova-pdf 配置
└── README.md                 # 使用文档
```

**语法验证**: ✓ 所有 Python 文件通过语法检查

---

## 15. 改造完成总结

### 15.1 主要变更

| 文件 | 变更内容 |
|------|----------|
| `_ai_service.py` | 重写为两步调用：上传 → Workflow |
| `_plugin.py` | 适配新 AIService 初始化参数 |
| `_converter.py` | 传递文件名给 AI 服务 |
| `pyproject.toml` | 添加 `[tool.nova-pdf]` 配置段 |
| `README.md` | 更新环境变量和配置说明 |
| `tests/test_ai_service.py` | 新增 AI 服务测试（13 个用例）|

### 15.2 环境变量

```bash
export NOVA_UPLOAD_TOKEN="your-fastgpt-token"      # 必需
export NOVA_WORKFLOW_TOKEN="your-workflow-token"  # 必需
export NOVA_BASE_URL="https://xny-test.glodon.com/jsf-ai"  # 可选
export NOVA_APP_ID="69fc37113fedac1eaaf65c82"     # 可选
```

### 15.3 快速开始

```python
from markitdown import MarkItDown

# 启用插件
md = MarkItDown(enable_plugins=True)

# 转换 PDF（复杂页面自动调用 AI）
result = md.convert("document.pdf")
print(result.markdown)
```

### 15.4 实测结果

**测试图片**: `数位顺序表.png` (22KB)

**测试结果**: ✓ 成功转换

```markdown
|  | 整数部分 | | | | | | | 小数部分 | | | | |
|:---:|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 数位 | ...... | 万位 | 千位 | 百位 | 十位 | 个位 | . | 十分位 | 百分位 | 千分位 | 万分位 | ...... |
| 单位 | ...... | 万 | 千 | 百 | 十 | 个 | | 十分之一 0.1 | 百分之一 0.01 | 千分之一 0.001 | 万分之一 0.0001 | ...... |
```

**关键修正**:
1. 上传接口返回 `code: 200`（不是 0）
2. Workflow 接口需要 `messages` 字段（OpenAI 兼容格式）
3. SSL 验证跳过（`verify=False`）以适配内部 API

---

## 13. 附录

### 13.1 参考实现
- `markitdown-ocr`: 已有的 OCR 插件，可参考架构
- `markitdown-sample-plugin`: 官方插件示例
- `_pdf_converter.py`: 默认 PDF 转换器实现

### 13.2 关键代码参考
```python
# 参考 markitdown-ocr 的插件注册方式
def register_converters(markitdown: MarkItDown, **kwargs: Any) -> None:
    PRIORITY_NOVA_PDF = -1.0  # 优先于默认 PDF 转换器

    llm_client = kwargs.get("llm_client")
    llm_model = kwargs.get("llm_model", "gpt-4o")

    ai_service = None
    if llm_client:
        ai_service = AIService(client=llm_client, model=llm_model)

    markitdown.register_converter(
        NovaPdfConverter(ai_service=ai_service),
        priority=PRIORITY_NOVA_PDF,
    )

# 页面截图渲染（简化版）
def render_page_to_image(page, dpi: int = 150) -> io.BytesIO:
    """使用 pdfplumber.to_image 渲染页面"""
    page_image = page.to_image(resolution=dpi)
    img_stream = io.BytesIO()
    page_image.original.save(img_stream, format="PNG")
    img_stream.seek(0)
    return img_stream
```

---

## 14. AI 接口改造方案（自定义两步调用）

### 14.1 背景

原方案使用 OpenAI 兼容的 base64 图片上传方式，现需改造为自定义两步流程：
1. 上传图片到文件服务，获取 URL
2. 调用 Workflow 接口处理图片

### 14.2 接口分析

#### Step 1: 文件上传接口

**请求**
```
POST https://xny-test.glodon.com/jsf-ai/api/common/file/upload
Content-Type: multipart/form-data
Cookie: fastgpt_token=<token>
```

**表单参数**
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| metadata | string | ✓ | JSON 字符串，如 `{"chatId":"<uuid>"}`，每次动态生成 |
| bucketName | string | ✓ | 固定值 `chat` |
| file | binary | ✓ | 图片文件（PNG/JPEG） |
| data | string | ✓ | JSON 字符串，如 `{"appId":"69fc37113fedac1eaaf65c82"}` |

**响应示例**
```json
{
  "code": 200,
  "data": {
    "previewUrl": "https://xny-test.glodon.com/jsf-ai/api/common/file/read/xxx.png?token=...",
    "fileId": "69fc42e024457b47b7e22b4a"
  }
}
```

> 注意：接口返回 `code: 200` 表示成功（不是 0）

#### Step 2: Workflow 调用接口

**请求**
```
POST https://xny-test.glodon.com/jsf-ai/api/v1/chat/completions
Content-Type: application/json
Authorization: Bearer <workflow_image2markdown_key>
```

**请求体**（OpenAI 兼容格式）
```json
{
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "请将这张图片的内容转换为 Markdown 格式。"},
        {"type": "image_url", "image_url": {"url": "https://...previewUrl..."}}
      ]
    }
  ]
}
```

**响应示例**（OpenAI 兼容格式）
```json
{
  "id": "",
  "model": "",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "| 数位顺序表 |\n|---|"
      }
    }
  ]
}
```

> 注意：Workflow 接口使用 OpenAI 兼容的消息格式，需要 `messages` 字段

### 14.3 改造后的 AIService

```python
"""AI service with custom two-step API calls."""

import io
import json
import requests
from dataclasses import dataclass
from typing import Any, BinaryIO, Optional


@dataclass
class AIResult:
    """Result from AI conversion."""
    text: str
    success: bool = True
    error: Optional[str] = None


class AIService:
    """
    AI 服务 - 自定义两步调用方式

    流程：
    1. 上传图片到文件服务，获取 previewUrl
    2. 调用 Workflow 接口，传入 fileUrls 参数
    """

    def __init__(
        self,
        base_url: str = "https://xny-test.glodon.com/jsf-ai",
        upload_token: str = "",           # fastgpt_token (Cookie)
        workflow_token: str = "",         # workflow_image2markdown_key (Authorization)
        chat_id: str = "",                # 用于上传接口的 chatId
        app_id: str = "",                 # 用于上传接口的 appId
        timeout: int = 60,
    ):
        """
        初始化 AI 服务

        Args:
            base_url: API 基础地址
            upload_token: 文件上传认证 token（fastgpt_token）
            workflow_token: Workflow 接口认证 token
            chat_id: 会话 ID
            app_id: 应用 ID
            timeout: 请求超时时间（秒）
        """
        self.base_url = base_url.rstrip("/")
        self.upload_token = upload_token
        self.workflow_token = workflow_token
        self.chat_id = chat_id
        self.app_id = app_id
        self.timeout = timeout

    def image_to_markdown(
        self,
        image_stream: BinaryIO,
        filename: str = "page.png",
    ) -> AIResult:
        """
        将图片转换为 Markdown（两步调用）

        Args:
            image_stream: 图片流
            filename: 文件名

        Returns:
            AIResult: 转换结果
        """
        try:
            # Step 1: 上传图片
            upload_result = self._upload_file(image_stream, filename)
            if not upload_result["success"]:
                return AIResult(
                    text="",
                    success=False,
                    error=f"Upload failed: {upload_result.get('error')}"
                )

            file_url = upload_result["preview_url"]

            # Step 2: 调用 Workflow
            workflow_result = self._call_workflow(file_url)
            if not workflow_result["success"]:
                return AIResult(
                    text="",
                    success=False,
                    error=f"Workflow failed: {workflow_result.get('error')}"
                )

            return AIResult(
                text=workflow_result["text"],
                success=True,
            )

        except Exception as e:
            return AIResult(
                text="",
                success=False,
                error=str(e),
            )

    def _upload_file(
        self,
        image_stream: BinaryIO,
        filename: str,
    ) -> dict:
        """
        上传文件到文件服务

        Args:
            image_stream: 图片流
            filename: 文件名

        Returns:
            dict: {"success": bool, "preview_url": str, "error": str}
        """
        url = f"{self.base_url}/api/common/file/upload"

        # 准备 multipart/form-data
        files = {
            "file": (filename, image_stream, "image/png")
        }

        data = {
            "metadata": json.dumps({"chatId": self.chat_id}),
            "bucketName": "chat",
            "data": json.dumps({"appId": self.app_id}),
        }

        headers = {
            "Cookie": f"fastgpt_token={self.upload_token}",
        }

        try:
            response = requests.post(
                url,
                files=files,
                data=data,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()

            result = response.json()

            if result.get("code") == 0 and result.get("data", {}).get("previewUrl"):
                return {
                    "success": True,
                    "preview_url": result["data"]["previewUrl"],
                }
            else:
                return {
                    "success": False,
                    "error": result.get("message", "Unknown error"),
                }

        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e),
            }

    def _call_workflow(self, file_url: str) -> dict:
        """
        调用 Workflow 接口处理图片

        Args:
            file_url: 文件 URL

        Returns:
            dict: {"success": bool, "text": str, "error": str}
        """
        url = f"{self.base_url}/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.workflow_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "fileUrls": [file_url],
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()

            result = response.json()

            # 解析 OpenAI 兼容响应格式
            choices = result.get("choices", [])
            if choices:
                content = choices[0].get("message", {}).get("content", "")
                return {
                    "success": True,
                    "text": content.strip(),
                }
            else:
                return {
                    "success": False,
                    "error": "No response content",
                }

        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e),
            }
```

### 14.4 使用示例

```python
from markitdown import MarkItDown
from nova_pdf import AIService, NovaPdfConverter

# 创建自定义 AI 服务
ai_service = AIService(
    base_url="https://xny-test.glodon.com/jsf-ai",
    upload_token="<your-fastgpt-token>",  # fastgpt_token
    workflow_token="your-workflow-token",
    chat_id="tv1cyJFTt4wEKLqTKEx1KPEN",
    app_id="69fc37113fedac1eaaf65c82",
    timeout=120,
)

# 创建转换器
converter = NovaPdfConverter(
    ai_service=ai_service,
    dpi=150,
)

# 手动注册
md = MarkItDown(enable_plugins=False)
md.register_converter(converter, priority=-1.0)

# 转换 PDF
result = md.convert("document.pdf")
print(result.markdown)
```

### 14.5 配置参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `base_url` | str | ✓ | API 基础地址 |
| `upload_token` | str | ✓ | 文件上传认证 token（fastgpt_token） |
| `workflow_token` | str | ✓ | Workflow 接口认证 token |
| `chat_id` | str | ✓ | 会话 ID（用于上传接口） |
| `app_id` | str | ✓ | 应用 ID（用于上传接口） |
| `timeout` | int | | 超时时间，默认 60 秒 |

### 14.6 错误处理

```python
def image_to_markdown(self, image_stream, filename="page.png") -> AIResult:
    """带完善错误处理的转换"""
    try:
        # Step 1: 上传
        upload_result = self._upload_file(image_stream, filename)
        if not upload_result["success"]:
            # 上传失败，返回详细错误
            return AIResult(
                text="",
                success=False,
                error=f"上传失败: {upload_result.get('error')}"
            )

        # Step 2: Workflow
        workflow_result = self._call_workflow(upload_result["preview_url"])
        if not workflow_result["success"]:
            # Workflow 失败，返回详细错误
            return AIResult(
                text="",
                success=False,
                error=f"AI 处理失败: {workflow_result.get('error')}"
            )

        return AIResult(
            text=workflow_result["text"],
            success=True,
        )

    except requests.Timeout:
        return AIResult(
            text="",
            success=False,
            error="请求超时，请检查网络或增加 timeout 设置"
        )
    except requests.ConnectionError:
        return AIResult(
            text="",
            success=False,
            error="网络连接失败，请检查网络设置"
        )
    except json.JSONDecodeError:
        return AIResult(
            text="",
            success=False,
            error="响应解析失败，接口返回非 JSON 格式"
        )
    except Exception as e:
        return AIResult(
            text="",
            success=False,
            error=f"未知错误: {str(e)}"
        )
```

### 14.7 与原方案的对比

| 对比项 | 原方案（base64） | 新方案（两步上传） |
|--------|-----------------|-------------------|
| 图片传输 | base64 内嵌 | URL 引用 |
| 请求大小 | 大（含图片数据） | 小（仅 URL） |
| 适用场景 | 小图片 | 大图片、多图片 |
| 依赖 | OpenAI SDK | requests |
| 认证方式 | API Key | Token + Cookie |
| 接口格式 | OpenAI 标准 | 自定义 |

### 14.8 配置确认

- [x] ~~`chat_id` 是否需要每次动态生成？~~ **是的，每次生成 UUID**
- [x] ~~`app_id` 是否固定？~~ **是的，固定值**
- [x] ~~`workflow_image2markdown_key` 如何获取？~~ **在 pyproject.toml 中配置**
- [x] ~~是否需要支持并发上传？~~ **否**

### 14.9 配置文件设计

**pyproject.toml 新增配置项**
```toml
[project.optional-dependencies]
nova-api = [
  "requests>=2.28.0",
]

[tool.nova-pdf]
# AI 服务配置
base_url = "https://xny-test.glodon.com/jsf-ai"
app_id = "69fc37113fedac1eaaf65c82"
timeout = 120

# 认证配置（建议通过环境变量覆盖）
# upload_token = ""    # 环境变量: NOVA_UPLOAD_TOKEN
# workflow_token = ""  # 环境变量: NOVA_WORKFLOW_TOKEN
```

**环境变量**
- `NOVA_UPLOAD_TOKEN`: 上传接口认证 token (fastgpt_token)
- `NOVA_WORKFLOW_TOKEN`: Workflow 接口认证 token
- `NOVA_BASE_URL`: API 基础地址（可选，覆盖配置文件）
- `NOVA_APP_ID`: 应用 ID（可选，覆盖配置文件）
