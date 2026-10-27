"""Unit tests for the DocumentIntelligenceConverter improvements.

These tests exercise the converter without making any network calls. They use
``__new__`` to bypass ``__init__`` (which would construct a real
``DocumentIntelligenceClient``) and instead inject a mock client.
"""

import io
from datetime import date
from types import SimpleNamespace
from unittest import mock

import pytest
import yaml
from azure.ai.documentintelligence.models import AnalyzedDocument, DocumentField

from markitdown._stream_info import StreamInfo
from markitdown.converters import _doc_intel_converter as di_mod
from markitdown.converters._doc_intel_converter import (
    DocumentIntelligenceConverter,
    DocumentIntelligenceFileType,
    _USER_AGENT,
    _field_value,
    _fields_to_front_matter,
    _yaml_dump,
)

# --------- helpers ---------------------------------------------------------


def _bare_converter(
    *,
    file_types=None,
    model_id="prebuilt-layout",
    features=None,
    query_fields=None,
    client=None,
):
    """Build a converter without calling __init__ (no real DI client)."""
    conv = DocumentIntelligenceConverter.__new__(DocumentIntelligenceConverter)
    conv._file_types = file_types or [
        DocumentIntelligenceFileType.PDF,
        DocumentIntelligenceFileType.DOCX,
    ]
    conv._model_id = model_id
    conv._features = list(features) if features is not None else None
    conv._query_fields = list(query_fields) if query_fields else None
    conv.endpoint = "https://example.cognitiveservices.azure.com/"
    conv.api_version = "2024-11-30"
    conv.doc_intel_client = client
    return conv


def _mock_field(**kwargs):
    """A SimpleNamespace with all DocumentField value_* attrs defaulting to None."""
    defaults = {
        "value_string": None,
        "value_boolean": None,
        "value_integer": None,
        "value_number": None,
        "value_date": None,
        "value_time": None,
        "value_phone_number": None,
        "value_country_region": None,
        "value_selection_mark": None,
        "value_signature": None,
        "value_currency": None,
        "value_address": None,
        "value_array": None,
        "value_object": None,
        "content": None,
    }
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


# --------- Phase 1: API version + user agent -------------------------------


def test_default_api_version_uses_sdk_default():
    """The default api_version must defer to the Document Intelligence SDK."""
    import inspect

    sig = inspect.signature(DocumentIntelligenceConverter.__init__)
    assert sig.parameters["api_version"].default is None


def test_user_agent_string_format():
    """User agent should start with 'markitdown-docintel/'."""
    assert _USER_AGENT.startswith("markitdown-docintel/")
    assert len(_USER_AGENT) > len("markitdown-docintel/")


def test_client_constructed_with_user_agent_and_sdk_default_api_version():
    """__init__ should pass user_agent without overriding the SDK API version."""
    fake_client = mock.MagicMock()
    with mock.patch.object(
        di_mod, "DocumentIntelligenceClient", return_value=fake_client
    ) as ctor:
        DocumentIntelligenceConverter(
            endpoint="https://example.cognitiveservices.azure.com/",
            credential=mock.MagicMock(),
        )
    kwargs = ctor.call_args.kwargs
    assert "api_version" not in kwargs
    assert kwargs["user_agent"] == _USER_AGENT


# --------- Phase 2: configurable model_id ----------------------------------


def test_default_model_id():
    """Default model_id preserves existing behavior."""
    import inspect

    sig = inspect.signature(DocumentIntelligenceConverter.__init__)
    assert sig.parameters["model_id"].default == "prebuilt-layout"


def test_convert_uses_default_model_id():
    """Without overrides, convert() calls begin_analyze_document with prebuilt-layout."""
    fake_poller = mock.MagicMock()
    fake_poller.result.return_value = SimpleNamespace(content="# hi", documents=None)
    client = mock.MagicMock()
    client.begin_analyze_document.return_value = fake_poller

    conv = _bare_converter(client=client)
    conv.convert(
        io.BytesIO(b"data"), StreamInfo(extension=".pdf", mimetype="application/pdf")
    )

    args, kwargs = client.begin_analyze_document.call_args
    assert kwargs["model_id"] == "prebuilt-layout"


