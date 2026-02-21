import sys
import re
import os
from typing import BinaryIO, Any, List
from enum import Enum

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException

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
AnalysisFeatureInput = DocumentAnalysisFeature | str
DEFAULT_DOCINTEL_ANALYSIS_FEATURES: List[DocumentAnalysisFeature] = [
    DocumentAnalysisFeature.FORMULAS,
    DocumentAnalysisFeature.OCR_HIGH_RESOLUTION,
    DocumentAnalysisFeature.STYLE_FONT,
]


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


class DocumentIntelligenceConverter(DocumentConverter):
    """Specialized DocumentConverter that uses Document Intelligence to extract text from documents."""

    def __init__(
        self,
        *,
        endpoint: str,
        api_version: str = "2024-07-31-preview",
        credential: AzureKeyCredential | TokenCredential | None = None,
        analysis_features: List[AnalysisFeatureInput] | None = None,
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
            api_version (str): The API version to use. Defaults to "2024-07-31-preview".
            credential (AzureKeyCredential | TokenCredential | None): The credential to use for authentication.
            analysis_features (List[AnalysisFeatureInput] | None): Optional analysis features to always send.
            file_types (List[DocumentIntelligenceFileType]): The file types to accept. Defaults to all supported file types.
        """

        super().__init__()
        self._file_types = file_types
        self._analysis_features_override = (
            self._normalize_analysis_feature_list(analysis_features)
            if analysis_features is not None
            else None
        )

        # Raise an error if the dependencies are not available.
        # This is different than other converters since this one isn't even instantiated
        # unless explicitly requested.
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                "DocumentIntelligenceConverter requires the optional dependency [az-doc-intel] (or [all]) to be installed. E.g., `pip install markitdown[az-doc-intel]`"
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
        self.doc_intel_client = DocumentIntelligenceClient(
            endpoint=self.endpoint,
            api_version=self.api_version,
            credential=credential,
        )

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

    def _coerce_analysis_features(
        self, features: AnalysisFeatureInput | List[AnalysisFeatureInput]
    ) -> List[AnalysisFeatureInput]:
        """Coerce analysis feature inputs into a flat list."""
        if isinstance(features, str):
            return features.split(",")

        if isinstance(features, (list, tuple, set)):
            coerced: List[AnalysisFeatureInput] = []
            for feature in features:
                if isinstance(feature, str):
                    coerced.extend(feature.split(","))
                else:
                    coerced.append(feature)
            return coerced

        return [features]

    def _resolve_analysis_feature(
        self, feature: AnalysisFeatureInput
    ) -> DocumentAnalysisFeature | None:
        """Resolve feature inputs to SDK constants."""
        if isinstance(feature, DocumentAnalysisFeature):
            return feature

        feature_value = getattr(feature, "value", feature)
        token = str(feature_value).strip()
        if len(token) == 0:
            return None

        if "." in token:
            token = token.rsplit(".", maxsplit=1)[-1]

        normalized_token = token.replace("-", "_").replace(" ", "_")
        if normalized_token.isupper():
            canonical_name = normalized_token
        else:
            canonical_name = re.sub(r"(?<!^)(?=[A-Z])", "_", normalized_token).upper()
        resolved = getattr(DocumentAnalysisFeature, canonical_name, None)
        if resolved is not None:
            return resolved

        raise ValueError(
            f"Invalid Document Intelligence analysis feature: {token}. "
            "Use SDK constants such as DocumentAnalysisFeature.FORMULAS."
        )

    def _normalize_analysis_feature_list(
        self, features: AnalysisFeatureInput | List[AnalysisFeatureInput]
    ) -> List[DocumentAnalysisFeature]:
        """Normalize and de-duplicate configured feature constants."""
        normalized: List[DocumentAnalysisFeature] = []
        seen = set()
        for feature in self._coerce_analysis_features(features):
            resolved = self._resolve_analysis_feature(feature)
            if resolved is None:
                continue

            dedupe_key = str(getattr(resolved, "value", resolved)).lower()
            if dedupe_key in seen:
                continue

            seen.add(dedupe_key)
            normalized.append(resolved)
        return normalized

    def _analysis_features(
        self,
        stream_info: StreamInfo,
        feature_overrides: AnalysisFeatureInput
        | List[AnalysisFeatureInput]
        | None = None,
    ) -> List[DocumentAnalysisFeature]:
        """
        Helper needed to determine which analysis features to use.
        Certain document analysis features are not availiable for
        office filetypes (.xlsx, .pptx, .html, .docx)
        """
        if feature_overrides is not None:
            return self._normalize_analysis_feature_list(feature_overrides)

        if self._analysis_features_override is not None:
            return self._analysis_features_override

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

        return DEFAULT_DOCINTEL_ANALYSIS_FEATURES.copy()

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Extract the text using Azure Document Intelligence
        poller = self.doc_intel_client.begin_analyze_document(
            model_id="prebuilt-layout",
            body=AnalyzeDocumentRequest(bytes_source=file_stream.read()),
            features=self._analysis_features(
                stream_info=stream_info,
                feature_overrides=kwargs.get("docintel_features"),
            ),
            output_content_format=CONTENT_FORMAT,  # TODO: replace with "ContentFormat.MARKDOWN" when the bug is fixed
        )
        result: AnalyzeResult = poller.result()

        # remove comments from the markdown content generated by Doc Intelligence and append to markdown string
        markdown_text = re.sub(r"<!--.*?-->", "", result.content, flags=re.DOTALL)
        return DocumentConverterResult(markdown=markdown_text)
