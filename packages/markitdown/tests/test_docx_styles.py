"""DOCX stylesheet repair must preserve namespace-qualified attributes."""

import io
from pathlib import Path
import re
import zipfile

from lxml import etree
import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown.converter_utils.docx.pre_process import _pre_process_styles


WORD_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{WORD_NAMESPACE}}}"
TEST_DOCX = Path(__file__).parent / "test_files" / "test.docx"


@pytest.mark.parametrize("missing_type", [False, True])
def test_docx_styles_with_redundant_default_namespace(missing_type: bool) -> None:
    markitdown = MarkItDown()
    expected = markitdown.convert(TEST_DOCX).markdown
    fixture = io.BytesIO()
    declaration = f'xmlns:w="{WORD_NAMESPACE}"'.encode("utf-8")

    with zipfile.ZipFile(TEST_DOCX) as source, zipfile.ZipFile(fixture, "w") as target:
        for item in source.infolist():
            content = source.read(item)
            if item.filename == "word/styles.xml":
                assert content.count(declaration) == 1
                content = content.replace(
                    declaration,
                    declaration + f' xmlns="{WORD_NAMESPACE}"'.encode("utf-8"),
                    1,
                )
                if missing_type:
                    content, count = re.subn(
                        rb'<w:style\s+w:type="[^"]+"(\s+w:styleId="1")',
                        rb"<w:style\1",
                        content,
                    )
                    assert count == 1
                styles = etree.fromstring(content).findall(W + "style")
                assert styles
                assert all(W + "styleId" in style.attrib for style in styles)
            target.writestr(item, content)

    fixture.seek(0)
    actual = markitdown.convert_stream(
        fixture, stream_info=StreamInfo(extension=".docx")
    ).markdown

    assert "# Abstract" in actual
    assert actual == expected


@pytest.fixture(params=["w", "word"])
def styles_xml(request: pytest.FixtureRequest) -> bytes:
    prefix = request.param
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<{prefix}:styles xmlns:{prefix}="{WORD_NAMESPACE}" xmlns="{WORD_NAMESPACE}"
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
    xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
    mc:Ignorable="w14">
  <{prefix}:style {prefix}:type="paragraph" {prefix}:styleId="Normal">
    <{prefix}:name {prefix}:val="Normal"/>
  </{prefix}:style>
</{prefix}:styles>""".encode(
        "utf-8"
    )


def test_valid_styles_are_returned_unchanged(styles_xml: bytes) -> None:
    assert _pre_process_styles(styles_xml) == styles_xml


def test_missing_type_repair_preserves_namespaces(styles_xml: bytes) -> None:
    malformed, count = re.subn(rb'\s+(?:w|word):type="paragraph"', b"", styles_xml)
    assert count == 1
    original = etree.fromstring(styles_xml)

    repaired = etree.fromstring(_pre_process_styles(malformed))

    assert repaired.nsmap == original.nsmap
    assert repaired.attrib == original.attrib
    style = repaired.find(W + "style")
    assert style is not None
    assert style.attrib == {W + "type": "paragraph", W + "styleId": "Normal"}
    name = style.find(W + "name")
    assert name is not None
    assert name.attrib == {W + "val": "Normal"}


def test_styles_without_ids_are_removed(styles_xml: bytes) -> None:
    malformed, count = re.subn(rb'\s+(?:w|word):styleId="Normal"', b"", styles_xml)
    assert count == 1

    repaired = etree.fromstring(_pre_process_styles(malformed))

    assert repaired.findall(W + "style") == []
