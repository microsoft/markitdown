#!/usr/bin/env python3 -m pytest
"""Tests for .msg files saved in the Unicode format."""

import io
from typing import Any, Dict
from unittest.mock import patch

import olefile
import pytest

from markitdown import DocumentConverterResult
from markitdown._stream_info import StreamInfo
from markitdown.converters._outlook_msg_converter import OutlookMsgConverter

SENDER = "ana.lopez@example.com"
RECIPIENT = "carlos.ruiz@example.com"
SUBJECT = "Confirmación de la reunión del martes"
BODY = "Hola Carlos,\r\n\r\nUn saludo,\r\nAna"

# Property ids of the string properties the converter reads.
SENDER_TAG = "0C1F"
RECIPIENT_TAG = "0E04"
SUBJECT_TAG = "0037"
BODY_TAG = "1000"


def _unicode_streams(terminator: bytes = b"") -> Dict[str, Any]:
    """The streams Outlook writes when saving in the Unicode format."""
    values = {
        SENDER_TAG: SENDER,
        RECIPIENT_TAG: RECIPIENT,
        SUBJECT_TAG: SUBJECT,
        BODY_TAG: BODY,
    }
    return {
        f"__substg1.0_{tag}001F": value.encode("utf-16-le") + terminator
        for tag, value in values.items()
    }


def _fake_olefile(streams: Dict[str, bytes]):
    """Build a stand-in for olefile.OleFileIO serving a fixed set of streams."""

    class _FakeOleFileIO(olefile.OleFileIO):
        def __init__(self, file_stream):
            # No container to open. The flag keeps OleFileIO.__del__ from
            # tripping over the state a real open() would have set up.
            self._we_opened_fp = False
            self._streams = streams

        def exists(self, path):
            return path in self._streams

        def openstream(self, path):
            return io.BytesIO(self._streams[path])

        def close(self):
            pass

    return _FakeOleFileIO


def _convert_result(streams: Dict[str, bytes]) -> DocumentConverterResult:
    with patch.object(olefile, "OleFileIO", _fake_olefile(streams)):
        return OutlookMsgConverter().convert(
            io.BytesIO(b""), StreamInfo(extension=".msg")
        )


@pytest.mark.parametrize("terminator", [b"\x00", b"\x00\x00", b"\x00\x00\x00"])
def test_unicode_terminators_are_removed(terminator: bytes) -> None:
    """A PT_UNICODE property may carry a trailing NUL terminator.

    The code units are UTF-16LE, so the terminator has to be removed a code
    unit at a time: str.strip() keeps NULs, and dropping whole bytes would take
    the last character of the property with them.
    """
    result = _convert_result(_unicode_streams(terminator))

    assert result.title == SUBJECT
    assert result.markdown == (
        f"# Email Message\n\n**From:** {SENDER}\n**To:** {RECIPIENT}\n"
        f"**Subject:** {SUBJECT}\n\n## Content\n\n{BODY}"
    )
    assert "\x00" not in result.markdown


@pytest.mark.parametrize("value", [b"", b"\x00", b"\x00\x00"])
def test_empty_unicode_properties_are_omitted(value: bytes) -> None:
    """A property carrying nothing but a terminator holds no value."""
    streams = _unicode_streams()
    for path in streams:
        streams[path] = value

    result = _convert_result(streams)

    assert not result.title
    assert result.markdown == "# Email Message\n\n\n## Content"
