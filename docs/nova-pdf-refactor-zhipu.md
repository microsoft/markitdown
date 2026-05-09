# Nova-PDF 重构方案：使用 zai-sdk + glm-ocr

## 1. 重构目标

将现有的自定义 AI 服务替换为 zai-sdk + glm-ocr，简化代码并提升 OCR 能力。

## 2. 技术对比

| 项目 | 原方案 | 新方案 |
|------|--------|--------|
| SDK | requests (手动调用) | zai-sdk (官方 SDK) |
| 模型 | 自定义 Workflow | glm-ocr |
| 接口 | 两步上传（上传+调用） | 直接调用 layout_parsing |
| 认证 | 双 token (upload + workflow) | 单 API key |
| 配置 | 环境变量 | 配置文件 + 环境变量 |

## 3. 接口分析

### 3.1 glm-ocr API

```python
from zai import ZhipuAiClient

client = ZhipuAiClient(api_key="your-api-key")

# 支持图片 URL
response = client.layout_parsing.create(
    model="glm-ocr",
    file="https://example.com/image.png"
)

# 支持本地文件路径
response = client.layout_parsing.create(
    model="glm-ocr",
    file="/path/to/image.png"
)

# 返回结果（包含 Markdown 格式的内容）
print(response)
```

### 3.2 响应结构

```python
# response 包含解析后的结构化内容
# 具体字段需查看实际返回，通常包括：
# - 文本内容
# - 布局信息
# - 表格识别结果
# - Markdown 格式输出
```

## 4. 架构设计

### 4.1 组件变更

```
原架构：
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Page Renderer  │────►│  File Uploader  │────►│  Workflow API   │
│  (截图)          │     │  (上传获取URL)   │     │  (自定义接口)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘

新架构：
┌─────────────────┐     ┌─────────────────┐
│  Page Renderer  │────►│   glm-ocr API   │
│  (截图→临时文件) │     │  (layout_parsing)│
└─────────────────┘     └─────────────────┘
```

### 4.2 文件变更清单

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `_ai_service.py` | **重写** | 使用 zai-sdk + glm-ocr |
| `_converter.py` | 微调 | 适配新 AIService 接口 |
| `_plugin.py` | 微调 | 简化配置参数 |
| `pyproject.toml` | 更新 | 添加 zai-sdk 依赖 |
| `_config.py` | **新增** | 配置文件读取 |
| `README.md` | 更新 | 新的使用说明 |

## 5. 详细设计

### 5.1 配置模块 (_config.py)

```python
"""Configuration management for nova-pdf."""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib


@dataclass
class NovaPdfConfig:
    """nova-pdf configuration."""
    
    # API 配置
    zhipu_api_key: str = ""
    
    # OCR 配置
    model: str = "glm-ocr"
    dpi: int = 150
    timeout: int = 120
    
    # 处理策略
    force_ai: bool = False
    
    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "NovaPdfConfig":
        """
        从多个来源加载配置（优先级从高到低）：
        1. 环境变量
        2. 配置文件 (pyproject.toml 或 nova-pdf.toml)
        3. 默认值
        """
        config = cls()
        
        # 1. 从配置文件加载
        config._load_from_file(config_path)
        
        # 2. 环境变量覆盖
        config._load_from_env()
        
        return config
    
    def _load_from_file(self, config_path: Optional[str] = None):
        """从配置文件加载"""
        # 查找配置文件
        search_paths = []
        
        if config_path:
            search_paths.append(Path(config_path))
        
        # 当前目录的 pyproject.toml
        search_paths.append(Path("pyproject.toml"))
        
        # 当前目录的 nova-pdf.toml
        search_paths.append(Path("nova-pdf.toml"))
        
        # 用户目录
        search_paths.append(Path.home() / ".config" / "nova-pdf" / "config.toml")
        
        for path in search_paths:
            if path.exists():
                try:
                    with open(path, "rb") as f:
                        data = tomllib.load(f)
                    
                    # 读取 [tool.nova-pdf] 配置段
                    if "tool" in data and "nova-pdf" in data["tool"]:
                        self._apply_config(data["tool"]["nova-pdf"])
                    elif "nova-pdf" in data:
                        self._apply_config(data["nova-pdf"])
                    
                    break
                except Exception:
                    pass
    
    def _apply_config(self, data: dict):
        """应用配置"""
        if "api_key" in data:
            self.zhipu_api_key = data["api_key"]
        if "model" in data:
            self.model = data["model"]
        if "dpi" in data:
            self.dpi = data["dpi"]
        if "timeout" in data:
            self.timeout = data["timeout"]
        if "force_ai" in data:
            self.force_ai = data["force_ai"]
    
    def _load_from_env(self):
        """从环境变量加载（优先级最高）"""
        if os.environ.get("NOVA_ZHIPU_API_KEY"):
            self.zhipu_api_key = os.environ["NOVA_ZHIPU_API_KEY"]
        if os.environ.get("NOVA_MODEL"):
            self.model = os.environ["NOVA_MODEL"]
        if os.environ.get("NOVA_DPI"):
            self.dpi = int(os.environ["NOVA_DPI"])
        if os.environ.get("NOVA_TIMEOUT"):
            self.timeout = int(os.environ["NOVA_TIMEOUT"])
        if os.environ.get("NOVA_FORCE_AI"):
            self.force_ai = os.environ["NOVA_FORCE_AI"].lower() in ("true", "1", "yes")
```

