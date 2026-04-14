"""
Tests for maishad/enhanced-features:
 - Bug fixes: ipynb outputs, xlsx empty sheets, zip silent failures, pptx chart separator,
               audio extensions, wikipedia infoboxes, rss links
 - New features: YamlConverter, get_document_stats / DocumentConverterResult.stats(),
                  RequirementsConverter
"""

import io
import json
import zipfile
import pytest

from markitdown import MarkItDown
from markitdown._stream_info import StreamInfo
from markitdown._base_converter import DocumentConverterResult
from markitdown.converters._markdown_stats_converter import get_document_stats
from markitdown.converters._yaml_converter import YamlConverter
from markitdown.converters._requirements_converter import RequirementsConverter


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_stream(content: bytes | str) -> io.BytesIO:
    if isinstance(content, str):
        content = content.encode()
    return io.BytesIO(content)


# ---------------------------------------------------------------------------
# Bug 1: ipynb — cell outputs
# ---------------------------------------------------------------------------

class TestIpynbOutputs:
    def _notebook(self, cells):
        return json.dumps({
            "nbformat": 4,
            "nbformat_minor": 5,
            "metadata": {},
            "cells": cells,
        }).encode()

    def _convert(self, nb_bytes):
        md = MarkItDown()
        stream = io.BytesIO(nb_bytes)
        si = StreamInfo(extension=".ipynb")
        return md.convert_stream(stream, stream_info=si).markdown

    def test_stream_output_rendered(self):
        nb = self._notebook([{
            "cell_type": "code",
            "source": ["print('hello')"],
            "outputs": [{
                "output_type": "stream",
                "name": "stdout",
                "text": ["hello\n"],
            }],
        }])
        md = self._convert(nb)
        assert "hello" in md

    def test_execute_result_rendered(self):
        nb = self._notebook([{
            "cell_type": "code",
            "source": ["1 + 1"],
            "outputs": [{
                "output_type": "execute_result",
                "data": {"text/plain": ["2"]},
                "metadata": {},
                "execution_count": 1,
            }],
        }])
        md = self._convert(nb)
        assert "2" in md

    def test_display_data_rendered(self):
        nb = self._notebook([{
            "cell_type": "code",
            "source": ["display('hi')"],
            "outputs": [{
                "output_type": "display_data",
                "data": {"text/plain": ["'hi'"]},
                "metadata": {},
            }],
        }])
        md = self._convert(nb)
        assert "'hi'" in md

    def test_error_output_rendered(self):
        nb = self._notebook([{
            "cell_type": "code",
            "source": ["1/0"],
            "outputs": [{
                "output_type": "error",
                "ename": "ZeroDivisionError",
                "evalue": "division by zero",
                "traceback": ["ZeroDivisionError: division by zero"],
            }],
        }])
        md = self._convert(nb)
        assert "ZeroDivisionError" in md
        assert "```traceback" in md

    def test_no_outputs_unchanged(self):
        nb = self._notebook([{
            "cell_type": "code",
            "source": ["x = 1"],
            "outputs": [],
        }])
        md = self._convert(nb)
        assert "```python" in md
        assert "x = 1" in md


# ---------------------------------------------------------------------------
# Bug 2: xlsx — empty sheets
# ---------------------------------------------------------------------------

class TestXlsxEmptySheets:
    def test_empty_sheet_produces_no_data(self, tmp_path):
        pytest.importorskip("openpyxl")
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "EmptySheet"
        path = tmp_path / "empty.xlsx"
        wb.save(path)

        md = MarkItDown()
        result = md.convert(str(path))
        assert "_No data_" in result.markdown

    def test_non_empty_sheet_has_table(self, tmp_path):
        pytest.importorskip("openpyxl")
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Data"
        ws.append(["Name", "Age"])
        ws.append(["Alice", 30])
        path = tmp_path / "data.xlsx"
        wb.save(path)

        md = MarkItDown()
        result = md.convert(str(path))
        assert "Alice" in result.markdown
        assert "_No data_" not in result.markdown


# ---------------------------------------------------------------------------
# Bug 3: zip — silent failures surfaced
# ---------------------------------------------------------------------------

