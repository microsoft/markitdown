import io

from markitdown.converters._csv_converter import CsvConverter
from markitdown._stream_info import StreamInfo

CSV_STREAM_INFO = StreamInfo(extension=".csv", mimetype="text/csv")


def _convert(data: bytes) -> str:
    return CsvConverter().convert(io.BytesIO(data), CSV_STREAM_INFO).markdown


def test_pipe_in_cell_is_escaped():
    markdown = _convert(b"name,note\nAlice,a|b\nBob,plain\n")
    lines = markdown.splitlines()
    # Header, separator and two data rows.
    assert len(lines) == 4
    # Every row must have the same number of unescaped column separators.
    expected_pipes = lines[0].count("|")
    for line in lines:
        assert line.replace("\\|", "").count("|") == expected_pipes
    assert "a\\|b" in markdown


def test_newline_in_cell_does_not_break_row():
    markdown = _convert(b'name,note\n"Bob","line1\nline2"\n')
    lines = markdown.splitlines()
    assert len(lines) == 3
    assert "line1 line2" in lines[2]
