import sys
import io
from warnings import warn

from typing import BinaryIO, Any, Optional

from ._html_converter import HtmlConverter
from ..converter_utils.docx.pre_process import pre_process_docx
from .._base_converter import DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import mammoth

except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]

ACCEPTED_FILE_EXTENSIONS = [".docx"]

DOCX_TABLE_FORMAT_MARKDOWN = "markdown"
DOCX_TABLE_FORMAT_HTML = "html"
DOCX_TABLE_FORMATS = {DOCX_TABLE_FORMAT_MARKDOWN, DOCX_TABLE_FORMAT_HTML}


def _validate_docx_table_format(docx_table_format: str) -> str:
    if docx_table_format not in DOCX_TABLE_FORMATS:
        raise ValueError(
            "docx_table_format must be one of: " + ", ".join(sorted(DOCX_TABLE_FORMATS))
        )
    return docx_table_format


class DocxConverter(HtmlConverter):
    """
    Converts DOCX files to Markdown. Style information (e.g.m headings) and tables are preserved where possible.
    """

    def __init__(
        self,
        *,
        docx_table_format: str = DOCX_TABLE_FORMAT_MARKDOWN,
        docx_markdownify_options: Optional[dict[str, Any]] = None,
    ):
        super().__init__()
        self._html_converter = HtmlConverter()
        self._docx_table_format = _validate_docx_table_format(docx_table_format)
        self._docx_markdownify_options = dict(docx_markdownify_options or {})

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
        # Check: the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".docx",
                    feature="docx",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        docx_table_format = _validate_docx_table_format(
            kwargs.pop("docx_table_format", self._docx_table_format)
        )
        docx_markdownify_options = dict(self._docx_markdownify_options)
        docx_markdownify_options.update(
            kwargs.pop("docx_markdownify_options", {}) or {}
        )
        if docx_table_format == DOCX_TABLE_FORMAT_HTML:
            docx_markdownify_options["_preserve_html_tables"] = True
        else:
            docx_markdownify_options.pop("_preserve_html_tables", None)

        style_map = kwargs.get("style_map", None)
        html_converter_kwargs = {**kwargs, **docx_markdownify_options}
        pre_process_stream = pre_process_docx(file_stream)
        return self._html_converter.convert_string(
            mammoth.convert_to_html(pre_process_stream, style_map=style_map).value,
            **html_converter_kwargs,
        )