def test_convert_uses_overridden_model_id():
    fake_poller = mock.MagicMock()
    fake_poller.result.return_value = SimpleNamespace(content="# hi", documents=None)
    client = mock.MagicMock()
    client.begin_analyze_document.return_value = fake_poller

    conv = _bare_converter(model_id="prebuilt-invoice", client=client)
    conv.convert(
        io.BytesIO(b"data"), StreamInfo(extension=".pdf", mimetype="application/pdf")
    )

    assert (
        client.begin_analyze_document.call_args.kwargs["model_id"] == "prebuilt-invoice"
    )


# --------- Phase 3: configurable features ---------------------------------


def test_no_features_are_enabled_by_default():
    conv = _bare_converter()
    features = conv._analysis_features(
        StreamInfo(extension=".pdf", mimetype="application/pdf")
    )

    assert features == []


def test_empty_features_disable_all_addons():
    conv = _bare_converter(features=[])

    assert (
        conv._analysis_features(
            StreamInfo(extension=".pdf", mimetype="application/pdf")
        )
        == []
    )


def test_explicit_features_are_copied():
    configured = [di_mod.DocumentAnalysisFeature.OCR_HIGH_RESOLUTION]
    conv = _bare_converter(features=configured)

    resolved = conv._analysis_features(
        StreamInfo(extension=".pdf", mimetype="application/pdf")
    )
    resolved.append(di_mod.DocumentAnalysisFeature.STYLE_FONT)

    assert configured == [di_mod.DocumentAnalysisFeature.OCR_HIGH_RESOLUTION]
    assert conv._features == [di_mod.DocumentAnalysisFeature.OCR_HIGH_RESOLUTION]


