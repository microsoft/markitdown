from email import policy
from email.message import EmailMessage, Message
from email.parser import BytesParser
from typing import Any, BinaryIO, Iterable

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from ._html_converter import HtmlConverter

ACCEPTED_MIME_TYPES = [
    "message/rfc822",
    "application/eml",
]

ACCEPTED_FILE_EXTENSIONS = [".eml"]


class EmlConverter(DocumentConverter):
    """Converts RFC 822 / EML email files to markdown."""

    def __init__(self) -> None:
        self._html_converter = HtmlConverter()

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

        if mimetype in ACCEPTED_MIME_TYPES:
            return True

        cur_pos = file_stream.tell()
        try:
            message = BytesParser(policy=policy.default).parsebytes(
                file_stream.read(65536)
            )
            return message.get("from") is not None and (
                message.get("to") is not None or message.get("subject") is not None
            )
        finally:
            file_stream.seek(cur_pos)

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        message = BytesParser(policy=policy.default).parse(file_stream)
        headers = self._headers(message)
        body = self._body_to_markdown(message)
        attachments = self._attachments(message)

        md_content = "# Email Message\n\n"
        for key, value in headers:
            if value:
                md_content += f"**{key}:** {value}\n"

        md_content += "\n## Content\n\n"
        if body:
            md_content += body.strip()

        if attachments:
            md_content += "\n\n## Attachments\n\n"
            for attachment in attachments:
                md_content += f"- {attachment}\n"

        return DocumentConverterResult(
            markdown=md_content.strip(),
            title=message.get("subject"),
        )

    def _headers(self, message: Message) -> list[tuple[str, str | None]]:
        return [
            ("From", message.get("from")),
            ("To", message.get("to")),
            ("Cc", message.get("cc")),
            ("Date", message.get("date")),
            ("Subject", message.get("subject")),
        ]

    def _body_to_markdown(self, message: Message) -> str:
        plain_parts: list[str] = []
        html_parts: list[str] = []

        for part in self._iter_body_parts(message):
            content_type = part.get_content_type()
            content = part.get_content()
            if not isinstance(content, str):
                continue

            if content_type == "text/plain":
                plain_parts.append(content)
            elif content_type == "text/html":
                html_parts.append(
                    self._html_converter.convert_string(content).markdown
                )

        if plain_parts:
            return "\n\n".join(part.strip() for part in plain_parts if part.strip())

        return "\n\n".join(part.strip() for part in html_parts if part.strip())

    def _iter_body_parts(self, message: Message) -> Iterable[EmailMessage]:
        if message.is_multipart():
            for part in message.walk():
                if part.is_multipart():
                    continue
                if part.get_content_disposition() == "attachment":
                    continue
                if part.get_content_type() in ("text/plain", "text/html"):
                    yield part  # type: ignore[misc]
        elif message.get_content_type() in ("text/plain", "text/html"):
            yield message  # type: ignore[misc]

    def _attachments(self, message: Message) -> list[str]:
        attachments: list[str] = []

        for part in message.walk() if message.is_multipart() else []:
            if part.get_content_disposition() != "attachment":
                continue

            filename = part.get_filename() or "unnamed attachment"
            content_type = part.get_content_type()
            attachments.append(f"{filename} ({content_type})")

        return attachments
