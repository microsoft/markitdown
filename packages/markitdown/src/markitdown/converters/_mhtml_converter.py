import io
from email import policy
from email.parser import BytesParser
from email.message import EmailMessage
from typing import Any, BinaryIO, Optional

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from ._html_converter import HtmlConverter

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/x-mimearchive",
    "multipart/related",
]

ACCEPTED_FILE_EXTENSIONS = [".mhtml", ".mht"]

HTML_TYPES = ["text/html", "application/xhtml+xml"]


class MhtmlConverter(DocumentConverter):
    """
    Converts MHTML (.mhtml / .mht) web page archives to Markdown.

    The main HTML document is pulled out of the MIME container and handed to
    HtmlConverter. Embedded resources such as images and stylesheets are ignored.
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
        message = BytesParser(policy=policy.default).parse(file_stream)

        html_part = self._find_html_part(message)
        if html_part is None:
            raise ValueError("No text/html part found in the MHTML file.")

        # Undo the transfer encoding. HtmlConverter decodes the bytes, using the
        # MIME charset when there is one and UTF-8 otherwise.
        payload = html_part.get_payload(decode=True)

        result = self._html_converter.convert(
            io.BytesIO(payload),
            StreamInfo(
                mimetype="text/html",
                extension=".html",
                charset=html_part.get_content_charset(),
            ),
            **kwargs,
        )
        if result.title is None and message["Subject"]:
            result.title = str(message["Subject"])
        return result

    @staticmethod
    def _find_html_part(message: EmailMessage) -> Optional[EmailMessage]:
        """Return the page itself: the part named by the `start` parameter if
        there is one, otherwise the first HTML part."""
        html_parts = [
            part for part in message.walk() if part.get_content_type() in HTML_TYPES
        ]
        start = message.get_param("start")
        if isinstance(start, str):
            for part in html_parts:
                if part.get("Content-ID", "").strip() == start.strip():
                    return part
        return html_parts[0] if html_parts else None