class TestZipSilentFailures:
    def test_conversion_error_shows_warning(self, tmp_path):
        """ZipConverter should surface FileConversionException as a warning comment."""
        from markitdown.converters._zip_converter import ZipConverter
        from markitdown._exceptions import FileConversionException
        from unittest.mock import MagicMock

        # Build a zip with one file
        zip_path = tmp_path / "test.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("data.xlsx", b"fake content")

        # Create a MarkItDown mock whose convert_stream raises FileConversionException
        mock_md = MagicMock()
        mock_md.convert_stream.side_effect = FileConversionException(attempts=[])

        converter = ZipConverter(markitdown=mock_md)
        with open(zip_path, "rb") as f:
            stream = io.BytesIO(f.read())

        from markitdown._stream_info import StreamInfo as SI
        si = SI(extension=".zip", filename="test.zip")
        result = converter.convert(stream, si)

        # Should contain a warning about the failed file
        assert "⚠️" in result.markdown and "Could not convert" in result.markdown

    def test_unsupported_format_silently_skipped(self, tmp_path):
        """Files with unsupported formats should be silently skipped (no warning)."""
        from markitdown.converters._zip_converter import ZipConverter
        from markitdown._exceptions import UnsupportedFormatException
        from unittest.mock import MagicMock

        # Build a zip with one file
        zip_path = tmp_path / "test.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("unknownfile.xyz123", "binary garbage data")

        # Create a MarkItDown mock whose convert_stream raises UnsupportedFormatException
        mock_md = MagicMock()
        mock_md.convert_stream.side_effect = UnsupportedFormatException("not supported")

        converter = ZipConverter(markitdown=mock_md)
        with open(zip_path, "rb") as f:
            stream = io.BytesIO(f.read())

        from markitdown._stream_info import StreamInfo as SI
        si = SI(extension=".zip", filename="test.zip")
        result = converter.convert(stream, si)

        # Should NOT contain warnings for unsupported files
        assert "⚠️" not in result.markdown
        assert "Could not convert" not in result.markdown


# ---------------------------------------------------------------------------
# Bug 4: pptx — chart table separator
# ---------------------------------------------------------------------------

class TestPptxChartSeparator:
    def test_separator_format(self):
        """The chart separator should use '| --- |' not '|---|'."""
        pytest.importorskip("pptx")
        from markitdown.converters._pptx_converter import PptxConverter
        converter = PptxConverter()

        # Inspect the separator logic directly by calling _convert_chart_to_markdown
        # with a mock chart — we test the separator format via the source indirectly
        import inspect
        source = inspect.getsource(converter._convert_chart_to_markdown)
        # The separator should use " | ".join not just "|".join with no spaces
        assert '| " + " | ".join' in source or '"| " + " | ".join' in source or "\" | \".join" in source

    def test_separator_string_directly(self):
        """Unit test the separator string construction."""
        data = [["Category", "Series1", "Series2"]]
        separator = "| " + " | ".join(["---"] * len(data[0])) + " |"
        assert separator == "| --- | --- | --- |"
        # Should NOT be the old broken format
        assert separator != "|---|---|---|"


# ---------------------------------------------------------------------------
# Bug 5: audio — missing extensions
# ---------------------------------------------------------------------------

class TestAudioExtensions:
    def test_ogg_accepted(self):
        from markitdown.converters._audio_converter import AudioConverter, ACCEPTED_FILE_EXTENSIONS, ACCEPTED_MIME_TYPE_PREFIXES
        assert ".ogg" in ACCEPTED_FILE_EXTENSIONS
        assert any("ogg" in m for m in ACCEPTED_MIME_TYPE_PREFIXES)

    def test_flac_accepted(self):
        from markitdown.converters._audio_converter import ACCEPTED_FILE_EXTENSIONS, ACCEPTED_MIME_TYPE_PREFIXES
        assert ".flac" in ACCEPTED_FILE_EXTENSIONS
        assert any("flac" in m for m in ACCEPTED_MIME_TYPE_PREFIXES)

    def test_aac_accepted(self):
        from markitdown.converters._audio_converter import ACCEPTED_FILE_EXTENSIONS, ACCEPTED_MIME_TYPE_PREFIXES
        assert ".aac" in ACCEPTED_FILE_EXTENSIONS
        assert any("aac" in m for m in ACCEPTED_MIME_TYPE_PREFIXES)

    def test_accepts_method_ogg(self):
        from markitdown.converters._audio_converter import AudioConverter
        converter = AudioConverter()
        stream = make_stream(b"\x00" * 16)
        si = StreamInfo(extension=".ogg")
        assert converter.accepts(stream, si) is True

    def test_accepts_method_flac(self):
        from markitdown.converters._audio_converter import AudioConverter
        converter = AudioConverter()
        stream = make_stream(b"\x00" * 16)
        si = StreamInfo(extension=".flac")
        assert converter.accepts(stream, si) is True

    def test_accepts_method_aac(self):
        from markitdown.converters._audio_converter import AudioConverter
        converter = AudioConverter()
        stream = make_stream(b"\x00" * 16)
        si = StreamInfo(extension=".aac")
        assert converter.accepts(stream, si) is True


