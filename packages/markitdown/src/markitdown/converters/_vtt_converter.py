import re
from typing import BinaryIO, Any, List, Optional
from charset_normalizer import from_bytes
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/vtt",
]
ACCEPTED_FILE_EXTENSIONS = [".vtt"]

# Matches WebVTT timestamp lines like: 00:00:00.000 --> 00:00:05.000
# Both HH:MM:SS.mmm and MM:SS.mmm forms are valid. Cue settings may follow.
_TIMESTAMP_RE = re.compile(
    r"^((?:\d{2}:)?\d{2}:\d{2}[.,]\d{3})\s*-->\s*((?:\d{2}:)?\d{2}:\d{2}[.,]\d{3})"
)

# WebVTT voice span: <v Speaker Name>text</v>
_VOICE_SPAN_RE = re.compile(r"<v\s+([^>]+)>")

# Any remaining WebVTT inline tags: <b>, <i>, <u>, <c.class>, timestamps, etc.
_TAG_RE = re.compile(r"<[^>]+>")


def _format_timestamp(ts: str) -> str:
    """Shorten HH:MM:SS.mmm to [HH:MM:SS] (drop milliseconds, drop leading 00: hours)."""
    ts = ts.replace(",", ".")
    # Drop milliseconds
    ts = ts.rsplit(".", 1)[0]
    # Drop leading "00:" for hours to keep it compact
    if ts.startswith("00:"):
        ts = ts[3:]
    return f"[{ts}]"


def _clean_cue_line(line: str) -> str:
    """
    Clean a single cue payload line:
    - Convert <v Speaker> to "Speaker: "
    - Strip all remaining inline tags
    """
    # Replace voice spans with "Speaker: " prefix
    line = _VOICE_SPAN_RE.sub(lambda m: f"{m.group(1).strip()}: ", line)
    # Strip all other tags
    line = _TAG_RE.sub("", line)
    return line.strip()


def _parse_vtt(content: str, include_timestamps: bool = False) -> List[str]:
    """
    Parse a WebVTT file and return formatted lines.

    When include_timestamps is False (default), only the cue text is returned
    and consecutive duplicate lines are collapsed (clean transcript mode).

    When include_timestamps is True, each cue is prefixed with its start
    timestamp in the form ``[HH:MM:SS] text`` (timestamp-preserving mode).
    """
    output_lines: List[str] = []

    # Split into blocks separated by one or more blank lines
    blocks = re.split(r"\n{2,}", content.strip())

    for block in blocks:
        lines = [line.strip() for line in block.splitlines()]

        # Skip the file header block (starts with WEBVTT)
        if lines and lines[0].startswith("WEBVTT"):
            continue

        # Find the timestamp line within the block
        ts_index: Optional[int] = None
        ts_match = None
        for i, line in enumerate(lines):
            m = _TIMESTAMP_RE.match(line)
            if m:
                ts_index = i
                ts_match = m
                break

        if ts_index is None:
            # No timestamp — skip this block (NOTE, STYLE, REGION, etc.)
            continue

        # Collect and clean the cue payload lines
        payload = [
            _clean_cue_line(line)
            for line in lines[ts_index + 1 :]
            if line
        ]
        payload = [p for p in payload if p]

        if not payload:
            continue

        if include_timestamps:
            assert ts_match is not None
            prefix = _format_timestamp(ts_match.group(1))
            # Indent continuation lines to align under the timestamp prefix
            indent = " " * (len(prefix) + 1)
            first = True
            for p in payload:
                if first:
                    output_lines.append(f"{prefix} {p}")
                    first = False
                else:
                    output_lines.append(f"{indent}{p}")
        else:
            output_lines.extend(payload)

    if not include_timestamps:
        # Collapse consecutive duplicate lines (common in rolling-caption VTT files)
        collapsed: List[str] = []
        for line in output_lines:
            if not collapsed or collapsed[-1] != line:
                collapsed.append(line)
        return collapsed

    return output_lines


class VttConverter(DocumentConverter):
    """
    Converts WebVTT subtitle files (.vtt) to Markdown.

    By default produces a clean transcript: timestamps and cue identifiers are
    stripped, speaker labels (``<v Name>``) are preserved as ``Name: text``,
    and consecutive duplicate lines are collapsed.

    Pass ``vtt_include_timestamps=True`` as a keyword argument to keep each
    cue's start timestamp in the output as ``[HH:MM:SS] text``.
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
        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if stream_info.charset:
            content = file_stream.read().decode(stream_info.charset)
        else:
            content = str(from_bytes(file_stream.read()).best())

        include_timestamps = bool(kwargs.get("vtt_include_timestamps", False))
        lines = _parse_vtt(content, include_timestamps=include_timestamps)
        markdown = "\n".join(lines)
        return DocumentConverterResult(markdown=markdown)
