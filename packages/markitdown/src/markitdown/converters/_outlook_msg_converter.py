from ast import Set
import email
import re
import sys
from typing import Any, Union, BinaryIO
from .._stream_info import StreamInfo
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
olefile = None
try:
    import olefile  # type: ignore[no-redef]
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/vnd.ms-outlook",
]

ACCEPTED_FILE_EXTENSIONS = [".msg"]


class OutlookMsgConverter(DocumentConverter):
    """Converts Outlook .msg files to markdown by extracting email metadata and content.

    Uses the olefile package to parse the .msg file structure and extract:
    - Email headers (From, To, Subject)
    - Email body content
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        # Check the extension and mimetype
        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        # Brute force, check if we have an OLE file
        cur_pos = file_stream.tell()
        try:
            if olefile and not olefile.isOleFile(file_stream):
                return False
        finally:
            file_stream.seek(cur_pos)

        # Brue force, check if it's an Outlook file
        try:
            if olefile is not None:
                msg = olefile.OleFileIO(file_stream)
                toc = "\n".join([str(stream) for stream in msg.listdir()])
                return (
                    "__properties_version1.0" in toc
                    and "__recip_version1.0_#00000000" in toc
                )
        except Exception as e:
            pass
        finally:
            file_stream.seek(cur_pos)

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
                    extension=".msg",
                    feature="outlook",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        assert (
            olefile is not None
        )  # If we made it this far, olefile should be available
        msg = olefile.OleFileIO(file_stream)

        # Extract email metadata
        md_content = "# Email Message\n\n"

        # Get raw headers
        raw_headers = self._get_stream_data(msg, "__substg1.0_007D001F")

        # Add the email date to markdown
        if raw_headers:
            parsed_headers = email.message_from_string(raw_headers)
            email_date = parsed_headers.get("Date")

            if email_date:
                md_content += f"- **Date:** {email_date}\n"
        
        # Fallback

        # Get headers
        headers = {
            "From": self._get_sender(msg),
            "To": self._get_stream_data(msg, "__substg1.0_0E04001F"),
            "Cc": self._get_stream_data(msg, "__substg1.0_0E03001F"),
            "Bcc": self._get_stream_data(msg, "__substg1.0_0E02001F"),
            "Subject": self._get_stream_data(msg, "__substg1.0_0037001F"),
        }

        # Add headers to markdown
        for key, value in headers.items():
            if value:
                md_content += f"- **{key}:** {value}\n"

        # Add attachment info
        attach_dirs = self._get_attach_dirs(msg)

        if attach_dirs:
            md_content += "\n\n## Attachments\n"

            for attach_dir in sorted(attach_dirs):
                md_content += self._get_attach_info(msg, attach_dir)

        md_content += "\n## Content\n\n"

        # Get email body
        body = self._get_stream_data(msg, "__substg1.0_1000001F")
        # Fallback
        if not body:
            body = self._get_stream_data(msg, "__substg1.0_10130102")

        if body:
            # Remove styles and scripts
            body = re.sub(r'<(style|script)[^>]*>.*?</\1>', '', body, flags=re.IGNORECASE | re.DOTALL)
            
            # Remove HTML code
            body = re.sub(r'<[^>]+>', '', body).strip()
            
            md_content += body

        msg.close()

        return DocumentConverterResult(
            markdown=md_content.strip(),
            title=headers.get("Subject"),
        )

    def _get_stream_data(self, msg: Any, stream_path: str) -> Union[str, None]:
        """Helper to safely extract and decode stream data from the MSG file."""
        assert olefile is not None
        assert isinstance(
            msg, olefile.OleFileIO
        )  # Ensure msg is of the correct type (type hinting is not possible with the optional olefile package)

        try:
            if msg.exists(stream_path):
                data = msg.openstream(stream_path).read()

                # Check the property type (the last 4 characters of the path)
                prop_type = stream_path[-4:]
                if prop_type == "001F":
                    # PT_UNICODE: Decode as UTF-16-LE
                    return data.decode("utf-16-le").replace('\x00', '').strip()
                else:
                    # PT_BINARY (0102) or PT_STRING8 (001E): Decode as UTF-8
                    try:
                        return data.decode("utf-8").replace('\x00', '').strip()
                    except UnicodeDecodeError:
                        # Fallback for older legacy encodings
                        return data.decode("windows-1252", errors="ignore").replace('\x00', '').strip()
        except Exception:
            pass
        return None
    
    def _get_attach_info(self, msg: any, attach_dir: any):
        # Get the filename
        filename = self._get_stream_data(msg, f"{attach_dir}/__substg1.0_3707001F")
        # Fallbacks
        if not filename:
            filename = self._get_stream_data(msg, f"{attach_dir}/__substg1.0_3704001F")
        if not filename:
            filename = "Unknown_Filename"

        # Get the file size
        data_stream_path = f"{attach_dir}/__substg1.0_37010102"
        size_bytes = 0

        try:
            if msg.exists(data_stream_path):
                        size_bytes = msg.get_size(data_stream_path)
        except Exception:
            pass
            
        # Format file size
        if size_bytes >= 1048576:
            size_str = f"{size_bytes / 1048576:.2f} MB"
        else:
            size_str = f"{size_bytes / 1024:.2f} KB"

        return f"* {filename} ({size_str})\n"
    
    def _get_attach_dirs(self, msg: any):
        attach_dirs = set()

        try:
            for stream_path in msg.listdir():
                if stream_path[0].startswith("__attach_version1.0_"):
                    attach_dirs.add(stream_path[0])
        except Exception:
            pass
        return attach_dirs
    
    def _get_sender(self, msg: Any):
        # When the downloaded .msg file came from the sent folder, the sender is behind a different path
        try:
            sender = self._get_stream_data(msg, "__substg1.0_5D01001F")
            
            if not sender:
                sender = self._get_stream_data(msg, "__substg1.0_0C1F001F")
                
            if sender and (sender.startswith("/O=") or sender.startswith("/o=")):
                raw_headers = self._get_stream_data(msg, "__substg1.0_007D001F")
                if raw_headers:
                    parsed_headers = email.message_from_string(raw_headers)
                    if parsed_headers.get("From"):
                        sender = parsed_headers.get("From")
        except Exception:
            pass
        return sender