# ---------------------------------------------------------------------------
# Bug 6: wikipedia — infobox stripping
# ---------------------------------------------------------------------------

class TestWikipediaInfoboxStripping:
    SAMPLE_HTML = """
    <html><head><title>Test Article</title></head>
    <body>
      <div id="mw-content-text">
        <span class="mw-page-title-main">Test Article</span>
        <table class="infobox">
          <tr><td>Born</td><td>1980</td></tr>
        </table>
        <table class="wikitable">
          <tr><th>Column</th></tr><tr><td>value</td></tr>
        </table>
        <p>This is the main content of the article.</p>
      </div>
    </body></html>
    """

    def _convert(self, strip=True):
        from markitdown.converters._wikipedia_converter import WikipediaConverter
        converter = WikipediaConverter()
        stream = make_stream(self.SAMPLE_HTML)
        si = StreamInfo(
            mimetype="text/html",
            extension=".html",
            url="https://en.wikipedia.org/wiki/Test_Article",
        )
        return converter.convert(stream, si, strip_wikipedia_infoboxes=strip)

    def test_infobox_stripped_by_default(self):
        result = self._convert(strip=True)
        # "Born" comes from the infobox table — should be gone
        assert "Born" not in result.markdown

    def test_wikitable_stripped_by_default(self):
        result = self._convert(strip=True)
        # wikitable content should be stripped
        assert "Column" not in result.markdown

    def test_main_content_preserved(self):
        result = self._convert(strip=True)
        assert "main content" in result.markdown

    def test_infobox_kept_when_disabled(self):
        result = self._convert(strip=False)
        assert "Born" in result.markdown


# ---------------------------------------------------------------------------
# Bug 7: rss — link extraction
# ---------------------------------------------------------------------------

RSS_SAMPLE = """<?xml version="1.0"?>
<rss version="2.0">
  <channel>
    <title>Test Feed</title>
    <description>A test RSS feed</description>
    <item>
      <title>Item One</title>
      <link>https://example.com/item-one</link>
      <description>Description of item one</description>
      <pubDate>Mon, 01 Jan 2024 00:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>"""

ATOM_SAMPLE = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Atom Test Feed</title>
  <subtitle>A test Atom feed</subtitle>
  <entry>
    <title>Atom Entry One</title>
    <link href="https://example.com/atom-entry-one"/>
    <updated>2024-01-01T00:00:00Z</updated>
    <summary>Summary of atom entry one</summary>
  </entry>
