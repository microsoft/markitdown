import io

from markitdown import MarkItDown


def _convert_html(html: str, **kwargs) -> str:
    result = MarkItDown().convert_stream(
        io.BytesIO(html.encode("utf-8")),
        file_extension=".html",
        **kwargs,
    )
    return result.markdown


def test_preserves_non_utf8_percent_encoded_href_path() -> None:
    href = "https://abc.com/hist/" "%a5%c8%a5%c3%a5%d7%a5%da%a1%bc%a5%b8"
    html = f'<a href="{href}">example</a>'

    markdown = _convert_html(html)

    assert f"[example]({href})" in markdown
    assert "%EF%BF%BD" not in markdown


def test_html_href_still_quotes_raw_unicode_and_spaces() -> None:
    href = "https://example.com/a path/日本語"
    expected_href = "https://example.com/a%20path/" "%E6%97%A5%E6%9C%AC%E8%AA%9E"

    markdown = _convert_html(f'<a href="{href}">example</a>')

    assert f"[example]({expected_href})" in markdown


def test_html_href_quotes_literal_percent_sign() -> None:
    href = "https://example.com/100% complete"
    expected_href = "https://example.com/100%25%20complete"

    markdown = _convert_html(f'<a href="{href}">example</a>')

    assert f"[example]({expected_href})" in markdown


def test_html_href_quotes_malformed_percent_escape() -> None:
    href = "https://example.com/items/%ZZ/%2F"
    expected_href = "https://example.com/items/%25ZZ/%2F"

    markdown = _convert_html(f'<a href="{href}">example</a>')

    assert f"[example]({expected_href})" in markdown


def test_html_href_preserves_encoded_slash() -> None:
    href = "https://example.com/items/a%2Fb"

    markdown = _convert_html(f'<a href="{href}">example</a>')

    assert f"[example]({href})" in markdown


def test_html_href_does_not_quote_query_or_fragment() -> None:
    href = "https://example.com/a path?query=a b%20c#fragment with spaces"
    expected_href = "https://example.com/a%20path?query=a b%20c#fragment with spaces"

    markdown = _convert_html(f'<a href="{href}">example</a>')

    assert f"[example]({expected_href})" in markdown


def test_img_prefers_data_src_over_placeholder_data_uri() -> None:
    placeholder = (
        "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBTAA7"
    )
    real_src = "https://example.com/photo.jpg"
    html = (
        f'<img src="{placeholder}" data-src="{real_src}" alt="A photo" loading="lazy">'
    )

    markdown = _convert_html(html)

    assert f"![A photo]({real_src})" in markdown
    assert placeholder not in markdown


def test_img_uses_real_src_over_data_src_when_both_present() -> None:
    real_src = "https://example.com/photo.jpg"
    other_src = "https://example.com/photo-alt.jpg"
    html = f'<img src="{real_src}" data-src="{other_src}" alt="A photo">'

    markdown = _convert_html(html)

    assert f"![A photo]({real_src})" in markdown


def test_img_falls_back_to_data_src_when_src_missing() -> None:
    real_src = "https://example.com/photo.jpg"
    html = f'<img data-src="{real_src}" alt="A photo">'

    markdown = _convert_html(html)

    assert f"![A photo]({real_src})" in markdown


def test_img_keeps_truncated_data_uri_when_no_data_src() -> None:
    placeholder = (
        "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBTAA7"
    )
    html = f'<img src="{placeholder}" alt="A photo">'

    markdown = _convert_html(html)

    assert "![A photo](data:image/gif;base64...)" in markdown


def test_img_keeps_embedded_data_uri_over_data_src_when_keeping_data_uris() -> None:
    embedded = (
        "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBTAA7"
    )
    other_src = "https://example.com/photo.jpg"
    html = f'<img src="{embedded}" data-src="{other_src}" alt="A photo">'

    markdown = _convert_html(html, keep_data_uris=True)

    assert f"![A photo]({embedded})" in markdown
    assert other_src not in markdown


def test_html_table_pipe_in_cell_is_escaped() -> None:
    # Issue #2438: a literal | in a cell is data, not a column separator.
    html = (
        "<table><thead><tr><th>Name</th><th>Note</th></tr></thead>"
        "<tbody><tr><td>Alice</td><td>Has a | pipe</td></tr></tbody></table>"
    )

    markdown = _convert_html(html)

    assert "| Alice | Has a \\| pipe |" in markdown


def test_html_table_pipe_in_header_is_escaped() -> None:
    html = (
        "<table><thead><tr><th>a | b</th><th>c</th></tr></thead>"
        "<tbody><tr><td>1</td><td>2</td></tr></tbody></table>"
    )

    markdown = _convert_html(html)

    assert "| a \\| b | c |" in markdown


def test_html_table_pipe_preceded_by_backslash_is_still_escaped() -> None:
    # Same rule as CSV: double the backslash run so `\|` survives as data.
    html = (
        "<table><tr><th>name</th><th>description</th></tr>"
        "<tr><td>Widget</td><td>left\\|right</td></tr></table>"
    )

    markdown = _convert_html(html)

    assert r"| Widget | left\\\|right |" in markdown


def test_html_table_plain_cells_are_unchanged() -> None:
    html = (
        "<table><tr><th>name</th><th>description</th></tr>"
        "<tr><td>Widget</td><td>cheap and fast</td></tr></table>"
    )

    markdown = _convert_html(html)

    assert "| Widget | cheap and fast |" in markdown
    assert "\\" not in markdown


def test_html_table_newline_in_cell_collapses_to_space() -> None:
    html = (
        "<table><tr><th>name</th><th>notes</th></tr>"
        "<tr><td>Widget</td><td>line one<br/>line two</td></tr></table>"
    )

    markdown = _convert_html(html)

    assert len([line for line in markdown.splitlines() if line.strip()]) == 3
    assert "| Widget | line one line two |" in markdown


def test_html_table_colspan_still_expands_after_escaping() -> None:
    html = (
        "<table><tr><th>a | b</th><th colspan=\"2\">c</th></tr>"
        "<tr><td>1</td><td>2</td><td>3</td></tr></table>"
    )

    markdown = _convert_html(html)

    assert "| a \\| b | c | |" in markdown
