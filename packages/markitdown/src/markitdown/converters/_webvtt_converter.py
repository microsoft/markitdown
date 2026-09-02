import html
import re
from typing import Any, BinaryIO

from charset_normalizer import from_bytes

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_MIME_TYPES = ["text/vtt"]
ACCEPTED_FILE_EXTENSIONS = [".vtt"]

_TIMESTAMP_RE = re.compile(
    r"^\s*(?:\d{2}:)?\d{2}:\d{2}\.\d{3}\s+-->\s+(?:\d{2}:)?\d{2}:\d{2}\.\d{3}"
)
_VOICE_OPEN_RE = re.compile(r"<v(?:\.[^>\s]+)?\s+([^>]+)>")
_TAG_RE = re.compile(r"<[^>]+>")


class WebVttConverter(DocumentConverter):
    """Convert WebVTT subtitle files to readable Markdown text."""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        return mimetype in ACCEPTED_MIME_TYPES or extension in ACCEPTED_FILE_EXTENSIONS

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if stream_info.charset:
            text = file_stream.read().decode(stream_info.charset)
        else:
            text = str(from_bytes(file_stream.read()).best())

        cues = []
        for block in re.split(r"\r?\n\s*\r?\n", text):
            cue = self._convert_block(block)
            if cue:
                cues.append(cue)

        return DocumentConverterResult(markdown="\n\n".join(cues))

    def _convert_block(self, block: str) -> str:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            return ""

        first = lines[0].lstrip("\ufeff")
        if first.startswith(("WEBVTT", "NOTE", "STYLE", "REGION")):
            return ""

        timestamp_index = next(
            (i for i, line in enumerate(lines) if _TIMESTAMP_RE.match(line)),
            None,
        )
        if timestamp_index is None:
            return ""

        text_lines = [
            self._clean_text_line(line)
            for line in lines[timestamp_index + 1 :]
            if line.strip()
        ]
        return "\n".join(line for line in text_lines if line)

    def _clean_text_line(self, line: str) -> str:
        line = _VOICE_OPEN_RE.sub(r"\1: ", line)
        line = _TAG_RE.sub("", line)
        line = html.unescape(line)
        return re.sub(r"\s+", " ", line).strip()
