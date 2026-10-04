import io
import re
import sys
import unicodedata
import zipfile
from contextlib import contextmanager
from typing import BinaryIO, Any, Iterator, Optional
from ._html_converter import HtmlConverter
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from .._stream_info import StreamInfo

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_xlsx_dependency_exc_info = None
try:
    import pandas as pd
    import openpyxl  # noqa: F401
except ImportError:
    _xlsx_dependency_exc_info = sys.exc_info()

_xls_dependency_exc_info = None
try:
    import pandas as pd  # noqa: F811
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


# Bracketed number-format syntax that never renders as cell text, e.g. locale
# blocks ([$-409]), color tags ([Red], [Color10]) and explicit conditions
# ([>=100]). See https://github.com/microsoft/markitdown/issues/53.
_SQUARE_BLOCK_RE = re.compile(r"\[[^\]]*\]")
# Quoted literals (e.g. '"$"#,##0.00'), honoring backslash escapes.
_QUOTED_LITERAL_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')
# Locale blocks that display a literal currency token (e.g. [$€-x-euro2]
# shows €, [$USD-409] shows USD). A payload starting with "-" ([$-409]) is
# locale metadata only, and "[$$-...]" names the system symbol, which cannot
# be determined statically, so neither contributes a token.
_LOCALE_CURRENCY_RE = re.compile(r"\[\$([^\]]*)\]")
# Leading explicit condition of a format section (e.g. [>=100]"$"0).
_CONDITION_RE = re.compile(r"^\s*\[(>=|<=|<>|>|<|=)\s*([^\]]+?)\s*\]")
# ISO 4217 currency codes are exactly three uppercase ASCII letters.
_CURRENCY_CODE_RE = re.compile(r"^[A-Z]{3}$")


def _find_currency_symbol(text: str) -> tuple[Optional[str], int]:
    """Return the first Unicode currency symbol (category Sc) and its index.

    Detecting category Sc covers every currency sign (e.g. $, €, ฿, ₱)
    instead of maintaining a partial hard-coded list.
    """
    for index, char in enumerate(text):
        if unicodedata.category(char) == "Sc":
            return char, index
    return None, -1


def _split_format_sections(number_format: str) -> list[str]:
    """Split an Excel number format on `;` separators.

    Separators inside quoted literals ("...") or escaped with a backslash
    are part of the section text, not separators.
    """
    parts: list[str] = []
    current: list[str] = []
    in_quotes = False
    escaped = False
    for char in number_format:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            current.append(char)
            escaped = True
        elif char == '"':
            in_quotes = not in_quotes
            current.append(char)
        elif char == ";" and not in_quotes:
            parts.append("".join(current))
            current = []
        else:
            current.append(char)
    parts.append("".join(current))
    return parts


def _strip_square_blocks(section: str) -> str:
    """Remove bracketed metadata (locale/color/condition blocks)."""
    return _SQUARE_BLOCK_RE.sub("", section)


def _display_text(section: str) -> str:
    """Section with metadata removed but displayed tokens preserved.

    Locale blocks carrying a literal token ([$USD-409] shows USD) are
    replaced by that token; locale-only blocks ([$-409]), system-symbol
    blocks ([$$-...]) and color/condition blocks are removed.
    """
    return _SQUARE_BLOCK_RE.sub(
        "", _LOCALE_CURRENCY_RE.sub(_locale_block_replacement, section)
    )


def _locale_block_replacement(match: re.Match[str]) -> str:
    payload = match.group(1)
    if payload.startswith("-") or payload.startswith("$"):
        return ""
    return payload.split("-", 1)[0].strip()


def _unescape_literal(text: str) -> str:
    """Collapse backslash escapes inside a quoted literal."""
    return re.sub(r"\\(.)", r"\1", text)


def _select_format_section(number_format: str, value: Any) -> str:
    """Pick the `;`-separated Excel section that applies to `value`.

    Without explicit conditions Excel uses: 1 section = all numbers,
    2 sections = positive+zero / negative, 3 sections = positive / negative
    / zero (a 4th text section is ignored). Explicit conditions such as
    [>=100] override the sign rules: the first matching section wins and an
    unconditional section acts as the fallback for values reaching it.
    """
    parts = _split_format_sections(number_format)
    if value is None or len(parts) == 1:
        return parts[0]
    try:
        numeric = float(value)
    except Exception:
        return parts[0]
    if not any(_CONDITION_RE.match(part) for part in parts):
        if len(parts) == 2:
            # Zero renders with the first section when only two are present.
            return parts[1] if numeric < 0 else parts[0]
        if numeric > 0:
            return parts[0]
        if numeric < 0:
            return parts[1]
        return parts[2]
    for part in parts:
        match = _CONDITION_RE.match(part)
        if match is None:
            return part
        if _condition_matches(match.group(1), match.group(2), numeric):
            return part
    return parts[0]


def _condition_matches(operator: str, target: str, value: float) -> bool:
    """Evaluate an explicit section condition such as [>=100]."""
    try:
        bound = float(target)
    except ValueError:
        return False
    if operator == ">=":
        return value >= bound
    if operator == "<=":
        return value <= bound
    if operator == "<>":
        return value != bound
    if operator == ">":
        return value > bound
    if operator == "<":
        return value < bound
    return value == bound


