"""Known formats remain usable without the optional content detector."""

import io
from importlib.metadata import requires
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from markitdown import (
    FileConversionException,
    MarkItDown,
    StreamInfo,
    UnsupportedFormatException,
)
import markitdown._markitdown as module


@pytest.fixture
def without_magika(monkeypatch):
    monkeypatch.setattr(module, "magika", None)
    return MarkItDown()


def test_format_extras_do_not_require_magika():
    dependencies = requires("markitdown")
    magika = [dep for dep in dependencies if dep.startswith("magika")]
    assert len(magika) == 2
    assert all("extra ==" in dep for dep in magika)
    assert any("'magika'" in dep or '"magika"' in dep for dep in magika)
    assert any("'all'" in dep or '"all"' in dep for dep in magika)


def test_known_pdf_without_magika(without_magika):
    result = without_magika.convert(Path(__file__).parent / "test_files/test.pdf")
    assert result.markdown.strip()


def test_hinted_text_charset_and_position(without_magika):
    body = "A useful message in UTF-16.".encode("utf-16")
    stream = io.BytesIO(b"prefix" + body)
    stream.seek(6)
    guesses = without_magika._get_stream_info_guesses(
        stream, StreamInfo(extension=".txt")
    )
    assert stream.tell() == 6
    assert guesses[0].mimetype == "text/plain"
    assert guesses[0].charset is not None
    assert without_magika.convert_stream(
        stream, stream_info=StreamInfo(extension=".txt")
    ).markdown == body.decode("utf-16")


def test_explicit_charset_is_preserved(without_magika):
    body = "caf\u00e9".encode("cp1252")
    result = without_magika.convert_stream(
        io.BytesIO(body),
        stream_info=StreamInfo(mimetype="text/plain", charset="cp1252"),
    )
    assert result.markdown == "caf\u00e9"


def test_unknown_stream_has_guidance(without_magika):
    with pytest.raises(UnsupportedFormatException, match=r"markitdown\[magika\]"):
        without_magika.convert_stream(io.BytesIO(b"unidentified stream"))


def test_failed_pdf_is_not_reported_as_missing_detection(without_magika):
    with pytest.raises(FileConversionException) as exc:
        without_magika.convert_stream(
            io.BytesIO(b"invalid pdf"), stream_info=StreamInfo(extension=".pdf")
        )
    assert "Install markitdown[magika]" not in str(exc.value)


def test_installed_detector_still_identifies_stream(monkeypatch):
    output = SimpleNamespace(
        label="txt", is_text=True, extensions=["txt"], mime_type="text/plain"
    )
    detector = Mock()
    detector.identify_stream.return_value = SimpleNamespace(
        status="ok", prediction=SimpleNamespace(output=output)
    )
    monkeypatch.setattr(module, "magika", SimpleNamespace(Magika=lambda: detector))
    stream = io.BytesIO(b"hello")
    assert MarkItDown().convert_stream(stream).markdown == "hello"
    assert stream.tell() == 0
    detector.identify_stream.assert_called_once()


def test_broken_installed_detector_is_not_silently_disabled(monkeypatch):
    def broken():
        raise RuntimeError("broken detector")

    monkeypatch.setattr(module, "magika", SimpleNamespace(Magika=broken))
    with pytest.raises(RuntimeError, match="broken detector"):
        MarkItDown()
