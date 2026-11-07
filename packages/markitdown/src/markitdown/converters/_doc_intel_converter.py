import sys
import re
import os
from datetime import date, datetime, time
from typing import BinaryIO, Any, List, Optional
from enum import Enum

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException
from .. import __version__ as _markitdown_version

_USER_AGENT = f"markitdown-docintel/{_markitdown_version}"

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import (
        AnalyzeDocumentRequest,
        AnalyzeResult,
        DocumentAnalysisFeature,
    )
    from azure.core.credentials import AzureKeyCredential, TokenCredential
    from azure.identity import DefaultAzureCredential
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()

    # Define these types for type hinting when the package is not available
    class AzureKeyCredential:
        pass

    class TokenCredential:
        pass

    class DocumentIntelligenceClient:
        pass

    class AnalyzeDocumentRequest:
        pass

    class AnalyzeResult:
        pass

    class DocumentAnalysisFeature:
        pass

    class DefaultAzureCredential:
        pass


# TODO: currently, there is a bug in the document intelligence SDK with importing the "ContentFormat" enum.
# This constant is a temporary fix until the bug is resolved.
CONTENT_FORMAT = "markdown"


class DocumentIntelligenceFileType(str, Enum):
    """Enum of file types supported by the Document Intelligence Converter."""

    # No OCR
    DOCX = "docx"
    PPTX = "pptx"
    XLSX = "xlsx"
    HTML = "html"
    # OCR
    PDF = "pdf"
    JPEG = "jpeg"
    PNG = "png"
    BMP = "bmp"
    TIFF = "tiff"


