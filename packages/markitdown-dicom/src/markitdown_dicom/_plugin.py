from typing import Any
from markitdown import MarkItDown
from ._dicom_converter import DicomConverter

__plugin_interface_version__ = 1

def register_converters(markitdown: MarkItDown, **kwargs: Any) -> None:
    """
    Called during construction of MarkItDown instances to register converters provided by plugins.
    """
    markitdown.register_converter(DicomConverter(**kwargs))
