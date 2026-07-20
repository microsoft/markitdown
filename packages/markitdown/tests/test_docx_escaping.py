import pytest
from markitdown.converters._html_converter import HtmlConverter

def test_markdown_special_character_escaping():
    html_content = "<p># Hello World</p><p>> Quote</p><p>- List</p><p>A | B</p><table><tr><td>C | D</td></tr></table>"
    converter = HtmlConverter()
    result = converter.convert_string(html_content)
    
    # Verify that the special characters at the start of paragraphs are escaped
    assert r"\# Hello World" in result.markdown
    assert r"\> Quote" in result.markdown
    assert r"\- List" in result.markdown
    
    # Verify that mid-line pipes are escaped
    assert r"A \| B" in result.markdown
    assert r"C \| D" in result.markdown
