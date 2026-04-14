"""
Tests for new features added by Maishad Hassan (maishad777):
  - TOML converter
  - Sitemap converter
  - .env converter
  - CSV pipe-escape bug fix
  - HTML metadata extraction
"""
import io
import pytest
from markitdown import MarkItDown
from markitdown._stream_info import StreamInfo
from markitdown.converters._toml_converter import TomlConverter
from markitdown.converters._sitemap_converter import SitemapConverter
from markitdown.converters._env_converter import EnvConverter
from markitdown.converters._csv_converter import CsvConverter, _escape_cell


# ─── TOML Converter ──────────────────────────────────────────────────────────

SAMPLE_TOML = b"""
[project]
name = "my-app"
version = "1.0.0"
description = "A sample project"

[dependencies]
requests = "^2.31"
fastapi = "^0.110"

[tool.ruff]
line-length = 100
"""

def test_toml_converter_accepts():
    conv = TomlConverter()
    stream = io.BytesIO(SAMPLE_TOML)
    info = StreamInfo(mimetype="application/toml", extension=".toml", filename="pyproject.toml")
    assert conv.accepts(stream, info)

def test_toml_converter_output():
    conv = TomlConverter()
    stream = io.BytesIO(SAMPLE_TOML)
    info = StreamInfo(mimetype="application/toml", extension=".toml", filename="pyproject.toml")
    result = conv.convert(stream, info)
    assert "my-app" in result.markdown
    assert "dependencies" in result.markdown.lower()
    assert "requests" in result.markdown

def test_toml_converter_rejects_non_toml():
    conv = TomlConverter()
    stream = io.BytesIO(b"hello world")
    info = StreamInfo(mimetype="text/plain", extension=".txt")
    assert not conv.accepts(stream, info)


# ─── Sitemap Converter ───────────────────────────────────────────────────────

SAMPLE_SITEMAP = b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-01</lastmod>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://example.com/about</loc>
    <lastmod>2024-02-01</lastmod>
    <priority>0.8</priority>
  </url>
</urlset>
"""

def test_sitemap_converter_accepts():
    conv = SitemapConverter()
    stream = io.BytesIO(SAMPLE_SITEMAP)
    info = StreamInfo(mimetype="text/xml", extension=".xml", url="https://example.com/sitemap.xml")
    assert conv.accepts(stream, info)

def test_sitemap_converter_output():
    conv = SitemapConverter()
    stream = io.BytesIO(SAMPLE_SITEMAP)
    info = StreamInfo(mimetype="text/xml", extension=".xml", url="https://example.com/sitemap.xml")
    result = conv.convert(stream, info)
    assert "https://example.com/" in result.markdown
    assert "https://example.com/about" in result.markdown
    assert "2024-01-01" in result.markdown

def test_sitemap_converter_index():
    sitemap_index = b"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-posts.xml</loc>
    <lastmod>2024-01-01</lastmod>
  </sitemap>
</sitemapindex>
"""
    conv = SitemapConverter()
    stream = io.BytesIO(sitemap_index)
    info = StreamInfo(mimetype="text/xml", extension=".xml", url="https://example.com/sitemap.xml")
    result = conv.convert(stream, info)
    assert "sitemap-posts.xml" in result.markdown
    assert "Index" in result.markdown


# ─── .env Converter ──────────────────────────────────────────────────────────

SAMPLE_ENV = b"""# Database configuration
DATABASE_URL=postgres://user:password@localhost/mydb
SECRET_KEY=supersecretkey123
DEBUG=false
PORT=3000
EMPTY_VAR=
"""

def test_env_converter_accepts():
    conv = EnvConverter()
    stream = io.BytesIO(SAMPLE_ENV)
    info = StreamInfo(extension=".env", filename=".env")
    assert conv.accepts(stream, info)

def test_env_converter_masks_values_by_default():
    conv = EnvConverter()
    stream = io.BytesIO(SAMPLE_ENV)
    info = StreamInfo(extension=".env", filename=".env")
    result = conv.convert(stream, info)
    assert "supersecretkey123" not in result.markdown
    assert "DATABASE_URL" in result.markdown
    assert "SECRET_KEY" in result.markdown
    assert "⚠️" in result.markdown

def test_env_converter_shows_values_when_flag_set():
    conv = EnvConverter()
    stream = io.BytesIO(SAMPLE_ENV)
    info = StreamInfo(extension=".env", filename=".env")
    result = conv.convert(stream, info, show_values=True)
    assert "false" in result.markdown  # DEBUG=false
    assert "3000" in result.markdown   # PORT=3000

def test_env_converter_comment_extraction():
    conv = EnvConverter()
    stream = io.BytesIO(SAMPLE_ENV)
    info = StreamInfo(extension=".env", filename=".env")
    result = conv.convert(stream, info)
    assert "Database configuration" in result.markdown


# ─── CSV pipe-escape bug fix ─────────────────────────────────────────────────

def test_escape_cell_pipes():
    assert _escape_cell("foo|bar") == "foo\\|bar"

def test_escape_cell_newlines():
    assert "\n" not in _escape_cell("line1\nline2")
    assert "\r" not in _escape_cell("line1\r\nline2")

def test_csv_with_pipes_in_data():
    conv = CsvConverter()
    csv_data = b"Name,Value\nFoo|Bar,123\nHello,World"
    stream = io.BytesIO(csv_data)
    info = StreamInfo(mimetype="text/csv", extension=".csv", charset="utf-8")
    result = conv.convert(stream, info)
    # The pipe in "Foo|Bar" must be escaped so the table stays valid
    assert "Foo\\|Bar" in result.markdown

def test_csv_with_multiline_cell():
    conv = CsvConverter()
    csv_data = "Name,Description\n\"Alice\",\"Line1\nLine2\"\n".encode("utf-8")
    stream = io.BytesIO(csv_data)
    info = StreamInfo(mimetype="text/csv", extension=".csv", charset="utf-8")
    result = conv.convert(stream, info)
    lines = result.markdown.splitlines()
    # Every non-empty line should start with |
    for line in lines:
        if line.strip():
            assert line.startswith("|"), f"Broken table row: {line!r}"


# ─── HTML metadata extraction ─────────────────────────────────────────────────

SAMPLE_HTML = b"""<!DOCTYPE html>
<html>
<head>
  <title>Test Page</title>
  <meta property="og:title" content="Open Graph Title">
  <meta property="og:description" content="OG Description here">
  <meta name="author" content="Maishad Hassan">
  <meta name="keywords" content="python, markdown, converter">
</head>
<body>
<h1>Hello World</h1>
<p>Some content here.</p>
</body>
</html>
"""

def test_html_metadata_extraction():
    from markitdown.converters._html_converter import HtmlConverter
    conv = HtmlConverter()
    stream = io.BytesIO(SAMPLE_HTML)
    info = StreamInfo(mimetype="text/html", extension=".html")
    result = conv.convert(stream, info, include_html_metadata=True)
    assert "og:title" in result.markdown
    assert "Open Graph Title" in result.markdown
    assert "Maishad Hassan" in result.markdown

def test_html_no_metadata_by_default():
    from markitdown.converters._html_converter import HtmlConverter
    conv = HtmlConverter()
    stream = io.BytesIO(SAMPLE_HTML)
    info = StreamInfo(mimetype="text/html", extension=".html")
    result = conv.convert(stream, info)
    # Metadata block should NOT appear without the flag
    assert "og:title" not in result.markdown
    # But content should still be there
    assert "Hello World" in result.markdown
