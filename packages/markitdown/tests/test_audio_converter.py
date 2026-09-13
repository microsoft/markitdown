#!/usr/bin/env python3 -m pytest
"""Tests for AudioConverter's format detection.

``accepts()`` lowercases the extension and mimetype before comparing, but
``convert()`` used to compare them verbatim. A file named ``recording.WAV``
was therefore accepted, emitted its metadata, and then silently skipped
transcription. The accepted mimetype list was also missing common aliases
(``audio/wav``, ``audio/mp4``, ``audio/x-m4a``, ...) for formats already
accepted by extension.
"""

import io

import pytest

from markitdown._stream_info import StreamInfo
from markitdown.converters import _audio_converter
from markitdown.converters._audio_converter import AudioConverter


@pytest.fixture
def recorded_formats(monkeypatch):
    """Record the audio_format passed to transcribe_audio, stubbing out the
    external exiftool binary and speech recognition service."""
    formats = []

    def fake_transcribe(file_stream, *, audio_format="wav"):
        formats.append(audio_format)
        return "the transcript"

    monkeypatch.setattr(_audio_converter, "transcribe_audio", fake_transcribe)
    monkeypatch.setattr(_audio_converter, "exiftool_metadata", lambda *a, **k: {})
    return formats


def test_accepts_is_case_insensitive() -> None:
    assert AudioConverter().accepts(io.BytesIO(b""), StreamInfo(extension=".WAV"))


@pytest.mark.parametrize(
    "mimetype",
    [
        "audio/x-wav",
        "audio/wav",
        "audio/mpeg",
        "audio/mp3",
        "video/mp4",
        "audio/mp4",
        "audio/m4a",
        "audio/x-m4a",
    ],
)
def test_accepts_mimetype_aliases(mimetype: str) -> None:
    assert AudioConverter().accepts(io.BytesIO(b""), StreamInfo(mimetype=mimetype))


@pytest.mark.parametrize(
    "extension,expected_format",
    [
        (".WAV", "wav"),
        (".Mp3", "mp3"),
        (".M4A", "mp4"),
        (".MP4", "mp4"),
    ],
)
def test_convert_detects_format_case_insensitively(
    recorded_formats, extension: str, expected_format: str
) -> None:
    result = AudioConverter().convert(io.BytesIO(b""), StreamInfo(extension=extension))
    assert recorded_formats == [expected_format]
    assert "the transcript" in result.markdown


@pytest.mark.parametrize(
    "mimetype,expected_format",
    [
        ("audio/wav", "wav"),
        ("audio/mp3", "mp3"),
        ("audio/mp4", "mp4"),
        ("AUDIO/X-M4A", "mp4"),
    ],
)
def test_convert_detects_format_from_mimetype_aliases(
    recorded_formats, mimetype: str, expected_format: str
) -> None:
    AudioConverter().convert(io.BytesIO(b""), StreamInfo(mimetype=mimetype))
    assert recorded_formats == [expected_format]


def test_convert_skips_transcription_for_unknown_format(recorded_formats) -> None:
    result = AudioConverter().convert(io.BytesIO(b""), StreamInfo(extension=".bin"))
    assert recorded_formats == []
    assert result.markdown == ""
