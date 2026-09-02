import codecs
import struct
import sys
from typing import Any, Dict, Union, BinaryIO
from charset_normalizer import from_bytes
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

# Fixed-width MAPI properties (PT_LONG among them) are not stored in a stream of
# their own -- they are packed into the message's property stream, after a header
# that is 32 bytes long for a top-level message, as 16-byte entries of tag, flags
# and value.
PROPERTIES_STREAM = "__properties_version1.0"
PROPERTIES_HEADER_SIZE = 32
PROPERTY_ENTRY_SIZE = 16
PT_LONG = 0x0003

PR_MESSAGE_CODEPAGE = 0x3FFD  # PidTagMessageCodepage
PR_INTERNET_CPID = 0x3FDE  # PidTagInternetCodepage

# Windows code page identifiers whose Python codec is not simply "cp<CPID>".
# Anything absent from this map is looked up under that name, so the common
# single-byte and East Asian pages (1250-1258, 874, 932, 936, 949, 950, ...)
# need no entry here.
CODEPAGE_CODECS = {
    708: "iso8859-6",
    20127: "ascii",
    20866: "koi8-r",
    21866: "koi8-u",
    28591: "iso8859-1",
    28592: "iso8859-2",
    28593: "iso8859-3",
    28594: "iso8859-4",
    28595: "iso8859-5",
    28596: "iso8859-6",
    28597: "iso8859-7",
    28598: "iso8859-8",
    28599: "iso8859-9",
    28603: "iso8859-13",
    28605: "iso8859-15",
    10000: "mac_roman",
    10006: "mac_greek",
    10007: "mac_cyrillic",
    10029: "mac_latin2",
    10079: "mac_iceland",
    10081: "mac_turkish",
    50220: "iso2022_jp",
    50221: "iso2022_jp",
    50222: "iso2022_jp",
    50225: "iso2022_kr",
    51932: "euc_jp",
    51936: "gb2312",
    51949: "euc_kr",
    54936: "gb18030",
    65000: "utf-7",
    65001: "utf-8",
}


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

        # Brute force, check if it's an Outlook file
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

        # The code page that PT_STRING8 properties are written in is declared by
        # the message itself, so read it once here rather than guessing at each
        # property. PidTagMessageCodepage covers the message's string properties;
        # PidTagInternetCodepage, when present, describes the body it arrived in.
        long_properties = self._get_long_properties(msg)
        message_encoding = self._get_codec_name(
            long_properties.get(PR_MESSAGE_CODEPAGE)
        )
        internet_encoding = self._get_codec_name(long_properties.get(PR_INTERNET_CPID))
        header_encoding = message_encoding or internet_encoding
        body_encoding = internet_encoding or message_encoding

        # Extract email metadata
        md_content = "# Email Message\n\n"

        # Get headers
        headers = {
            "From": self._get_property_data(
                msg, "0C1F", header_encoding
            ),  # PR_SENDER_EMAIL_ADDRESS
            "To": self._get_property_data(
                msg, "0E04", header_encoding
            ),  # PR_DISPLAY_TO
            "Subject": self._get_property_data(
                msg, "0037", header_encoding
            ),  # PR_SUBJECT
        }

        # Add headers to markdown
        for key, value in headers.items():
            if value:
                md_content += f"**{key}:** {value}\n"

        md_content += "\n## Content\n\n"

        # Get email body
        body = self._get_property_data(msg, "1000", body_encoding)  # PR_BODY
        if body:
            md_content += body

        msg.close()

        return DocumentConverterResult(
            markdown=md_content.strip(),
            title=headers.get("Subject"),
        )

    def _get_long_properties(self, msg: Any) -> Dict[int, int]:
        """Helper to read the message's PT_LONG properties, keyed by property id.

        Fixed-width properties carry no stream of their own: they sit in the
        message's property stream, whose entries are 16 bytes of tag, flags and
        value, following a 32-byte header for a top-level message.
        """
        assert olefile is not None
        assert isinstance(msg, olefile.OleFileIO)

        properties: Dict[int, int] = {}
        try:
            if not msg.exists(PROPERTIES_STREAM):
                return properties
            data = msg.openstream(PROPERTIES_STREAM).read()
        except Exception:
            return properties

        offset = PROPERTIES_HEADER_SIZE
        while offset + PROPERTY_ENTRY_SIZE <= len(data):
            entry = data[offset : offset + PROPERTY_ENTRY_SIZE]
            offset += PROPERTY_ENTRY_SIZE
            tag, _flags, value = struct.unpack("<III", entry[:12])
            if tag & 0xFFFF == PT_LONG:
                properties[tag >> 16] = value
        return properties

    def _get_codec_name(self, codepage: Union[int, None]) -> Union[str, None]:
        """Helper to map a Windows code page identifier to a Python codec.

        Returns None for a code page the message does not declare, or for one
        Python cannot decode -- either way the encoding has to be detected.
        """
        if not codepage:
            return None

        name = CODEPAGE_CODECS.get(codepage, "cp%d" % codepage)
        try:
            return codecs.lookup(name).name
        except LookupError:
            return None

    def _get_property_data(
        self, msg: Any, property_tag: str, encoding: Union[str, None] = None
    ) -> Union[str, None]:
        """Helper to read a MAPI string property, whichever string type is used.

        Outlook stores each string property either as PT_UNICODE (stream type
        001F, UTF-16LE) or as PT_STRING8 (stream type 001E, the message's 8-bit
        code page), depending on whether the message was saved in Unicode or in
        the legacy non-Unicode format. A message carries one or the other, so
        reading only 001F returns nothing at all for a non-Unicode .msg.
        """
        value = self._get_stream_data(msg, "__substg1.0_%s001F" % property_tag)
        if value:
            return value
        return self._get_ansi_stream_data(
            msg, "__substg1.0_%s001E" % property_tag, encoding
        )

    def _get_ansi_stream_data(
        self, msg: Any, stream_path: str, encoding: Union[str, None] = None
    ) -> Union[str, None]:
        """Helper to extract and decode a PT_STRING8 stream from the MSG file.

        These streams record no encoding of their own -- they are written in the
        code page the message declares, which is what ``encoding`` carries. Only
        when that declaration is missing, unsupported, or contradicted by the
        bytes is the charset detected instead: a header is a short and highly
        ambiguous sample, and detection routinely misreads one (a CP1252
        "Résumé" reads as UTF-16BE, a CP1251 "Привет мир" as CP1125).
        """
        assert olefile is not None
        assert isinstance(msg, olefile.OleFileIO)

        try:
            if not msg.exists(stream_path):
                return None
            data = msg.openstream(stream_path).read()
        except Exception:
            return None

        if not data:
            return None

        if encoding is not None:
            try:
                return data.decode(encoding).strip()
            except (UnicodeDecodeError, LookupError):
                pass  # The declared code page does not fit; fall back to detection

        detected = from_bytes(data).best()
        if detected is not None:
            return str(detected).strip()
        return data.decode("utf-8", errors="ignore").strip()

    def _get_stream_data(self, msg: Any, stream_path: str) -> Union[str, None]:
        """Helper to safely extract and decode stream data from the MSG file."""
        assert olefile is not None
        assert isinstance(
            msg, olefile.OleFileIO
        )  # Ensure msg is of the correct type (type hinting is not possible with the optional olefile package)

        try:
            if msg.exists(stream_path):
                data = msg.openstream(stream_path).read()
                # Try UTF-16 first (common for .msg files)
                try:
                    return data.decode("utf-16-le").strip()
                except UnicodeDecodeError:
                    # Fall back to UTF-8
                    try:
                        return data.decode("utf-8").strip()
                    except UnicodeDecodeError:
                        # Last resort - ignore errors
                        return data.decode("utf-8", errors="ignore").strip()
        except Exception:
            pass
        return None
