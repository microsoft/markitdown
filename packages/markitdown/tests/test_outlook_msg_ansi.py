#!/usr/bin/env python3 -m pytest
"""Tests for .msg files saved in the legacy non-Unicode format."""

import io
import os
import struct
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

# Strings short enough, and in code pages close enough, that charset detection
# picks the wrong codec: charset_normalizer reads the first as UTF-16BE
# ("勩獵淩") and the second as CP1125 ("╧ЁштхҐ ьшЁ").
AMBIGUOUS_LATIN = "Résumé"
AMBIGUOUS_CYRILLIC = "Привет мир"

PR_MESSAGE_CODEPAGE = 0x3FFD
PR_INTERNET_CPID = 0x3FDE

# Property ids of the string properties the converter reads.
SENDER_TAG = "0C1F"
RECIPIENT_TAG = "0E04"
SUBJECT_TAG = "0037"
BODY_TAG = "1000"


def _properties_stream(codepages: dict) -> bytes:
    """Build a top-level message property stream declaring the given code pages.

    A 32-byte header, then one 16-byte entry per property: tag, flags, value.
    """
    data = b"\x00" * 32
    for property_id, codepage in codepages.items():
        tag = (property_id << 16) | 0x0003  # PT_LONG
        data += struct.pack("<III", tag, 0x00000006, codepage) + b"\x00" * 4
    return data


def _unicode_streams() -> dict:
    """The streams Outlook writes when saving in the Unicode format."""
    return {
        "__substg1.0_0C1F001F": SENDER.encode("utf-16-le"),
        "__substg1.0_0E04001F": RECIPIENT.encode("utf-16-le"),
        "__substg1.0_0037001F": SUBJECT.encode("utf-16-le"),
        "__substg1.0_1000001F": BODY.encode("utf-16-le"),
    }


def _ansi_streams(encoding: str = "cp1252", codepage: int = 1252) -> dict:
    """The same message saved in the non-Unicode format, in a declared code page.

    Passing ``codepage=0`` leaves the declaration out, as a malformed message
    would, so that only detection is left to fall back on.
    """
    streams = {
        "__substg1.0_0C1F001E": SENDER.encode(encoding),
        "__substg1.0_0E04001E": RECIPIENT.encode(encoding),
        "__substg1.0_0037001E": SUBJECT.encode(encoding),
        "__substg1.0_1000001E": BODY.encode(encoding),
    }
    if codepage:
        streams["__properties_version1.0"] = _properties_stream(
            {PR_MESSAGE_CODEPAGE: codepage}
        )
    return streams


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


def test_declared_codepage_decodes_cyrillic_headers() -> None:
    """A CP1251 header is decoded from the declared code page, not detected.

    Detection reads this subject as CP1125 and yields "╧ЁштхҐ ьшЁ".
    """
    streams = {
        "__substg1.0_0037001E": AMBIGUOUS_CYRILLIC.encode("cp1251"),
        "__properties_version1.0": _properties_stream({PR_MESSAGE_CODEPAGE: 1251}),
    }

    assert f"**Subject:** {AMBIGUOUS_CYRILLIC}" in _convert(streams)


def test_declared_codepage_decodes_short_latin_headers() -> None:
    """A short CP1252 header is decoded from the declared code page.

    Detection reads these six bytes as UTF-16BE and yields "勩獵淩".
    """
    streams = {
        "__substg1.0_0037001E": AMBIGUOUS_LATIN.encode("cp1252"),
        "__properties_version1.0": _properties_stream({PR_MESSAGE_CODEPAGE: 1252}),
    }

    assert f"**Subject:** {AMBIGUOUS_LATIN}" in _convert(streams)


def test_internet_codepage_decodes_the_body() -> None:
    """PidTagInternetCodepage describes the body, PidTagMessageCodepage the rest."""
    streams = {
        "__substg1.0_0037001E": AMBIGUOUS_LATIN.encode("cp1252"),
        "__substg1.0_1000001E": AMBIGUOUS_CYRILLIC.encode("cp1251"),
        "__properties_version1.0": _properties_stream(
            {PR_MESSAGE_CODEPAGE: 1252, PR_INTERNET_CPID: 1251}
        ),
    }
    markdown = _convert(streams)

    assert f"**Subject:** {AMBIGUOUS_LATIN}" in markdown
    assert AMBIGUOUS_CYRILLIC in markdown


def test_greek_codepage_is_honored() -> None:
    """CP1253 bytes are Greek, however little of the alphabet a header shows."""
    subject = "Ελληνικά"
    streams = {
        "__substg1.0_0037001E": subject.encode("cp1253"),
        "__properties_version1.0": _properties_stream({PR_MESSAGE_CODEPAGE: 1253}),
    }

    assert f"**Subject:** {subject}" in _convert(streams)


def test_codepage_needing_a_codec_alias_is_honored() -> None:
    """Code pages whose codec is not named "cp<CPID>" still have to map.

    Python has no "cp28595" -- ISO 8859-5 is reached under its own name.
    """
    subject = AMBIGUOUS_CYRILLIC
    streams = {
        "__substg1.0_0037001E": subject.encode("iso8859-5"),
        "__properties_version1.0": _properties_stream({PR_MESSAGE_CODEPAGE: 28595}),
    }

    assert f"**Subject:** {subject}" in _convert(streams)


def test_utf8_codepage_is_honored() -> None:
    """PT_STRING8 may be UTF-8, which the message declares as code page 65001."""
    streams = {
        "__substg1.0_0037001E": SUBJECT.encode("utf-8"),
        "__properties_version1.0": _properties_stream({PR_MESSAGE_CODEPAGE: 65001}),
    }

    assert f"**Subject:** {SUBJECT}" in _convert(streams)


def test_missing_codepage_falls_back_to_detection() -> None:
    """Without a declaration there is nothing to go on but the bytes."""
    markdown = _convert(_ansi_streams(codepage=0))

    assert f"**From:** {SENDER}" in markdown
    assert "Te confirmo la reunión del martes" in markdown


def test_unsupported_codepage_falls_back_to_detection() -> None:
    """A code page Python cannot decode must not lose the message either."""
    streams = _ansi_streams()
    streams["__properties_version1.0"] = _properties_stream(
        {PR_MESSAGE_CODEPAGE: 99999}
    )
    markdown = _convert(streams)

    assert f"**From:** {SENDER}" in markdown
    assert "Te confirmo la reunión del martes" in markdown


def test_undecodable_bytes_fall_back_to_detection() -> None:
    """A declaration the bytes contradict must not raise, nor drop the field."""
    streams = {
        # US-ASCII (code page 20127) cannot represent the accents in the body.
        "__substg1.0_1000001E": BODY.encode("cp1252"),
        "__properties_version1.0": _properties_stream({PR_MESSAGE_CODEPAGE: 20127}),
    }

    assert "Te confirmo la reunión del martes" in _convert(streams)


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
    import pytest

    pytest.main([__file__, "-v"])
