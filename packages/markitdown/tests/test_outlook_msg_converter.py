from io import BytesIO
from types import SimpleNamespace

from markitdown import StreamInfo
from markitdown.converters._outlook_msg_converter import OutlookMsgConverter
from markitdown.converters import _outlook_msg_converter as outlook_msg_converter


def _utf16_stream(value: str) -> bytes:
    return value.encode("utf-16-le")


def _install_fake_olefile(monkeypatch, streams: dict[str, bytes]) -> None:
    class FakeOleFileIO:
        def __init__(self, _file_stream):
            self._streams = streams

        def exists(self, stream_path: str) -> bool:
            return stream_path in self._streams

        def openstream(self, stream_path: str) -> BytesIO:
            return BytesIO(self._streams[stream_path])

        def close(self) -> None:
            return None

    monkeypatch.setattr(outlook_msg_converter, "_dependency_exc_info", None)
    monkeypatch.setattr(
        outlook_msg_converter,
        "olefile",
        SimpleNamespace(OleFileIO=FakeOleFileIO),
    )


def test_convert_prefers_html_body_when_present(monkeypatch):
    _install_fake_olefile(
        monkeypatch,
        {
            "__substg1.0_0C1F001F": _utf16_stream("sender@example.com"),
            "__substg1.0_0E04001F": _utf16_stream("recipient@example.com"),
            "__substg1.0_0037001F": _utf16_stream("HTML table email"),
            "__substg1.0_1000001F": _utf16_stream("plain fallback body"),
            "__substg1.0_10130102": (
                b"<html><body><p>Summary</p><table><tr><th>Name</th><th>Value</th></tr>"
                b"<tr><td>Alpha</td><td>1</td></tr></table></body></html>"
            ),
        },
    )

    result = OutlookMsgConverter().convert(
        BytesIO(b"fake msg payload"),
        StreamInfo(extension=".msg", mimetype="application/vnd.ms-outlook"),
    )

    assert result.title == "HTML table email"
    assert "**Subject:** HTML table email" in result.markdown
    assert "Summary" in result.markdown
    assert "| Name | Value |" in result.markdown
    assert "| Alpha | 1 |" in result.markdown
    assert "plain fallback body" not in result.markdown


def test_convert_falls_back_to_plain_text_body(monkeypatch):
    _install_fake_olefile(
        monkeypatch,
        {
            "__substg1.0_0037001F": _utf16_stream("Plain text email"),
            "__substg1.0_1000001F": _utf16_stream("plain text body"),
        },
    )

    result = OutlookMsgConverter().convert(
        BytesIO(b"fake msg payload"),
        StreamInfo(extension=".msg", mimetype="application/vnd.ms-outlook"),
    )

    assert result.title == "Plain text email"
    assert "plain text body" in result.markdown
