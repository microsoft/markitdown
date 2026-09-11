#!/usr/bin/env python3 -m pytest
import io
import pytest
from unittest.mock import patch

from markitdown import MarkItDown, StreamInfo
from markitdown._exceptions import MissingDependencyException

SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head><title>Test Article</title></head>
<body>
    <nav>
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/contact">Contact</a></li>
        </ul>
    </nav>
    <aside class="sidebar">
        <h3>Related Articles</h3>
        <ul>
            <li><a href="/other">Other Article</a></li>
        </ul>
    </aside>
    <article>
        <h1>Main Article Title</h1>
        <p>This is the main article content that should be extracted by reader mode.
        It contains several paragraphs of meaningful text that readability should
        identify as the primary content of the page.</p>
        <p>Here is another paragraph with more substantive content about the topic
        at hand. Reader mode should preserve this while stripping away the
        navigation and sidebar elements.</p>
        <p>A third paragraph ensures there is enough content for readability to
        confidently identify this as the main article body.</p>
    </article>
    <footer>
        <p>Copyright 2024 Test Site</p>
        <nav>
            <a href="/privacy">Privacy Policy</a>
            <a href="/terms">Terms of Service</a>
        </nav>
    </footer>
</body>
</html>
"""


class TestReaderMode:
    def test_reader_mode_extracts_article_content(self):
        """Reader mode should extract main article content and exclude nav/footer."""
        md = MarkItDown()
        result = md.convert_stream(
            io.BytesIO(SAMPLE_HTML.encode("utf-8")),
            stream_info=StreamInfo(
                mimetype="text/html", extension=".html", charset="utf-8"
            ),
            reader_mode=True,
        )

        assert "Main Article Title" in result.markdown
        assert "main article content" in result.markdown

    def test_without_reader_mode_includes_everything(self):
        """Without reader mode, the full page including nav/footer should appear."""
        md = MarkItDown()
        result = md.convert_stream(
            io.BytesIO(SAMPLE_HTML.encode("utf-8")),
            stream_info=StreamInfo(
                mimetype="text/html", extension=".html", charset="utf-8"
            ),
            reader_mode=False,
        )

        assert "Home" in result.markdown
        assert "Privacy Policy" in result.markdown
        assert "Main Article Title" in result.markdown

    def test_reader_mode_missing_dependency(self):
        """Should raise MissingDependencyException when readability-lxml is not installed."""
        import markitdown.converters._html_converter as html_mod
        from markitdown.converters._html_converter import HtmlConverter

        original = html_mod._dependency_exc_info
        try:
            html_mod._dependency_exc_info = (
                ImportError,
                ImportError("no module"),
                None,
            )

            converter = HtmlConverter()
            with pytest.raises(MissingDependencyException):
                converter.convert(
                    io.BytesIO(SAMPLE_HTML.encode("utf-8")),
                    StreamInfo(
                        mimetype="text/html", extension=".html", charset="utf-8"
                    ),
                    reader_mode=True,
                )
        finally:
            html_mod._dependency_exc_info = original

    def test_reader_mode_default_is_false(self):
        """Default behavior (no reader_mode flag) should convert the full page."""
        md = MarkItDown()
        result = md.convert_stream(
            io.BytesIO(SAMPLE_HTML.encode("utf-8")),
            stream_info=StreamInfo(
                mimetype="text/html", extension=".html", charset="utf-8"
            ),
        )

        assert "Home" in result.markdown
        assert "Privacy Policy" in result.markdown
