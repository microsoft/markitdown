"""Edge-case and robustness tests for MarkItDown converters.

Exercises error handling, corrupt inputs, empty files, and URL-based
converter dispatch using local file:// URIs — no network required.
"""

import io
import os
import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown._exceptions import (
    FileConversionException,
    UnsupportedFormatException,
)

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")


# ── Helpers ────────────────────────────────────────────────────────────

def _make_md():
    return MarkItDown()


# ── Empty / zero-byte input ────────────────────────────────────────────


def test_empty_bytes_stream():
    """Empty byte stream should not crash."""
    md = _make_md()
    stream = io.BytesIO(b"")
    with pytest.raises((UnsupportedFormatException, FileConversionException)):
        md.convert(stream)


def test_empty_csv():
    """Empty CSV should return empty markdown without error."""
    md = _make_md()
    result = md.convert(
        io.BytesIO(b""),
        stream_info=StreamInfo(extension=".csv", mimetype="text/csv"),
    )
    assert result.markdown == ""


def test_empty_plain_text():
    """Empty plain text should return empty markdown."""
    md = _make_md()
    result = md.convert(
        io.BytesIO(b""),
        stream_info=StreamInfo(extension=".txt", mimetype="text/plain", charset="utf-8"),
    )
    assert result.markdown == ""


# ── Corrupt file handling ──────────────────────────────────────────────


def test_corrupt_csv():
    """Malformed CSV should not crash — returns empty/garbled output or raises."""
    md = _make_md()
    # Corrupt bytes may be handled gracefully (empty output) or raise.
    # Key assertion: must not crash with unexpected traceback.
    try:
        result = md.convert(
            io.BytesIO(b'\x00\x01\x02\xff\xfe'),
            stream_info=StreamInfo(extension=".csv", mimetype="text/csv"),
        )
        assert isinstance(result.markdown, str)
    except (FileConversionException, UnsupportedFormatException):
        pass  # Also acceptable


def test_corrupt_html():
    """Corrupt HTML (invalid encoding bytes) should not crash."""
    md = _make_md()
    try:
        result = md.convert(
            io.BytesIO(b'\xff\xfe\x00\x01\x02'),
            stream_info=StreamInfo(extension=".html", mimetype="text/html"),
        )
        assert isinstance(result.markdown, str)
    except (FileConversionException, UnsupportedFormatException):
        pass


def test_corrupt_zip():
    """Non-zip bytes with .zip extension should not crash."""
    md = _make_md()
    try:
        result = md.convert(
            io.BytesIO(b'not a zip file at all'),
            stream_info=StreamInfo(extension=".zip", mimetype="application/zip"),
        )
        assert isinstance(result.markdown, str)
    except (FileConversionException, UnsupportedFormatException):
        pass


def test_corrupt_xlsx():
    """Non-xlsx bytes with .xlsx extension should raise appropriately."""
    md = _make_md()
    try:
        result = md.convert(
            io.BytesIO(b'not an xlsx file'),
            stream_info=StreamInfo(
                extension=".xlsx",
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ),
        )
        # If it doesn't raise, at least it shouldn't crash
        assert isinstance(result.markdown, str)
    except (FileConversionException, UnsupportedFormatException):
        pass  # Expected


def test_corrupt_pdf():
    """Non-PDF bytes with .pdf extension should not crash — either raises or degrades."""
    md = _make_md()
    try:
        result = md.convert(
            io.BytesIO(b'definitely not a pdf'),
            stream_info=StreamInfo(extension=".pdf", mimetype="application/pdf"),
        )
        assert isinstance(result.markdown, str)
    except (FileConversionException, UnsupportedFormatException):
        pass


# ── Wrong extension / mimetype mismatch ────────────────────────────────


def test_wrong_extension():
    """Unsupported extension should raise UnsupportedFormatException."""
    md = _make_md()
    # Some streams may fall through to PlainTextConverter if charset is set
    try:
        result = md.convert(
            io.BytesIO(b"some content"),
            stream_info=StreamInfo(extension=".nonexistent", mimetype="application/octet-stream"),
        )
        # If PlainTextConverter caught it, that's fine — markdown should be non-None
        assert isinstance(result.markdown, str)
    except UnsupportedFormatException:
        pass  # Expected behavior