def test_explicit_features_are_not_sent_for_office_types():
    conv = _bare_converter(features=[di_mod.DocumentAnalysisFeature.STYLE_FONT])

    assert (
        conv._analysis_features(
            StreamInfo(
                extension=".docx",
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        )
        == []
    )


def test_query_fields_extend_explicit_features_without_mutating_them():
    configured = [di_mod.DocumentAnalysisFeature.OCR_HIGH_RESOLUTION]
    conv = _bare_converter(features=configured, query_fields=["VendorName"])

    features = conv._analysis_features(
        StreamInfo(extension=".pdf", mimetype="application/pdf")
    )

    assert features == [
        di_mod.DocumentAnalysisFeature.OCR_HIGH_RESOLUTION,
        di_mod.DocumentAnalysisFeature.QUERY_FIELDS,
    ]
    assert configured == [di_mod.DocumentAnalysisFeature.OCR_HIGH_RESOLUTION]


# --------- Phase 4: YAML front matter --------------------------------------


def test_field_value_typed_scalars():
    assert _field_value(_mock_field(value_string="Contoso")) == "Contoso"
    assert _field_value(_mock_field(value_integer=42)) == 42
    assert _field_value(_mock_field(value_number=12.5)) == 12.5
    assert _field_value(_mock_field(value_boolean=True)) is True
    assert _field_value(_mock_field(value_date=date(2026, 3, 15))) == "2026-03-15"


def test_field_value_currency():
    cur = SimpleNamespace(amount=1250.0, currency_code="USD", currency_symbol="$")
    assert _field_value(_mock_field(value_currency=cur)) == "1250.0 USD"


def test_field_value_falls_back_to_content():
    assert _field_value(_mock_field(content="raw text")) == "raw text"


def test_field_value_array_of_scalars():
    items = [_mock_field(value_string="A"), _mock_field(value_string="B")]
    assert _field_value(_mock_field(value_array=items)) == ["A", "B"]


@pytest.mark.parametrize("content", [None, ":selected: :unselected:"])
def test_selection_group_preserves_selected_values_in_front_matter(content):
    field = DocumentField(
        type="selectionGroup", value_selection_group=["Email", "SMS"], content=content
    )
    doc = AnalyzedDocument(
        doc_type="custom", fields={"ContactPreference": field}, spans=[], confidence=1.0
    )

    assert _field_value(field) == ["Email", "SMS"]
    assert _fields_to_front_matter([doc]) == (
        "---\nfields:\n  ContactPreference:\n    - Email\n    - SMS\n---\n\n"
    )


def test_empty_selection_group_does_not_fall_back_to_content():
    field = DocumentField(
        type="selectionGroup", value_selection_group=[], content=":unselected:"
    )
    assert _field_value(field) == []


def test_front_matter_preserves_separate_documents():
    documents = [
        AnalyzedDocument(
            doc_type="invoice",
            fields={
                "VendorName": DocumentField(type="string", value_string="Vendor A"),
                "InvoiceTotal": DocumentField(type="number", value_number=100.0),
            },
            spans=[],
            confidence=1.0,
        ),
        AnalyzedDocument(
            doc_type="invoice",
            fields={
                "VendorName": DocumentField(type="string", value_string="Vendor B"),
                "InvoiceId": DocumentField(type="string", value_string="INV-B"),
            },
            spans=[],
            confidence=1.0,
        ),
    ]

    assert _fields_to_front_matter(documents, "prebuilt-invoice") == (
        "---\n"
        "modelId: prebuilt-invoice\n"
        "documents:\n"
        "  -\n"
        "    fields:\n"
        "      VendorName: Vendor A\n"
        "      InvoiceTotal: 100.0\n"
        "  -\n"
        "    fields:\n"
        "      VendorName: Vendor B\n"
        "      InvoiceId: INV-B\n"
        "---\n\n"
    )


def test_front_matter_preserves_empty_document_positions():
    empty = SimpleNamespace(fields={})
    populated = SimpleNamespace(fields={"Name": _mock_field(value_string="Contoso")})

    assert _fields_to_front_matter([empty, populated, empty]) == (
        "---\n"
        "documents:\n"
        "  -\n"
        "    fields: {}\n"
        "  -\n"
        "    fields:\n"
        "      Name: Contoso\n"
        "  -\n"
        "    fields: {}\n"
        "---\n\n"
    )
    assert _fields_to_front_matter([empty, empty]) == ""


def test_fields_to_front_matter_empty_when_no_documents():
    assert _fields_to_front_matter(None) == ""
    assert _fields_to_front_matter([]) == ""


def test_fields_to_front_matter_empty_when_no_fields():
    doc = SimpleNamespace(fields={})
    assert _fields_to_front_matter([doc]) == ""


def test_fields_to_front_matter_basic():
    doc = SimpleNamespace(
        fields={
            "VendorName": _mock_field(value_string="Contoso Ltd."),
            "InvoiceTotal": _mock_field(value_number=1250.0),
        }
    )
    fm = _fields_to_front_matter([doc], model_id="prebuilt-invoice")
    assert fm.startswith("---\n")
    assert fm.endswith("---\n\n")
    assert "modelId: prebuilt-invoice" in fm
    assert "fields:" in fm
    assert "  VendorName: Contoso Ltd." in fm
    assert "  InvoiceTotal: 1250.0" in fm


def test_fields_to_front_matter_omits_model_id_when_not_provided():
    doc = SimpleNamespace(fields={"X": _mock_field(value_string="y")})
    fm = _fields_to_front_matter([doc])
    assert "modelId:" not in fm
    assert "fields:" in fm


def test_fields_with_special_chars_are_quoted():
    doc = SimpleNamespace(
        fields={"Note": _mock_field(value_string="line1\nline2: with colon")}
    )
    fm = _fields_to_front_matter([doc])
    # Value contains both \n and ':' so it must be quoted.
    assert '  Note: "line1\\nline2: with colon"' in fm


@pytest.mark.parametrize(
    "text",
    [
        "page one\fpage two",
        "back\bspace",
        "null\x00byte",
        "vertical\vtab",
        "control\x1fend",
        "delete\x7fcharacter",
        "next\x85line",
        "control\x9fend",
        "line\u2028separator",
        "paragraph\u2029separator",
        "noncharacter\ufffe",
        "noncharacter\uffff",
        "tab\tnewline\nreturn\r",
        'quote"backslash\\',
        "café 😀",
        "00123",
        "[1, 2]",
        "- pending",
        "+12065550100",
        "on",
        "1e-7",
        "1e20",
    ],
)
def test_front_matter_string_keys_and_values_round_trip(text):
    doc = AnalyzedDocument(
        doc_type="custom",
        fields={text: DocumentField(type="string", value_string=text)},
        spans=[],
        confidence=1.0,
    )

    front_matter = _fields_to_front_matter([doc])
    assert front_matter.startswith("---\n")
    assert front_matter.endswith("---\n\n")
    assert yaml.safe_load(front_matter[4:-5]) == {"fields": {text: text}}


@pytest.mark.parametrize(
    "value",
    [
        1e-7,
        -1e-7,
        1e20,
        -1e20,
        1.25e-7,
        5e-324,
        1.7976931348623157e308,
        1.25,
        0.0,
        -0.0,
    ],
)
def test_front_matter_floats_round_trip(value):
    doc = AnalyzedDocument(
        doc_type="custom",
        fields={"Measurement": DocumentField(type="number", value_number=value)},
        spans=[],
        confidence=1.0,
    )

    front_matter = _fields_to_front_matter([doc])
    parsed = yaml.safe_load(front_matter[4:-5])["fields"]["Measurement"]
    assert type(parsed) is float
    assert repr(parsed) == repr(value)


def test_yaml_dump_nested_dict():
    out = _yaml_dump({"a": 1, "b": {"c": "x"}})
    assert "a: 1" in out
    assert "b:" in out
    assert "  c: x" in out


def test_convert_prepends_front_matter_when_fields_present():
    doc = SimpleNamespace(fields={"VendorName": _mock_field(value_string="Contoso")})
    fake_poller = mock.MagicMock()
    fake_poller.result.return_value = SimpleNamespace(
        content="# Invoice\n\nbody", documents=[doc]
    )
    client = mock.MagicMock()
    client.begin_analyze_document.return_value = fake_poller

    conv = _bare_converter(model_id="prebuilt-invoice", client=client)
    result = conv.convert(
        io.BytesIO(b"data"), StreamInfo(extension=".pdf", mimetype="application/pdf")
    )

    assert result.markdown.startswith("---\n")
    assert "modelId: prebuilt-invoice" in result.markdown
    assert "  VendorName: Contoso" in result.markdown
    assert "# Invoice" in result.markdown


def test_convert_no_front_matter_when_no_documents():
    fake_poller = mock.MagicMock()
    fake_poller.result.return_value = SimpleNamespace(
        content="# Layout", documents=None
    )
    client = mock.MagicMock()
    client.begin_analyze_document.return_value = fake_poller

    conv = _bare_converter(client=client)
    result = conv.convert(
        io.BytesIO(b"data"), StreamInfo(extension=".pdf", mimetype="application/pdf")
    )

    assert not result.markdown.startswith("---")
    assert result.markdown.startswith("# Layout")


# --------- Phase 5: query fields -------------------------------------------


def test_query_fields_adds_feature_for_ocr_types():
    conv = _bare_converter(query_fields=["VendorName", "Total"])
    features = conv._analysis_features(
        StreamInfo(extension=".pdf", mimetype="application/pdf")
    )
    from azure.ai.documentintelligence.models import DocumentAnalysisFeature

    assert DocumentAnalysisFeature.QUERY_FIELDS in features


def test_query_fields_skipped_for_office_types():
    conv = _bare_converter(query_fields=["VendorName"])
    features = conv._analysis_features(
        StreamInfo(
            extension=".docx",
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    )
    # Office types skip OCR features entirely.
    assert features == []


def test_query_fields_passed_to_begin_analyze_document_for_pdf():
    fake_poller = mock.MagicMock()
    fake_poller.result.return_value = SimpleNamespace(content="x", documents=None)
    client = mock.MagicMock()
    client.begin_analyze_document.return_value = fake_poller

    conv = _bare_converter(query_fields=["A", "B"], client=client)
    conv.convert(
        io.BytesIO(b"data"), StreamInfo(extension=".pdf", mimetype="application/pdf")
    )

    assert client.begin_analyze_document.call_args.kwargs.get("query_fields") == [
        "A",
        "B",
    ]


def test_query_fields_not_passed_for_office_types():
    fake_poller = mock.MagicMock()
    fake_poller.result.return_value = SimpleNamespace(content="x", documents=None)
    client = mock.MagicMock()
    client.begin_analyze_document.return_value = fake_poller

    conv = _bare_converter(query_fields=["A"], client=client)
    conv.convert(
        io.BytesIO(b"data"),
        StreamInfo(
            extension=".docx",
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
    )

    assert "query_fields" not in client.begin_analyze_document.call_args.kwargs


# --------- _markitdown.py wiring -------------------------------------------


def test_markitdown_forwards_docintel_kwargs(monkeypatch):
    """MarkItDown(...) should forward Document Intelligence configuration."""
    from markitdown import _markitdown as md_mod

    captured = {}

    class _Fake:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr(md_mod, "DocumentIntelligenceConverter", _Fake)

    md_mod.MarkItDown(
        docintel_endpoint="https://example.cognitiveservices.azure.com/",
        docintel_model_id="prebuilt-invoice",
        docintel_features=[],
        docintel_query_fields=["A", "B"],
    )

    assert captured.get("endpoint") == "https://example.cognitiveservices.azure.com/"
    assert captured.get("model_id") == "prebuilt-invoice"
    assert captured.get("features") == []
    assert captured.get("query_fields") == ["A", "B"]
