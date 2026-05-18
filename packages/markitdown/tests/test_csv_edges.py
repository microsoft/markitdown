"""Edge-case tests for CsvConverter — mixed columns, special chars, encoding.

Exercises CSV parsing robustness beyond happy-path vectors.
"""

import io
import pytest

from markitdown import MarkItDown, StreamInfo, FileConversionException


def _make_md():
    return MarkItDown()


def _convert_csv(content: str, **kwargs) -> str:
    md = _make_md()
    result = md.convert(
        io.BytesIO(content.encode("utf-8")),
        stream_info=StreamInfo(extension=".csv", mimetype="text/csv", charset="utf-8"),
        **kwargs,
    )
    return result.markdown


# ============================================================
# Column count variations
# ============================================================


def test_csv_mixed_column_lengths():
    """Rows with fewer columns than header should be padded."""
    result = _convert_csv("A,B,C\n1,2\n3,4,5,6")
    # Row "1,2" should be padded to 3 cols; "3,4,5,6" truncated to 3
    lines = result.strip().split("\n")
    assert len(lines) == 4  # header + sep + 2 data
    # Check all data rows have exactly 3 columns
    for line in lines[2:]:
        assert line.count("|") == 4  # 3 cols = 4 pipes


def test_csv_single_column():
    result = _convert_csv("Value\n1\n2\n3")
    assert "| Value |" in result
    assert "| --- |" in result


def test_csv_single_row_no_data():
    result = _convert_csv("Header")
    assert "| Header |" in result
    assert "| --- |" in result


# ============================================================
# Special characters in fields
# ============================================================


def test_csv_fields_with_pipes():
    """Pipe characters inside CSV fields should not break the table."""
    result = _convert_csv("Name,Description\nfoo,bar|baz")
    assert "foo" in result
    assert "bar|baz" in result


def test_csv_fields_with_commas():
    """Quoted fields with commas should be preserved."""
    content = 'Name,Description\n"Smith, John","Engineer, Senior"\n'
    result = _convert_csv(content)
    assert "Smith, John" in result
    assert "Engineer, Senior" in result
    # Verify table structure intact (2 cols)
    lines = result.strip().split("\n")
    for line in lines[2:]:  # skip header and separator
        assert line.count("|") == 3  # 2 cols


def test_csv_fields_with_newlines_quoted():
    """Quoted fields containing newlines should be handled."""
    content = 'Header\n"Line1\nLine2"\n'
    result = _convert_csv(content)
    assert "Line1" in result
    assert "Line2" in result


def test_csv_fields_with_quotes():
    """Escaped quotes should be preserved."""
    content = 'Name,Note\n"He said ""hello""",ok\n'
    result = _convert_csv(content)
    assert "hello" in result


# ============================================================
# Empty / whitespace
# ============================================================


def test_csv_whitespace_only_field():
    result = _convert_csv("A,B\n , \n")
    lines = result.strip().split("\n")
    # Should have a data row with spaces
    assert len(lines) >= 3


def test_csv_empty_strings():
    result = _convert_csv("A,B,C\n,,\n")
    assert "|  |  |  |" in result or "|||" in result.replace(" ", "")


# ============================================================
# Encoding edge cases
# ============================================================


def test_csv_latin1_encoding():
    md = _make_md()
    content = "Nom,Ville\nAndré,Genève\n".encode("latin-1")
    result = md.convert(
        io.BytesIO(content),
        stream_info=StreamInfo(extension=".csv", mimetype="text/csv"),
    )
    assert "André" in result.markdown


def test_empty_csv_returns_empty():
    md = _make_md()
    result = md.convert(
        io.BytesIO(b""),
        stream_info=StreamInfo(extension=".csv", mimetype="text/csv"),
    )
    assert result.markdown == ""


# ============================================================
# Corrupt CSV
# ============================================================


def test_csv_malformed_raises():
    """Unterminated quoted field should either raise or produce truncated output."""
    md = _make_md()
    # csv.Error: unterminated quoted field
    try:
        result = md.convert(
            io.BytesIO(b'Header\n"unterminated'),
            stream_info=StreamInfo(extension=".csv", mimetype="text/csv", charset="utf-8"),
        )
        # If it doesn't raise, should produce some output
        assert isinstance(result.markdown, str)
    except FileConversionException:
        pass  # Also acceptable


def test_csv_wrong_charset_handles_gracefully():
    md = _make_md()
    content = "Hello,World\n1,2\n".encode("utf-8")
    # Invalid charset → CSV fails, falls through to PlainTextConverter
    result = md.convert(
        io.BytesIO(content),
        stream_info=StreamInfo(
            extension=".csv", mimetype="text/csv", charset="invalid-charset"
        ),
    )
    assert isinstance(result.markdown, str)
