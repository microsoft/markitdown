import sys
import io
import os
import subprocess
from warnings import warn
from typing import BinaryIO, Any, Optional

from ._html_converter import HtmlConverter
from ._docx_converter import DocxConverter
from ..converter_utils.docx.pre_process import pre_process_docx
from .._base_converter import DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import mammoth

except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/msword",
]

ACCEPTED_FILE_EXTENSIONS = [".doc"]


class DocConverter(DocxConverter):
    """
    Converts legacy DOC files (Word 97-2003) to Markdown.
    Uses external tools (antiword or libreoffice) to convert DOC to DOCX format first,
    then leverages the DocxConverter's mammoth-based conversion.
    """

    def __init__(self):
        super().__init__()
        self._docx_converter = DocxConverter()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def _convert_doc_to_docx(self, doc_stream: BinaryIO) -> Optional[io.BytesIO]:
        """
        Attempt to convert DOC to DOCX using available external tools.
        Returns a BytesIO containing the DOCX data, or None if conversion fails.
        """
        # Read the DOC file content
        doc_content = doc_stream.read()
        
        # Try using libreoffice (more reliable)
        try:
            # Create a temporary file
            import tempfile
            
            with tempfile.NamedTemporaryFile(suffix='.doc', delete=False) as tmp_input:
                tmp_input.write(doc_content)
                tmp_input_path = tmp_input.name
            
            tmp_output_path = tmp_input_path.replace('.doc', '.docx')
            
            # Use libreoffice to convert
            result = subprocess.run(
                ['libreoffice', '--headless', '--convert-to', 'docx', '--outdir', 
                 tempfile.gettempdir(), tmp_input_path],
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0 and os.path.exists(tmp_output_path):
                with open(tmp_output_path, 'rb') as f:
                    docx_content = f.read()
                os.unlink(tmp_input_path)
                os.unlink(tmp_output_path)
                return io.BytesIO(docx_content)
            else:
                if os.path.exists(tmp_input_path):
                    os.unlink(tmp_input_path)
        except Exception:
            pass
        
        # Try antiword as fallback
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.doc', delete=False) as tmp_input:
                tmp_input.write(doc_content)
                tmp_input_path = tmp_input.name
            
            result = subprocess.run(
                ['antiword', '-w', '0', tmp_input_path],
                capture_output=True,
                timeout=10
            )
            
            os.unlink(tmp_input_path)
            
            if result.returncode == 0:
                # antiword outputs plain text, wrap it in a simple HTML-like format
                text = result.stdout.decode('utf-8', errors='ignore')
                html_content = f"<html><body><pre>{text}</pre></body></html>"
                return io.BytesIO(html_content.encode('utf-8'))
        except Exception:
            pass
        
        return None

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
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
            ].with_traceback(
                _dependency_exc_info[2]
            )

        # Try to convert DOC to DOCX or HTML
        converted_stream = self._convert_doc_to_docx(file_stream)
        
        if converted_stream is None:
            # Fallback: try to read as plain text with some basic parsing
            # This is a last resort - many DOC files can still be partially parsed
            doc_content = file_stream.read()
            try:
                # Try to decode as if it's plain text (works for some older DOC files)
                text = doc_content.decode('latin-1', errors='ignore')
                # Remove binary garbage
                import re
                text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', '', text)
                html_content = f"<html><body><pre>{text}</pre></body></html>"
                converted_stream = io.BytesIO(html_content.encode('utf-8'))
            except Exception:
                raise MissingDependencyException(
                    "Cannot convert .doc file. Please install either 'libreoffice' or 'antiword' to enable DOC support, "
                    "or convert the file to .docx format first."
                )

        # Check if we got HTML (from antiword) or DOCX (from libreoffice)
        converted_stream.seek(0)
        content_check = converted_stream.read(100)
        converted_stream.seek(0)
        
        if b'<html>' in content_check.lower():
            # It's HTML from antiword - convert using HtmlConverter
            html_content = converted_stream.read().decode('utf-8', errors='ignore')
            html_converter = HtmlConverter()
            return html_converter.convert_string(html_content, **kwargs)
        else:
            # It's DOCX from libreoffice - use DocxConverter
            converted_stream.seek(0)
            pre_process_stream = pre_process_docx(converted_stream)
            return self._docx_converter.convert(
                pre_process_stream,
                stream_info,
                **kwargs,
            )