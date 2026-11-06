from typing import Any, BinaryIO

from ._exiftool import exiftool_metadata
from ._transcribe_audio import transcribe_audio
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException

ACCEPTED_MIME_TYPE_PREFIXES = [
    "audio/x-wav",
    "audio/mpeg",
    "video/mp4",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".wav",
    ".mp3",
    ".m4a",
    ".mp4",
]


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

        # accepts() matches extensions and mimetypes case-insensitively; the
        # format detection below must do the same, or an uppercase extension
        # (e.g. from a zip member name) silently skips transcription.
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

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

        # Figure out the audio format for transcription
        if extension == ".wav" or mimetype == "audio/x-wav":
            audio_format = "wav"
        elif extension == ".mp3" or mimetype == "audio/mpeg":
            audio_format = "mp3"
        elif extension in [".mp4", ".m4a"] or mimetype == "video/mp4":
            audio_format = "mp4"
        else:
            audio_format = None

        # Figure out the audio language for transcription, default to "en-US"
        language = kwargs.get("language", "en-US")

        # Transcribe
        if audio_format:
            try:
                transcript = transcribe_audio(
                    file_stream, audio_format=audio_format, language=language
                )
                if transcript:
                    md_content += "\n\n### Audio Transcript:\n" + transcript
            except MissingDependencyException:
                pass

        # Return the result
        return DocumentConverterResult(markdown=md_content.strip())
