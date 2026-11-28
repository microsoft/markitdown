import io
import re
import sys
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
    import openpyxl
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


_CURRENCY_SYMBOLS = ("$", "£", "€", "¥", "₹", "₩", "₪", "₺", "₫")


# Matches a condition bracket: [>=100], [<0], [>=.5], [>=1E3].
# (?:\d+\.?\d*|\.\d+) accepts thresholds with or without a leading digit.
# (?:[eE][+-]?\d+)? adds optional scientific-notation exponent.
# search() (not match()) lets a leading colour code such as [Red] precede the bracket.
_CONDITION_RE = re.compile(
    r"\[([<>]=?|=)(-?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)\]"
)

# Matches a double-quoted Excel format literal: "text".  Used to blank out
# quoted spans before scanning a section for condition brackets so that
# bracket-like content inside quotes (e.g. "val[>=0]") is never mistaken for
# a conditional operator.  Excel format strings do not support escape sequences
# inside double-quoted literals, so a simple [^"]* inner pattern is correct.
_QUOTED_RE = re.compile(r'"[^"]*"')


def _condition_match_outside_quotes(section: str):
    """Return a _CONDITION_RE match from text that is outside quoted literals.

    Replaces every "..." span with spaces of equal length so that bracket
    content inside quotes is invisible to _CONDITION_RE while all character
    positions remain unchanged — m.start()/m.end() index correctly into the
    original section string.
    """
    blanked = _QUOTED_RE.sub(lambda m: " " * len(m.group()), section)
    return _CONDITION_RE.search(blanked)


def _select_format_section(fmt: str, value: object) -> str:
    """Return the format section applicable to *value*.

    Excel's sign-based rules (sections without conditional operators):
      1 section  → applies to everything
      2 sections → [0] positive/zero, [1] negative
      3 sections → [0] positive, [1] negative, [2] zero
      4 sections → [0] positive, [1] negative, [2] zero, [3] text

    When sections contain a conditional operator ([>N], [>=N], [<N], [<=N],
    [=N]) — possibly preceded by a color code such as [Red] — the first
    section whose condition evaluates to True is used; the condition bracket is
    removed from the returned section so color/locale brackets remain intact.
    The first section without a condition serves as the catch-all. If no
    condition matches and there is no catch-all, an empty string is returned so
    that _extract_currency_prefix() produces no prefix rather than searching a
    section that does not apply to this value.
    """
    sections = fmt.split(";")
    n = len(sections)
    if n <= 1:
        return fmt

    has_conditional = any(_condition_match_outside_quotes(s) for s in sections)

    if not has_conditional:
        # Standard sign-based section selection
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return sections[3] if n >= 4 else sections[0]
        if n == 2:
            return sections[1] if value < 0 else sections[0]
        # n >= 3
        if value > 0:
            return sections[0]
        if value < 0:
            return sections[1]
        return sections[2]  # zero

    # Conditional format: evaluate sections in declaration order.
    # Non-numeric values cannot satisfy numeric conditions → no prefix.
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return ""

    fval = float(value)
    catch_all: Optional[str] = None
    for section in sections:
        m = _condition_match_outside_quotes(section)
        if m:
            op, threshold = m.group(1), float(m.group(2))
            matched = (
                (op == ">" and fval > threshold)
                or (op == ">=" and fval >= threshold)
                or (op == "<" and fval < threshold)
                or (op == "<=" and fval <= threshold)
                or (op == "=" and fval == threshold)
            )
            if matched:
                # Remove the condition bracket; keep any preceding color/locale
                # brackets (e.g. [Red]) so _extract_currency_prefix can process them.
                return section[: m.start()] + section[m.end() :]
        elif catch_all is None:
            catch_all = section  # first unconditional section is the catch-all

    # No condition matched — use the catch-all, or "" if none exists.
    return catch_all if catch_all is not None else ""


