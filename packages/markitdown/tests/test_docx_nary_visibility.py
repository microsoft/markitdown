"""Stored hidden n-ary limits must not become visible DOCX math."""

import io
import zipfile
from xml.etree import ElementTree as ET

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown.converter_utils.docx.math.omml import OMML_NS, oMath2Latex


def _nary_visibility_math(properties, lower="lower", upper="upper"):
    return (
        f'<m:oMath xmlns:m="{OMML_NS[1:-1]}"><m:nary>'
        '<m:naryPr><m:chr m:val="∑"/>'
        f"{properties}</m:naryPr>"
        f"<m:sub><m:r><m:t>{lower}</m:t></m:r></m:sub>"
        f"<m:sup><m:r><m:t>{upper}</m:t></m:r></m:sup>"
        "<m:e><m:r><m:t>x</m:t></m:r></m:e>"
        "</m:nary></m:oMath>"
    )


@pytest.mark.parametrize("bound", ["sub", "sup"])
@pytest.mark.parametrize("value", [None, "1", "true", "on", "0", "false", "off"])
def test_nary_limit_visibility(bound, value):
    attribute = "" if value is None else f' m:val="{value}"'
    properties = f"<m:{bound}Hide{attribute}/>"
    hidden = value in (None, "1", "true", "on")
    expected = r"\sum"
    if not (bound == "sub" and hidden):
        expected += "_{lower}"
    if not (bound == "sup" and hidden):
        expected += "^{upper}"
    expected += "x"
    assert (
        oMath2Latex(ET.fromstring(_nary_visibility_math(properties))).latex == expected
    )


def test_nary_limits_are_visible_without_hide_properties():
    assert (
        oMath2Latex(ET.fromstring(_nary_visibility_math(""))).latex
        == r"\sum_{lower}^{upper}x"
    )


def _nary_visibility_docx(properties):
    document = (
        '<w:document xmlns:w="http://schemas.openxmlformats.org/'
        'wordprocessingml/2006/main"><w:body><w:p>'
        + _nary_visibility_math(properties)
        + "</w:p><w:p><w:r><w:t>After equation</w:t></w:r></w:p></w:body></w:document>"
    )
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr(
            "[Content_Types].xml",
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            "</Types>",
        )
        archive.writestr(
            "_rels/.rels",
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            "</Relationships>",
        )
        archive.writestr("word/document.xml", document)
    stream.seek(0)
    return stream


@pytest.mark.parametrize(
    "properties,visible,hidden",
    [
        ('<m:subHide m:val="1"/>', "upper", "lower"),
        ("<m:supHide/>", "lower", "upper"),
        ('<m:subHide/><m:supHide m:val="true"/>', None, "lower"),
    ],
)
def test_nary_visibility_through_public_docx_conversion(properties, visible, hidden):
    markdown = (
        MarkItDown()
        .convert_stream(
            _nary_visibility_docx(properties), stream_info=StreamInfo(extension=".docx")
        )
        .markdown
    )
    assert hidden not in markdown
    if visible is not None:
        assert visible in markdown
    else:
        assert "upper" not in markdown
    assert r"\sum" in markdown
    assert "x$" in markdown
    assert "After equation" in markdown
