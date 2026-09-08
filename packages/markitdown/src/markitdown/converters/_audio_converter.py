from typing import Any, BinaryIO

from ._exiftool import exiftool_metadata
from ._transcribe_audio import transcribe_audio
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException

# Map each accepted file extension and mimetype prefix to the audio format
# name understood by transcribe_audio(). The ACCEPTED_* lists are derived from
# these maps so that the formats we accept and the formats we can transcribe
# cannot drift apart.
_AUDIO_FORMAT_BY_EXTENSION = {
    ".wav": "wav",
    ".mp3": "mp3",
    ".m4a": "mp4",
    ".mp4": "mp4",
}

_AUDIO_FORMAT_BY_MIME_PREFIX = {
    "audio/x-wav": "wav",
    "audio/wav": "wav",
    "audio/mpeg": "mp3",
    "audio/mp3": "mp3",
    "video/mp4": "mp4",
    "audio/mp4": "mp4",
    "audio/m4a": "mp4",
    "audio/x-m4a": "mp4",
}

ACCEPTED_MIME_TYPE_PREFIXES = list(_AUDIO_FORMAT_BY_MIME_PREFIX)

ACCEPTED_FILE_EXTENSIONS = list(_AUDIO_FORMAT_BY_EXTENSION)


class AudioConverter(DocumentConverter):
    """
    Converts audio files to markdown via extraction of metadata (if `exiftool` is installed), and speech transcription (if `speech_recognition` is installed).
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        md_content = ""

        # Add metadata
        metadata = exiftool_metadata(
            file_stream, exiftool_path=kwargs.get("exiftool_path")
        )
        if metadata:
            for f in [
                "Title",
                "Artist",
                "Author",
                "Band",
                "Album",
                "Genre",
                "Track",
                "DateTimeOriginal",
                "CreateDate",
                # "Duration", -- Wrong values when read from memory
                "NumChannels",
                "SampleRate",
                "AvgBytesPerSec",
                "BitsPerSample",
            ]:
                if f in metadata:
                    md_content += f"{f}: {metadata[f]}\n"

        # Figure out the audio format for transcription. Normalize case here,
        # just as accepts() does, so that e.g. "recording.WAV" is transcribed
        # rather than silently skipped.
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        audio_format = _AUDIO_FORMAT_BY_EXTENSION.get(extension)
        if audio_format is None:
            for prefix, fmt in _AUDIO_FORMAT_BY_MIME_PREFIX.items():
                if mimetype.startswith(prefix):
                    audio_format = fmt
                    break

        # Transcribe
        if audio_format:
            try:
                transcript = transcribe_audio(file_stream, audio_format=audio_format)
                if transcript:
                    md_content += "\n\n### Audio Transcript:\n" + transcript
            except MissingDependencyException:
                pass

        # Return the result
        return DocumentConverterResult(markdown=md_content.strip())
