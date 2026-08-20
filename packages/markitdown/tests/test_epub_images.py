import re

from markitdown import MarkItDown


def test_epub_image_conversion():
    markitdown = MarkItDown()
    result = markitdown.convert(
        "test_files/test_epub_images.epub",
        keep_data_uris=True,
    )
    md = result.markdown
    image_re = re.compile(pattern=r"!\[(.*?)\]\(data:image/(.*?);base64,(.*?)\)")
    images = image_re.findall(md)

    assert len(images) > 0


if __name__ == "__main__":
    test_epub_image_conversion()