### 5.2 AI 服务模块 (_ai_service.py)

```python
"""AI service using zai-sdk and glm-ocr."""

import io
import os
import tempfile
from dataclasses import dataclass
from typing import BinaryIO, Optional

try:
    from zai import ZhipuAiClient
except ImportError:
    ZhipuAiClient = None

from ._config import NovaPdfConfig


@dataclass
class AIResult:
    """Result from AI conversion."""
    text: str
    success: bool = True
    error: Optional[str] = None


class AIService:
    """
    AI 服务 - 使用 zai-sdk + glm-ocr
    
    特点：
    - 直接调用 glm-ocr 的 layout_parsing API
    - 支持本地文件路径或图片 URL
    - 自动处理图片格式转换
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "glm-ocr",
        timeout: int = 120,
        config: Optional[NovaPdfConfig] = None,
    ):
        """
        初始化 AI 服务
        
        Args:
            api_key: 智谱 API Key，默认从配置读取
            model: 模型名称，默认 glm-ocr
            timeout: 请求超时时间（秒）
            config: 配置对象
        """
        if ZhipuAiClient is None:
            raise ImportError(
                "zai-sdk is required for AIService. "
                "Install with: pip install nova-pdf[zhipu]"
            )
        
        # 从配置加载
        if config:
            self.api_key = api_key or config.zhipu_api_key
            self.model = model or config.model
            self.timeout = timeout or config.timeout
        else:
            config = NovaPdfConfig.load()
            self.api_key = api_key or config.zhipu_api_key
            self.model = model
            self.timeout = timeout
        
        if not self.api_key:
            raise ValueError(
                "API key is required. Set NOVA_ZHIPU_API_KEY environment variable "
                "or add 'api_key' to [tool.nova-pdf] in pyproject.toml"
            )
        
        # 初始化客户端
        self.client = ZhipuAiClient(api_key=self.api_key)
    
    def image_to_markdown(
        self,
        image_stream: BinaryIO,
        filename: str = "page.png",
    ) -> AIResult:
        """
        将图片转换为 Markdown
        
        Args:
            image_stream: 图片流
            filename: 文件名（用于临时文件）
        
        Returns:
            AIResult: 转换结果
        """
        try:
            # 方案1：保存为临时文件，传文件路径
            with tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False
            ) as tmp:
                tmp.write(image_stream.read())
                tmp_path = tmp.name
            
            image_stream.seek(0)
            
            # 调用 glm-ocr API
            response = self.client.layout_parsing.create(
                model=self.model,
                file=tmp_path
            )
            
            # 清理临时文件
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
            
            # 解析响应
            # 响应格式可能是字符串或对象，需要适配
            if hasattr(response, 'content'):
                text = response.content
            elif hasattr(response, 'text'):
                text = response.text
            elif isinstance(response, str):
                text = response
            else:
                text = str(response)
            
            return AIResult(
                text=text.strip() if text else "",
                success=True,
            )
        
        except Exception as e:
            return AIResult(
                text="",
                success=False,
                error=str(e),
            )
```

### 5.3 插件注册 (_plugin.py)

```python
"""Plugin registration for nova-pdf."""

from typing import Any
from markitdown import MarkItDown

from ._config import NovaPdfConfig
from ._ai_service import AIService
from ._converter import NovaPdfConverter


__plugin_interface_version__ = 1


def register_converters(markitdown: MarkItDown, **kwargs: Any) -> None:
    """
    注册 nova-pdf 转换器
    
    配置来源（优先级从高到低）：
    1. kwargs 参数
    2. 环境变量
    3. 配置文件 (pyproject.toml)
    4. 默认值
    """
    # 加载配置
    config = NovaPdfConfig.load()
    
    # kwargs 覆盖配置
    api_key = kwargs.get("api_key") or kwargs.get("zhipu_api_key") or config.zhipu_api_key
    model = kwargs.get("model", config.model)
    dpi = kwargs.get("dpi", config.dpi)
    force_ai = kwargs.get("force_ai", config.force_ai)
    timeout = kwargs.get("timeout", config.timeout)
    
    # 创建 AI 服务
    ai_service = None
    if api_key:
        try:
            ai_service = AIService(
                api_key=api_key,
                model=model,
                timeout=timeout,
            )
        except Exception:
            pass
    
    # 注册转换器
    PRIORITY_NOVA_PDF = -1.0
    
    markitdown.register_converter(
        NovaPdfConverter(
            ai_service=ai_service,
            dpi=dpi,
            force_ai=force_ai,
        ),
        priority=PRIORITY_NOVA_PDF,
    )
```

