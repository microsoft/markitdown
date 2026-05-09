"""Page content analyzer for detecting images and tables."""

from enum import Enum
from typing import Any


class PageType(Enum):
    """Page content type classification."""
    PLAIN_TEXT = "plain_text"      # 纯文本，使用默认解析
    HAS_IMAGES = "has_images"      # 包含图片
    HAS_TABLES = "has_tables"      # 包含表格
    COMPLEX = "complex"            # 复杂内容（图片+表格+混合）


def detect_images(page: Any) -> bool:
    """
    检测页面是否包含图片

    Args:
        page: pdfplumber 页面对象

    Returns:
        bool: 是否包含图片
    """
    # 方法1: 直接检测 page.images
    if hasattr(page, 'images') and len(page.images) > 0:
        return True

    # 方法2: 检测页面对象中的图像资源
    if hasattr(page, 'objects'):
        objects = page.objects
        if 'image' in objects and len(objects['image']) > 0:
            return True
        # 检测 XObject (可能包含内嵌图像)
        if 'xobject' in objects and len(objects['xobject']) > 0:
            for obj in objects['xobject']:
                if isinstance(obj, dict) and obj.get('subtype') == 'Image':
                    return True

    # 方法3: 检测页面资源字典
    try:
        if hasattr(page, 'page') and hasattr(page.page, 'get_resources'):
            resources = page.page.get_resources()
            if resources and 'XObject' in resources:
                return True
    except Exception:
        pass

    return False


def detect_tables(page: Any) -> bool:
    """
    检测页面是否包含表格

    Args:
        page: pdfplumber 页面对象

    Returns:
        bool: 是否包含表格
    """
    # 方法1: 使用 pdfplumber 的 extract_tables
    try:
        tables = page.extract_tables()
        if tables and len(tables) > 0:
            # 过滤空表格
            for table in tables:
                if table and any(any(cell for cell in row if cell) for row in table):
                    return True
    except Exception:
        pass

    # 方法2: 检测表格线（边框线）
    try:
        if hasattr(page, 'objects') and 'line' in page.objects:
            lines = page.objects['line']
            if len(lines) > 10:  # 大量线条可能构成表格
                # 分析线条是否形成网格结构
                h_lines = []
                v_lines = []
                for line in lines:
                    # 水平线：高度很小
                    if abs(line.get('height', 1)) < 2:
                        h_lines.append(line)
                    # 垂直线：宽度很小
                    elif abs(line.get('width', 1)) < 2:
                        v_lines.append(line)

                if len(h_lines) > 2 and len(v_lines) > 2:
                    return True
    except Exception:
        pass

    return False


def analyze_page(page: Any) -> PageType:
    """
    分析页面类型

    Args:
        page: pdfplumber 页面对象

    Returns:
        PageType: 页面类型
    """
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
