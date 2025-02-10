from typing import Union
from striprtf.striprtf import rtf_to_text

from markitdown import DocumentConverter, DocumentConverterResult


class RtfConverter(DocumentConverter):
    """
    Converts an RTF file to in the simplest possible way.
    """

    def convert(self, local_path, **kwargs) -> Union[None, DocumentConverterResult]:
        # Bail if not a DOCX
        extension = kwargs.get("file_extension", "")
        if extension.lower() != ".rtf":
            return None

        # Read the RTF file
        with open(local_path, "r") as f:
            rtf = f.read()

        # Return the result
        return DocumentConverterResult(
            title=None,
            text_content=rtf_to_text(rtf),
        )