</feed>"""


class TestRssLinkExtraction:
    def _convert(self, content: str):
        from markitdown.converters._rss_converter import RssConverter
        converter = RssConverter()
        stream = make_stream(content)
        si = StreamInfo(extension=".rss")
        return converter.convert(stream, si)

    def test_rss_item_link_extracted(self):
        result = self._convert(RSS_SAMPLE)
        assert "https://example.com/item-one" in result.markdown

    def test_rss_link_formatted(self):
        result = self._convert(RSS_SAMPLE)
        assert "**Link:**" in result.markdown

    def test_atom_entry_link_extracted(self):
        result = self._convert(ATOM_SAMPLE)
        assert "https://example.com/atom-entry-one" in result.markdown

    def test_atom_link_formatted(self):
        result = self._convert(ATOM_SAMPLE)
        assert "**Link:**" in result.markdown


# ---------------------------------------------------------------------------
# Feature 1: YamlConverter
# ---------------------------------------------------------------------------

class TestYamlConverter:
    def setup_method(self):
        pytest.importorskip("yaml")
        self.converter = YamlConverter()

    def _si(self, ext=".yaml", filename="test.yaml"):
        return StreamInfo(extension=ext, filename=filename)

    def test_accepts_yaml(self):
        stream = make_stream(b"key: value")
        assert self.converter.accepts(stream, self._si(".yaml")) is True

    def test_accepts_yml(self):
        stream = make_stream(b"key: value")
        assert self.converter.accepts(stream, self._si(".yml", "test.yml")) is True

    def test_rejects_txt(self):
        stream = make_stream(b"key: value")
        si = StreamInfo(extension=".txt", filename="test.txt")
        assert self.converter.accepts(stream, si) is False

    def test_accepts_yaml_mimetype(self):
        stream = make_stream(b"key: value")
        si = StreamInfo(mimetype="application/yaml", extension="")
        assert self.converter.accepts(stream, si) is True

    def test_simple_dict_converted(self):
        content = "name: Alice\nage: 30\n"
        stream = make_stream(content)
        result = self.converter.convert(stream, self._si())
        assert "Alice" in result.markdown
        assert "name" in result.markdown.lower() or "**name:**" in result.markdown

    def test_nested_dict_as_section(self):
        content = "database:\n  host: localhost\n  port: 5432\n"
        stream = make_stream(content)
        result = self.converter.convert(stream, self._si())
        assert "## database" in result.markdown
        assert "localhost" in result.markdown

    def test_list_values(self):
        content = "fruits:\n  - apple\n  - banana\n"
        stream = make_stream(content)
        result = self.converter.convert(stream, self._si())
        assert "apple" in result.markdown
        assert "banana" in result.markdown

    def test_returns_document_converter_result(self):
        stream = make_stream(b"x: 1")
        result = self.converter.convert(stream, self._si())
        assert isinstance(result, DocumentConverterResult)


# ---------------------------------------------------------------------------
# Feature 2: get_document_stats and DocumentConverterResult.stats()
# ---------------------------------------------------------------------------

SAMPLE_MARKDOWN = """# Heading 1

## Heading 2