def _get_mime_type_prefixes(types: List[DocumentIntelligenceFileType]) -> List[str]:
    """Get the MIME type prefixes for the given file types."""
    prefixes: List[str] = []
    for type_ in types:
        if type_ == DocumentIntelligenceFileType.DOCX:
            prefixes.append(
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        elif type_ == DocumentIntelligenceFileType.PPTX:
            prefixes.append(
                "application/vnd.openxmlformats-officedocument.presentationml"
            )
        elif type_ == DocumentIntelligenceFileType.XLSX:
            prefixes.append(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        elif type_ == DocumentIntelligenceFileType.HTML:
            prefixes.append("text/html")
            prefixes.append("application/xhtml+xml")
        elif type_ == DocumentIntelligenceFileType.PDF:
            prefixes.append("application/pdf")
            prefixes.append("application/x-pdf")
        elif type_ == DocumentIntelligenceFileType.JPEG:
            prefixes.append("image/jpeg")
        elif type_ == DocumentIntelligenceFileType.PNG:
            prefixes.append("image/png")
        elif type_ == DocumentIntelligenceFileType.BMP:
            prefixes.append("image/bmp")
        elif type_ == DocumentIntelligenceFileType.TIFF:
            prefixes.append("image/tiff")
    return prefixes


def _get_file_extensions(types: List[DocumentIntelligenceFileType]) -> List[str]:
    """Get the file extensions for the given file types."""
    extensions: List[str] = []
    for type_ in types:
        if type_ == DocumentIntelligenceFileType.DOCX:
            extensions.append(".docx")
        elif type_ == DocumentIntelligenceFileType.PPTX:
            extensions.append(".pptx")
        elif type_ == DocumentIntelligenceFileType.XLSX:
            extensions.append(".xlsx")
        elif type_ == DocumentIntelligenceFileType.PDF:
            extensions.append(".pdf")
        elif type_ == DocumentIntelligenceFileType.JPEG:
            extensions.append(".jpg")
            extensions.append(".jpeg")
        elif type_ == DocumentIntelligenceFileType.PNG:
            extensions.append(".png")
        elif type_ == DocumentIntelligenceFileType.BMP:
            extensions.append(".bmp")
        elif type_ == DocumentIntelligenceFileType.TIFF:
            extensions.append(".tiff")
        elif type_ == DocumentIntelligenceFileType.HTML:
            extensions.append(".html")
    return extensions


def _field_value(field: Any) -> Any:
    """
    Extract a serializable Python value from a Document Intelligence DocumentField.

    Returns the most specific typed value when available, falling back to the
    raw ``content`` string. Returns ``None`` when nothing usable is present.
    """
    if field is None:
        return None

    # Typed scalar values (in rough order of specificity).
    for attr in (
        "value_string",
        "value_boolean",
        "value_integer",
        "value_number",
        "value_date",
        "value_time",
        "value_phone_number",
        "value_country_region",
        "value_selection_mark",
        "value_signature",
    ):
        v = getattr(field, attr, None)
        if v is not None:
            if isinstance(v, (date, datetime, time)):
                return v.isoformat()
            return v

    # Currency: { amount, currencySymbol, currencyCode }
    cur = getattr(field, "value_currency", None)
    if cur is not None:
        amount = getattr(cur, "amount", None)
        code = getattr(cur, "currency_code", None) or getattr(
            cur, "currency_symbol", None
        )
        if amount is not None and code:
            return f"{amount} {code}"
        if amount is not None:
            return amount

    # Address: serialize to its content/string form.
    addr = getattr(field, "value_address", None)
    if addr is not None:
        return getattr(field, "content", None) or str(addr)

    # Selection groups contain the selected labels, not DocumentField objects.
    selection_group = getattr(field, "value_selection_group", None)
    if selection_group is not None:
        return list(selection_group)

    # Array of fields -> list of values.
    arr = getattr(field, "value_array", None)
    if arr is not None:
        return [_field_value(item) for item in arr]

    # Object of fields -> dict of values.
    obj = getattr(field, "value_object", None)
    if obj is not None:
        return {k: _field_value(v) for k, v in obj.items()}

    # Last resort: the raw extracted text.
    return getattr(field, "content", None)


def _yaml_scalar(value: Any) -> str:
    """Render a scalar value as a YAML string."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        rendered = repr(value)
        if isinstance(value, float) and "e" in rendered:
            mantissa, exponent = rendered.split("e", 1)
            # YAML 1.1 requires a decimal point in exponential float mantissas.
            if "." not in mantissa:
                mantissa += ".0"
            rendered = f"{mantissa}e{exponent}"
        return rendered
    s = str(value)
    # Quote when necessary: contains special chars, leading/trailing whitespace,
    # or characters that would confuse a YAML parser.
    if (
        not re.fullmatch(r"[A-Za-z_][A-Za-z0-9 _./-]*", s)
        or s != s.strip()
        or s.lower() in ("null", "true", "false", "yes", "no", "on", "off", "y", "n")
    ):
        # Escape backslashes, double quotes, and common whitespace characters.
        escaped = (
            s.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")
        )
        # Quoting alone does not make YAML control characters valid. Escape
        # those too, including Unicode line breaks that YAML would normalize.
        escaped = re.sub(
            r"[\x00-\x1f\x7f-\x9f\u2028\u2029\ud800-\udfff\ufffe\uffff]",
            lambda match: f"\\u{ord(match.group()):04x}",
            escaped,
        )
        return f'"{escaped}"'
    return s


def _yaml_dump(value: Any, indent: int = 0) -> str:
    """Minimal YAML emitter for scalars, lists, and dicts of scalars/lists/dicts."""
    pad = "  " * indent
    if isinstance(value, dict):
        if not value:
            return f"{pad}{{}}"
        lines: List[str] = []
        for k, v in value.items():
            key = _yaml_scalar(k)
            if isinstance(v, (dict, list)) and v:
                lines.append(f"{pad}{key}:")
                lines.append(_yaml_dump(v, indent + 1))
            else:
                lines.append(
                    f"{pad}{key}: {_yaml_scalar(v) if not isinstance(v, (dict, list)) else ('{}' if isinstance(v, dict) else '[]')}"
                )
        return "\n".join(lines)
    if isinstance(value, list):
        if not value:
            return f"{pad}[]"
        lines = []
        for item in value:
            if isinstance(item, (dict, list)) and item:
                lines.append(f"{pad}-")
                lines.append(_yaml_dump(item, indent + 1))
            else:
                lines.append(
                    f"{pad}- {_yaml_scalar(item) if not isinstance(item, (dict, list)) else ('{}' if isinstance(item, dict) else '[]')}"
                )
        return "\n".join(lines)
    return f"{pad}{_yaml_scalar(value)}"


def _fields_to_front_matter(documents: Any, model_id: Optional[str] = None) -> str:
    """
    Build a YAML front matter block from ``AnalyzeResult.documents[*].fields``.

    Returns an empty string when there are no documents or no non-empty fields.
    A single document uses a ``fields`` mapping. Multiple documents use an
    ordered ``documents`` list, each with its own ``fields`` mapping, so values
    from different documents cannot overwrite or be combined with one another.

    A single document has the following shape:

        ---
        modelId: prebuilt-invoice
        fields:
          VendorName: Contoso Ltd.
          InvoiceTotal: 1250.0
        ---
    """
    if not documents:
        return ""

    document_fields: List[dict] = []
    for doc in documents:
        extracted: dict = {}
        fields = getattr(doc, "fields", None) or {}
        for name, field in fields.items():
            value = _field_value(field)
            if value is None or value == "" or value == [] or value == {}:
                continue
            extracted[name] = value
        document_fields.append(extracted)

    if not any(document_fields):
        return ""

    payload: dict = {}
    if model_id:
        payload["modelId"] = model_id
    if len(document_fields) == 1:
        payload["fields"] = document_fields[0]
    else:
        payload["documents"] = [{"fields": fields} for fields in document_fields]

    body = _yaml_dump(payload)
    return f"---\n{body}\n---\n\n"


class DocumentIntelligenceConverter(DocumentConverter):
    """Specialized DocumentConverter that uses Document Intelligence to extract text from documents."""

    def __init__(
        self,
        *,
        endpoint: str,
        api_version: str | None = None,
        credential: AzureKeyCredential | TokenCredential | None = None,
        model_id: str = "prebuilt-layout",
        features: Optional[List[str]] = None,
        query_fields: Optional[List[str]] = None,
        file_types: List[DocumentIntelligenceFileType] = [
            DocumentIntelligenceFileType.DOCX,
            DocumentIntelligenceFileType.PPTX,
            DocumentIntelligenceFileType.XLSX,
            DocumentIntelligenceFileType.PDF,
            DocumentIntelligenceFileType.JPEG,
            DocumentIntelligenceFileType.PNG,
            DocumentIntelligenceFileType.BMP,
            DocumentIntelligenceFileType.TIFF,
        ],
    ):
        """
        Initialize the DocumentIntelligenceConverter.

        Args:
            endpoint (str): The endpoint for the Document Intelligence service.
            api_version (str | None): The API version to use. Defaults to None.
            credential (AzureKeyCredential | TokenCredential | None): The credential to use for authentication.
            model_id (str): The Document Intelligence model ID to use (e.g., "prebuilt-layout",
                "prebuilt-invoice", "prebuilt-receipt", or a custom model ID). Defaults to "prebuilt-layout".
            features (List[str] | None): Analysis add-on features to request for OCR-supported
                file types. No add-ons are enabled by default. Query fields automatically add
                the required ``queryFields`` feature.
            query_fields (List[str] | None): Optional list of field names to extract via the DI
                ``queryFields`` add-on. Only applied to OCR-supported file types (PDF/images).
            file_types (List[DocumentIntelligenceFileType]): The file types to accept. Defaults to all supported file types.
        """

        super().__init__()
        self._file_types = file_types
        self._model_id = model_id
        self._features = list(features) if features is not None else None
        self._query_fields = list(query_fields) if query_fields else None

        # Raise an error if the dependencies are not available.
        # This is different than other converters since this one isn't even instantiated
        # unless explicitly requested.
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                "DocumentIntelligenceConverter requires the optional dependency [az-doc-intel] (or [all]) to be installed. E.g., `pip install 'markitdown[az-doc-intel]'`"
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        if credential is None:
            if os.environ.get("AZURE_API_KEY") is None:
                credential = DefaultAzureCredential()
            else:
                credential = AzureKeyCredential(os.environ["AZURE_API_KEY"])

        self.endpoint = endpoint
        self.api_version = api_version
        client_kwargs: dict[str, Any] = {
            "endpoint": self.endpoint,
            "credential": credential,
            "user_agent": _USER_AGENT,
        }
        if self.api_version is not None:
            client_kwargs["api_version"] = self.api_version

        self.doc_intel_client = DocumentIntelligenceClient(**client_kwargs)

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in _get_file_extensions(self._file_types):
            return True

        for prefix in _get_mime_type_prefixes(self._file_types):
            if mimetype.startswith(prefix):
                return True

        return False

    def _analysis_features(self, stream_info: StreamInfo) -> List[str]:
        """
        Helper needed to determine which analysis features to use.
        Certain document analysis features are not available for
        office filetypes (.xlsx, .pptx, .html, .docx)
        """
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        # Types that don't support ocr
        no_ocr_types = [
            DocumentIntelligenceFileType.DOCX,
            DocumentIntelligenceFileType.PPTX,
            DocumentIntelligenceFileType.XLSX,
            DocumentIntelligenceFileType.HTML,
        ]

        if extension in _get_file_extensions(no_ocr_types):
            return []

        for prefix in _get_mime_type_prefixes(no_ocr_types):
            if mimetype.startswith(prefix):
                return []

        features = list(self._features) if self._features is not None else []

        if self._query_fields and DocumentAnalysisFeature.QUERY_FIELDS not in features:
            features.append(DocumentAnalysisFeature.QUERY_FIELDS)
        return features

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Build optional kwargs so that we only pass query_fields when the
        # QUERY_FIELDS feature is actually enabled for this file type.
        features = self._analysis_features(stream_info)
        extra: dict = {}
        if self._query_fields and DocumentAnalysisFeature.QUERY_FIELDS in features:
            extra["query_fields"] = self._query_fields

        # Extract the text using Azure Document Intelligence
        poller = self.doc_intel_client.begin_analyze_document(
            model_id=self._model_id,
            body=AnalyzeDocumentRequest(bytes_source=file_stream.read()),
            features=features,
            output_content_format=CONTENT_FORMAT,  # TODO: replace with "ContentFormat.MARKDOWN" when the bug is fixed
            **extra,
        )
        result: AnalyzeResult = poller.result()

        # remove comments from the markdown content generated by Doc Intelligence and append to markdown string
        markdown_text = re.sub(r"<!--.*?-->", "", result.content, flags=re.DOTALL)

        # Prepend YAML front matter when DI returned structured fields (e.g., from
        # prebuilt-invoice/-receipt, custom models, or queryFields).
        front_matter = _fields_to_front_matter(
            getattr(result, "documents", None), model_id=self._model_id
        )
        if front_matter:
            markdown_text = front_matter + markdown_text

        return DocumentConverterResult(markdown=markdown_text)
