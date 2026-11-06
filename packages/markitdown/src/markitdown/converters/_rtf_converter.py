"""RTF (Rich Text Format) to Markdown converter.

Parses RTF control words and groups to extract styled text, tables, and
Unicode escapes, producing Markdown output.
"""

import re
from typing import Any, BinaryIO, Optional

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/rtf",
    "application/rtf",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".rtf",
]

# Mapping of RTF font-charset identifiers to Python codec names.
_CHARSET_MAP = {
    0: "cp1252",     # ANSI
    1: "cp1252",     # Default
    2: "symbol",
    77: "mac-roman",
    128: "cp932",    # Shift-JIS
    129: "cp949",    # Hangul
    134: "gb2312",
    136: "big5",
    161: "cp1253",   # Greek
    162: "cp1254",   # Turkish
    163: "cp1258",   # Vietnamese
    177: "cp1255",   # Hebrew
    178: "cp1256",   # Arabic
    186: "cp1257",   # Baltic
    204: "cp1251",   # Russian
    222: "cp874",    # Thai
    238: "cp1250",   # Eastern European
    255: "cp437",    # OEM
}


class _RTFToken:
    """Represents a single RTF token produced by the lexer."""

    __slots__ = ("kind", "value")

    # Token kinds
    GROUP_START = "group_start"
    GROUP_END = "group_end"
    CONTROL_WORD = "control_word"
    CONTROL_SYMBOL = "control_symbol"
    TEXT = "text"

    def __init__(self, kind: str, value: str = ""):
        self.kind = kind
        self.value = value


# Pre-compiled patterns used by the lexer.
_CTRL_WORD_RE = re.compile(r"\\([a-zA-Z]+)(-?\d+)? ?")
_CTRL_SYMBOL_RE = re.compile(r"\\([^a-zA-Z\r\n])")
_HEX_ESCAPE_RE = re.compile(r"\\'([0-9a-fA-F]{2})")
_UNICODE_RE = re.compile(r"\\u(-?\d+)[?]?")


def _tokenize(rtf: str):
    """Yield RTF tokens from *rtf* string."""
    pos = 0
    length = len(rtf)
    while pos < length:
        ch = rtf[pos]
        if ch == "{":
            yield _RTFToken(_RTFToken.GROUP_START)
            pos += 1
        elif ch == "}":
            yield _RTFToken(_RTFToken.GROUP_END)
            pos += 1
        elif ch == "\\":
            # Try Unicode escape first  \\uN
            m = _UNICODE_RE.match(rtf, pos)
            if m:
                yield _RTFToken(_RTFToken.CONTROL_WORD, m.group(0))
                pos = m.end()
                continue
            # Hex escape  \\'XX
            m = _HEX_ESCAPE_RE.match(rtf, pos)
            if m:
                yield _RTFToken(_RTFToken.CONTROL_SYMBOL, m.group(0))
                pos = m.end()
                continue
            # Control word  \\word[-]N?
            m = _CTRL_WORD_RE.match(rtf, pos)
            if m:
                yield _RTFToken(_RTFToken.CONTROL_WORD, m.group(0))
                pos = m.end()
                continue
            # Control symbol  \\<char>
            m = _CTRL_SYMBOL_RE.match(rtf, pos)
            if m:
                yield _RTFToken(_RTFToken.CONTROL_SYMBOL, m.group(0))
                pos = m.end()
                continue
            # Lone backslash (malformed) – skip
            pos += 1
        elif ch in ("\r", "\n"):
            pos += 1
        else:
            # Collect plain text until next special character
            start = pos
            while pos < length and rtf[pos] not in ("{", "}", "\\", "\r", "\n"):
                pos += 1
            yield _RTFToken(_RTFToken.TEXT, rtf[start:pos])


def _parse_control_word(token_value: str):
    """Return ``(word, param)`` from a control-word token value.

    *param* is ``None`` when the control word has no numeric parameter.
    """
    m = _CTRL_WORD_RE.match(token_value)
    if not m:
        return token_value.lstrip("\\").rstrip(), None
    word = m.group(1)
    param = int(m.group(2)) if m.group(2) is not None else None
    return word, param


def _decode_hex_escape(token_value: str, charset: str = "cp1252") -> str:
    """Decode an RTF hex escape (``\\'XX``) using *charset*."""
    m = _HEX_ESCAPE_RE.search(token_value)
    if not m:
        return ""
    byte_val = int(m.group(1), 16)
    try:
        return bytes([byte_val]).decode(charset)
    except (UnicodeDecodeError, LookupError):
        return bytes([byte_val]).decode("cp1252", errors="replace")


def _decode_unicode_escape(token_value: str) -> str:
    """Decode an RTF Unicode escape (``\\uN``) to a Python character."""
    m = _UNICODE_RE.search(token_value)
    if not m:
        return ""
    code_point = int(m.group(1))
    if code_point < 0:
        code_point += 65536
    try:
        return chr(code_point)
    except (ValueError, OverflowError):
        return "\ufffd"


