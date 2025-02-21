from typing import Union

import mammoth

from ._base import (
    DocumentConverterResult,
)

from ._base import DocumentConverter
from ._html_converter import HtmlConverter
from ._converter_input import ConverterInput


class DocxConverter(HtmlConverter):
    """
    Converts DOCX files to Markdown. Style information (e.g.m headings) and tables are preserved where possible.
    """

    def __init__(
        self, priority: float = DocumentConverter.PRIORITY_SPECIFIC_FILE_FORMAT
    ):
        super().__init__(priority=priority)

    def convert(
        self, input: ConverterInput, **kwargs
    ) -> Union[None, DocumentConverterResult]:
        # Bail if not a DOCX
        extension = kwargs.get("file_extension", "")
        if extension.lower() != ".docx":
            return None

        result = None
        style_map = kwargs.get("style_map", None)
        file_obj = input.read_file(mode="rb")
        result = mammoth.convert_to_html(file_obj, style_map=style_map)
        file_obj.close()
        html_content = result.value
        result = self._convert(html_content)

        return result