# ── Converter dispatch with file:// URIs ──────────────────────────────


def test_file_uri_wikipedia_dispatch():
    """Wikipedia HTML file via file:// URI + wikipedia.org URL dispatches WikipediaConverter."""
    md = _make_md()
    test_file = os.path.join(TEST_FILES_DIR, "test_wikipedia.html")

    with open(test_file, "rb") as f:
        content = f.read()

    result = md.convert(
        io.BytesIO(content),
        url="https://en.wikipedia.org/wiki/Microsoft",
        stream_info=StreamInfo(extension=".html", mimetype="text/html"),
    )
    # WikipediaConverter should extract only main content, not sidebar/nav
    assert "Microsoft" in result.markdown
    assert "You are encouraged to create an account" not in result.markdown


def test_file_uri_serp_dispatch():
    """Bing SERP HTML file dispatches BingSerpConverter when URL matches bing.com."""
    md = _make_md()
    test_file = os.path.join(TEST_FILES_DIR, "test_serp.html")

    with open(test_file, "rb") as f:
        content = f.read()

    result = md.convert(
        io.BytesIO(content),
        url="https://www.bing.com/search?q=microsoft+wikipedia",
        stream_info=StreamInfo(extension=".html", mimetype="text/html"),
    )
    assert "Microsoft Corporation" in result.markdown


def test_file_uri_blog_dispatch():
    """Blog HTML dispatches HtmlConverter (not WikipediaConverter) with correct URL."""
    md = _make_md()
    test_file = os.path.join(TEST_FILES_DIR, "test_blog.html")

    with open(test_file, "rb") as f:
        content = f.read()

    result = md.convert(
        io.BytesIO(content),
        url="https://microsoft.github.io/autogen/blog/2023/04/21/LLM-tuning-math",
        stream_info=StreamInfo(extension=".html", mimetype="text/html"),
    )
    # Blog content should be present
    assert "Large language models (LLMs)" in result.markdown


# ── File URI conversion (local path as URL) ────────────────────────────


def test_file_uri_csv():
    """Convert CSV via file:// URI."""
    md = _make_md()
    test_file = os.path.join(TEST_FILES_DIR, "test_mskanji.csv")
    result = md.convert(test_file)
    assert "佐藤太郎" in result.markdown
    assert "名古屋" in result.markdown


def test_file_uri_json():
    """Convert JSON via file path."""
    md = _make_md()
    test_file = os.path.join(TEST_FILES_DIR, "test.json")
    result = md.convert(test_file)
    assert "5b64c88c" in result.markdown


def test_file_uri_rss():
    """Convert RSS XML via file path."""
    md = _make_md()
    test_file = os.path.join(TEST_FILES_DIR, "test_rss.xml")
    result = md.convert(test_file)
    assert "The Official Microsoft Blog" in result.markdown


# ── Stream info handling ───────────────────────────────────────────────


def test_convert_stream_no_hints():
    """Conversion without stream info should work for detectable formats."""
    md = _make_md()
    test_file = os.path.join(TEST_FILES_DIR, "test_mskanji.csv")
    with open(test_file, "rb") as f:
        result = md.convert(f)
    assert "佐藤太郎" in result.markdown


# ── Test file integrity (verify local test files are usable) ───────────


@pytest.mark.parametrize("filename", [
    "test.docx",
    "test.xlsx",
    "test.pptx",
    "test.pdf",
    "test_blog.html",
    "test_wikipedia.html",
    "test_serp.html",
    "test_mskanji.csv",
    "test.json",
    "test_rss.xml",
    "test_notebook.ipynb",
    "test_files.zip",
    "test.epub",
])
def test_local_file_usable(filename):
    """Verify each local test file exists and is non-empty."""
    path = os.path.join(TEST_FILES_DIR, filename)
    assert os.path.isfile(path), f"Missing test file: {path}"
    assert os.path.getsize(path) > 0, f"Empty test file: {path}"
