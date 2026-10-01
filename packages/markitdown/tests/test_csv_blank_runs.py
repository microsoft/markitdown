"""CSV conversion preserves table contents when trimming long blank runs."""

import io

import pytest

from markitdown import MarkItDown, StreamInfo


@pytest.mark.parametrize("position", ["leading", "after_header", "trailing", "all"])
def test_csv_long_blank_runs(position: str) -> None:
    blank = b"\n" * 100_000
    header = b"name,value\n"
    # An internal blank row and a wider data row must survive trimming.
    data = b"Alice,1\n\nBob,2,extra\n"
    content = {
        "leading": blank + header + data,
        "after_header": header + blank + data,
        "trailing": header + data + blank,
        "all": blank,
    }[position]

    result = MarkItDown(enable_plugins=False).convert_stream(
        io.BytesIO(content),
        stream_info=StreamInfo(extension=".csv", charset="utf-8"),
    )

    expected = (
        "| name | value |  |\n"
        "| --- | --- | --- |\n"
        "| Alice | 1 |  |\n"
        "|  |  |  |\n"
        "| Bob | 2 | extra |"
    )
    assert result.markdown == ("" if position == "all" else expected)
