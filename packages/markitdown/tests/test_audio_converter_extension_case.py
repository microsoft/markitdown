#!/usr/bin/env python3 -m pytest
"""Audio format detection must be case-insensitive, matching accepts().

convert() compared the raw extension, while accepts() lowercased it: for a
member like "TRACK.MP3" inside a zip (the ZipConverter passes the raw
splitext extension and no mimetype), accepts() returned True but the format
detection resolved to None, so transcription was silently skipped.
"""

import io
import wave
from unittest.mock import patch

import pytest

from markitdown import StreamInfo
from markitdown.converters._audio_converter import AudioConverter


@pytest.fixture
def wav_bytes() -> io.BytesIO:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(b"\x00\x00" * 1600)
    return io.BytesIO(buf.getvalue())


@pytest.fixture
def audio_converter() -> AudioConverter:
    return AudioConverter()


def _convert_with_stub_transcript(audio: AudioConverter, data: io.BytesIO, extension: str):
    seen = {}

    def fake_transcribe(file_stream, audio_format=None, language=None):
        seen["audio_format"] = audio_format
        return "STUB TRANSCRIPT"

    with patch(
        "markitdown.converters._audio_converter.transcribe_audio",
        side_effect=fake_transcribe,
    ):
        result = audio.convert(data, StreamInfo(extension=extension))
    return result, seen.get("audio_format")


@pytest.mark.parametrize(
    ("extension", "expected_format"),
    [(".wav", "wav"), (".WAV", "wav"), (".mp3", "mp3"), (".MP3", "mp3")],
)
def test_transcription_ignores_extension_case(
    audio_converter: AudioConverter, wav_bytes: io.BytesIO, extension: str, expected_format: str
) -> None:
    result, audio_format = _convert_with_stub_transcript(
        audio_converter, io.BytesIO(wav_bytes.read()), extension
    )
    assert audio_format == expected_format
    assert "STUB TRANSCRIPT" in result.markdown
