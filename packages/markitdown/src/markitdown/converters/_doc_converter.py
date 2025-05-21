import sys
import tempfile
import uuid

from typing import BinaryIO, Any
#from io import BytesIO
import io
import os

from ._html_converter import HtmlConverter
from ..converter_utils.docx.pre_process import pre_process_docx
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import mammoth
    from doc2docx import convert as doc2docxConverter
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/msword",
]

ACCEPTED_FILE_EXTENSIONS = [".doc"]

def doc2docxStream(path):
    tf = uuid.uuid4().hex + '.docx'
    doc2docxConverter(path,tf)
    with open(tf, 'rb') as file:
        pre_process_stream = pre_process_docx(io.BufferedReader(file))
    os.remove(tf)
    return pre_process_stream
    
    


class DocConverter(HtmlConverter):
    """
    Converts DOC files to Markdown. Style information (e.g.m headings) and tables are preserved where possible.
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
                    extension=".doc",
                    feature="doc",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )
        
        style_map = kwargs.get("style_map", None)

        pre_process_stream = doc2docxStream(file_stream.name)
        

        return self._html_converter.convert_string(
            mammoth.convert_to_html(pre_process_stream, style_map=style_map).value,
            **kwargs,
        )
