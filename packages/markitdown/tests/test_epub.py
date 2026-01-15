import base64
import os
import re

from markitdown import MarkItDown


def test_epub_conversion():
    markitdown = MarkItDown()
    result = markitdown.convert(
        "test_files/piper-temple-trouble.epub",
        keep_data_uris=True,
    )
    md = result.markdown
    image_re = re.compile(pattern=r"!\[(.*?)\]\(data:image/(.*?);base64,(.*?)\)")
    images = image_re.findall(md)

    print(f"get images num: {len(images)}")


if __name__ == "__main__":
    test_epub_conversion()
