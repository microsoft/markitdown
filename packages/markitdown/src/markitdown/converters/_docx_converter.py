import sys

from typing import Union

from ._base import (
    DocumentConverterResult,
)

from ._base import DocumentConverter
from ._html_converter import HtmlConverter
from .._exceptions import MissingDependencyException

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import mammoth
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


class DocxConverter(HtmlConverter):
    """
    Converts DOCX files to Markdown. Style information (e.g.m headings) and tables are preserved where possible.
    """

    def __init__(
        self, priority: float = DocumentConverter.PRIORITY_SPECIFIC_FILE_FORMAT
    ):
        super().__init__(priority=priority)

    def convert(self, local_path, **kwargs) -> Union[None, DocumentConverterResult]:
        # Bail if not a DOCX
        extension = kwargs.get("file_extension", "")
        if extension.lower() != ".docx":
            return None

        # Load the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                f"""{type(self).__name__} recognized the input as a potential .docx file, but the dependencies needed to read .docx files have not been installed. To resolve this error, include the optional dependency [docx] or [all] when installing MarkItDown. For example:

* pip install markitdown[docx]
* pip install markitdown[all]
* pip install markitdown[pptx, docx, ...]
* etc."""
            ) from _dependency_exc_info[1].with_traceback(
                _dependency_exc_info[2]
            )  # Restore the original traceback

        result = None
        with open(local_path, "rb") as docx_file:
            style_map = kwargs.get("style_map", None)

            result = mammoth.convert_to_html(docx_file, style_map=style_map)
            html_content = result.value
            result = self._convert(html_content)

        return result