### 5.4 pyproject.toml 更新

```toml
[project]
name = "nova-pdf"
dependencies = [
    "markitdown>=0.1.0",
    "pdfminer.six>=20251230",
    "pdfplumber>=0.11.9",
    "Pillow>=9.0.0",
    "tomli>=2.0.0;python_version<'3.11'",
]

[project.optional-dependencies]
zhipu = [
    "zai-sdk>=0.2.2",
]
dev = [
    "pytest>=7.0.0",
]

[project.entry-points."markitdown.plugin"]
nova_pdf = "nova_pdf"

[tool.nova-pdf]
# API 配置
api_key = ""
model = "glm-ocr"
dpi = 150
timeout = 120
force_ai = false
```

## 6. 配置方式

### 6.1 本地敏感配置文件（推荐）

项目根目录下的 `.secrets.local` 文件存储敏感信息，此文件不会被提交到 Git：

```bash
# .secrets.local
NOVA_ZHIPU_API_KEY="your-api-key-here"
```

使用方式：
```bash
# 加载敏感配置
source .secrets.local

# 或使用脚本
source scripts/load_secrets.sh

# 然后运行
markitdown -p document.pdf
```

### 6.2 配置文件 (pyproject.toml)

```toml
[tool.nova-pdf]
# API key 请通过环境变量或 .secrets.local 文件设置，不要硬编码
api_key = ""
model = "glm-ocr"
dpi = 150
timeout = 120
```

### 6.3 环境变量（推荐）

```bash
export NOVA_ZHIPU_API_KEY="your-api-key-here"
export NOVA_MODEL="glm-ocr"
export NOVA_DPI="150"
```

### 6.3 Python API

```python
from markitdown import MarkItDown

md = MarkItDown(
    enable_plugins=True,
    api_key="your-api-key",
)
```

### 6.4 命令行

```bash
export NOVA_ZHIPU_API_KEY="your-api-key"
markitdown -p document.pdf
```

## 7. 使用示例

```python
from markitdown import MarkItDown
from nova_pdf import AIService, NovaPdfConverter

# 方式1：自动加载配置
md = MarkItDown(enable_plugins=True)
result = md.convert("document.pdf")

# 方式2：手动配置
from nova_pdf import NovaPdfConfig, AIService

config = NovaPdfConfig.load()
ai_service = AIService(
    api_key="your-api-key",
    model="glm-ocr",
)

converter = NovaPdfConverter(
    ai_service=ai_service,
    dpi=150,
)

md = MarkItDown(enable_plugins=False)
md.register_converter(converter, priority=-1.0)
result = md.convert("document.pdf")
```

## 8. 迁移路径

### 8.1 从旧版本迁移

| 旧配置 | 新配置 |
|--------|--------|
| `NOVA_UPLOAD_TOKEN` | `NOVA_ZHIPU_API_KEY` |
| `NOVA_WORKFLOW_TOKEN` | （删除） |
| `NOVA_BASE_URL` | （删除） |
| `NOVA_APP_ID` | （删除） |

### 8.2 API 兼容性

- 旧版 `AIService(upload_token, workflow_token, ...)` → 废弃
- 新版 `AIService(api_key, ...)` → 推荐

## 9. 实施计划

### ✅ Phase 1: 核心实现（已完成）
- [x] 设计配置模块
- [x] 实现 `_config.py`
- [x] 重写 `_ai_service.py`（使用 zai-sdk + glm-ocr）
- [x] 更新 `_plugin.py`

### ✅ Phase 2: 集成测试（已完成）
- [x] 更新 `pyproject.toml`
- [x] 测试 glm-ocr API
- [x] 测试插件集成

### Phase 3: 文档更新（进行中）
- [x] 更新 README.md
- [ ] 更新技术方案文档
- [ ] 添加迁移指南

## 10. 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| zai-sdk 接口变化 | 封装适配层，隔离 SDK 细节 |
| glm-ocr 返回格式不确定 | 做多种格式兼容处理 |
| 临时文件清理失败 | 使用 try-finally 确保清理 |
| API key 泄露 | 支持环境变量，避免硬编码 |

## 11. 待确认事项

- [ ] glm-ocr 返回的具体数据结构
- [ ] 是否支持直接传图片字节流（不保存临时文件）
- [ ] 超时和重试策略
- [ ] 并发请求限制
