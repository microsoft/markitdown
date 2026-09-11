"""Tests for TwelveLabsConverter.

Covers accepts() routing, convert() via a mocked TwelveLabs client, the
MissingDependency / missing-key error paths, and registration. A single
live test against the real Pegasus API is gated on TWELVELABS_API_KEY and
skipped when it is not set. Follows the pattern of test_cu_converter.py.
"""

import io
import os

import pytest

from markitdown.converters._twelvelabs_converter import (
    TwelveLabsConverter,
    ACCEPTED_FILE_EXTENSIONS,
    ACCEPTED_MIME_TYPE_PREFIXES,
    DEFAULT_PROMPT,
)
from markitdown._stream_info import StreamInfo


def _make_converter():
    """Create a converter bypassing __init__ (no SDK / API key needed)."""
    conv = TwelveLabsConverter.__new__(TwelveLabsConverter)
    conv._file_extensions = ACCEPTED_FILE_EXTENSIONS
    conv._mime_type_prefixes = ACCEPTED_MIME_TYPE_PREFIXES
    conv._model_name = "pegasus1.5"
    conv._prompt = None
    conv._max_tokens = 2048
    return conv


# ---------------------------------------------------------------------------
# accepts() routing
# ---------------------------------------------------------------------------


class TestAccepts:
    @pytest.mark.parametrize("ext", [".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v"])
    def test_accepts_video_extensions(self, ext):
        conv = _make_converter()
        assert conv.accepts(io.BytesIO(b""), StreamInfo(extension=ext))

    @pytest.mark.parametrize(
        "mime", ["video/mp4", "video/quicktime", "video/webm", "video/x-matroska"]
    )
    def test_accepts_video_mimetypes(self, mime):
        conv = _make_converter()
        assert conv.accepts(io.BytesIO(b""), StreamInfo(mimetype=mime))

    @pytest.mark.parametrize("ext", [".pdf", ".mp3", ".wav", ".jpg", ".txt", ".zip"])
    def test_rejects_non_video(self, ext):
        conv = _make_converter()
        assert not conv.accepts(io.BytesIO(b""), StreamInfo(extension=ext))


# ---------------------------------------------------------------------------
# convert() with a mocked client
# ---------------------------------------------------------------------------


class _FakeResponse:
    def __init__(self, data):
        self.data = data


class _FakeClient:
    def __init__(self, data="# Video\n\nA cat plays piano."):
        self._data = data
        self.last_call = None

    def analyze(self, **kwargs):
        self.last_call = kwargs
        return _FakeResponse(self._data)


class TestConvert:
    def test_returns_markdown_from_pegasus(self):
        conv = _make_converter()
        conv._client = _FakeClient(data="# Video\n\nA cat plays piano.")

        result = conv.convert(
            io.BytesIO(b"fake video bytes"),
            StreamInfo(extension=".mp4", filename="cat.mp4"),
        )

        assert result.markdown == "# Video\n\nA cat plays piano."
        assert result.title == "cat.mp4"

    def test_wires_model_and_prompt(self):
        conv = _make_converter()
        conv._model_name = "pegasus1.5"
        conv._client = _FakeClient()

        conv.convert(io.BytesIO(b"data"), StreamInfo(extension=".mp4"))

        call = conv._client.last_call
        assert call["model_name"] == "pegasus1.5"
        assert call["prompt"] == DEFAULT_PROMPT
        assert call["max_tokens"] == 2048
        # video is passed as a base64 VideoContext
        assert call["video"].base_64_string  # non-empty base64 payload

    def test_per_call_prompt_override(self):
        conv = _make_converter()
        conv._client = _FakeClient()

        conv.convert(
            io.BytesIO(b"data"),
            StreamInfo(extension=".mp4"),
            twelvelabs_prompt="List every spoken sentence.",
        )

        assert conv._client.last_call["prompt"] == "List every spoken sentence."

    def test_stream_position_restored(self):
        conv = _make_converter()
        conv._client = _FakeClient()
        stream = io.BytesIO(b"abc")
        stream.read(1)  # advance position
        conv.convert(stream, StreamInfo(extension=".mp4"))
        assert stream.tell() == 1

    def test_none_data_yields_empty_markdown(self):
        conv = _make_converter()
        conv._client = _FakeClient(data=None)
        result = conv.convert(io.BytesIO(b"data"), StreamInfo(extension=".mp4"))
        assert result.markdown == ""


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------


class TestErrors:
    def test_missing_dependency_message(self):
        import markitdown.converters._twelvelabs_converter as tl_module
        from markitdown._exceptions import MissingDependencyException
        from unittest.mock import patch

        import_error = ImportError("No module named 'twelvelabs'")
        dependency_exc_info = (ImportError, import_error, None)

        with patch.object(
            tl_module, "_dependency_exc_info", dependency_exc_info
        ), pytest.raises(MissingDependencyException) as exc_info:
            TwelveLabsConverter(api_key="fake")

        assert "twelvelabs" in str(exc_info.value)
        assert exc_info.value.__cause__ is import_error

    def test_missing_api_key_raises(self, monkeypatch):
        import markitdown.converters._twelvelabs_converter as tl_module
        from unittest.mock import patch

        monkeypatch.delenv("TWELVELABS_API_KEY", raising=False)
        # Pretend the SDK is installed so we reach the key check.
        with patch.object(tl_module, "_dependency_exc_info", None):
            with pytest.raises(ValueError, match="requires an API key"):
                TwelveLabsConverter()


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


class TestRegistration:
    def test_registered_when_api_key_provided(self):
        from unittest.mock import patch
        import markitdown.converters._twelvelabs_converter as tl_module

        with patch.object(tl_module, "_dependency_exc_info", None), patch.object(
            tl_module, "TwelveLabs"
        ):
            from markitdown import MarkItDown
            from markitdown.converters import TwelveLabsConverter as TLC

            md = MarkItDown(twelvelabs_api_key="fake-key")
            assert any(isinstance(reg.converter, TLC) for reg in md._converters)

    def test_not_registered_without_api_key(self, monkeypatch):
        monkeypatch.delenv("TWELVELABS_API_KEY", raising=False)
        from markitdown import MarkItDown
        from markitdown.converters import TwelveLabsConverter as TLC

        md = MarkItDown()
        assert not any(isinstance(reg.converter, TLC) for reg in md._converters)


# ---------------------------------------------------------------------------
# Live API smoke test (opt-in)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    os.environ.get("TWELVELABS_API_KEY") is None,
    reason="TWELVELABS_API_KEY not set; skipping live TwelveLabs API test.",
)
def test_live_pegasus_analyze():
    """End-to-end smoke test against the real Pegasus API.

    Uses a short public sample video. Pegasus analysis can be slow, so this is
    opt-in and only runs when TWELVELABS_API_KEY is set.
    """
    import urllib.request

    sample_url = (
        "https://commondatastorage.googleapis.com/"
        "gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
    )
    video_bytes = urllib.request.urlopen(sample_url, timeout=60).read()

    conv = TwelveLabsConverter()
    result = conv.convert(
        io.BytesIO(video_bytes),
        StreamInfo(extension=".mp4", mimetype="video/mp4", filename="sample.mp4"),
    )
    assert isinstance(result.markdown, str)
    assert len(result.markdown) > 0
