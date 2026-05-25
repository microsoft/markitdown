"""Azure Content Understanding converter for MarkItDown.

Converts files using Azure Content Understanding (CU) for high-quality,
multi-modal extraction with structured field output. Supports documents,
images, audio, and video. Fields are serialized as YAML front matter via
the CU SDK's ``to_llm_input()`` helper.

Install dependencies: ``pip install markitdown[az-content-understanding]``
"""

import sys
import os
from typing import BinaryIO, Any, List, Optional, Dict
from enum import Enum

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException

# Try loading optional dependencies — save error for later
_dependency_exc_info = None
try:
    from azure.ai.contentunderstanding import ContentUnderstandingClient, to_llm_input
    from azure.core.credentials import AzureKeyCredential, TokenCredential
    from azure.core.pipeline.policies import UserAgentPolicy
    from azure.identity import DefaultAzureCredential
except ImportError:
    _dependency_exc_info = sys.exc_info()

    # Stub classes for type hinting
    class AzureKeyCredential:  # type: ignore[no-redef]
        pass

    class TokenCredential:  # type: ignore[no-redef]
        pass

    class ContentUnderstandingClient:  # type: ignore[no-redef]
        pass

    class UserAgentPolicy:  # type: ignore[no-redef]
        pass

    class DefaultAzureCredential:  # type: ignore[no-redef]
        pass

    def to_llm_input(*args, **kwargs):  # type: ignore[no-redef]
        pass


# ---------------------------------------------------------------------------
# File type enum and routing tables
# ---------------------------------------------------------------------------


class ContentUnderstandingFileType(str, Enum):
    """Supported file types for Content Understanding conversion."""

    # Documents
    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    XLSX = "xlsx"
    HTML = "html"
    TXT = "txt"
    MD = "md"
    RTF = "rtf"
    XML = "xml"

    # Email
    EML = "eml"
    MSG = "msg"

    # Images (document modality)
    JPEG = "jpeg"
    PNG = "png"
    BMP = "bmp"
    TIFF = "tiff"
    HEIF = "heif"

    # Video
    MP4 = "mp4"
    M4V = "m4v"
    MOV = "mov"
    AVI = "avi"
    MKV = "mkv"
    WEBM = "webm"
    FLV = "flv"
    WMV = "wmv"

    # Audio
    WAV = "wav"
    MP3 = "mp3"
    M4A = "m4a"
    FLAC = "flac"
    OGG = "ogg"
    AAC = "aac"
    WMA = "wma"


# Extension → file type
_EXTENSION_MAP: Dict[str, ContentUnderstandingFileType] = {
    # Documents
    ".pdf": ContentUnderstandingFileType.PDF,
    ".docx": ContentUnderstandingFileType.DOCX,
    ".pptx": ContentUnderstandingFileType.PPTX,
    ".xlsx": ContentUnderstandingFileType.XLSX,
    ".html": ContentUnderstandingFileType.HTML,
    ".txt": ContentUnderstandingFileType.TXT,
    ".md": ContentUnderstandingFileType.MD,
    ".rtf": ContentUnderstandingFileType.RTF,
    ".xml": ContentUnderstandingFileType.XML,
    # Email
    ".eml": ContentUnderstandingFileType.EML,
    ".msg": ContentUnderstandingFileType.MSG,
    # Images
    ".jpg": ContentUnderstandingFileType.JPEG,
    ".jpeg": ContentUnderstandingFileType.JPEG,
    ".jpe": ContentUnderstandingFileType.JPEG,
    ".png": ContentUnderstandingFileType.PNG,
    ".bmp": ContentUnderstandingFileType.BMP,
    ".tiff": ContentUnderstandingFileType.TIFF,
    ".heif": ContentUnderstandingFileType.HEIF,
    ".heic": ContentUnderstandingFileType.HEIF,
    # Video
    ".mp4": ContentUnderstandingFileType.MP4,
    ".m4v": ContentUnderstandingFileType.M4V,
    ".mov": ContentUnderstandingFileType.MOV,
    ".avi": ContentUnderstandingFileType.AVI,
    ".mkv": ContentUnderstandingFileType.MKV,
    ".webm": ContentUnderstandingFileType.WEBM,
    ".flv": ContentUnderstandingFileType.FLV,
    ".wmv": ContentUnderstandingFileType.WMV,
    # Audio
    ".wav": ContentUnderstandingFileType.WAV,
    ".mp3": ContentUnderstandingFileType.MP3,
    ".m4a": ContentUnderstandingFileType.M4A,
    ".flac": ContentUnderstandingFileType.FLAC,
    ".ogg": ContentUnderstandingFileType.OGG,
    ".aac": ContentUnderstandingFileType.AAC,
    ".wma": ContentUnderstandingFileType.WMA,
}