class _RTFState:
    """Mutable formatting state tracked while walking tokens."""

    __slots__ = ("bold", "italic", "underline", "charset", "in_table", "cell_texts", "skip_group")

    def __init__(self):
        self.bold = False
        self.italic = False
        self.underline = False
        self.charset: str = "cp1252"
        self.in_table = False
        self.cell_texts: list[str] = []
        self.skip_group = False

    def copy(self) -> "_RTFState":
        new = _RTFState()
        new.bold = self.bold
        new.italic = self.italic
        new.underline = self.underline
        new.charset = self.charset
        new.in_table = self.in_table
        new.cell_texts = list(self.cell_texts)
        new.skip_group = self.skip_group
        return new


# Destination control words whose group contents should be skipped entirely.
_SKIP_DESTINATIONS = frozenset([
    "fonttbl", "colortbl", "stylesheet", "info", "pict",
    "header", "footer", "headerl", "headerr", "headerf",
    "footerl", "footerr", "footerf", "footnote",
    "field", "fldinst", "xe", "tc", "rxe",
])


def _rtf_to_markdown(rtf: str) -> str:
    """Convert raw RTF text to a Markdown string."""
    output_parts: list[str] = []
    state_stack: list[_RTFState] = []
    state = _RTFState()
    table_rows: list[list[str]] = []

    for token in _tokenize(rtf):
        if token.kind == _RTFToken.GROUP_START:
            state_stack.append(state.copy())
            continue

        if token.kind == _RTFToken.GROUP_END:
            if state_stack:
                state = state_stack.pop()
            continue

        if state.skip_group:
            continue

        if token.kind == _RTFToken.CONTROL_WORD:
            word, param = _parse_control_word(token.value)

            # Check for destination groups to skip
            if word in _SKIP_DESTINATIONS:
                state.skip_group = True
                continue

            # Style toggles
            if word == "b":
                state.bold = param != 0 if param is not None else True
            elif word == "i":
                state.italic = param != 0 if param is not None else True
            elif word == "ul" or word == "ulnone":
                state.underline = word == "ul"
            elif word == "plain":
                state.bold = False
                state.italic = False
                state.underline = False

            # Paragraph / line breaks
            elif word == "par" or word == "line":
                output_parts.append("\n\n" if word == "par" else "\n")
            elif word == "tab":
                output_parts.append("\t")

            # Table handling
            elif word == "trowd":
                state.in_table = True
                state.cell_texts = []
            elif word == "cell":
                state.cell_texts.append("".join(output_parts).split("\n")[-1].strip() if output_parts else "")
                # Remove the last text segment that was part of this cell
                if output_parts:
                    last_newline = -1
                    for idx in range(len(output_parts) - 1, -1, -1):
                        if "\n" in output_parts[idx]:
                            last_newline = idx
                            break
                    if last_newline >= 0:
                        output_parts = output_parts[: last_newline + 1]
                    else:
                        output_parts = []
            elif word == "row":
                if state.cell_texts:
                    table_rows.append(list(state.cell_texts))
                state.cell_texts = []
                state.in_table = False

            # Unicode escape
            elif word == "u":
                ch = _decode_unicode_escape(token.value)
                output_parts.append(ch)

            # Charset (from font table, but we track the last one seen)
            elif word == "fcharset":
                if param is not None and param in _CHARSET_MAP:
                    state.charset = _CHARSET_MAP[param]

            continue

        if token.kind == _RTFToken.CONTROL_SYMBOL:
            if token.value.startswith("\\'"):
                ch = _decode_hex_escape(token.value, state.charset)
                output_parts.append(ch)
            elif token.value == "\\~":
                output_parts.append("\u00a0")  # non-breaking space
            elif token.value == "\\-":
                pass  # optional hyphen – ignore
            elif token.value == "\\_":
                output_parts.append("\u2011")  # non-breaking hyphen
            continue

        if token.kind == _RTFToken.TEXT:
            text = token.value
            # Apply inline formatting
            if state.bold and state.italic:
                text = f"***{text}***"
            elif state.bold:
                text = f"**{text}**"
            elif state.italic:
                text = f"*{text}*"
            if state.underline:
                text = f"<u>{text}</u>"
            output_parts.append(text)

    # Flush any pending table rows
    md = "".join(output_parts)

    if table_rows:
        table_md_parts: list[str] = []
        for row_idx, row in enumerate(table_rows):
            table_md_parts.append("| " + " | ".join(row) + " |")
            if row_idx == 0:
                table_md_parts.append("| " + " | ".join("---" for _ in row) + " |")
        md = md.rstrip() + "\n\n" + "\n".join(table_md_parts)

    # Collapse excessive blank lines
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


class RtfConverter(DocumentConverter):
    """Convert RTF documents to Markdown."""

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
        raw_bytes = file_stream.read()

        # Try UTF-8 first, then fall back to latin-1 which never fails.
        charset = stream_info.charset
        if charset:
            try:
                rtf_text = raw_bytes.decode(charset)
            except (UnicodeDecodeError, LookupError):
                rtf_text = raw_bytes.decode("latin-1")
        else:
            try:
                rtf_text = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                rtf_text = raw_bytes.decode("latin-1")

        markdown = _rtf_to_markdown(rtf_text)
        return DocumentConverterResult(markdown=markdown)
