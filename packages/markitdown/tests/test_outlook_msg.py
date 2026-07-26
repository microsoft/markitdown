#!/usr/bin/env python3 -m pytest
"""Tests for .msg files saved from Outlook 365 / Exchange.

Two properties of such files break the naive reads:

* ``PR_SENDER_EMAIL_ADDRESS`` (0x0C1F) holds an Exchange Distinguished Name
  rather than an email address whenever ``PR_SENDER_ADDRTYPE`` (0x0C1E) is
  ``EX``; the address lives in ``PR_SENDER_SMTP_ADDRESS`` (0x5D01).
* HTML-only messages leave ``PR_BODY`` (0x1000) empty and store their content
  in ``PR_HTML`` (0x1013), so reading only ``PR_BODY`` drops the whole message.

A .msg file is an OLE2 compound file and nothing in the dependency set can
write that container, so these tests serve the MAPI streams through a stand-in
for ``olefile.OleFileIO`` instead of a binary fixture.
"""
import io

import olefile

from markitdown._stream_info import StreamInfo
from markitdown.converters._outlook_msg_converter import OutlookMsgConverter

EXCHANGE_DN = (
    "/O=EXCHANGELABS/OU=EXCHANGE ADMINISTRATIVE GROUP"
    " (FYDIBOHF23SPDLT)/CN=RECIPIENTS/CN=ab12cd34"
)


class _FakeMsg(olefile.OleFileIO):
    """Serves a fixed set of MSG streams. ``_get_stream_data`` asserts the type."""

    def __init__(self, streams):
        self._streams = streams
        # OleFileIO.__del__ reads this; we deliberately skip super().__init__.
        self._we_opened_fp = False

    def exists(self, path):
        return path in self._streams

    def openstream(self, path):
        return io.BytesIO(self._streams[path])

    def close(self):
        pass


def _unicode_stream(value: str) -> bytes:
    """MAPI PT_UNICODE properties are stored little-endian UTF-16."""
    return value.encode("utf-16-le")


def _patch_olefile(monkeypatch, streams) -> None:
    """Make ``olefile.OleFileIO(...)`` open the given streams instead of a file."""

    class _PatchedOleFileIO(_FakeMsg):
        def __init__(self, *_args, **_kwargs):
            super().__init__(streams)

    monkeypatch.setattr(olefile, "OleFileIO", _PatchedOleFileIO)


def test_sender_prefers_smtp_address_over_exchange_dn() -> None:
    msg = _FakeMsg(
        {
            "__substg1.0_0C1E001F": _unicode_stream("EX"),
            "__substg1.0_0C1F001F": _unicode_stream(EXCHANGE_DN),
            "__substg1.0_5D01001F": _unicode_stream("sender@example.com"),
        }
    )

    assert OutlookMsgConverter()._get_sender(msg) == "sender@example.com"


def test_sender_prefers_sent_representing_smtp_address() -> None:
    msg = _FakeMsg(
        {
            "__substg1.0_0C1E001F": _unicode_stream("EX"),
            "__substg1.0_0C1F001F": _unicode_stream(EXCHANGE_DN),
            "__substg1.0_5D02001F": _unicode_stream("delegate@example.com"),
        }
    )

    assert OutlookMsgConverter()._get_sender(msg) == "delegate@example.com"


def test_sender_skips_exchange_dn_for_sent_representing_address() -> None:
    msg = _FakeMsg(
        {
            "__substg1.0_0C1E001F": _unicode_stream("EX"),
            "__substg1.0_0C1F001F": _unicode_stream(EXCHANGE_DN),
            "__substg1.0_0064001F": _unicode_stream("SMTP"),
            "__substg1.0_0065001F": _unicode_stream("onbehalf@example.com"),
        }
    )

    assert OutlookMsgConverter()._get_sender(msg) == "onbehalf@example.com"


def test_sender_keeps_smtp_addrtype_address() -> None:
    # The common non-Exchange case must keep behaving exactly as before.
    msg = _FakeMsg(
        {
            "__substg1.0_0C1E001F": _unicode_stream("SMTP"),
            "__substg1.0_0C1F001F": _unicode_stream("plain@example.com"),
        }
    )

    assert OutlookMsgConverter()._get_sender(msg) == "plain@example.com"