# MIME type prefixes for each file type
_MIME_PREFIXES: Dict[ContentUnderstandingFileType, List[str]] = {
    # Documents
    ContentUnderstandingFileType.PDF: ["application/pdf", "application/x-pdf"],
    ContentUnderstandingFileType.DOCX: [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ],
    ContentUnderstandingFileType.PPTX: [
        "application/vnd.openxmlformats-officedocument.presentationml"
    ],
    ContentUnderstandingFileType.XLSX: [
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ],
    ContentUnderstandingFileType.HTML: ["text/html", "application/xhtml+xml"],
    ContentUnderstandingFileType.TXT: ["text/plain"],
    ContentUnderstandingFileType.MD: ["text/markdown"],
    ContentUnderstandingFileType.RTF: ["text/rtf", "application/rtf"],
    ContentUnderstandingFileType.XML: ["text/xml", "application/xml"],
    # Email
    ContentUnderstandingFileType.EML: ["message/rfc822"],
    ContentUnderstandingFileType.MSG: ["application/vnd.ms-outlook"],
    # Images
    ContentUnderstandingFileType.JPEG: ["image/jpeg"],
    ContentUnderstandingFileType.PNG: ["image/png"],
    ContentUnderstandingFileType.BMP: ["image/bmp"],
    ContentUnderstandingFileType.TIFF: ["image/tiff"],
    ContentUnderstandingFileType.HEIF: ["image/heif", "image/heic"],
    # Video
    ContentUnderstandingFileType.MP4: ["video/mp4"],
    ContentUnderstandingFileType.M4V: ["video/x-m4v"],
    ContentUnderstandingFileType.MOV: ["video/quicktime"],
    ContentUnderstandingFileType.AVI: ["video/x-msvideo"],
    ContentUnderstandingFileType.MKV: ["video/x-matroska"],
    ContentUnderstandingFileType.WEBM: ["video/webm"],
    ContentUnderstandingFileType.FLV: ["video/x-flv"],
    ContentUnderstandingFileType.WMV: ["video/x-ms-wmv"],
    # Audio
    ContentUnderstandingFileType.WAV: ["audio/wav", "audio/x-wav"],
    ContentUnderstandingFileType.MP3: ["audio/mpeg", "audio/mp3"],
    ContentUnderstandingFileType.M4A: ["audio/mp4", "audio/m4a", "audio/x-m4a"],
    ContentUnderstandingFileType.FLAC: ["audio/flac", "audio/x-flac"],
    ContentUnderstandingFileType.OGG: ["audio/ogg"],
    ContentUnderstandingFileType.AAC: ["audio/aac"],
    ContentUnderstandingFileType.WMA: ["audio/x-ms-wma"],
}

_MIME_ALIASES: Dict[str, str] = {
    "audio/x-wav": "audio/wav",
    "audio/x-flac": "audio/flac",
    "audio/x-m4a": "audio/mp4",
    "video/x-m4v": "video/mp4",
}

# File type → modality category
_DOCUMENT_TYPES = {
    ContentUnderstandingFileType.PDF,
    ContentUnderstandingFileType.DOCX,
    ContentUnderstandingFileType.PPTX,
    ContentUnderstandingFileType.XLSX,
    ContentUnderstandingFileType.HTML,
    ContentUnderstandingFileType.TXT,
    ContentUnderstandingFileType.MD,
    ContentUnderstandingFileType.RTF,
    ContentUnderstandingFileType.XML,
    ContentUnderstandingFileType.EML,
    ContentUnderstandingFileType.MSG,
}

