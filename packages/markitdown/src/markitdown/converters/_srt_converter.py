import re
from typing import Any, BinaryIO

from charset_normalizer import from_bytes

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/srt",
    "text/x-srt",
    "application/x-subrip",
]
ACCEPTED_FILE_EXTENSIONS = [".srt"]

# "00:01:05,250 --> 00:01:07,000", capturing the start time without milliseconds.
_TIMING_RE = re.compile(
    r"^(\d{1,3}):(\d{2}):(\d{2})(?:[,.]\d{1,3})?\s*-->\s*\d{1,3}:\d{2}:\d{2}(?:[,.]\d{1,3})?"
)
# Styling markup: <i>, <b>, <u>, <font ...> and {\an8}-style overrides. Other
# angle brackets, like "<Bob>" or "x<y", are real text and are kept.
_MARKUP_RE = re.compile(r"</?(?:i|b|u|font)(?:\s[^>]{0,200})?>|\{\\[^}]{0,200}\}", re.I)


class SrtConverter(DocumentConverter):
    """
    Converts SubRip (.srt) subtitle files to a Markdown transcript, one line per
    cue, each prefixed with its start time.
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
        data = file_stream.read()
        content = None
        if stream_info.charset:
            # The charset hint comes from a sample of the file, so it can be
            # wrong for later bytes (e.g. "ascii" for a file that turns non-ASCII
            # after the sample). Fall through to a full-file guess in that case.
            try:
                content = data.decode(stream_info.charset)
            except (UnicodeDecodeError, LookupError):
                pass
        if content is None:
            detected = from_bytes(data).best()
            content = (
                str(detected)
                if detected is not None
                else data.decode("utf-8", errors="ignore")
            )

        content = content.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")

        # A cue starts at each timing line and runs to the next one, so a cue
        # with a blank line inside it, or a missing separator, still parses.
        lines = content.split("\n")
        timings = [
            (i, m)
            for i, line in enumerate(lines)
            if (m := _TIMING_RE.match(line.strip()))
        ]
        if not timings and content.strip():
            raise ValueError("No SRT cues found.")

        cues = []
        for n, (i, timing) in enumerate(timings):
            end = timings[n + 1][0] if n + 1 < len(timings) else len(lines)
            body = [line.strip() for line in lines[i + 1 : end]]
            while body and not body[-1]:
                body.pop()
            # The last line before the next timing line is its cue number.
            if n + 1 < len(timings) and body and body[-1].isdigit():
                body.pop()

            text = " ".join(_MARKUP_RE.sub("", " ".join(body)).split())
            if text:
                hours, minutes, seconds = timing.groups()
                cues.append(f"[{hours.zfill(2)}:{minutes}:{seconds}] {text}")

        return DocumentConverterResult(markdown="\n\n".join(cues))