def _display_currency_tokens(section: str) -> list[str]:
    """Currency labels a format section actually displays, in order.

    Quoted literals keep their full label ("R$", not "$"); locale blocks
    contribute their literal payload ([$USD-409] shows USD) while
    locale-only blocks ([$-409]) and system-symbol blocks ([$$-...])
    contribute nothing; anything else must be a bare currency symbol.
    """
    tokens: list[str] = []
    for raw in _QUOTED_LITERAL_RE.findall(section):
        literal = _unescape_literal(raw).strip()
        if not literal:
            continue
        symbol, _ = _find_currency_symbol(literal)
        if symbol is not None:
            tokens.append(literal)
        elif _CURRENCY_CODE_RE.match(literal):
            tokens.append(literal)
    for match in _LOCALE_CURRENCY_RE.finditer(section):
        payload = match.group(1)
        if payload.startswith("-") or payload.startswith("$"):
            continue
        token = payload.split("-", 1)[0].strip()
        if token:
            tokens.append(token)
    display = _QUOTED_LITERAL_RE.sub("", _strip_square_blocks(section))
    symbol, _ = _find_currency_symbol(display)
    if symbol is not None:
        tokens.append(symbol)
    return tokens


def _currency_symbol(number_format: Any, value: Any = None) -> Optional[str]:
    """Return the currency label of an Excel number format, if it has one.

    When `value` is given, the `;`-separated section matching it (by sign,
    or by explicit conditions such as [>=100]) is inspected. Otherwise the
    first section is used, matching how positive values are rendered.
    """
    if not isinstance(number_format, str):
        return None
    section = (
        _select_format_section(number_format, value)
        if value is not None
        else _split_format_sections(number_format)[0]
    )
    tokens = _display_currency_tokens(section)
    return tokens[0] if tokens else None


def _is_currency_position_prefix(number_format: str, value: Any = None) -> bool:
    """Decide whether the currency label renders before the value.

    Placement is computed from the displayed label and numeric placeholders
    in the metadata-stripped section. Quoted and escaped literal digits are
    excluded from the numeric placeholder search.
    """
    if not isinstance(number_format, str):
        return True
    section = (
        _select_format_section(number_format, value)
        if value is not None
        else _split_format_sections(number_format)[0]
    )
    tokens = _display_currency_tokens(section)
    if not tokens:
        return True
    display = _display_text(section)
    position = display.find(tokens[0])
    placeholders = _QUOTED_LITERAL_RE.sub(
        lambda match: " " * len(match.group(0)), display
    )
    placeholders = re.sub(r"\\.", lambda match: " " * len(match.group(0)), placeholders)
    placeholder_match = re.search(r"[#0?]", placeholders)
    if position == -1 or placeholder_match is None:
        return True
    return position < placeholder_match.start()


def _overlay_currency_labels(sheets: dict[str, Any], workbook_stream: BinaryIO) -> None:
    """Rewrite currency-formatted numeric cells with their display label.

    `pandas.read_excel` returns raw values and drops Excel number formats, so
    currency-formatted cells lose their label (e.g. 1199 instead of $1199).
    This overlays the label in place so the downstream HTML/markdown table
    shows what the spreadsheet shows. DataFrames are mutated in place.
    """
    import openpyxl  # Local import: already a required dependency (see above).

    position = workbook_stream.tell()
    try:
        workbook_stream.seek(0)
        workbook = openpyxl.load_workbook(workbook_stream, data_only=True)
    except Exception:
        return
    try:
        for worksheet in workbook.worksheets:
            frame = sheets.get(worksheet.title)
            if frame is None:
                continue
            object_cols: set[int] = set()
            # Drive iteration from the rows pandas actually read: the
            # declared worksheet dimension can be stale (hiding trailing
            # rows from iter_rows()) while pandas still returns them.
            # pandas treats the first row as the header, so data row i
            # lives in openpyxl row i + 2.
            for data_row in range(len(frame)):
                for data_col in range(len(frame.columns)):
                    cell = worksheet.cell(row=data_row + 2, column=data_col + 1)
                    value = cell.value
                    if (
                        value is None
                        or isinstance(value, bool)
                        or not isinstance(value, (int, float))
                    ):
                        continue
                    symbol = _currency_symbol(cell.number_format, value)
                    if symbol is None:
                        continue
                    if not (0 <= data_row < len(frame)) or not (
                        0 <= data_col < len(frame.columns)
                    ):
                        continue
                    text = str(frame.iat[data_row, data_col])
                    if symbol in text:
                        continue
                    if data_col not in object_cols:
                        # A str label cannot live in a numeric column: widen it once.
                        frame[frame.columns[data_col]] = frame[
                            frame.columns[data_col]
                        ].astype(object)
                        object_cols.add(data_col)
                    if _is_currency_position_prefix(str(cell.number_format), value):
                        text = f"{symbol}{text}"
                    else:
                        text = f"{text}{symbol}"
                    frame.iat[data_row, data_col] = text
    finally:
        try:
            workbook.close()
        except Exception:
            pass
        try:
            workbook_stream.seek(position)
        except Exception:
            pass


# Some producers write the legacy attribute "showZeroes" on <sheetView>, where the
# schema calls it "showZeros". openpyxl rejects the unknown attribute outright, so the
# workbook is repaired by renaming it. The rename is confined to <sheetView> start tags.
_SHEET_VIEW_START_TAG = re.compile(rb"<sheetView(?=[\s/>])[^>]*>")
_SHOW_ZEROES_ATTRIBUTE = re.compile(rb"(?<=[\s])showZeroes(\s*=)")


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
            # pandas drops Excel number formats: overlay currency labels so
            # currency-formatted cells render as the spreadsheet shows them.
            _overlay_currency_labels(sheets, workbook_stream)
            images = None
            if type(self)._image_to_html is not XlsxConverter._image_to_html:
                from ..converter_utils._xlsx_images import _XlsxImages

                images = _XlsxImages(workbook_stream)

            for s in sheets:
                md_content += f"## {s}\n"
                html_content = sheets[s].to_html(index=False)
                md_content += (
                    self._html_converter.convert_string(
                        html_content, **kwargs
                    ).markdown.strip()
                    + "\n\n"
                )
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
    ) -> Optional[str]:
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
