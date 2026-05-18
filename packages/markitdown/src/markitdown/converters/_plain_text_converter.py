"""PlainTextConverter — text/*, JSON/JSONL, Markdown files → Markdown.

Phase 2.5 exploratory rewrite:
  - JSON/JSONL → structured Markdown tables (key-value or multi-column)
  - Title extraction from content first line or filename
  - Clean method decomposition for maintainability
  - Preserves backward compatibility (existing test vectors pass)
"""

import sys
import json as _json
import logging

from typing import Any, BinaryIO, List, Optional

from charset_normalizer import from_bytes

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import FileConversionException

logger = logging.getLogger(__name__)

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/",
    "application/json",
    "application/markdown",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".txt",
    ".text",
    ".md",
    ".markdown",
    ".json",
    ".jsonl",
]

# Files larger than this skip JSON parsing (fallback to raw text pass-through)
_MAX_JSON_PARSE_BYTES = 10 * 1024 * 1024  # 10 MB


class PlainTextConverter(DocumentConverter):
    """Converts plain text, JSON, JSONL, and Markdown files to Markdown.

    JSON/JSONL files are rendered as structured Markdown tables.
    Plain text and Markdown files pass through as-is.
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        if stream_info.charset is not None:
            return True
        return self._accepted_by_mime_or_ext(
            stream_info, ACCEPTED_MIME_TYPE_PREFIXES, ACCEPTED_FILE_EXTENSIONS
        )

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        raw_bytes = file_stream.read()
        if not raw_bytes:
            return DocumentConverterResult(markdown="")

        # --- Decode bytes → text ---
        text_content = self._decode(raw_bytes, stream_info)

        ext = (stream_info.extension or "").lower()

        # --- Structured JSON/JSONL rendering ---
        if ext in (".json",) and ext != ".ipynb":
            text_content = self._render_json(text_content, raw_bytes)
        elif ext == ".jsonl":
            text_content = self._render_jsonl(text_content, raw_bytes)

        # --- Title extraction ---
        title = self._extract_title(text_content, stream_info)

        return DocumentConverterResult(markdown=text_content, title=title)

    # ================================================================
    #  Decode
    # ================================================================

    def _decode(self, raw_bytes: bytes, stream_info: StreamInfo) -> str:
        """Decode raw bytes using known charset or auto-detection."""
        try:
            if stream_info.charset:
                return raw_bytes.decode(stream_info.charset)
            result = from_bytes(raw_bytes)
            best = result.best()
            if best is None:
                raise FileConversionException(
                    "PlainTextConverter: charset detection returned no result"
                )
            return str(best)
        except (UnicodeDecodeError, LookupError) as e:
            logger.warning("PlainText encoding detection failed: %s", e)
            raise FileConversionException(
                f"PlainTextConverter: unable to decode content with "
                f"charset={stream_info.charset}: {e}"
            ) from e

    # ================================================================
    #  Title extraction
    # ================================================================

    def _extract_title(self, text: str, stream_info: StreamInfo) -> Optional[str]:
        """Extract a title from the content or filename.

        Priority: filename (without extension) > first markdown heading >
        first non-empty line.
        """
        if stream_info.filename:
            name = stream_info.filename.rsplit(".", 1)[0]
            if name:
                return name

        # Try first heading
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()

        # Try first non-empty line (truncate if too long)
        for line in text.splitlines():
            stripped = line.strip()
            if stripped:
                return stripped[:80] + ("..." if len(stripped) > 80 else "")

        return None

    # ================================================================
    #  JSON / JSONL → Markdown
    # ================================================================

    def _render_json(self, text: str, raw_bytes: bytes) -> str:
        """Render JSON content as Markdown table(s). Falls back to raw text."""
        if len(raw_bytes) > _MAX_JSON_PARSE_BYTES:
            return text  # Too large; pass through as-is

        try:
            data = _json.loads(text)
            return self._render_value(data)
        except (_json.JSONDecodeError, ValueError, TypeError) as e:
            logger.debug("JSON → Markdown fallback (invalid JSON): %s", e)
            return text

    def _render_jsonl(self, text: str, raw_bytes: bytes) -> str:
        """Render JSONL content as a Markdown table."""
        if len(raw_bytes) > _MAX_JSON_PARSE_BYTES:
            return text

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return text

        objects: List[dict] = []
        for line in lines:
            try:
                obj = _json.loads(line)
                if isinstance(obj, dict):
                    objects.append(obj)
                else:
                    return text  # Non-dict in JSONL → fallback
            except _json.JSONDecodeError:
                return text

        if not objects:
            return text

        # Collect all unique keys in order of first appearance
        all_keys = list(dict.fromkeys(k for obj in objects for k in obj))
        return self._dicts_to_table(objects, all_keys)

    def _render_value(self, data: Any) -> str:
        """Render a parsed JSON value as Markdown."""
        if isinstance(data, dict):
            # Single flat dict → two-column key-value table
            rows = [f"| {k} | {self._fmt(v)} |" for k, v in data.items()]
            return "\n".join(["| Key | Value |", "|-----|-------|"] + rows)

        if isinstance(data, list):
            if not data:
                return "*empty list*"
            if all(isinstance(item, dict) for item in data):
                all_keys = list(dict.fromkeys(k for obj in data for k in obj))
                return self._dicts_to_table(data, all_keys)
            # Simple list → markdown list
            return "\n".join(f"- {self._fmt(item)}" for item in data)

        return str(data)

    def _dicts_to_table(self, objects: List[dict], keys: List[str]) -> str:
        """Render a list of dicts as a multi-column Markdown table."""
        header = "| " + " | ".join(str(k) for k in keys) + " |"
        sep = "|" + "|".join(" --- " for _ in keys) + "|"
        lines = [header, sep]
        for obj in objects:
            row = "| " + " | ".join(self._fmt(obj.get(k, "")) for k in keys) + " |"
            lines.append(row)
        return "\n".join(lines)

    @staticmethod
    def _fmt(v: Any) -> str:
        """Format a JSON value for safe Markdown table inclusion."""
        if v is None:
            return ""
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, (int, float)):
            return str(v)
        if isinstance(v, str):
            # Escape pipes and compact whitespace for table cells
            return v.replace("|", "\\|").replace("\n", " ")
        if isinstance(v, (list, dict)):
            return _json.dumps(v, ensure_ascii=False)
        return str(v)
