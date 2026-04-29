import pytest
from markitdown.converters._doc_intel_converter import (
    DEFAULT_DOCINTEL_ANALYSIS_FEATURES,
    DocumentIntelligenceConverter,
    DocumentIntelligenceFileType,
    DocumentAnalysisFeature,
    _dependency_exc_info,
)
from markitdown._stream_info import StreamInfo

if _dependency_exc_info is not None:
    pytest.skip(
        "azure-ai-documentintelligence is not installed", allow_module_level=True
    )


def _make_converter():
    conv = DocumentIntelligenceConverter.__new__(DocumentIntelligenceConverter)
    conv._file_types = [
        DocumentIntelligenceFileType.DOCX,
        DocumentIntelligenceFileType.PPTX,
        DocumentIntelligenceFileType.XLSX,
        DocumentIntelligenceFileType.PDF,
    ]
    conv._analysis_features_override = None
    return conv


def test_docintel_default_analysis_features_for_pdf():
    conv = _make_converter()
    stream_info = StreamInfo(mimetype="application/pdf", extension=".pdf")

    assert conv._analysis_features(stream_info) == DEFAULT_DOCINTEL_ANALYSIS_FEATURES


def test_docintel_default_analysis_features_for_no_ocr_documents():
    conv = _make_converter()
    stream_info = StreamInfo(
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        extension=".docx",
    )

    assert conv._analysis_features(stream_info) == []


def test_docintel_analysis_features_can_be_set_on_converter():
    conv = _make_converter()
    conv._analysis_features_override = [
        DocumentAnalysisFeature.LANGUAGES,
        DocumentAnalysisFeature.QUERY_FIELDS,
    ]
    stream_info = StreamInfo(mimetype="application/pdf", extension=".pdf")

    assert conv._analysis_features(stream_info) == [
        DocumentAnalysisFeature.LANGUAGES,
        DocumentAnalysisFeature.QUERY_FIELDS,
    ]


def test_docintel_analysis_features_can_be_overridden_per_request():
    conv = _make_converter()
    stream_info = StreamInfo(mimetype="application/pdf", extension=".pdf")

    assert conv._analysis_features(
        stream_info,
        feature_overrides=[
            "FORMULAS",
            "ocr_high_resolution",
            "DocumentAnalysisFeature.STYLE_FONT",
            "formulas",
        ],
    ) == [
        DocumentAnalysisFeature.FORMULAS,
        DocumentAnalysisFeature.OCR_HIGH_RESOLUTION,
        DocumentAnalysisFeature.STYLE_FONT,
    ]


def test_docintel_analysis_features_invalid_value_raises():
    conv = _make_converter()
    stream_info = StreamInfo(mimetype="application/pdf", extension=".pdf")

    with pytest.raises(ValueError):
        conv._analysis_features(stream_info, feature_overrides=["not_a_real_feature"])
