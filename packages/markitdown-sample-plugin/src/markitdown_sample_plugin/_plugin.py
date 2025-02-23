from typing import Union
from striprtf.striprtf import rtf_to_text

from markitdown import MarkItDown, DocumentConverter, DocumentConverterResult

__plugin_interface_version__ = (
    1  # The version of the plugin interface that this plugin uses
)


def register_converters(markitdown: MarkItDown, **kwargs):
    """
    Called during construction of MarkItDown instances to register converters provided by plugins.
    """

    # Simply create and attach an RtfConverter instance
    markitdown.register_converter(RtfConverter())


class RtfConverter(DocumentConverter):
    """
    Converts an RTF file to in the simplest possible way.
    """

    def convert(self, local_path, **kwargs) -> Union[None, DocumentConverterResult]:
        # Bail if not a RTF
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