def test_sender_falls_back_to_dn_when_no_smtp_address_exists() -> None:
    # Nothing better on file: keep the DN rather than dropping the header.
    msg = _FakeMsg(
        {
            "__substg1.0_0C1E001F": _unicode_stream("EX"),
            "__substg1.0_0C1F001F": _unicode_stream(EXCHANGE_DN),
        }
    )

    assert OutlookMsgConverter()._get_sender(msg) == EXCHANGE_DN


def test_html_only_body_is_converted_to_markdown() -> None:
    msg = _FakeMsg(
        {
            "__substg1.0_10130102": (
                b"<html><body><h1>Status</h1><p>Hello <b>world</b></p></body></html>"
            ),
        }
    )

    body = OutlookMsgConverter()._get_html_body(msg)

    assert body is not None
    assert "# Status" in body
    assert "Hello **world**" in body
    # The HTML must be converted, not passed through verbatim.
    assert "<p>" not in body


def test_html_body_reads_the_string_property_variant() -> None:
    msg = _FakeMsg(
        {
            "__substg1.0_1013001F": _unicode_stream(
                "<html><body><p>String variant</p></body></html>"
            ),
        }
    )

    assert "String variant" in (OutlookMsgConverter()._get_html_body(msg) or "")


def test_html_body_decodes_non_utf8_bytes() -> None:
    # PR_HTML carries no encoding of its own; assuming UTF-8 mangles this.
    msg = _FakeMsg(
        {
            "__substg1.0_10130102": (
                "<html><body><p>Grüße aus München</p></body></html>".encode("cp1252")
            ),
        }
    )

    assert "Grüße aus München" in (OutlookMsgConverter()._get_html_body(msg) or "")


def test_html_body_absent_returns_none() -> None:
    assert OutlookMsgConverter()._get_html_body(_FakeMsg({})) is None


def test_html_body_skips_an_empty_binary_property() -> None:
    # An empty binary stream must not mask a populated string variant.
    msg = _FakeMsg(
        {
            "__substg1.0_10130102": b"",
            "__substg1.0_1013001F": _unicode_stream(
                "<html><body><p>Fallback body</p></body></html>"
            ),
        }
    )

    assert "Fallback body" in (OutlookMsgConverter()._get_html_body(msg) or "")


def test_plain_text_body_wins_over_html(monkeypatch) -> None:
    streams = {
        "__substg1.0_0037001F": _unicode_stream("Q3 planning"),
        "__substg1.0_0E04001F": _unicode_stream("recipient@example.com"),
        "__substg1.0_0C1E001F": _unicode_stream("SMTP"),
        "__substg1.0_0C1F001F": _unicode_stream("sender@example.com"),
        "__substg1.0_1000001F": _unicode_stream("The plain text body."),
        "__substg1.0_10130102": b"<html><body><p>The HTML body.</p></body></html>",
    }
    _patch_olefile(monkeypatch, streams)

    result = OutlookMsgConverter().convert(
        io.BytesIO(b""), StreamInfo(extension=".msg")
    )

    assert "The plain text body." in result.markdown
    assert "The HTML body." not in result.markdown


def test_convert_renders_exchange_message(monkeypatch) -> None:
    # End-to-end shape of the message reported in #1188: Exchange sender, no
    # plain-text body.
    streams = {
        "__substg1.0_0037001F": _unicode_stream("Q3 planning"),
        "__substg1.0_0E04001F": _unicode_stream("recipient@example.com"),
        "__substg1.0_0C1E001F": _unicode_stream("EX"),
        "__substg1.0_0C1F001F": _unicode_stream(EXCHANGE_DN),
        "__substg1.0_5D01001F": _unicode_stream("sender@example.com"),
        "__substg1.0_10130102": b"<html><body><p>Hello <b>world</b></p></body></html>",
    }
    _patch_olefile(monkeypatch, streams)

    result = OutlookMsgConverter().convert(
        io.BytesIO(b""), StreamInfo(extension=".msg")
    )

    assert "**From:** sender@example.com" in result.markdown
    assert "EXCHANGELABS" not in result.markdown
    assert "Hello **world**" in result.markdown
    assert result.title == "Q3 planning"
