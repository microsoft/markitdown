from email import policy
from email.message import EmailMessage, Message
from email.parser import BytesParser
from typing import Any, BinaryIO, Iterable, Optional

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from ._html_converter import HtmlConverter

ACCEPTED_MIME_TYPE_PREFIXES = [
    "message/rfc822",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".eml",
]


class EmlConverter(DocumentConverter):
    """Converts RFC 822 / MIME email messages to Markdown."""

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

        cur_pos = file_stream.tell()
        try:
            headers = BytesParser(policy=policy.default).parse(
                file_stream, headersonly=True
            )
            return self._looks_like_email(headers)
        except Exception:
            return False
        finally:
            file_stream.seek(cur_pos)

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        message = BytesParser(policy=policy.default).parse(file_stream)
        subject = self._header_value(message, "Subject")

        lines = ["# Email Message", ""]

        headers = [
            ("From", self._header_value(message, "From")),
            ("To", self._header_value(message, "To")),
            ("Cc", self._header_value(message, "Cc")),
            ("Bcc", self._header_value(message, "Bcc")),
            ("Date", self._header_value(message, "Date")),
            ("Subject", subject),
        ]

        for key, value in headers:
            if value:
                lines.append(f"**{key}:** {value}")

        body = self._extract_body(message)
        attachments = self._extract_attachment_names(message)

        if body:
            lines.extend(["", "## Content", "", body.strip()])

        if attachments:
            lines.extend(["", "## Attachments", ""])
            lines.extend([f"- {name}" for name in attachments])

        return DocumentConverterResult(
            markdown="\n".join(lines).strip(),
            title=subject,
        )

    def _looks_like_email(self, message: Message) -> bool:
        if not message.keys():
            return False

        has_sender = message.get("From") is not None
        has_recipient = any(message.get(header) is not None for header in ["To", "Cc"])
        has_subject = message.get("Subject") is not None

        return has_sender and (has_recipient or has_subject)

    def _header_value(self, message: Message, name: str) -> Optional[str]:
        value = message.get(name)
        return None if value is None else str(value).strip()

    def _extract_body(self, message: Message) -> str:
        plain_parts = list(self._iter_body_parts(message, "text/plain"))
        if plain_parts:
            return "\n\n".join(plain_parts)

        html_parts = list(self._iter_body_parts(message, "text/html"))
        if not html_parts:
            return ""

        html = "\n\n".join(html_parts)
        result = HtmlConverter().convert_string(html)
        return result.markdown

    def _iter_body_parts(self, message: Message, content_type: str) -> Iterable[str]:
        if message.is_multipart():
            for part in message.walk():
                if part.is_multipart():
                    continue
                if part.get_content_disposition() == "attachment":
                    continue
                if part.get_content_type() == content_type:
                    yield self._get_part_content(part)
        elif message.get_content_type() == content_type:
            yield self._get_part_content(message)

    def _get_part_content(self, part: Message) -> str:
        if isinstance(part, EmailMessage):
            content = part.get_content()
            return content if isinstance(content, str) else str(content)

        payload = part.get_payload(decode=True)
        if payload is None:
            content = part.get_payload()
            return content if isinstance(content, str) else str(content)

        charset = part.get_content_charset() or "utf-8"
        return payload.decode(charset, errors="replace")

    def _extract_attachment_names(self, message: Message) -> list[str]:
        if not message.is_multipart():
            return []

        attachments: list[str] = []
        for part in message.walk():
            if part.get_content_disposition() == "attachment":
                filename = part.get_filename()
                if filename:
                    attachments.append(filename)

        return attachments
