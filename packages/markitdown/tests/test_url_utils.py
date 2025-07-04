import pytest

from markitdown._url_utils import convert_relative_to_absolute_path

# 参数化测试用例
test_cases = [
    # TC01: 相对路径 '../d/e.js' 应正确解析
    ("https://example.com/a/b/c.html", "../d/e.js", "https://example.com/a/d/e.js"),
    # TC02: 绝对路径 '/d/e.js' 应保留不变
    ("https://example.com/a/b/c.html", "/d/e.js", "https://example.com/d/e.js"),
    # TC03: 完整 URL 不应修改
    ("https://example.com/a/b/c.html", "https://other.com/x/y.js", "https://other.com/x/y.js"),
    # TC04: 空 resource_url 返回原路径
    ("", "abc.js", "abc.js"),
    # TC06: 多级 '..' 路径应正确解析
    ("https://example.com/a/b/c.html", "../../x.js", "https://example.com/x.js"),
    # TC07: file:// 协议支持
    ("file:///C:/project/docs/index.md", "../assets/img.png", "file:///C:/project/assets/img.png"),
    # TC08: 路径穿越应正常解析
    ("https://example.com/a/b/c.html", "../../../etc/passwd", "https://example.com/etc/passwd"),
]

@pytest.mark.parametrize("resource_url, path, expected", test_cases)
def test_convert_relative_to_absolute_path(resource_url, path, expected):
    assert convert_relative_to_absolute_path(resource_url, path) == expected


# TC10: None 类型的 path 应保持不变
def test_none_path():
    result = convert_relative_to_absolute_path("https://example.com/a/b/c.html", None)
    assert result is None
