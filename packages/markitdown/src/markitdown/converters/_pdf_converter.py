import pdfminer
import pdfminer.high_level
from typing import Union
from io import StringIO
from ._base import DocumentConverter, DocumentConverterResult
from ._converter_input import ConverterInput


class PdfConverter(DocumentConverter):
    """
    Converts PDFs to Markdown. Most style information is ignored, so the results are essentially plain-text.
    """

    def __init__(
        self, priority: float = DocumentConverter.PRIORITY_SPECIFIC_FILE_FORMAT
    ):
        super().__init__(priority=priority)

    def convert(
        self, input: ConverterInput, **kwargs
    ) -> Union[None, DocumentConverterResult]:
        # Bail if not a PDF
        extension = kwargs.get("file_extension", "")
        if extension.lower() != ".pdf":
            return None

        output = StringIO()
        file_obj = input.read_file(mode="rb")
        pdfminer.high_level.extract_text_to_fp(file_obj, output)
        file_obj.close()

        return DocumentConverterResult(
            title=None,
            text_content=output.getvalue(),
        )
