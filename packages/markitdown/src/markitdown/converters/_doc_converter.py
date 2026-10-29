import subprocess
import tempfile
import shutil
import os

from typing import BinaryIO, Any, Optional

from ._html_converter import HtmlConverter
from .._base_converter import DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/msword",
    "application/doc",
    "application/ms-word",
]
ACCEPTED_FILE_EXTENSIONS = [".doc"]


def _find_doc_converter_tool() -> Optional[str]:
    """Find a tool that can convert .doc files to HTML or text."""
    for tool in ["textutil", "libreoffice", "antiword"]:
        path = shutil.which(tool)
        if path:
            return tool
    return None


class DocConverter(HtmlConverter):
    """
    Converts legacy .doc (MS Word 97-2003) files to Markdown.
    Uses a system tool (textutil on macOS, libreoffice, or antiword) to
    extract the content, then processes it through the HTML converter.
    """

    def __init__(self):
        super().__init__()

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
        tool = _find_doc_converter_tool()
        if tool is None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".doc",
                    feature="doc",
                )
                + "\n\nInstall a .doc conversion tool:\n"
                + "  macOS: textutil (built-in)\n"
                + "  Linux: sudo apt install libreoffice or antiword\n"
                + "  Windows: install LibreOffice"
            )

        with tempfile.NamedTemporaryFile(suffix=".doc", delete=False) as tmp:
            tmp.write(file_stream.read())
            doc_path = tmp.name

        try:
            if tool == "textutil":
                return self._convert_with_textutil(doc_path, **kwargs)
            elif tool == "libreoffice":
                return self._convert_with_libreoffice(doc_path, **kwargs)
            elif tool == "antiword":
                return self._convert_with_antiword(doc_path, **kwargs)
            else:
                raise MissingDependencyException(
                    f"No supported .doc converter found. Tried: {tool}"
                )
        finally:
            os.unlink(doc_path)

    def _convert_with_textutil(
        self, doc_path: str, **kwargs: Any
    ) -> DocumentConverterResult:
        result = subprocess.run(
            ["textutil", "-convert", "html", doc_path, "-stdout"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"textutil failed: {result.stderr}")
        return self.convert_string(result.stdout, **kwargs)

    def _convert_with_libreoffice(
        self, doc_path: str, **kwargs: Any
    ) -> DocumentConverterResult:
        output_dir = tempfile.mkdtemp()
        try:
            subprocess.run(
                [
                    "libreoffice",
                    "--headless",
                    "--convert-to",
                    "html",
                    "--outdir",
                    output_dir,
                    doc_path,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            html_files = [
                f
                for f in os.listdir(output_dir)
                if f.endswith(".html") or f.endswith(".htm")
            ]
            if not html_files:
                raise RuntimeError("libreoffice produced no HTML output")
            with open(os.path.join(output_dir, html_files[0]), "rb") as f:
                html_content = f.read()
            return self.convert_string(html_content, **kwargs)
        finally:
            shutil.rmtree(output_dir, ignore_errors=True)

    def _convert_with_antiword(
        self, doc_path: str, **kwargs: Any
    ) -> DocumentConverterResult:
        result = subprocess.run(
            ["antiword", doc_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"antiword failed: {result.stderr}")
        html_content = f"<html><body><pre>{result.stdout}</pre></body></html>"
        return self.convert_string(html_content, **kwargs)