_IMAGE_TYPES = {
    ContentUnderstandingFileType.JPEG,
    ContentUnderstandingFileType.PNG,
    ContentUnderstandingFileType.BMP,
    ContentUnderstandingFileType.TIFF,
    ContentUnderstandingFileType.HEIF,
}

_VIDEO_TYPES = {
    ContentUnderstandingFileType.MP4,
    ContentUnderstandingFileType.M4V,
    ContentUnderstandingFileType.MOV,
    ContentUnderstandingFileType.AVI,
    ContentUnderstandingFileType.MKV,
    ContentUnderstandingFileType.WEBM,
    ContentUnderstandingFileType.FLV,
    ContentUnderstandingFileType.WMV,
}

_AUDIO_TYPES = {
    ContentUnderstandingFileType.WAV,
    ContentUnderstandingFileType.MP3,
    ContentUnderstandingFileType.M4A,
    ContentUnderstandingFileType.FLAC,
    ContentUnderstandingFileType.OGG,
    ContentUnderstandingFileType.AAC,
    ContentUnderstandingFileType.WMA,
}

_PREBUILT_ANALYZERS = {
    "document": "prebuilt-documentSearch",
    "image": "prebuilt-documentSearch",
    "video": "prebuilt-videoSearch",
    "audio": "prebuilt-audioSearch",
}

# All supported file types (default set when file_types is None)
_ALL_FILE_TYPES = list(ContentUnderstandingFileType)


def _get_modality(file_type: ContentUnderstandingFileType) -> str:
    """Get the modality category for a file type."""
    if file_type in _DOCUMENT_TYPES:
        return "document"
    elif file_type in _IMAGE_TYPES:
        return "image"
    elif file_type in _VIDEO_TYPES:
        return "video"
    elif file_type in _AUDIO_TYPES:
        return "audio"
    raise ValueError(f"Unknown file type: {file_type}")


def _detect_file_type(
    stream_info: StreamInfo,
    file_types: Optional[List[ContentUnderstandingFileType]] = None,
) -> Optional[ContentUnderstandingFileType]:
    """Detect a supported CU file type from extension or MIME type."""
    allowed = set(file_types) if file_types is not None else None

    extension = (stream_info.extension or "").lower()
    file_type = _EXTENSION_MAP.get(extension)
    if file_type is not None and (allowed is None or file_type in allowed):
        return file_type

    mimetype = _clean_mime_type(stream_info.mimetype)
    if not mimetype:
        return None

    return _detect_file_type_from_mime(mimetype, allowed)


def _clean_mime_type(mimetype: Optional[str]) -> str:
    return (mimetype or "").split(";", 1)[0].strip().lower()


def _canonical_mime_type(mimetype: Optional[str]) -> str:
    cleaned = _clean_mime_type(mimetype)
    return _MIME_ALIASES.get(cleaned, cleaned) or "application/octet-stream"


def _content_type_for(
    file_type: ContentUnderstandingFileType,
    mimetype: Optional[str],
) -> str:
    """Resolve the content type to send to the CU API.

    Uses the resolved ``file_type`` as the source of truth so analyzer
    routing and payload metadata stay consistent. The caller-provided
    ``mimetype`` is only used when it is consistent with ``file_type``
    (e.g., to preserve subtype distinctions like ``image/heic`` vs
    ``image/heif``). When ``mimetype`` disagrees with the resolved
    ``file_type`` (e.g., ``.pdf`` extension with ``audio/mpeg``
    mimetype), the canonical MIME type for ``file_type`` is used.
    """
    prefixes = _MIME_PREFIXES.get(file_type, [])
    canonical = _canonical_mime_type(mimetype)

    # Use caller-provided MIME if it's consistent with the resolved file_type
    if prefixes and canonical != "application/octet-stream":
        for prefix in prefixes:
            if canonical.startswith(prefix):
                return canonical

    # Fallback: derive from the resolved file_type (single source of truth)
    if prefixes:
        return _canonical_mime_type(prefixes[0])

    return canonical


