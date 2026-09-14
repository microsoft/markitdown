import io

from markitdown import MarkItDown


def _convert_html(html: str):
    return MarkItDown().convert_stream(
        io.BytesIO(html.encode("utf-8")),
        file_extension=".html",
    )


def test_title_does_not_leak_into_markdown_when_body_tag_is_absent() -> None:
    # HTML5 allows <html>, <head> and <body> tags to be omitted, and many
    # hand-written pages do. Nothing here moves <title> out of the document
    # tree the way a browser would, so its text must not appear in the body.
    result = _convert_html(
        "<!DOCTYPE html><title>Page Title</title><p>Hello body</p>"
    )

    assert result.markdown == "Hello body"
    assert result.title == "Page Title"


def test_head_element_does_not_leak_into_markdown_when_body_tag_is_absent() -> None:
    result = _convert_html(
        "<html><head><title>T</title></head><h1>Heading</h1></html>"
    )

    assert result.markdown == "# Heading"
    assert result.title == "T"


def test_content_outside_body_element_is_not_dropped() -> None:
    # Content before or after <body> is still rendered by browsers, so it
    # must survive conversion instead of being silently discarded.
    result = _convert_html(
        "<html><p>Intro outside body</p><body><p>Main</p></body>"
        "<p>Footer outside</p></html>"
    )

    assert "Intro outside body" in result.markdown
    assert "Main" in result.markdown
    assert "Footer outside" in result.markdown


def test_svg_title_is_preserved() -> None:
    # <title> inside <svg> describes a graphic and is content, unlike a
    # document <title>, so it must survive the metadata removal.
    result = _convert_html(
        "<body><svg><title>Square</title><rect width='4' height='4'/></svg>"
        "<p>text</p></body>"
    )

    assert "Square" in result.markdown
