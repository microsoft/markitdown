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


# Some producers write the legacy attribute "showZeroes" on <sheetView>, where the
# schema calls it "showZeros". openpyxl rejects the unknown attribute outright, so the
# workbook is repaired by renaming it. The rename is confined to <sheetView> start tags.
_SHEET_VIEW_START_TAG = re.compile(rb"<sheetView(?=[\s/>])[^>]*>")
_SHOW_ZEROES_ATTRIBUTE = re.compile(rb"(?<=[\s])showZeroes(\s*=)")

# Currency symbols and ISO 4217 codes recognized in Excel number formats.
_CURRENCY_SYMBOLS = "$€£¥₹₩₽₺₴₫₪₸"
_CURRENCY_CODES = frozenset(
    "USD EUR GBP JPY CNY INR AUD CAD CHF SEK NOK DKK PLN CZK HUF ILS MXN BRL ARS "
    "CLP COP PEN ZAR NGN KES EGP SAR AED QAR KWD TRY RUB UAH SGD HKD TWD THB MYR "
    "IDR PHP VND KRW NZD".split()
)
_CURRENCY_FORMAT_RE = re.compile(
    r'\[\$([^\]-]+)[^\]]*\]|"([^"]+)"|([' + re.escape(_CURRENCY_SYMBOLS) + r"])|\b([A-Z]{3})\b"
)


def _format_currency(value: float, number_format: str) -> Optional[str]:
    """Render a number using an Excel currency number format.

    Returns None when the format carries no recognizable currency, so the
    caller keeps the value pandas produced.
    """
    section = (number_format or "General").split(";")[0]
    symbol = None
    symbol_pos = 0
    for match in _CURRENCY_FORMAT_RE.finditer(section):
        candidate = next(g for g in match.groups() if g is not None).strip()
        if (len(candidate) == 1 and candidate in _CURRENCY_SYMBOLS) or (
            len(candidate) == 3 and candidate.upper() in _CURRENCY_CODES
        ):
            symbol = candidate if len(candidate) == 1 else candidate.upper()
            symbol_pos = match.start()
            break
    if symbol is None:
        return None
    placeholder = re.search(r"[#0?]", section)
    if placeholder is None:
        return None
    decimals = re.search(r"\.(0+)", section)
    decimals = len(decimals.group(1)) if decimals else 0
    grouped = "," in section.split(".")[0]
    amount = f"{abs(value):,.{decimals}f}" if grouped else f"{abs(value):.{decimals}f}"
    sign = "-" if value < 0 else ""
    if symbol_pos < placeholder.start():
        sep = "" if len(symbol) == 1 else " "
        return f"{sign}{symbol}{sep}{amount}"
    return f"{sign}{amount} {symbol}"


def _apply_currency_formats(dataframe: Any, worksheet: Any) -> None:
    """Rewrite currency-formatted numeric cells as text carrying the currency.

    pandas only sees cell values, never number formats, so currency-formatted
    cells would otherwise render as bare numbers. Only cells holding a number
    whose format names a currency are touched; everything else keeps the
    value pandas produced.
    """
    if not len(dataframe) or not len(dataframe.columns):
        return
    replacements = {}
    rows = worksheet.iter_rows(
        min_row=2, max_row=len(dataframe) + 1, max_col=len(dataframe.columns)
    )
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            value = cell.value
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            text = _format_currency(value, cell.number_format)
            if text is not None:
                replacements[(i, j)] = text
    if not replacements:
        return
    for j in {j for _, j in replacements}:
        name = dataframe.columns[j]
        dataframe[name] = dataframe[name].astype(object)
    for (i, j), text in replacements.items():
        dataframe.iat[i, j] = text


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
            images = None
            if type(self)._image_to_html is not XlsxConverter._image_to_html:
                from ..converter_utils._xlsx_images import _XlsxImages

                images = _XlsxImages(workbook_stream)

            workbook_stream.seek(0)
            workbook = openpyxl.load_workbook(workbook_stream, read_only=True)
            try:
                for s in sheets:
                    if s in workbook.sheetnames:
                        _apply_currency_formats(sheets[s], workbook[s])
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
            finally:
                workbook.close()

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
