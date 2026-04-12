"""MarkItDown 单例封装，供 FastAPI Depends 注入使用。"""

import os
from markitdown import MarkItDown

_md: MarkItDown | None = None


def get_converter() -> MarkItDown:
    """返回 MarkItDown 全局单例，避免重复初始化。

    可通过环境变量 ENABLE_PLUGINS=true 启用插件（如 markitdown-ocr）。
    """
    global _md
    if _md is None:
        enable_plugins = os.getenv("ENABLE_PLUGINS", "false").lower() == "true"
        _md = MarkItDown(enable_plugins=enable_plugins)
    return _md
