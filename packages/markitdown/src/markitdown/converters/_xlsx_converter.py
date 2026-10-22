import inspect
import io
import re
import sys
import zipfile
from collections.abc import Iterator
from contextlib import contextmanager
from html import unescape
from html.parser import HTMLParser
from typing import Any, BinaryIO

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MISSING_DEPENDENCY_MESSAGE, MissingDependencyException
from .._stream_info import StreamInfo
from ._html_converter import HtmlConverter
from ._markdownify import _CustomMarkdownify

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_xlsx_dependency_exc_info = None
try:
    import openpyxl  # noqa: F401
    import pandas as pd
except ImportError:
    _xlsx_dependency_exc_info = sys.exc_info()

_xls_dependency_exc_info = None
try:
    import pandas as pd
    import xlrd  # noqa: F401
except ImportError:
    _xls_dependency_exc_info = sys.exc_info()

ACCEPTED_XLSX_MIME_TYPE_PREFIXES = [
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
]
ACCEPTED_XLSX_FILE_EXTENSIONS = [".xlsx"]

ACCEPTED_XLS_MIME_TYPE_PREFIXES = [
    "application/vnd.ms-excel",
    "application/excel",
]
ACCEPTED_XLS_FILE_EXTENSIONS = [".xls"]


# Some producers write the legacy attribute "showZeroes" on <sheetView>, where the
# schema calls it "showZeros". openpyxl rejects the unknown attribute outright, so the
# workbook is repaired by renaming it. The rename is confined to <sheetView> start tags.
_SHEET_VIEW_START_TAG = re.compile(rb"<sheetView(?=[\s/>])[^>]*>")
_SHOW_ZEROES_ATTRIBUTE = re.compile(rb"(?<=[\s])showZeroes(\s*=)")
_NON_ASCII_SPACE_WHITESPACE = re.compile(r"[^\S ]")

_PANDAS_TABLE_RE = re.compile(
    r'\A<table border="1" class="dataframe">\s*<thead>\s*'
    r"(?P<header><tr[^>]*>.*?</tr>)\s*</thead>\s*<tbody>\s*"
    r"(?P<body>.*?)</tbody>\s*</table>\s*\Z",
    re.DOTALL,
)


def _scan_pandas_rows(
    section: str,
    expected_tag: str,
    formatter: _CustomMarkdownify,
    expected_width: int | None = None,
) -> tuple[list[str], int] | None:
    lines: list[str] = []
    position = 0
    width = expected_width
    escape_has_parent_tags = (
        "parent_tags" in inspect.signature(formatter.escape).parameters
    )
    while position < len(section):
        if not section.startswith("<tr", position):
            return None
        tag_end = section.find(">", position + 3)
        row_end = section.find("</tr>", position)
        if tag_end < 0 or row_end < 0 or tag_end >= row_end:
            return None
        row_text = section[tag_end + 1 : row_end]
        open_tag = f"<{expected_tag}>"
        close_tag = f"</{expected_tag}>"
        parts = row_text.split(open_tag)
        if len(parts) < 2 or parts[0].strip():
            return None
        cells: list[str] = []
        for part in parts[1:]:
            raw, closing, trailing = part.partition(close_tag)
            if not closing or "<" in raw or trailing.strip():
                return None
            if "&" in raw:
                raw = unescape(raw)
            if _NON_ASCII_SPACE_WHITESPACE.search(raw) is not None:
                return None
            normalized = " ".join(raw.split()) if " " in raw else raw
            if escape_has_parent_tags:
                cells.append(formatter.escape(normalized, []))
            else:
                cells.append(formatter.escape(normalized))
        if not cells or (width is not None and len(cells) != width):
            return None
        width = len(cells)
        lines.append("| " + " | ".join(cells) + " |")
        position = row_end + len("</tr>")
        if position < len(section):
            next_tag = section.find("<", position)
            if next_tag < 0:
                if section[position:].strip():
                    return None
                position = len(section)
            elif section[position:next_tag].strip():
                return None
            else:
                position = next_tag
    return lines, width if width is not None else 0