def _detect_file_type_from_mime(
    mimetype: str,
    allowed: Optional[set[ContentUnderstandingFileType]],
) -> Optional[ContentUnderstandingFileType]:
    for candidate, prefixes in _MIME_PREFIXES.items():
        if allowed is not None and candidate not in allowed:
            continue
        for prefix in prefixes:
            if mimetype.startswith(prefix):
                return candidate
    return None


# ---------------------------------------------------------------------------
# Smart routing: base_analyzer_id → modality mapping
# ---------------------------------------------------------------------------

_BASE_TO_MODALITY: Dict[str, str] = {
    "prebuilt-document": "document",
    "prebuilt-image": "image",
    "prebuilt-audio": "audio",
    "prebuilt-video": "video",
}

# Cache of known prebuilt analyzer name → modality (avoids API call)
_KNOWN_PREBUILT_MODALITY: Dict[str, str] = {
    # Document-based prebuilts
    "prebuilt-documentSearch": "document",
    "prebuilt-layout": "document",
    "prebuilt-read": "document",
    "prebuilt-document": "document",
    "prebuilt-invoice": "document",
    "prebuilt-receipt": "document",
    "prebuilt-receipt.generic": "document",
    "prebuilt-receipt.hotel": "document",
    "prebuilt-idDocument": "document",
    "prebuilt-idDocument.generic": "document",
    "prebuilt-idDocument.passport": "document",
    "prebuilt-healthInsuranceCard.us": "document",
    "prebuilt-contract": "document",
    "prebuilt-creditCard": "document",
    "prebuilt-creditMemo": "document",
    "prebuilt-bankStatement.us": "document",
    "prebuilt-check.us": "document",
    "prebuilt-purchaseOrder": "document",
    "prebuilt-procurement": "document",
    "prebuilt-payStub.us": "document",
    "prebuilt-utilityBill": "document",
    "prebuilt-marriageCertificate.us": "document",
    "prebuilt-documentFieldSchema": "document",
    "prebuilt-documentFields": "document",
    # Tax prebuilts (all document-based)
    "prebuilt-tax.us": "document",
    "prebuilt-tax.us.w2": "document",
    "prebuilt-tax.us.w4": "document",
    "prebuilt-tax.us.1040": "document",
    # Mortgage prebuilts
    "prebuilt-mortgage.us": "document",
    "prebuilt-mortgage.us.1003": "document",
    "prebuilt-mortgage.us.closingDisclosure": "document",
    # Image-based prebuilts
    "prebuilt-image": "image",
    "prebuilt-imageSearch": "image",
    # Audio-based prebuilts
    "prebuilt-audio": "audio",
    "prebuilt-audioSearch": "audio",
    "prebuilt-callCenter": "audio",
    # Video-based prebuilts
    "prebuilt-video": "video",
    "prebuilt-videoSearch": "video",
    "prebuilt-videoSynopsis": "video",
}


def _resolve_analyzer_modality(client: Any, analyzer_id: str) -> str:
    """Resolve analyzer modality from cache or via get_analyzer() fallback.

    For known prebuilt-* names, returns the modality from
    ``_KNOWN_PREBUILT_MODALITY`` without an API call.  For unknown
    prebuilt-* names or custom analyzers, calls ``get_analyzer()``
    to inspect ``base_analyzer_id``.

    Args:
        client: A ``ContentUnderstandingClient`` instance.
        analyzer_id: The analyzer ID to resolve.

    Returns:
        Modality string ("document", "image", "audio", or "video").

    Raises:
        ValueError: If ``get_analyzer()`` fails.
    """
    # Known prebuilt — use cache, no API call
    if analyzer_id in _KNOWN_PREBUILT_MODALITY:
        return _KNOWN_PREBUILT_MODALITY[analyzer_id]

    # Unknown prebuilt or custom analyzer — call get_analyzer()
    try:
        analyzer_info = client.get_analyzer(analyzer_id)
    except Exception as exc:
        raise ValueError(f"Failed to resolve analyzer '{analyzer_id}': {exc}") from exc

    if analyzer_info.base_analyzer_id:
        return _BASE_TO_MODALITY.get(analyzer_info.base_analyzer_id, "document")
    return "document"


