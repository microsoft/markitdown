import io
import pytest
from markitdown.converters._html_converter import HtmlConverter
from markitdown._stream_info import StreamInfo

# Sample HTML to test selector scoping
SAMPLE_HTML = """
<html>
  <body>
    <header>Skip Me</header>
    <article class="entry">
      <h1>Title</h1>
      <p>Body text.</p>
    </article>
    <footer>Also Skip</footer>
  </body>
</html>
"""


def test_selector_extracts_only_matching_nodes():
    converter = HtmlConverter()
    # Use the convenience method to convert a string with selector
    result = converter.convert_string(SAMPLE_HTML, selector="article.entry")
    md = result.markdown
    # Print the markdown for inspection
    print("\n--- Extracted Markdown (test_selector_extracts_only_matching_nodes) ---\n")
    print(md)
    # Only the article content should appear
    assert "Title" in md
    assert "Body text." in md
    assert "Skip Me" not in md
    assert "Also Skip" not in md


def test_selector_no_match_raises():
    converter = HtmlConverter()
    # Non-existing selector should raise a ValueError
    with pytest.raises(ValueError):
        converter.convert_string(SAMPLE_HTML, selector=".does-not-exist")


def test_no_selector_returns_full_content():
    converter = HtmlConverter()
    # Without selector, header and footer should remain
    result = converter.convert_string(SAMPLE_HTML)
    md = result.markdown
    # Print the markdown for inspection
    print("\n--- Extracted Markdown (test_no_selector_returns_full_content) ---\n")
    print(md)
    assert "Skip Me" in md
    assert "Title" in md
    assert "Body text." in md
    assert "Also Skip" in md


def test_convert_method_with_stream_and_selector():
    converter = HtmlConverter()
    html_bytes = SAMPLE_HTML.encode("utf-8")
    stream = io.BytesIO(html_bytes)
    stream_info = StreamInfo(
        mimetype="text/html",
        extension=".html",
        charset="utf-8",
        url=None,
    )
    # Directly call convert(), passing selector
    result = converter.convert(stream, stream_info, selector="article.entry")
    md = result.markdown
    # Print the markdown for inspection
    print("\n--- Extracted Markdown (test_convert_method_with_stream_and_selector) ---\n")
    print(md)
    assert "Title" in md
    assert "Body text." in md
    assert "Skip Me" not in md
    assert "Also Skip" not in md
