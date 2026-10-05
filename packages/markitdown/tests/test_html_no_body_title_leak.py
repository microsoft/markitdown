from io import BytesIO
from markitdown import MarkItDown, StreamInfo


def convert(html: bytes):
    md = MarkItDown()
    r = md.convert_stream(BytesIO(html), stream_info=StreamInfo(extension='.html'))
    return r.markdown, r.title


def test_title_not_in_body_without_body_tags():
    md, title = convert(b'<html><head><title>Page Title</title></head><p>hello</p></html>')
    assert md == 'hello', md
    assert title == 'Page Title', title


def test_head_metadata_not_in_body():
    html = b'<html><head><title>T</title><meta name="d" content="C"><noscript>Enable JS</noscript></head><p>hello</p></html>'
    md, title = convert(html)
    assert md == 'hello', md
    assert title == 'T', title


def test_body_only_content_preserved():
    md, _ = convert(b'before<body><p>in body</p></body>after')
    assert md == 'in body', md