def _is_analyzer_compatible(file_modality: str, analyzer_modality: str) -> bool:
    """Return True when an analyzer modality can process a file modality."""
    if analyzer_modality == "document":
        return file_modality in {"document", "image"}
    return file_modality == analyzer_modality


# ---------------------------------------------------------------------------
# Converter
# ---------------------------------------------------------------------------


class ContentUnderstandingConverter(DocumentConverter):
    """Converts files using Azure Content Understanding.

    Provides high-quality document, image, audio, and video conversion
    with structured field extraction via YAML front matter.
    """

    def __init__(
        self,
        *,
        endpoint: str,
        credential: AzureKeyCredential | TokenCredential | None = None,
        analyzer_id: Optional[str] = None,
        file_types: Optional[List[ContentUnderstandingFileType]] = None,
    ):
        """Initialize the Content Understanding converter.

        Args:
            endpoint: CU resource endpoint URL.
            credential: Explicit credential. If None, falls back to
                AZURE_API_KEY env var, then DefaultAzureCredential.
            analyzer_id: Custom analyzer for compatible file types.
                When set, the converter checks the analyzer's base modality
                (via get_analyzer() at init) and routes only compatible
                file types to it. Incompatible modalities auto-route to
                default prebuilts. If None, auto-selects by extension/MIME.
            file_types: Which file types to handle. If None, uses the
                default set (all supported formats).
        """
        super().__init__()

        # Raise if dependencies are missing
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                "ContentUnderstandingConverter requires the optional dependency "
                "[az-content-understanding] (or [all]) to be installed. "
                "E.g., `pip install markitdown[az-content-understanding]`"
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        self._file_types = file_types if file_types is not None else _ALL_FILE_TYPES
        self._analyzer_id = analyzer_id
        self._analyzer_modality: Optional[str] = None

        # Resolve credential
        if credential is None:
            api_key = os.environ.get("AZURE_API_KEY")
            if api_key is not None:
                credential = AzureKeyCredential(api_key)
            else:
                credential = DefaultAzureCredential()

        # User agent for telemetry
        try:
            from ..__about__ import __version__
        except ImportError:
            __version__ = "unknown"
        user_agent = f"markitdown-cu/{__version__}"

        # Create CU client
        self._client = ContentUnderstandingClient(
            endpoint=endpoint,
            credential=credential,
            user_agent_policy=UserAgentPolicy(user_agent=user_agent),
        )

        # Smart routing: resolve analyzer modality at init (at most one API call)
        if self._analyzer_id is not None:
            self._analyzer_modality = _resolve_analyzer_modality(
                self._client, self._analyzer_id
            )

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        """Return True if the file type is in the configured set."""
        return _detect_file_type(stream_info, self._file_types) is not None

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        """Convert the file using CU and return Markdown with YAML front matter."""

        # 1. Determine analyzer_id (smart routing: check modality)
        file_type = _detect_file_type(stream_info, self._file_types)
        if file_type is None:
            raise ValueError(
                "Unsupported file type for Content Understanding conversion."
            )
        file_modality = _get_modality(file_type)

        if (
            self._analyzer_id is not None
            and self._analyzer_modality is not None
            and _is_analyzer_compatible(file_modality, self._analyzer_modality)
        ):
            analyzer_id = self._analyzer_id
        else:
            analyzer_id = _PREBUILT_ANALYZERS.get(
                file_modality, "prebuilt-documentSearch"
            )

        # 2. Read file bytes and determine MIME type
        file_bytes = file_stream.read()
        content_type = _content_type_for(file_type, stream_info.mimetype)

        # 3. Call CU SDK
        poller = self._client.begin_analyze_binary(
            analyzer_id=analyzer_id,
            binary_input=file_bytes,
            content_type=content_type,
        )

        # 4. Block on result
        result = poller.result()

        # 5. Format output using to_llm_input()
        text = to_llm_input(result)

        # 6. Return
        return DocumentConverterResult(markdown=text)
