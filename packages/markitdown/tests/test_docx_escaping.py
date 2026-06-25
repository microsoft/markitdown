import pytest
from markitdown.converters._html_converter import HtmlConverter

def test_markdown_special_character_escaping():
    html_content = "<p># Hello World</p><p>> Quote</p><p>- List</p>"
    converter = HtmlConverter()
    result = converter.convert_string(html_content)
    
    # Verify that the special characters at the start of paragraphs are escaped
    assert r"\# Hello World" in result.markdown
    assert r"\> Quote" in result.markdown
    assert r"\- List" in result.markdown
