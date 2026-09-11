import re
from typing import BinaryIO, Any
from charset_normalizer import from_bytes
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import FileConversionException

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/vtt",
]
ACCEPTED_FILE_EXTENSIONS = [".vtt"]

MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_CUES = 10000


class VttConverter(DocumentConverter):
    """
    Converts WebVTT (.vtt) subtitle files to Markdown.
    Parses cue timings, speaker tags, and multi-line cues.
    Outputs timestamped transcript format: [HH:MM:SS.mmm] cue text
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        cur_pos = file_stream.tell()
        header = file_stream.read(6)
        file_stream.seek(cur_pos)
        if header == b"WEBVTT":
            return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        file_stream.seek(0, 2)
        file_size = file_stream.tell()
        file_stream.seek(0)

        if file_size > MAX_FILE_SIZE:
            raise FileConversionException(
                f"VTT file too large: {file_size} bytes (max {MAX_FILE_SIZE})"
            )

        if stream_info.charset:
            content = file_stream.read().decode(stream_info.charset)
        else:
            content = str(from_bytes(file_stream.read()).best())

        if "\x00" in content:
            raise FileConversionException("VTT file contains null bytes")

        paragraphs = self._parse_vtt(content)
        markdown = "\n\n".join(paragraphs)

        return DocumentConverterResult(markdown=markdown)

    def _parse_vtt(self, content: str) -> list[str]:
        lines = content.splitlines()
        paragraphs = []
        cue_count = 0
        in_cue = False
        current_lines = []
        cue_timing_pattern = re.compile(
            r"^(\d{2}):(\d{2}):(\d{2})\.(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})\.(\d{3})"
        )

        for line in lines:
            stripped = line.strip()

            if stripped == "WEBVTT":
                continue

            if not in_cue and (
                stripped == ""
                or stripped.startswith("NOTE")
                or stripped.startswith("REGION")
            ):
                continue

            timing_match = cue_timing_pattern.match(stripped)
            if timing_match:
                cue_count += 1
                if cue_count > MAX_CUES:
                    raise FileConversionException(
                        f"Too many cues in VTT file: {cue_count} (max {MAX_CUES})"
                    )

                (
                    hours,
                    mins,
                    secs,
                    millis,
                    end_hours,
                    end_mins,
                    end_secs,
                    end_millis,
                ) = map(int, timing_match.groups())

                if hours > 99 or mins > 59 or secs > 59:
                    raise FileConversionException(
                        f"Invalid timestamp in VTT: {timing_match.group(0)}"
                    )
                if end_hours > 99 or end_mins > 59 or end_secs > 59:
                    raise FileConversionException(
                        f"Invalid end timestamp in VTT: {timing_match.group(0)}"
                    )

                start_time = f"{hours:02d}:{mins:02d}:{secs:02d}.{millis:03d}"

                if current_lines:
                    text = " ".join(current_lines)
                    text = self._clean_text(text)
                    if text.strip():
                        paragraphs.append(f"[{start_time}] {text}")
                    current_lines = []

                in_cue = True
                continue

            if stripped == "" and in_cue:
                if current_lines:
                    text = " ".join(current_lines)
                    text = self._clean_text(text)
                    if text.strip():
                        paragraphs.append(f"[{start_time}] {text}")
                    current_lines = []
                in_cue = False
                continue

            if in_cue and stripped:
                current_lines.append(stripped)

        if current_lines and in_cue:
            text = " ".join(current_lines)
            text = self._clean_text(text)
            if text.strip():
                paragraphs.append(f"[{start_time}] {text}")

        return paragraphs

    def _clean_text(self, text: str) -> str:
        # Handle <v Name> - voice only
        text = re.sub(r"<v\s+([^>]+)>", r"\1: ", text)
        # Handle <v.class Name> - voice with class (extract just the name)
        text = re.sub(r"<v\.\S+\s+([^>]+)>", r"\1: ", text)
        # Handle <v.class> - voice with class only (no name)
        text = re.sub(r"<v\.([^>\s]+)>", r"\1: ", text)
        text = re.sub(r"</?c[^>]*>", "", text)
        text = re.sub(r"</?b>", "", text)
        text = re.sub(r"</?i>", "", text)
        text = re.sub(r"</?u>", "", text)
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip()
