import io

from markitdown._stream_info import StreamInfo
from markitdown.converters._doc_intel_converter import (
    DocumentIntelligenceConverter,
    DocumentIntelligenceFileType,
)

ALL_TYPES = list(DocumentIntelligenceFileType)


def _make_converter(features=None, model_id="prebuilt-layout"):
    """Build a converter without touching Azure (mirrors test_docintel_html.py)."""
    conv = DocumentIntelligenceConverter.__new__(DocumentIntelligenceConverter)
    conv._file_types = ALL_TYPES
    conv._features = features
    conv.model_id = model_id
    return conv


PDF = StreamInfo(mimetype="application/pdf", extension=".pdf")
DOCX = StreamInfo(mimetype=None, extension=".docx")


def _values(features):
    """Azure's feature enum is a str-enum; compare on the wire values."""
    return [getattr(f, "value", f) for f in features]


def test_default_features_unchanged():
    conv = _make_converter()
    assert _values(conv._analysis_features(PDF)) == [
        "formulas",
        "ocrHighResolution",
        "styleFont",
    ]


def test_default_model_id_unchanged():
    assert _make_converter().model_id == "prebuilt-layout"


def test_empty_features_disables_addons():
    conv = _make_converter(features=[])
    assert conv._analysis_features(PDF) == []


def test_explicit_features_are_used():
    conv = _make_converter(features=["ocrHighResolution"])
    assert _values(conv._analysis_features(PDF)) == ["ocrHighResolution"]


def test_explicit_features_not_sent_for_office_types():
    """Office file types do not support add-ons, so they stay empty."""
    conv = _make_converter(features=["ocrHighResolution"])
    assert conv._analysis_features(DOCX) == []


def test_explicit_features_list_is_copied():
    """The caller's list must not be aliased into the request."""
    requested = ["ocrHighResolution"]
    conv = _make_converter(features=requested)
    returned = conv._analysis_features(PDF)
    returned.append("styleFont")
    assert requested == ["ocrHighResolution"]


def test_custom_model_id_is_stored():
    assert _make_converter(model_id="prebuilt-read").model_id == "prebuilt-read"


def test_accepts_still_works():
    """Sanity: the new attributes do not disturb accepts()."""
    assert _make_converter().accepts(io.BytesIO(b""), PDF)
