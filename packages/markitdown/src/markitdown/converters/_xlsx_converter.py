from typing import Union

import pandas as pd

from ._base import DocumentConverter, DocumentConverterResult
from ._html_converter import HtmlConverter
from ._converter_input import ConverterInput


class XlsxConverter(HtmlConverter):
    """
    Converts XLSX files to Markdown, with each sheet presented as a separate Markdown table.
    """

    def __init__(
        self, priority: float = DocumentConverter.PRIORITY_SPECIFIC_FILE_FORMAT
    ):
        super().__init__(priority=priority)

    def convert(
        self, input: ConverterInput, **kwargs
    ) -> Union[None, DocumentConverterResult]:
        # Bail if not a XLSX
        extension = kwargs.get("file_extension", "")
        if extension.lower() != ".xlsx":
            return None

        file_obj = input.read_file(mode="rb")
        sheets = pd.read_excel(file_obj, sheet_name=None, engine="openpyxl")
        file_obj.close()

        md_content = ""
        for s in sheets:
            md_content += f"## {s}\n"
            html_content = sheets[s].to_html(index=False)
            md_content += self._convert(html_content).text_content.strip() + "\n\n"

        return DocumentConverterResult(
            title=None,
            text_content=md_content.strip(),
        )


class XlsConverter(HtmlConverter):
    """
    Converts XLS files to Markdown, with each sheet presented as a separate Markdown table.
    """

    def convert(
        self, input: ConverterInput, **kwargs
    ) -> Union[None, DocumentConverterResult]:
        # Bail if not a XLS
        extension = kwargs.get("file_extension", "")
        if extension.lower() != ".xls":
            return None

        file_obj = input.read_file(mode="rb")
        sheets = pd.read_excel(file_obj, sheet_name=None, engine="xlrd")
        file_obj.close()

        md_content = ""
        for s in sheets:
            md_content += f"## {s}\n"
            html_content = sheets[s].to_html(index=False)
            md_content += self._convert(html_content).text_content.strip() + "\n\n"

        return DocumentConverterResult(
            title=None,
            text_content=md_content.strip(),
        )
