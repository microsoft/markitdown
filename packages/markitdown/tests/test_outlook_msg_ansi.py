#!/usr/bin/env python3 -m pytest
"""Tests for .msg files saved in the legacy non-Unicode format.

Every string property in a .msg is stored under a stream whose name ends in
its MAPI type: ``001F`` for PT_UNICODE (UTF-16LE) or ``001E`` for PT_STRING8
(the message's 8-bit code page). Outlook writes one or the other for a given
message, never both, so a message saved in the non-Unicode format has no
``001F`` streams at all.

The converter addressed only the ``001F`` names, so such a message produced a
document with every header missing and no body -- just the "# Email Message"
and "## Content" scaffolding -- with no error raised to signal the loss.

A .msg is an OLE2 compound file and nothing in the dependency set can write
that container, so these tests serve the streams through a stand-in for
``olefile.OleFileIO`` rather than a binary fixture. ``test_outlook_msg.msg``
in the test vectors covers the Unicode format end to end.
"""

import io
import os
from unittest.mock import patch

import olefile

from markitdown import MarkItDown
from markitdown._stream_info import StreamInfo
from markitdown.converters._outlook_msg_converter import OutlookMsgConverter

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

SENDER = "ana.lopez@example.com"
RECIPIENT = "carlos.ruiz@example.com"
SUBJECT = "Confirmación de la reunión del martes"
BODY = (
    "Hola Carlos,\r\n\r\n"
    "Te confirmo la reunión del martes a las diez en la oficina de Bilbao. "
    "He adjuntado el informe de facturación del último trimestre para que "
    "puedas revisarlo antes, junto con la propuesta de calendario que "
    "comentamos por teléfono la semana pasada.\r\n\r\n"
    "Un saludo,\r\nAna"
)


def _unicode_streams() -> dict:
    """The streams Outlook writes when saving in the Unicode format."""
    return {
        "__substg1.0_0C1F001F": SENDER.encode("utf-16-le"),
        "__substg1.0_0E04001F": RECIPIENT.encode("utf-16-le"),
        "__substg1.0_0037001F": SUBJECT.encode("utf-16-le"),
        "__substg1.0_1000001F": BODY.encode("utf-16-le"),
    }


def _ansi_streams() -> dict:
    """The same message saved in the non-Unicode format (code page 1252)."""
    return {
        "__substg1.0_0C1F001E": SENDER.encode("cp1252"),
        "__substg1.0_0E04001E": RECIPIENT.encode("cp1252"),
        "__substg1.0_0037001E": SUBJECT.encode("cp1252"),
        "__substg1.0_1000001E": BODY.encode("cp1252"),
    }


def _fake_olefile(streams: dict):
    """Build a stand-in for olefile.OleFileIO serving a fixed set of streams."""

    class _FakeOleFileIO(olefile.OleFileIO):
        def __init__(self, file_stream):
            # No container to open. The flag keeps OleFileIO.__del__ from
            # tripping over the state a real open() would have set up.
            self._we_opened_fp = False

        def exists(self, path):
            return path in streams

        def openstream(self, path):
            return io.BytesIO(streams[path])

        def close(self):
            pass

    return _FakeOleFileIO


def _convert(streams: dict) -> str:
    with patch.object(olefile, "OleFileIO", _fake_olefile(streams)):
        return (
            OutlookMsgConverter()
            .convert(io.BytesIO(b""), StreamInfo(extension=".msg"))
            .markdown
        )


def test_ansi_message_keeps_headers_and_body() -> None:
    """A non-Unicode .msg must convert like its Unicode counterpart."""
    markdown = _convert(_ansi_streams())

    assert f"**From:** {SENDER}" in markdown
    assert f"**To:** {RECIPIENT}" in markdown
    assert f"**Subject:** {SUBJECT}" in markdown
    assert "Te confirmo la reunión del martes" in markdown
    assert "informe de facturación" in markdown


def test_ansi_message_is_not_silently_empty() -> None:
    """The failure mode was scaffolding with every field dropped."""
    markdown = _convert(_ansi_streams())

    assert markdown != "# Email Message\n\n## Content"
    assert "**Subject:**" in markdown


def test_unicode_message_is_unaffected() -> None:
    """The Unicode format must keep taking the same path as before."""
    markdown = _convert(_unicode_streams())

    assert f"**From:** {SENDER}" in markdown
    assert f"**To:** {RECIPIENT}" in markdown
    assert f"**Subject:** {SUBJECT}" in markdown
    assert "Te confirmo la reunión del martes" in markdown


def test_real_unicode_fixture_still_converts() -> None:
    """Regression guard over the checked-in .msg, read through real olefile."""
    result = MarkItDown().convert(os.path.join(TEST_FILES_DIR, "test_outlook_msg.msg"))

    assert "**From:** test.sender@example.com" in result.markdown
    assert "**Subject:** Test Email Message" in result.markdown
    assert "This is the body of the test email message" in result.markdown


if __name__ == "__main__":
    test_ansi_message_keeps_headers_and_body()
    test_ansi_message_is_not_silently_empty()
    test_unicode_message_is_unaffected()
    test_real_unicode_fixture_still_converts()
    print("All tests passed!")
