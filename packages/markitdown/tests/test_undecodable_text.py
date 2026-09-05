"""Undecodable input must not turn into the literal text "None".

CsvConverter and PlainTextConverter fall back to charset detection when no
charset is known. charset_normalizer's ``best()`` returns ``None`` when
detection fails outright, and ``str(None)`` is the three-character string
``"None"`` - content that was never in the file.
"""

import io

from charset_normalizer import from_bytes

from markitdown import MarkItDown, StreamInfo
from markitdown.converters import CsvConverter, PlainTextConverter

# charset_normalizer cannot settle on an encoding for this byte string, so
# from_bytes(...).best() is None. Asserted below so the fixture failing to be
# undecodable can never quietly turn these tests green.
UNDECODABLE = b"\xff\xfe" + bytes([0xD8, 0x00, 0xDC])


def test_fixture_is_actually_undecodable() -> None:
    assert from_bytes(UNDECODABLE).best() is None


def test_csv_converter_undecodable_is_not_the_string_none() -> None:
    result = CsvConverter().convert(
        io.BytesIO(UNDECODABLE),
        StreamInfo(extension=".csv", mimetype="text/csv"),
    )
    assert "None" not in result.markdown


def test_plain_text_converter_undecodable_is_not_the_string_none() -> None:
    result = PlainTextConverter().convert(
        io.BytesIO(UNDECODABLE),
        StreamInfo(extension=".txt", mimetype="text/plain"),
    )
    assert result.markdown != "None"
    assert "None" not in result.markdown


def test_undecodable_csv_through_markitdown() -> None:
    result = MarkItDown().convert_stream(
        io.BytesIO(UNDECODABLE),
        stream_info=StreamInfo(extension=".csv", mimetype="text/csv"),
    )
    assert "None" not in result.markdown


def test_undecodable_text_through_markitdown() -> None:
    result = MarkItDown().convert_stream(
        io.BytesIO(UNDECODABLE),
        stream_info=StreamInfo(extension=".txt", mimetype="text/plain"),
    )
    assert "None" not in result.markdown


def test_decodable_input_still_uses_detected_charset() -> None:
    # Guards the fallback from swallowing the normal path: Shift-JIS text has
    # no declared charset here and must still round-trip through detection.
    payload = "名前,年齢\n佐藤太郎,30\n".encode("shift_jis")
    result = CsvConverter().convert(
        io.BytesIO(payload),
        StreamInfo(extension=".csv", mimetype="text/csv"),
    )
    assert "名前" in result.markdown
    assert "佐藤太郎" in result.markdown


def test_declared_charset_path_is_unchanged() -> None:
    payload = "a,b\n1,2\n".encode("utf-8")
    result = CsvConverter().convert(
        io.BytesIO(payload),
        StreamInfo(extension=".csv", mimetype="text/csv", charset="utf-8"),
    )
    assert "| a | b |" in result.markdown
