"""Page renderer for converting PDF pages to images."""

import io
from typing import Any


def render_page_to_image(page: Any, dpi: int = 150) -> io.BytesIO:
    """
    将 PDF 页面渲染为图片

    Args:
        page: pdfplumber 页面对象
        dpi: 渲染分辨率，默认 150（平衡质量和速度）

    Returns:
        io.BytesIO: PNG 图片流
    """
    # 使用 pdfplumber 的 to_image 方法
    page_image = page.to_image(resolution=dpi)

    # 转换为 BytesIO
    img_stream = io.BytesIO()
    page_image.original.save(img_stream, format="PNG")
    img_stream.seek(0)

    return img_stream


# DPI 预设值
DPI_LOW = 72      # 快速预览，文件小
DPI_MEDIUM = 150  # 平衡质量和速度（默认）
DPI_HIGH = 300    # 高质量，适合复杂图表
