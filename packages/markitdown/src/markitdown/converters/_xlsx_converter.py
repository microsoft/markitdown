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


# Currency symbols that may appear in Excel number formats, either as quoted
# literals (e.g. '"$"#,##0.00') or locale blocks (e.g. '[$€-x-euro2]').
# See https://github.com/microsoft/markitdown/issues/53.
_CURRENCY_SYMBOL_RE = re.compile(r'[$€£¥₹₽₩₪₺₴₸₫₦¤]')
_LOCALE_BLOCK_RE = re.compile(r'\[\$([^\]-]+)')
_QUOTED_LITERAL_RE = re.compile(r'"([^"]*)"')


def _currency_symbol(number_format: Any) -> Optional[str]:
  """Return the currency symbol of an Excel number format, if it has one.

  Only the first (`;`-separated) section is considered, matching how
  positive values are rendered.
  """
  if not isinstance(number_format, str):
    return None
  first_section = number_format.split(';')[0]
  quoted = ''.join(_QUOTED_LITERAL_RE.findall(first_section))
  locale = ''.join(_LOCALE_BLOCK_RE.findall(first_section))
  candidates = quoted + locale
  if not candidates:
    candidates = first_section
  match = _CURRENCY_SYMBOL_RE.search(candidates)
  return match.group(0) if match else None


def _is_currency_position_prefix(number_format: str) -> bool:
  """Decide whether the currency symbol renders before the value."""
  first_section = number_format.split(';')[0]
  symbol_match = _CURRENCY_SYMBOL_RE.search(first_section)
  placeholder_match = re.search(r'[#0?]', first_section)
  if not symbol_match or not placeholder_match:
    return True
  return symbol_match.start() < placeholder_match.start()


def _overlay_currency_labels(
    sheets: dict[str, Any], workbook_stream: BinaryIO
) -> None:
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
    workbook = openpyxl.load_workbook(
        workbook_stream, data_only=True, read_only=True
    )
  except Exception:
    return
  try:
    for worksheet in workbook.worksheets:
      frame = sheets.get(worksheet.title)
      if frame is None:
        continue
      object_cols: set[int] = set()
      # pandas treats the first row as the header, so data row i lives in
      # openpyxl row i + 2 (both 1-indexed vs 0-indexed and header offset).
      for openpyxl_row in worksheet.iter_rows(min_row=2):
        for cell in openpyxl_row:
          value = cell.value
          if (
              value is None
              or isinstance(value, bool)
              or not isinstance(value, (int, float))
          ):
            continue
          symbol = _currency_symbol(cell.number_format)
          if symbol is None:
            continue
          data_row = cell.row - 2
          data_col = cell.column - 1
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
          if _is_currency_position_prefix(str(cell.number_format)):
            text = f'{symbol}{text}'
          else:
            text = f'{text}{symbol}'
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