def _pandas_table_to_markdown_scanner(html_content: str) -> str | None:
    table_match = _PANDAS_TABLE_RE.fullmatch(html_content.lstrip())
    if table_match is None:
        return None
    formatter = _CustomMarkdownify()
    header = _scan_pandas_rows(table_match.group("header"), "th", formatter)
    if header is None or len(header[0]) != 1 or header[1] == 0:
        return None
    body = _scan_pandas_rows(table_match.group("body"), "td", formatter, header[1])
    if body is None:
        return None
    lines = [header[0][0]]
    lines.append("| " + " | ".join("---" for _ in range(header[1])) + " |")
    lines.extend(body[0])
    return "\n".join(lines)


@contextmanager
def _read_xlsx_sheets(
    file_stream: BinaryIO,
) -> Iterator[tuple[dict[str, Any], BinaryIO]]:
    start_pos = file_stream.tell()
    repaired_stream = None
    try:
        try:
            sheets = pd.read_excel(file_stream, sheet_name=None, engine="openpyxl")
        except TypeError as exc:
            if "showZeroes" not in str(exc):
                raise
            repaired_stream = _repair_sheetview_show_zeroes(file_stream, start_pos)
            sheets = pd.read_excel(repaired_stream, sheet_name=None, engine="openpyxl")
        yield sheets, repaired_stream if repaired_stream is not None else file_stream
    finally:
        if repaired_stream is not None:
            repaired_stream.close()


def _rename_show_zeroes_attribute(data: bytes) -> bytes:
    return _SHEET_VIEW_START_TAG.sub(
        lambda match: _SHOW_ZEROES_ATTRIBUTE.sub(rb"showZeros\1", match.group(0)),
        data,
    )


def _repair_sheetview_show_zeroes(
    file_stream: BinaryIO, start_pos: int = 0
) -> io.BytesIO:
    file_stream.seek(start_pos)
    repaired_stream = io.BytesIO()

    with zipfile.ZipFile(file_stream) as source:
        with zipfile.ZipFile(repaired_stream, "w", zipfile.ZIP_DEFLATED) as target:
            for item in source.infolist():
                data = source.read(item.filename)
                if (
                    item.filename.startswith("xl/worksheets/")
                    and item.filename.endswith(".xml")
                    and b"showZeroes" in data
                ):
                    data = _rename_show_zeroes_attribute(data)
                target.writestr(item, data)

    repaired_stream.seek(0)
    return repaired_stream