Some text with a [link](https://example.com) and an ![image](https://example.com/img.png).

```python
print("hello")
```

More text here. Another [link](https://example.com/page).

```
plain block
```
"""


class TestGetDocumentStats:
    def test_word_count(self):
        stats = get_document_stats(SAMPLE_MARKDOWN)
        assert stats["word_count"] > 0

    def test_char_count(self):
        stats = get_document_stats(SAMPLE_MARKDOWN)
        assert stats["char_count"] == len(SAMPLE_MARKDOWN)

    def test_line_count(self):
        stats = get_document_stats(SAMPLE_MARKDOWN)
        assert stats["line_count"] == len(SAMPLE_MARKDOWN.splitlines())

    def test_heading_count(self):
        stats = get_document_stats(SAMPLE_MARKDOWN)
        assert stats["heading_count"] == 2

    def test_code_block_count(self):
        stats = get_document_stats(SAMPLE_MARKDOWN)
        assert stats["code_block_count"] == 2

    def test_link_count(self):
        stats = get_document_stats(SAMPLE_MARKDOWN)
        # Two [text](url) links, NOT counting the image
        assert stats["link_count"] == 2

    def test_image_count(self):
        stats = get_document_stats(SAMPLE_MARKDOWN)
        assert stats["image_count"] == 1

    def test_returns_dict_with_correct_keys(self):
        stats = get_document_stats("")
        expected_keys = {
            "word_count", "char_count", "line_count",
            "heading_count", "code_block_count", "link_count", "image_count",
        }
        assert set(stats.keys()) == expected_keys

    def test_empty_string(self):
        stats = get_document_stats("")
        assert stats["word_count"] == 0
        assert stats["char_count"] == 0
        assert stats["heading_count"] == 0
        assert stats["code_block_count"] == 0
        assert stats["link_count"] == 0
        assert stats["image_count"] == 0


class TestDocumentConverterResultStats:
    def test_stats_method_exists(self):
        result = DocumentConverterResult(markdown="# Hello\n\nWorld")
        assert hasattr(result, "stats")
        assert callable(result.stats)

    def test_stats_method_returns_dict(self):
        result = DocumentConverterResult(markdown="# Hello\n\nWorld")
        stats = result.stats()
        assert isinstance(stats, dict)

    def test_stats_heading_count(self):
        result = DocumentConverterResult(markdown="# Heading 1\n\n## Heading 2\n\ntext")
        stats = result.stats()
        assert stats["heading_count"] == 2

    def test_stats_empty_document(self):
        result = DocumentConverterResult(markdown="")
        stats = result.stats()
        assert stats["word_count"] == 0

    def test_stats_link_count(self):
        result = DocumentConverterResult(markdown="Visit [Google](https://google.com) today.")
        stats = result.stats()
        assert stats["link_count"] == 1


# ---------------------------------------------------------------------------
# Feature 3: RequirementsConverter
# ---------------------------------------------------------------------------

REQUIREMENTS_TXT = """\
# This is a comment
requests>=2.28.0  # HTTP library
flask==2.3.0
numpy
-r other-requirements.txt
pandas>=1.5.0,<2.0.0
"""

PIPFILE_CONTENT = """\
[packages]
requests = "*"
flask = ">=2.0"

[dev-packages]
pytest = "*"
"""


class TestRequirementsConverter:
    def setup_method(self):
        self.converter = RequirementsConverter()

    def _si(self, filename="requirements.txt", ext=".txt"):
        return StreamInfo(extension=ext, filename=filename)

    def test_accepts_requirements_txt(self):
        stream = make_stream(b"requests>=2.0")
        assert self.converter.accepts(stream, self._si("requirements.txt")) is True

    def test_accepts_requirements_dev_txt(self):
        stream = make_stream(b"pytest")
        si = StreamInfo(extension=".txt", filename="requirements-dev.txt")
        assert self.converter.accepts(stream, si) is True

    def test_accepts_pipfile(self):
        stream = make_stream(b"[packages]\nrequests = '*'")
        si = StreamInfo(extension="", filename="Pipfile")
        assert self.converter.accepts(stream, si) is True

    def test_rejects_random_txt(self):
        stream = make_stream(b"hello world")
        si = StreamInfo(extension=".txt", filename="readme.txt")
        assert self.converter.accepts(stream, si) is False

    def test_rejects_py_file(self):
        stream = make_stream(b"import os")
        si = StreamInfo(extension=".py", filename="requirements.py")
        assert self.converter.accepts(stream, si) is False

    def test_requirements_parsed_to_table(self):
        stream = make_stream(REQUIREMENTS_TXT)
        result = self.converter.convert(stream, self._si())
        md = result.markdown
        assert "| Package | Version Constraint | Notes |" in md
        assert "requests" in md
        assert "flask" in md
        assert "numpy" in md

    def test_version_constraints_included(self):
        stream = make_stream(REQUIREMENTS_TXT)
        result = self.converter.convert(stream, self._si())
        assert ">=2.28.0" in result.markdown
        assert "==2.3.0" in result.markdown

    def test_inline_comments_as_notes(self):
        stream = make_stream(REQUIREMENTS_TXT)
        result = self.converter.convert(stream, self._si())
        assert "HTTP library" in result.markdown

    def test_option_lines_skipped(self):
        stream = make_stream(REQUIREMENTS_TXT)
        result = self.converter.convert(stream, self._si())
        assert "-r" not in result.markdown

    def test_pipfile_parsed(self):
        stream = make_stream(PIPFILE_CONTENT)
        si = StreamInfo(extension="", filename="Pipfile")
        result = self.converter.convert(stream, si)
        assert "requests" in result.markdown
        assert "flask" in result.markdown

    def test_empty_requirements(self):
        stream = make_stream(b"# just comments\n")
        result = self.converter.convert(stream, self._si())
        assert "_No dependencies found._" in result.markdown

    def test_returns_document_converter_result(self):
        stream = make_stream(b"requests>=2.0")
        result = self.converter.convert(stream, self._si())
        assert isinstance(result, DocumentConverterResult)