def _extract_currency_prefix(fmt: str) -> Optional[str]:
    """Return the currency symbol or code from an openpyxl number_format string.

    Handles Excel locale blocks ([$USD-409] → 'USD', [$€-407] → '€'),
    bare locale markers ([$-409] → None), color prefixes, and simple symbols.
    Returns None for non-currency formats such as percentages or General.
    """
    if not fmt or fmt in ("General", "@"):
        return None
    # An unmatched " indicates a malformed format (unclosed quoted literal).
    # Scanning such a string for currency symbols is unreliable; fail safely.
    if '"' in _QUOTED_RE.sub("", fmt):
        return None
    # [$USD-409] → 'USD', [$€-407] → '€'; [$-409] has no chars before '-', no match.
    m = re.search(r"\[\$([^-\]]+)", fmt)
    if m:
        return m.group(1)
    # Blank out multi-character quoted literals so that a dollar sign in display
    # text like "$10 off" is not mistaken for a currency prefix.  Single-symbol
    # quoted literals ("$", "£", …) are preserved so they ARE recognised.
    def _keep_single_symbol(qm: re.Match) -> str:
        inner = qm.group()[1:-1]
        return qm.group() if (len(inner) == 1 and inner in _CURRENCY_SYMBOLS) else " " * len(qm.group())
    stripped = re.sub(r"\[[^\]]*\]", "", _QUOTED_RE.sub(_keep_single_symbol, fmt))
    for sym in _CURRENCY_SYMBOLS:
        if sym in stripped:
            return sym
    return None


def _build_currency_overlays(
    workbook_stream: BinaryIO,
) -> dict[str, dict[tuple[int, int], tuple[str, Any]]]:
    """Return per-sheet maps of (df_row_index, column_index) → (prefix, display_value).

    Uses openpyxl to read cell.number_format, which pandas discards.
    For sign-based negative sections (no conditional operators), display_value is
    abs(cell.value) to match Excel's convention of applying the negative section to
    the absolute value.  For conditional sections, the actual value is used.
    workbook_stream may be at any position; openpyxl locates the ZIP central
    directory by seeking from the end of the stream.
    """
    overlays: dict[str, dict[tuple[int, int], tuple[str, Any]]] = {}
    wb = openpyxl.load_workbook(workbook_stream, data_only=True, read_only=True)
    try:
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            rows = list(ws.iter_rows())
            if not rows:
                continue
            sheet_overlay: dict[tuple[int, int], tuple[str, Any]] = {}
            for df_row_idx, row in enumerate(rows[1:]):
                for cell in row:
                    if cell.value is None:
                        continue
                    col_idx = cell.column - 1
                    fmt_string = cell.number_format or ""
                    applicable_fmt = _select_format_section(fmt_string, cell.value)
                    prefix = _extract_currency_prefix(applicable_fmt)
                    if (
                        prefix
                        and isinstance(cell.value, (int, float))
                        and not isinstance(cell.value, bool)
                    ):
                        is_conditional = any(
                            _condition_match_outside_quotes(s)
                            for s in fmt_string.split(";")
                        )
                        display_val: Any = (
                            abs(cell.value)
                            if (not is_conditional and cell.value < 0)
                            else cell.value
                        )
                        sheet_overlay[(df_row_idx, col_idx)] = (prefix, display_val)
            if sheet_overlay:
                overlays[sheet_name] = sheet_overlay
    finally:
        wb.close()
    return overlays


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

            currency_overlays = _build_currency_overlays(workbook_stream)

            for s in sheets:
                md_content += f"## {s}\n"
                sheet_df = sheets[s]
                if s in currency_overlays:
                    sheet_df = sheet_df.copy().astype(object)
                    for (df_row_idx, col_idx), (prefix, display_val) in currency_overlays[s].items():
                        if df_row_idx < len(sheet_df) and col_idx < len(sheet_df.columns):
                            sheet_df.iloc[df_row_idx, col_idx] = f"{prefix}{display_val}"
                html_content = sheet_df.to_html(index=False)
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
