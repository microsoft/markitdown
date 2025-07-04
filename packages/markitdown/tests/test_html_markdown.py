
from markitdown import MarkItDown

def test_html_path():
    result = MarkItDown().convert_uri("https://wms-docs.linyikj.com/guide/getting-started.html").markdown
    print(result)