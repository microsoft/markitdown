"""Tests for EmlConverter: body extraction, header parsing, and attachment conversion."""

import io
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from unittest.mock import MagicMock


from markitdown import StreamInfo
from markitdown.converters import EmlConverter


def _make_simple_eml(
    subject="Test Subject",
    from_addr="sender@example.com",
    to_addr="recipient@example.com",
    body="Hello, this is the email body.",
) -> bytes:
    """Build a plain-text EML message as bytes."""
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Date"] = "Sat, 04 Apr 2026 12:00:00 +0000"
    return msg.as_bytes()


def _make_multipart_eml(body_text: str, attachments: list[tuple[str, bytes]]) -> bytes:
    """Build a multipart EML with a plain-text body and file attachments."""
    msg = MIMEMultipart()
    msg["Subject"] = "Multipart Test"
    msg["From"] = "sender@example.com"
    msg["To"] = "recipient@example.com"

    msg.attach(MIMEText(body_text, "plain", "utf-8"))

    for filename, data in attachments:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(data)
        part.add_header("Content-Disposition", "attachment", filename=filename)
        msg.attach(part)

    return msg.as_bytes()


class TestEmlConverterBody:
    def test_simple_plain_text_email(self):
        eml = _make_simple_eml(body="This is the body.")
        converter = EmlConverter()
        result = converter.convert(
            io.BytesIO(eml),
            StreamInfo(extension=".eml"),
        )
        assert "# Email Message" in result.markdown
        assert "**From:** sender@example.com" in result.markdown
        assert "**To:** recipient@example.com" in result.markdown
        assert "**Subject:** Test Subject" in result.markdown
        assert "This is the body." in result.markdown

    def test_title_is_subject(self):
        eml = _make_simple_eml(subject="My Subject")
        converter = EmlConverter()
        result = converter.convert(
            io.BytesIO(eml),
            StreamInfo(extension=".eml"),
        )
        assert result.title == "My Subject"

    def test_empty_subject_gives_none_title(self):
        eml = _make_simple_eml(subject="")
        converter = EmlConverter()
        result = converter.convert(
            io.BytesIO(eml),
            StreamInfo(extension=".eml"),
        )
        assert result.title is None

    def test_missing_cc_not_shown(self):
        eml = _make_simple_eml()
        converter = EmlConverter()
        result = converter.convert(
            io.BytesIO(eml),
            StreamInfo(extension=".eml"),
        )
        assert "**Cc:**" not in result.markdown

    def test_accepts_eml_extension(self):
        converter = EmlConverter()
        assert converter.accepts(
            io.BytesIO(b""),
            StreamInfo(extension=".eml"),
        )

    def test_accepts_rfc822_mimetype(self):
        converter = EmlConverter()
        assert converter.accepts(
            io.BytesIO(b""),
            StreamInfo(mimetype="message/rfc822"),
        )

    def test_rejects_unrelated_extension(self):
        converter = EmlConverter()
        assert not converter.accepts(
            io.BytesIO(b""),
            StreamInfo(extension=".pdf"),
        )


class TestEmlConverterAttachments:
    def test_no_attachments_no_section(self):
        eml = _make_simple_eml()
        converter = EmlConverter()
        result = converter.convert(
            io.BytesIO(eml),
            StreamInfo(extension=".eml"),
        )
        assert "## Attachments" not in result.markdown

    def test_attachment_without_markitdown_shows_notice(self):
        eml = _make_multipart_eml("Body text.", [("report.pdf", b"%PDF-fake")])
        converter = EmlConverter(markitdown=None)
        result = converter.convert(
            io.BytesIO(eml),
            StreamInfo(extension=".eml"),
        )
        assert "## Attachments" in result.markdown
        assert "report.pdf" in result.markdown
        assert "Pass a MarkItDown instance" in result.markdown

    def test_attachment_converted_with_markitdown(self):
        mock_md = MagicMock()
        mock_result = MagicMock()
        mock_result.markdown = "| col1 | col2 |\n|------|------|\n| a    | b    |"
        mock_md.convert_stream.return_value = mock_result

        eml = _make_multipart_eml("See attached.", [("data.csv", b"col1,col2\na,b")])
        converter = EmlConverter(markitdown=mock_md)
        result = converter.convert(
            io.BytesIO(eml),
            StreamInfo(extension=".eml"),
        )

        assert "## Attachments" in result.markdown
        assert "### data.csv" in result.markdown
        assert "col1 | col2" in result.markdown
        mock_md.convert_stream.assert_called_once()

    def test_unsupported_attachment_shows_note(self):
        from markitdown._exceptions import UnsupportedFormatException

        mock_md = MagicMock()
        mock_md.convert_stream.side_effect = UnsupportedFormatException("not supported")

        eml = _make_multipart_eml("Body.", [("weird.xyz", b"\x00\x01\x02")])
        converter = EmlConverter(markitdown=mock_md)
        result = converter.convert(
            io.BytesIO(eml),
            StreamInfo(extension=".eml"),
        )

        assert "weird.xyz" in result.markdown
        assert "unsupported format" in result.markdown

    def test_multiple_attachments_all_listed(self):
        mock_md = MagicMock()
        mock_md.convert_stream.return_value = MagicMock(markdown="converted content")

        attachments = [("first.txt", b"hello"), ("second.txt", b"world")]
        eml = _make_multipart_eml("Body.", attachments)
        converter = EmlConverter(markitdown=mock_md)
        result = converter.convert(
            io.BytesIO(eml),
            StreamInfo(extension=".eml"),
        )

        assert "### first.txt" in result.markdown
        assert "### second.txt" in result.markdown
        assert mock_md.convert_stream.call_count == 2

    def test_body_excludes_attachment_parts(self):
        """Body extraction should not include attachment MIME parts as text."""
        eml = _make_multipart_eml(
            "This is the real body.",
            [("attach.txt", b"This should not be in the body.")],
        )
        converter = EmlConverter()
        result = converter.convert(
            io.BytesIO(eml),
            StreamInfo(extension=".eml"),
        )
        assert "This is the real body." in result.markdown
        # Attachment content should not bleed into the body section
        content_section = result.markdown.split("## Content")[1]
        assert "This should not be in the body." not in content_section