class _PandasTableParser(HTMLParser):
    """Parse the restricted table HTML emitted by pandas.DataFrame.to_html."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[list[str]] = []
        self._formatter = _CustomMarkdownify()
        self._escape_has_parent_tags = (
            "parent_tags" in inspect.signature(self._formatter.escape).parameters
        )
        self._row: list[str] | None = None
        self._cell_text: list[str] | None = None
        self.valid = True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag == "tr":
            if self._row is not None or self._cell_text is not None:
                self.valid = False
            self._row = []
        elif tag in {"th", "td"}:
            if self._row is None or self._cell_text is not None:
                self.valid = False
            self._cell_text = []
        elif tag not in {"table", "thead", "tbody"}:
            self.valid = False

    def handle_data(self, data: str) -> None:
        if self._cell_text is not None:
            self._cell_text.append(data)
        elif data.strip():
            self.valid = False

    def handle_endtag(self, tag: str) -> None:
        if tag in {"th", "td"}:
            if self._row is None or self._cell_text is None:
                self.valid = False
                return
            raw = "".join(self._cell_text)
            if _NON_ASCII_SPACE_WHITESPACE.search(raw) is not None:
                self.valid = False
            normalized = " ".join(raw.split())
            if self._escape_has_parent_tags:
                self._row.append(self._formatter.escape(normalized, []))
            else:
                self._row.append(self._formatter.escape(normalized))
            self._cell_text = None
        elif tag == "tr":
            if self._row is None or self._cell_text is not None:
                self.valid = False
                return
            self.rows.append(self._row)
            self._row = None
        elif tag not in {"table", "thead", "tbody"}:
            self.valid = False


def _pandas_table_to_markdown_fastpath(html_content: str) -> str | None:
    """Convert simple pandas tables without traversing a general HTML DOM."""
    if not html_content.lstrip().startswith('<table border="1" class="dataframe">'):
        return None

    scanned = _pandas_table_to_markdown_scanner(html_content)
    if scanned is not None:
        return scanned

    parser = _PandasTableParser()
    parser.feed(html_content)
    parser.close()
    if (
        not parser.valid
        or parser._row is not None
        or parser._cell_text is not None
        or not parser.rows
    ):
        return None

    width = len(parser.rows[0])
    if width == 0 or any(len(row) != width for row in parser.rows):
        return None

    lines = ["| " + " | ".join(parser.rows[0]) + " |"]
    lines.append("| " + " | ".join("---" for _ in range(width)) + " |")
    lines.extend("| " + " | ".join(row) + " |" for row in parser.rows[1:])
    return "\n".join(lines)


class XlsxConverter(DocumentConverter):
    """
    Converts XLSX files to Markdown, with each sheet presented as a separate Markdown table.
    """

    def __init__(self):
        super().__init__()
        self._html_converter = HtmlConverter()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_XLSX_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_XLSX_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Check the dependencies
        if _xlsx_dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".xlsx",
                    feature="xlsx",
                )
            ) from _xlsx_dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _xlsx_dependency_exc_info[2]
            )

        md_content = ""
        with _read_xlsx_sheets(file_stream) as (sheets, workbook_stream):
            images = None
            if type(self)._image_to_html is not XlsxConverter._image_to_html:
                from ..converter_utils._xlsx_images import _XlsxImages

                images = _XlsxImages(workbook_stream)

            for s in sheets:
                md_content += f"## {s}\n"
                html_content = sheets[s].to_html(index=False)
                framework_keys = {"_parent_converters", "file_extension", "url"}
                formatting_kwargs = {key for key in kwargs if key not in framework_keys}
                table_markdown = None
                if not formatting_kwargs and images is None:
                    table_markdown = _pandas_table_to_markdown_fastpath(html_content)
                if table_markdown is None:
                    table_markdown = self._html_converter.convert_string(
                        html_content, **kwargs
                    ).markdown.strip()
                md_content += table_markdown + "\n\n"
                if images is not None:
                    image_content = images.to_html(s, self._image_to_html, kwargs)
                    if image_content:
                        md_content += (
                            self._html_converter.convert_string(
                                image_content, **kwargs
                            ).markdown.strip()
                            + "\n\n"
                        )

        return DocumentConverterResult(markdown=md_content.strip())

    def _image_to_html(
        self,
        image_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> str | None:
        """Override to render an embedded image as an HTML fragment.

        The stream is borrowed, seekable, and positioned at zero; do not close
        or retain it. StreamInfo describes the image, not the workbook. Existing
        conversion options are forwarded through kwargs.

        Return None or blank text to retain the native representation (no image
        output). Otherwise return HTML, escaping any literal text. Images appear
        after their sheet's table, in the existing worksheet image order. Linked
        images are not fetched. Hook failures propagate through the normal
        conversion failure path.
        """
        return None


class XlsConverter(DocumentConverter):
    """
    Converts XLS files to Markdown, with each sheet presented as a separate Markdown table.
    """

    def __init__(self):
        super().__init__()
        self._html_converter = HtmlConverter()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_XLS_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_XLS_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Load the dependencies
        if _xls_dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".xls",
                    feature="xls",
                )
            ) from _xls_dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _xls_dependency_exc_info[2]
            )

        sheets = pd.read_excel(file_stream, sheet_name=None, engine="xlrd")
        md_content = ""
        for s in sheets:
            md_content += f"## {s}\n"
            html_content = sheets[s].to_html(index=False)
            md_content += (
                self._html_converter.convert_string(
                    html_content, **kwargs
                ).markdown.strip()
                + "\n\n"
            )

        return DocumentConverterResult(markdown=md_content.strip())
