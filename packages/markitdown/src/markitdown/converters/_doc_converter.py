import sys
import os
import subprocess
import tempfile
import shutil
from typing import BinaryIO, Any, Optional

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

try:
    import olefile
except ImportError as e:
    olefile = None
    _olefile_exc_info = sys.exc_info()

try:
    from ._docx_converter import DocxConverter
except ImportError:
    DocxConverter = None

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/msword",
    "application/vnd.ms-word",
]

ACCEPTED_FILE_EXTENSIONS = [".doc"]


class DocConverter(DocumentConverter):
    """
    Converts legacy DOC files to Markdown by first converting them to DOCX.
    
    This converter uses an OS-specific approach:
    - On Windows, it uses the Word Application COM interface.
    - On other platforms (Linux, macOS), it uses LibreOffice/Soffice.
    
    """

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

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if olefile is None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".doc",
                    feature="doc (olefile)",
                )
            ) from _olefile_exc_info[1].with_traceback(_olefile_exc_info[2])
            
        if DocxConverter is None:
            return DocumentConverterResult(
                markdown="Error: The DocxConverter is not available. Please ensure it is installed."
            )

        file_stream.seek(0)
        if not olefile.isOleFile(file_stream):
            return DocumentConverterResult(
                markdown="Error: Not a valid Microsoft Word DOC file."
            )
        file_stream.seek(0)
        
        tmp_dir = tempfile.mkdtemp()
        doc_path = os.path.join(tmp_dir, "input.doc")
        
        with open(doc_path, "wb") as f:
            shutil.copyfileobj(file_stream, f)
            
        docx_path = ""
        try:
            if sys.platform == "win32":
                docx_path = self._convert_to_docx_windows(doc_path)
            else:
                docx_path = self._convert_to_docx_unix(doc_path)
                
            if not docx_path or not os.path.exists(docx_path):
                return DocumentConverterResult(markdown="Error: Failed to convert DOC to DOCX.")
                
            docx_converter = DocxConverter()
            with open(docx_path, "rb") as docx_file:
                docx_stream_info = StreamInfo(
                    mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    extension=".docx",
                )
                return docx_converter.convert(docx_file, docx_stream_info, **kwargs)

        except Exception as e:
            return DocumentConverterResult(markdown=f"Error converting DOC file: {str(e)}")
            
        finally:
            shutil.rmtree(tmp_dir)

    def _convert_to_docx_windows(self, doc_path: str) -> str:
        """
        Converts DOC to DOCX using the Word COM interface on Windows.
        """
        try:
            # This comment tells the linter to ignore the "unresolved import" error.
            import win32com.client  # type: ignore 
        except ImportError as e:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".doc",
                    feature="doc (pywin32)",
                )
            ) from e
        
        word = None
        try:
            word = win32com.client.Dispatch("Word.Application")
            word.visible = 0
            
            in_file = os.path.abspath(doc_path)
            doc = word.Documents.Open(in_file)
            
            out_file = os.path.splitext(in_file)[0] + ".docx"
            doc.SaveAs2(out_file, FileFormat=16)
            doc.Close()
            
            return out_file
        finally:
            if word:
                word.Quit()
    
    def _convert_to_docx_unix(self, doc_path: str) -> str:
        """
        Converts DOC to DOCX using LibreOffice/Soffice on Unix-like systems.
        """
        soffice_path = self._find_soffice()
        if not soffice_path:
            raise MissingDependencyException(
                "LibreOffice/Soffice is not installed or not in the system's PATH. "
                "Please install it to convert .doc files."
            )
            
        output_dir = os.path.dirname(doc_path)
        
        try:
            subprocess.run(
                [
                    soffice_path,
                    "--headless",
                    "--convert-to",
                    "docx",
                    "--outdir",
                    output_dir,
                    doc_path,
                ],
                check=True,
                capture_output=True,
                timeout=60, 
            )
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode(errors="ignore") if e.stderr else "Unknown error."
            raise RuntimeError(f"LibreOffice conversion failed: {error_message}") from e
        except subprocess.TimeoutExpired as e:
            raise RuntimeError("LibreOffice conversion timed out after 60 seconds.") from e

        
        docx_path = os.path.splitext(doc_path)[0] + ".docx"
        return docx_path
        
    def _find_soffice(self) -> Optional[str]:
        """
        Finds the path to the soffice or libreoffice executable.
        """
        for cmd in ["soffice", "libreoffice"]:
            path = shutil.which(cmd)
            if path:
                return path
        return None