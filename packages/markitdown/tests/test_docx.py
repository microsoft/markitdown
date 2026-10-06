"""DOCX conversion, math, styles, and image hooks."""

import base64
import inspect
import io
import os
import re
import zipfile
from pathlib import Path
from typing import Any, BinaryIO, Callable, Optional
from unittest.mock import Mock
from xml.etree import ElementTree as ET

import mammoth
import pytest
from bs4 import BeautifulSoup
from lxml import etree
from mammoth.docx.files import InvalidFileReferenceError

from markitdown import (
    FileConversionException,
    MarkItDown,
    MissingDependencyException,
    StreamInfo,
)
from markitdown.converter_utils.docx.math.latex_dict import (
    CHR,
    CHR_BO,
    CHR_DEFAULT,
    POS,
    POS_DEFAULT,
    T,
)
from markitdown.converter_utils.docx.math.omml import OMML_NS, load_string, oMath2Latex
from markitdown.converter_utils.docx.pre_process import _pre_process_styles
from markitdown.converters import DocxConverter, HtmlConverter, _docx_converter


# Math functions


def test_omml_known_function():
    omml_xml = """<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
        <m:oMath>
            <m:func>
                <m:fName><m:r><m:t>log</m:t></m:r></m:fName>
                <m:e><m:r><m:t>x</m:t></m:r></m:e>
            </m:func>
        </m:oMath>
    </m:oMathPara>"""
    results = list(load_string(omml_xml))
    assert len(results) == 1
    assert r"\log" in str(results[0])


def test_omml_unknown_function_fallback():
    omml_xml = """<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
        <m:oMath>
            <m:func>
                <m:fName><m:r><m:t>customFunc</m:t></m:r></m:fName>
                <m:e><m:r><m:t>x</m:t></m:r></m:e>
            </m:func>
        </m:oMath>
    </m:oMathPara>"""
    results = list(load_string(omml_xml))
    assert len(results) == 1
    assert r"\operatorname{customFunc}" in str(results[0])


def test_omml_function_name_split_across_runs():
    # Word can break a single function name into several runs (e.g. at a
    # formatting boundary); the runs must be joined before the lookup.
    omml_xml = """<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
        <m:oMath>
            <m:func>
                <m:fName><m:r><m:t>custom</m:t></m:r><m:r><m:t>Func</m:t></m:r></m:fName>
                <m:e><m:r><m:t>x</m:t></m:r></m:e>
            </m:func>
        </m:oMath>
    </m:oMathPara>"""
    results = list(load_string(omml_xml))
    assert len(results) == 1
    assert str(results[0]) == r"\operatorname{customFunc}(x)"


def test_omml_known_function_split_across_runs():
    omml_xml = """<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
        <m:oMath>
            <m:func>
                <m:fName><m:r><m:t>si</m:t></m:r><m:r><m:t>n</m:t></m:r></m:fName>
                <m:e><m:r><m:t>x</m:t></m:r></m:e>
            </m:func>
        </m:oMath>
    </m:oMathPara>"""
    results = list(load_string(omml_xml))
    assert len(results) == 1
    assert str(results[0]) == r"\sin(x)"


# Math accents

# Tests for DOCX math accent templates.
#
# Every accent in ``latex_dict.CHR`` is a ``str.format`` template applied by
# ``oMath2Latex.do_acc`` as ``latex_s.format(c_dict["e"])``. A template whose
# braces are unbalanced raises ``ValueError`` at that call.
#
# That failure is not local to the equation. ``pre_process_docx`` runs
# ``_pre_process_math`` over the whole of ``word/document.xml`` inside a blanket
# ``except Exception`` and, on error, writes the *original* unprocessed XML back.
# Mammoth does not render OMML, so a single unformattable accent silently removes
# every equation in the document -- with no error and a zero exit code.
#
# ``test_accent_templates_are_formattable`` guards the whole table against that
# class of typo; ``test_caron_and_ring_accents`` covers the two entries that
# carried an extra closing brace.

# Accent characters, as Word writes them into <m:chr m:val="...">.
CARON = "\u030c"  # COMBINING CARON        -> \check

RING_ABOVE = "\u030a"  # COMBINING RING ABOVE   -> \ocirc

CIRCUMFLEX = "\u0302"  # COMBINING CIRCUMFLEX   -> \hat

_OMML_DOC = (
    "<w:document "
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
    "<m:oMath><m:acc>"
    '<m:accPr><m:chr m:val="{chr}"/></m:accPr>'
    "<m:e><m:r><m:t>x</m:t></m:r></m:e>"
    "</m:acc></m:oMath></w:document>"
)


def _latex_for_accent(accent_char: str) -> str:
    """Convert a single accented variable to LaTeX, as pre_process_docx would."""
    return next(load_string(_OMML_DOC.format(chr=accent_char))).latex


def test_accent_templates_are_formattable() -> None:
    """Every {0} template must survive .format(); do_acc calls it unguarded."""
    unformattable = []
    for name, table in (
        ("CHR", CHR),
        ("CHR_BO", CHR_BO),
        ("CHR_DEFAULT", CHR_DEFAULT),
        ("POS", POS),
        ("POS_DEFAULT", POS_DEFAULT),
    ):
        for key, template in table.items():
            if not isinstance(template, str) or "{0}" not in template:
                continue
            try:
                template.format("x")
            except ValueError as exc:
                unformattable.append(f"{name}[{key!r}] = {template!r}: {exc}")

    assert not unformattable, "unformattable accent templates: " + "; ".join(
        unformattable
    )


def test_caron_and_ring_accents() -> None:
    """U+030C and U+030A each carried an extra '}' and raised ValueError."""
    assert _latex_for_accent(CARON) == "\\check{x}"
    assert _latex_for_accent(RING_ABOVE) == "\\ocirc{x}"


def test_unmodified_accent_still_converts() -> None:
    """Control: a neighbouring accent that was never broken."""
    assert _latex_for_accent(CIRCUMFLEX) == "\\hat{x}"


# Math symbols

# Tests for the OMML -> LaTeX symbol tables used by the DOCX converter.
#
# Two independent defects are covered here:
#
# ``CHR`` maps a combining accent to a LaTeX template. U+20EE COMBINING LEFT
# ARROW BELOW mapped to ``\underledtarrow``, which is not a LaTeX macro -- the
# name is a scrambled ``\underleftarrow``. Its two neighbours in the same table
# (U+20D6 -> ``\overleftarrow``, U+20EF -> ``\underrightarrow``) show the
# intent. The template still formats, so nothing raises: the document simply ends
# up with an undefined control sequence that no renderer can typeset.
#
# ``T`` normalizes the Mathematical Alphanumeric Symbols back to ASCII, so that
# an equation written with math italic letters yields ``h(x)`` rather than a
# string of astral-plane codepoints. U+1D455 -- the slot where math italic small
# h would sit -- is permanently reserved, because Unicode unifies that letter
# with U+210E PLANCK CONSTANT. The table followed the contiguous block and so
# skipped h, leaving it as the single letter of the alphabet that survived
# untranslated into the LaTeX output.

# Math italic Latin: A-Z is contiguous, a-z has a hole at U+1D455 (small h),
# which Unicode unifies with U+210E.
ITALIC_UPPERCASE = {
    chr(0x1D434 + i): c for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
}

ITALIC_LOWERCASE = {
    chr(0x1D44E + i): c for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")
}

ITALIC_LOWERCASE.pop(chr(0x1D455))  # reserved codepoint, never assigned

ITALIC_LOWERCASE["ℎ"] = "h"

_DOC = (
    "<w:document "
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
    "{0}</w:document>"
)

_ACCENT = (
    "<m:oMath><m:acc>"
    '<m:accPr><m:chr m:val="{chr}"/></m:accPr>'
    "<m:e><m:r><m:t>x</m:t></m:r></m:e>"
    "</m:acc></m:oMath>"
)

_RUN = "<m:oMath><m:r><m:t>{text}</m:t></m:r></m:oMath>"


def _latex(fragment: str) -> str:
    return next(load_string(_DOC.format(fragment))).latex


def _accent_latex(accent_char: str) -> str:
    return _latex(_ACCENT.format(chr=accent_char))


def _run_latex(text: str) -> str:
    return _latex(_RUN.format(text=text))


def test_arrow_accents_are_consistent() -> None:
    """The three arrow accents share one naming scheme; none may be misspelled."""
    assert _accent_latex("⃖") == "\\overleftarrow{x}"  # left arrow above
    assert _accent_latex("⃯") == "\\underrightarrow{x}"  # right arrow below
    assert _accent_latex("⃮") == "\\underleftarrow{x}"  # U+20EE, left arrow below


def test_math_italic_latin_alphabet_is_complete() -> None:
    """Normalize the full alphabet, including U+210E (italic small h)."""
    for char, expected in {**ITALIC_UPPERCASE, **ITALIC_LOWERCASE}.items():
        assert T.get(char) == expected, f"U+{ord(char):04X} is missing from T"
        assert _run_latex(char) == expected


def test_math_italic_expression_is_fully_normalized() -> None:
    """A whole expression must come out as plain ASCII LaTeX."""
    # h(x) = g(x), written entirely with math italic codepoints.
    expression = "ℎ(\U0001d465)=\U0001d454(\U0001d465)"
    assert _run_latex(expression) == "h(x)=g(x)"


# Malformed math runs

# Regression test for a crash in the OMML -> LaTeX converter when a math run
# (<m:r>) has no <m:t> text child (e.g. a run that only carries formatting
# properties). Previously `do_r()` called `elm.findtext(...)` directly and
# iterated over the result, which raised `TypeError: 'NoneType' object is not
# iterable` when the run had no text, aborting equation conversion for the
# entire document.

MATH_NS_DECL = f'xmlns:m="{OMML_NS[1:-1]}"'


def _parse_omath(xml_fragment: str):
    wrapped = f"<m:oMath {MATH_NS_DECL}>{xml_fragment}</m:oMath>"
    return ET.fromstring(wrapped)


def test_run_without_text_child_does_not_crash():
    # <m:r> with only <m:rPr>, no <m:t> child.
    element = _parse_omath("<m:r><m:rPr/></m:r>")
    # Should not raise TypeError: 'NoneType' object is not iterable
    result = oMath2Latex(element)
    assert result.latex == ""


def test_run_with_text_still_converts():
    element = _parse_omath("<m:r><m:t>x</m:t></m:r>")
    result = oMath2Latex(element)
    assert result.latex == "x"


def test_subscript_with_missing_text_run_does_not_crash():
    # Mirrors a real-world document: a subscript expression where one of the
    # runs involved has no text (e.g. produced by some Word equation editors).
    element = _parse_omath(
        "<m:sSub>"
        "<m:e><m:r><m:t>l</m:t></m:r></m:e>"
        "<m:sub><m:r><m:rPr/></m:r><m:r><m:t>1</m:t></m:r></m:sub>"
        "</m:sSub>"
    )
    result = oMath2Latex(element)
    assert "l" in result.latex
    assert "1" in result.latex


def test_delimiter_multiple_arguments_with_sepchr():
    element = _parse_omath(
        "<m:r><m:t>f</m:t></m:r>"
        "<m:d>"
        '<m:dPr><m:sepChr m:val=","/></m:dPr>'
        "<m:e><m:r><m:t>x</m:t></m:r></m:e>"
        "<m:e><m:r><m:t>y</m:t></m:r></m:e>"
        "</m:d>"
    )
    result = oMath2Latex(element)
    assert result.latex == r"f\left(x,y\right)"


def test_delimiter_multiple_arguments_default_separator():
    element = _parse_omath(
        "<m:d>"
        '<m:dPr><m:begChr m:val="{"/><m:endChr m:val="}"/></m:dPr>'
        "<m:e><m:r><m:t>x</m:t></m:r></m:e>"
        "<m:e><m:r><m:t>x&gt;0</m:t></m:r></m:e>"
        "</m:d>"
    )
    result = oMath2Latex(element)
    assert result.latex == r"\left\{x|x>0\right\}"


# Stylesheet repair

WORD_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

W = f"{{{WORD_NAMESPACE}}}"

TEST_DOCX = Path(__file__).parent / "test_files" / "test.docx"


@pytest.mark.parametrize("double_strike", [False, True])
@pytest.mark.parametrize("missing_type", [False, True])
def test_docx_styles_with_redundant_default_namespace(
    missing_type: bool, double_strike: bool
) -> None:
    markitdown = MarkItDown()
    expected = markitdown.convert(TEST_DOCX).markdown
    fixture = io.BytesIO()
    declaration = f'xmlns:w="{WORD_NAMESPACE}"'.encode("utf-8")

    with zipfile.ZipFile(TEST_DOCX) as source, zipfile.ZipFile(fixture, "w") as target:
        for item in source.infolist():
            content = source.read(item)
            if item.filename == "word/styles.xml":
                if double_strike:
                    assert content.count(b"</w:styles>") == 1
                    content = content.replace(
                        b"</w:styles>",
                        b'<w:style w:type="character" w:styleId="DoubleStrike">'
                        b'<w:name w:val="Double Strike"/>'
                        b'<w:rPr><w:dstrike w:val="1"/></w:rPr>'
                        b"</w:style></w:styles>",
                        1,
                    )
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


@pytest.mark.parametrize("value", [None, "0", "1"])
@pytest.mark.parametrize("missing_type", [False, True])
def test_style_strike_repair_preserves_namespaces(
    styles_xml: bytes, value: str | None, missing_type: bool
) -> None:
    original = etree.fromstring(styles_xml)
    style = original.find(W + "style")
    assert style is not None
    if missing_type:
        del style.attrib[W + "type"]
    properties = etree.SubElement(style, W + "rPr")
    strike = etree.SubElement(properties, W + "dstrike")
    if value is not None:
        strike.set(W + "val", value)
    etree.SubElement(properties, W + "b")

    repaired = etree.fromstring(_pre_process_styles(etree.tostring(original)))

    assert repaired.nsmap == original.nsmap
    assert repaired.attrib == original.attrib
    style = repaired.find(W + "style")
    assert style is not None
    assert style.attrib == {W + "type": "paragraph", W + "styleId": "Normal"}
    assert repaired.find(".//" + W + "dstrike") is None
    strike = style.find(f"{W}rPr/{W}strike")
    assert strike is not None
    assert strike.attrib == ({} if value is None else {W + "val": value})
    assert style.find(f"{W}rPr/{W}b") is not None


def test_other_namespace_dstrike_is_unchanged(styles_xml: bytes) -> None:
    original = etree.fromstring(styles_xml)
    etree.SubElement(original, "{urn:extension}dstrike")
    content = etree.tostring(original)

    assert _pre_process_styles(content) == content


# Image hooks

_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAM"
    "BAQDJ/pLvAAAAAElFTkSuQmCC"
)

_GIF = base64.b64decode("R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBTAA7")

_INFO = StreamInfo(extension=".docx")

_FILES = Path(__file__).parent / "test_files"


def _image(rid: str = "rIdPng", number: int = 1) -> str:
    return f"""<w:r><w:drawing><wp:inline>
  <wp:extent cx="9525" cy="9525"/>
  <wp:docPr id="{number}" name="Image {number}" descr="Image {number}"/>
  <a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
    <pic:pic>
      <pic:nvPicPr><pic:cNvPr id="{number}" name="Image {number}"/><pic:cNvPicPr/></pic:nvPicPr>
      <pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
      <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="9525" cy="9525"/></a:xfrm>
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
      </pic:spPr>
    </pic:pic>
  </a:graphicData></a:graphic>
</wp:inline></w:drawing></w:r>"""


def _text(text: str) -> str:
    return f'<w:r><w:t xml:space="preserve">{text}</w:t></w:r>'


def _paragraph(content: str) -> str:
    return f"<w:p>{content}</w:p>"


_BODY = _paragraph(_text("Before") + _image() + _text("After"))


def _docx(body: str = _BODY, *, embedded_style_map: Optional[str] = None) -> io.BytesIO:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr(
            "[Content_Types].xml",
            """<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Default Extension="gif" ContentType="image/gif"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>""",
        )
        archive.writestr(
            "_rels/.rels",
            """<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdDocument" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>""",
        )
        archive.writestr(
            "word/_rels/document.xml.rels",
            """<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdPng" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image.png"/>
  <Relationship Id="rIdGif" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image.gif"/>
</Relationships>""",
        )
        archive.writestr(
            "word/document.xml",
            f"""<w:document
  xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
  xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
  xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
  xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
  xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
  <w:body>{body}</w:body>
</w:document>""",
        )
        archive.writestr("word/media/image.png", _PNG)
        archive.writestr("word/media/image.gif", _GIF)
    if embedded_style_map is not None:
        stream.seek(0)
        mammoth.embed_style_map(stream, embedded_style_map)
    stream.seek(0)
    return stream


class _ImageConverter(DocxConverter):
    def __init__(self, render: Callable[..., Optional[str]]):
        super().__init__()
        self.render = render

    def _image_to_html(
        self, image_stream: BinaryIO, stream_info: StreamInfo, **kwargs: Any
    ) -> Optional[str]:
        return self.render(image_stream, stream_info, **kwargs)


def test_image_hook_does_not_change_public_conversion_signature() -> None:
    assert list(inspect.signature(DocxConverter.convert).parameters) == [
        "self",
        "file_stream",
        "stream_info",
        "kwargs",
    ]
    assert _ImageConverter.convert is DocxConverter.convert
    assert list(inspect.signature(DocxConverter.__init__).parameters) == ["self"]


@pytest.mark.parametrize("via_dispatcher", [False, True])
def test_inherited_hook_receives_images_and_options_in_order(
    via_dispatcher: bool,
) -> None:
    seen = []
    streams = []
    service = object()
    options: dict[str, Any] = {
        "ocr_service": service,
        "heading_style": "underlined",
    }

    def render(stream: BinaryIO, info: StreamInfo, **kwargs: Any) -> str:
        assert stream.tell() == 0
        data = stream.read()
        stream.seek(0)
        assert stream.read() == data
        seen.append((data, info, kwargs))
        streams.append(stream)
        return f"<strong>image{len(seen)}</strong>"

    class InheritedImages(_ImageConverter):
        pass

    converter = InheritedImages(render)
    source = _docx(
        _paragraph(
            _image("rIdGif", 1)
            + _text(" ")
            + _image("rIdPng", 2)
            + _text(" ")
            + _image("rIdGif", 3)
        )
    )
    original = source.getvalue()
    info = StreamInfo(
        extension=".docx",
        filename="document.docx",
        url="https://example.test/document.docx",
        local_path="/document.docx",
    )
    if via_dispatcher:
        markitdown = MarkItDown()
        markitdown.register_converter(converter, priority=-1)
        result = markitdown.convert_stream(source, stream_info=info, **options)
    else:
        source.seek(7)
        result = converter.convert(source, info, **options)

    assert [entry[:2] for entry in seen] == [
        (_GIF, StreamInfo(mimetype="image/gif", extension=".gif")),
        (_PNG, StreamInfo(mimetype="image/png", extension=".png")),
        (_GIF, StreamInfo(mimetype="image/gif", extension=".gif")),
    ]
    assert all(entry[2]["ocr_service"] is service for entry in seen)
    assert all(entry[2]["heading_style"] == "underlined" for entry in seen)
    assert result.markdown == "**image1** **image2** **image3**"
    assert all(stream.closed for stream in streams)
    assert not source.closed and source.getvalue() == original


@pytest.mark.parametrize("keep_data_uris", [False, True])
@pytest.mark.parametrize("fallback", [None, "", " \n\t"])
def test_declining_hook_preserves_native_output(
    monkeypatch: pytest.MonkeyPatch, fallback: Optional[str], keep_data_uris: bool
) -> None:
    expected_converter = DocxConverter()
    expected_html = Mock(wraps=expected_converter._html_converter.convert_string)
    monkeypatch.setattr(
        expected_converter._html_converter, "convert_string", expected_html
    )
    expected = expected_converter.convert(_docx(), _INFO, keep_data_uris=keep_data_uris)
    converter = _ImageConverter(Mock(return_value=fallback))
    actual_html = Mock(wraps=converter._html_converter.convert_string)
    monkeypatch.setattr(converter._html_converter, "convert_string", actual_html)

    actual = converter.convert(_docx(), _INFO, keep_data_uris=keep_data_uris)

    assert actual_html.call_args == expected_html.call_args
    assert actual.markdown == expected.markdown
    assert actual.title == expected.title


def test_native_converter_does_not_add_image_processing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    convert_html = Mock(wraps=mammoth.convert_to_html)
    monkeypatch.setattr(mammoth, "convert_to_html", convert_html)

    class UnmodifiedSubclass(DocxConverter):
        pass

    for converter in (DocxConverter(), UnmodifiedSubclass()):
        result = converter.convert(_docx(), _INFO)
        assert "![Image 1](data:image/png;base64...)" in result.markdown
        assert "convert_image" not in convert_html.call_args.kwargs


def test_override_can_delegate_to_super() -> None:
    class NativeImages(DocxConverter):
        def _image_to_html(self, image_stream, stream_info, **kwargs):
            return super()._image_to_html(image_stream, stream_info, **kwargs)

    actual = NativeImages().convert(_docx(), _INFO)
    assert actual.markdown == DocxConverter().convert(_docx(), _INFO).markdown


@pytest.mark.parametrize(
    ("fragment", "expected"),
    [
        ("<strong>text</strong>", "<p>Before<strong>text</strong>After</p>"),
        ("one<br>two", "<p>Beforeone<br/>twoAfter</p>"),
        ("A &amp; B &lt; C", "<p>BeforeA &amp; B &lt; CAfter</p>"),
        (
            "<p>one</p><p>two</p>",
            "<p>Before</p><p>one</p><p>two</p><p>After</p>",
        ),
        (
            "<div><p>one</p><p>two</p></div>",
            "<p>Before</p><div><p>one</p><p>two</p></div><p>After</p>",
        ),
        (
            "<ul><li>one</li><li>two</li></ul>",
            "<p>Before</p><ul><li>one</li><li>two</li></ul><p>After</p>",
        ),
        (
            "<table><tr><th>Key</th></tr><tr><td>Value</td></tr></table>",
            "<p>Before</p><table><tr><th>Key</th></tr><tr><td>Value</td></tr>"
            "</table><p>After</p>",
        ),
        (
            "<details><summary>Title</summary><p>Body</p></details>",
            "<p>Before</p><details><summary>Title</summary><p>Body</p>"
            "</details><p>After</p>",
        ),
        (
            "lead<p>block</p>tail",
            "<p>Beforelead</p><p>block</p><p>tailAfter</p>",
        ),
        (
            "<pre><code>a &lt; b\n  *literal*</code></pre>",
            "<p>Before</p><pre><code>a &lt; b\n  *literal*</code></pre><p>After</p>",
        ),
    ],
)
def test_fragment_placement_precedes_shared_html_conversion(
    monkeypatch: pytest.MonkeyPatch, fragment: str, expected: str
) -> None:
    converter = _ImageConverter(Mock(return_value=fragment))
    convert_html = Mock(wraps=converter._html_converter.convert_string)
    monkeypatch.setattr(converter._html_converter, "convert_string", convert_html)
    options = {"escape_asterisks": False, "custom_option": "forwarded"}

    result = converter.convert(_docx(), _INFO, **options)

    assert convert_html.call_args.args == (expected,)
    assert convert_html.call_args.kwargs == options
    assert (
        result.markdown
        == HtmlConverter().convert_string(expected, escape_asterisks=False).markdown
    )
    assert "data-markitdown-image" not in expected


@pytest.mark.parametrize(
    ("style_map", "expected"),
    [
        (None, "<p>one</p><p>two</p>"),
        ("p => ul > li:fresh", "<ul><li><p>one</p><p>two</p></li></ul>"),
        ("p => blockquote > p:fresh", "<blockquote><p>one</p><p>two</p></blockquote>"),
        ("p => h2:fresh > strong", "<p>one</p><p>two</p>"),
    ],
)
def test_standalone_block_image_does_not_leave_empty_wrappers(
    monkeypatch: pytest.MonkeyPatch, style_map: Optional[str], expected: str
) -> None:
    converter = _ImageConverter(Mock(return_value="<p>one</p><p>two</p>"))
    convert_html = Mock(wraps=converter._html_converter.convert_string)
    monkeypatch.setattr(converter._html_converter, "convert_string", convert_html)

    converter.convert(_docx(_paragraph(_image())), _INFO, style_map=style_map)

    assert convert_html.call_args.args == (expected,)


def test_block_image_keeps_its_table_cell(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    body = (
        "<w:tbl><w:tblPr/><w:tblGrid><w:gridCol/><w:gridCol/></w:tblGrid>"
        "<w:tr><w:tc>"
        + _paragraph(_text("Item"))
        + "</w:tc><w:tc>"
        + _paragraph(_text("Details"))
        + "</w:tc></w:tr><w:tr><w:tc>"
        + _paragraph(_text("A"))
        + "</w:tc><w:tc>"
        + _paragraph(_image())
        + "</w:tc></w:tr></w:tbl>"
    )
    converter = _ImageConverter(
        Mock(return_value="<p>Serial: 12345</p><p>Status: active</p>")
    )
    convert_html = Mock(wraps=converter._html_converter.convert_string)
    monkeypatch.setattr(converter._html_converter, "convert_string", convert_html)

    result = converter.convert(_docx(body), _INFO)

    soup = BeautifulSoup(convert_html.call_args.args[0], "html.parser")
    assert len(soup.find_all("tr")) == 2
    assert len(soup.find_all("td")) == 4
    assert (
        str(soup.find_all("td")[-1])
        == "<td><p>Serial: 12345</p><p>Status: active</p></td>"
    )
    assert not soup.select("p p")
    assert "| A | Serial: 12345  Status: active |" in result.markdown


def test_nested_run_formatting_is_preserved_around_blocks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    converter = _ImageConverter(Mock(return_value="<p>block</p>"))
    convert_html = Mock(wraps=converter._html_converter.convert_string)
    monkeypatch.setattr(converter._html_converter, "convert_string", convert_html)

    converter.convert(_docx(), _INFO, style_map="p => p:fresh > em > strong")

    assert convert_html.call_args.args == (
        "<p><em><strong>Before</strong></em></p><p>block</p>"
        "<p><em><strong>After</strong></em></p>",
    )


def test_hook_inherits_preprocessing_and_style_precedence() -> None:
    body = (
        _BODY
        + _paragraph(
            '<w:r><w:rPr><w:u w:val="single"/></w:rPr><w:t>underlined</w:t></w:r>'
        )
        + _paragraph("<w:r><w:rPr><w:dstrike/></w:rPr><w:t>deleted</w:t></w:r>")
        + _paragraph("<m:oMath><m:r><m:t>x</m:t></m:r></m:oMath>")
    )

    result = _ImageConverter(Mock(return_value="image")).convert(
        _docx(body, embedded_style_map="u => em"),
        _INFO,
        style_map="u => strong",
    )

    assert result.markdown == "BeforeimageAfter\n\n**underlined**\n\n~~deleted~~\n\n$x$"


def test_multiple_images_and_native_fallback_keep_their_own_positions() -> None:
    converter = _ImageConverter(Mock(side_effect=[None, "<em>recognized</em>", ""]))
    body = _paragraph(
        _image(number=1) + _text(" ") + _image(number=2) + _text(" ") + _image(number=3)
    )

    result = converter.convert(_docx(body), _INFO)

    assert result.markdown == (
        "![Image 1](data:image/png;base64...) *recognized* "
        "![Image 3](data:image/png;base64...)"
    )


def test_many_images_have_independent_replacements() -> None:
    converter = _ImageConverter(
        Mock(side_effect=[f"<p>Image {number}</p>" for number in range(12)])
    )
    body = _paragraph("".join(_image(number=number) for number in range(12)))

    result = converter.convert(_docx(body), _INFO)

    assert result.markdown == "\n\n".join(f"Image {number}" for number in range(12))


def test_returned_image_and_literal_text_use_normal_html_rendering() -> None:
    render = Mock(
        return_value=(
            "<p>&lt;literal&gt; *not emphasis* &amp; text</p>"
            '<img alt="generated" src="image.png"><script>discard</script>'
        )
    )
    result = _ImageConverter(render).convert(_docx(_paragraph(_image())), _INFO)

    assert (
        result.markdown
        == r"<literal> \*not emphasis\* & text" + "\n\n![generated](image.png)"
    )
    render.assert_called_once()


@pytest.mark.parametrize("result", [False, 123, b"<p>not a string</p>"])
def test_invalid_return_is_not_silent_native_fallback(result: Any) -> None:
    with pytest.raises(TypeError, match="HTML string or None"):
        _ImageConverter(Mock(return_value=result)).convert(_docx(), _INFO)


@pytest.mark.parametrize(
    "fragment",
    [
        "<html><body>document</body></html>",
        "<head><title>title</title></head>",
        "<body>content</body>",
        "<!DOCTYPE html><p>content</p>",
    ],
)
def test_full_document_is_not_a_valid_fragment(fragment: str) -> None:
    with pytest.raises(ValueError, match="fragment, not a document"):
        _ImageConverter(Mock(return_value=fragment)).convert(_docx(), _INFO)


@pytest.mark.parametrize("via_dispatcher", [False, True])
def test_hook_errors_propagate_and_close_the_image_stream(via_dispatcher: bool) -> None:
    streams = []
    error = RuntimeError("Image service failed")

    def render(stream, info, **kwargs):
        streams.append(stream)
        raise error

    converter = _ImageConverter(render)
    if via_dispatcher:
        markitdown = MarkItDown(enable_builtins=False)
        markitdown.register_converter(converter, priority=-1)
        with pytest.raises(FileConversionException) as caught:
            markitdown.convert_stream(_docx(), stream_info=_INFO)
        assert caught.value.attempts is not None
        assert any(
            attempt.exc_info and attempt.exc_info[1] is error
            for attempt in caught.value.attempts
        )
    else:
        with pytest.raises(RuntimeError) as caught_direct:
            converter.convert(_docx(), _INFO)
        assert caught_direct.value is error
    assert streams and all(stream.closed for stream in streams)


def test_dispatcher_can_fall_back_to_native_docx_after_hook_error() -> None:
    render = Mock(side_effect=RuntimeError("Image service failed"))
    markitdown = MarkItDown()
    markitdown.register_converter(_ImageConverter(render), priority=-1)

    result = markitdown.convert_stream(_docx(), stream_info=_INFO)

    assert result.markdown == DocxConverter().convert(_docx(), _INFO).markdown
    render.assert_called()


def test_mammoth_does_not_swallow_hook_file_reference_errors() -> None:
    error = InvalidFileReferenceError("hook failed")
    render = Mock(side_effect=error)

    with pytest.raises(RuntimeError, match="_image_to_html failed") as caught:
        _ImageConverter(render).convert(_docx(), _INFO)

    assert caught.value.__cause__ is error
    render.assert_called_once()


def test_per_call_options_and_fragments_do_not_leak_between_conversions() -> None:
    converter = _ImageConverter(lambda stream, info, **kwargs: kwargs.get("image_text"))
    first = converter.convert(_docx(), _INFO, image_text="<p>first</p>")
    second = converter.convert(_docx(), _INFO, image_text="<p>second</p>")
    third = converter.convert(_docx(), _INFO)

    assert first.markdown == "Before\n\nfirst\n\nAfter"
    assert second.markdown == "Before\n\nsecond\n\nAfter"
    assert third.markdown == DocxConverter().convert(_docx(), _INFO).markdown


def test_unreferenced_media_does_not_invoke_the_hook() -> None:
    render = Mock(side_effect=AssertionError("unexpected image"))

    result = _ImageConverter(render).convert(
        _docx(_paragraph(_text("Only text"))), _INFO
    )

    assert result.markdown == "Only text"
    render.assert_not_called()


@pytest.mark.parametrize(
    "fragment",
    [
        '<a href="https://example.test/new">new</a>',
        '<p><a href="https://example.test/new">new</a></p>',
    ],
)
def test_image_html_does_not_create_nested_links(
    monkeypatch: pytest.MonkeyPatch, fragment: str
) -> None:
    body = _paragraph(
        '<w:hyperlink w:anchor="target">'
        + _text("Before")
        + _image()
        + _text("After")
        + "</w:hyperlink>"
    )
    converter = _ImageConverter(Mock(return_value=fragment))
    convert_html = Mock(wraps=converter._html_converter.convert_string)
    monkeypatch.setattr(converter._html_converter, "convert_string", convert_html)

    result = converter.convert(_docx(body), _INFO)

    soup = BeautifulSoup(convert_html.call_args.args[0], "html.parser")
    assert not soup.select("a a")
    assert [link.get("href") for link in soup.find_all("a")] == [
        "#target",
        "https://example.test/new",
        "#target",
    ]
    assert "[Before](#target)" in result.markdown
    assert "[new](https://example.test/new)" in result.markdown
    assert "[After](#target)" in result.markdown


@pytest.mark.parametrize("keep_data_uris", [False, True])
def test_declining_hook_preserves_a_real_document(keep_data_uris: bool) -> None:
    content = (_FILES / "test.docx").read_bytes()
    expected = DocxConverter().convert(
        io.BytesIO(content), _INFO, keep_data_uris=keep_data_uris
    )
    render = Mock(return_value=None)

    actual = _ImageConverter(render).convert(
        io.BytesIO(content), _INFO, keep_data_uris=keep_data_uris
    )

    assert actual.markdown == expected.markdown
    assert actual.title == expected.title
    render.assert_called()


def test_hook_reads_images_from_the_preprocessed_archive() -> None:
    import struct

    stream = _docx()
    data = bytearray(stream.getvalue())
    with zipfile.ZipFile(stream) as archive:
        offset = archive.getinfo("word/media/image.png").header_offset
    length = struct.unpack_from("<H", data, offset + 26)[0]
    data[offset + 30 : offset + 30 + length] = b"WORD/MEDIA/IMAGE.PNG"
    with pytest.raises(zipfile.BadZipFile), zipfile.ZipFile(
        io.BytesIO(data)
    ) as archive:
        archive.read("word/media/image.png")
    observed = []

    def render(image_stream, stream_info, **kwargs):
        observed.append(image_stream.read())
        return "<span>image</span>"

    result = _ImageConverter(render).convert(io.BytesIO(data), _INFO)

    assert observed == [_PNG]
    assert result.markdown == "BeforeimageAfter"


def test_missing_dependencies_fail_before_invoking_hook(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    error = ModuleNotFoundError("No module named 'mammoth'")
    monkeypatch.setattr(
        _docx_converter, "_dependency_exc_info", (ModuleNotFoundError, error, None)
    )
    render = Mock()

    with pytest.raises(MissingDependencyException) as caught:
        _ImageConverter(render).convert(_docx(), _INFO)

    assert caught.value.__cause__ is error
    render.assert_not_called()


# Conversion regressions

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

DOCX_COMMENT_TEST_STRINGS = [
    "314b0a30-5b04-470b-b9f7-eed2c2bec74a",
    "49e168b7-d2ae-407f-a055-2167576f39a1",
    "## d666f1f7-46cb-42bd-9a39-9a39cf2a509f",
    "# Abstract",
    "# Introduction",
    "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
    "This is a test comment. 12df-321a",
    "Yet another comment in the doc. 55yiyi-asd09",
]


# --- Helper Functions ---
def validate_strings(result, expected_strings, exclude_strings=None):
    """Validate presence or absence of specific strings."""
    text_content = result.text_content.replace("\\", "")
    for string in expected_strings:
        assert string in text_content
    if exclude_strings:
        for string in exclude_strings:
            assert string not in text_content


def test_docx_comments() -> None:
    # Test DOCX processing, with comments and setting style_map on init
    markitdown_with_style_map = MarkItDown(style_map="comment-reference => ")
    result = markitdown_with_style_map.convert(
        os.path.join(TEST_FILES_DIR, "test_with_comment.docx")
    )
    validate_strings(result, DOCX_COMMENT_TEST_STRINGS)


def _write_underlined_docx(
    path,
    embedded_style_map: Optional[str] = None,
    *,
    paragraph_xml: str = (
        "<w:r><w:t>plain </w:t></w:r>"
        '<w:r><w:rPr><w:u w:val="single"/></w:rPr><w:t>underlined</w:t></w:r>'
    ),
) -> str:
    """Write a minimal .docx holding one underlined run, and return its path."""
    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p>{paragraph_xml}</w:p>
  </w:body>
</w:document>"""

    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>""",
        )
        archive.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>""",
        )
        archive.writestr(
            "word/_rels/document.xml.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>""",
        )
        archive.writestr("word/document.xml", document_xml)

    if embedded_style_map is not None:
        import mammoth

        with open(path, "r+b") as f:
            mammoth.embed_style_map(f, embedded_style_map)

    return str(path)


def test_docx_underlined_text_is_preserved(tmp_path) -> None:
    docx_file = _write_underlined_docx(tmp_path / "underlined.docx")

    result = MarkItDown().convert(docx_file)

    assert "plain <u>underlined</u>" in result.markdown


@pytest.mark.parametrize(
    ("run_xml", "expected"),
    [
        ('<w:t xml:space="preserve"> </w:t>', "First Last"),
        ("<w:tab/>", "First Last"),
        ("<w:t>&#160;</w:t>", "First\u00a0Last"),
        ("<w:br/>", "First\nLast"),
    ],
)
def test_docx_underlined_whitespace_is_preserved(
    tmp_path, run_xml: str, expected: str
) -> None:
    docx_file = _write_underlined_docx(
        tmp_path / "underlined_whitespace.docx",
        paragraph_xml=(
            "<w:r><w:t>First</w:t></w:r>"
            f'<w:r><w:rPr><w:u w:val="single"/></w:rPr>{run_xml}</w:r>'
            "<w:r><w:t>Last</w:t></w:r>"
        ),
    )

    assert MarkItDown().convert(docx_file).markdown == expected


def test_docx_embedded_style_map_overrides_underline_default(tmp_path) -> None:
    # A style map embedded in the document takes precedence over the default
    # "u => u" mapping that preserves underlines.
    docx_file = _write_underlined_docx(
        tmp_path / "embedded.docx", embedded_style_map="u => em"
    )

    result = MarkItDown().convert(docx_file)

    assert "plain *underlined*" in result.markdown
    assert "<u>" not in result.markdown


def test_docx_caller_style_map_overrides_embedded_style_map(tmp_path) -> None:
    # ... and a caller-supplied style map still outranks the embedded one.
    docx_file = _write_underlined_docx(
        tmp_path / "embedded.docx", embedded_style_map="u => em"
    )

    result = MarkItDown(style_map="u => strong").convert(docx_file)

    assert "plain **underlined**" in result.markdown


def test_docx_equations() -> None:
    markitdown = MarkItDown()
    docx_file = os.path.join(TEST_FILES_DIR, "equations.docx")
    result = markitdown.convert(docx_file)

    # Check for inline equation m=1 (wrapped with single $) is present
    assert "$m=1$" in result.text_content, "Inline equation $m=1$ not found"

    # Find block equations wrapped with double $$ and check if they are present
    block_equations = re.findall(r"\$\$(.+?)\$\$", result.text_content)
    assert block_equations, "No block equations found in the document."


def test_docx_zip_filename_casing_mismatch() -> None:
    """Test that DOCX files with inconsistent ZIP filename casing are handled.

    Some document generators produce .docx files where the central directory
    records one casing (e.g. 'word/document.xml') but the local file headers
    record another (e.g. 'Word/Document.XML'). Python's zipfile module raises
    BadZipFile when reading such files. This test verifies that MarkItDown
    handles this gracefully.

    See: https://github.com/microsoft/markitdown/issues/1812
    """
    import struct

    markitdown = MarkItDown()
    docx_file = os.path.join(TEST_FILES_DIR, "test.docx")

    # Read the original docx and get its expected content
    original_result = markitdown.convert(docx_file)
    assert original_result.markdown.strip(), "Original DOCX should have content"

    # Read raw bytes and corrupt the local file header filenames
    with open(docx_file, "rb") as f:
        raw = bytearray(f.read())

    # Find all local file headers and uppercase their filenames
    corrupted = bytearray(raw)
    offset = 0
    patched_count = 0
    while offset + 30 <= len(corrupted):
        if corrupted[offset : offset + 4] != b"PK\x03\x04":
            break
        fname_len = struct.unpack_from("<H", corrupted, offset + 26)[0]
        extra_len = struct.unpack_from("<H", corrupted, offset + 28)[0]
        if offset + 30 + fname_len > len(corrupted):
            break
        # Uppercase the filename in the local header
        old_name = corrupted[offset + 30 : offset + 30 + fname_len]
        new_name = old_name.upper()
        if old_name != new_name:
            corrupted[offset + 30 : offset + 30 + fname_len] = new_name
            patched_count += 1
        comp_size = struct.unpack_from("<I", corrupted, offset + 18)[0]
        offset = offset + 30 + fname_len + extra_len + comp_size

    assert patched_count > 0, "Should have patched at least one local file header"

    # Verify the corrupted file would fail with plain zipfile
    with pytest.raises(zipfile.BadZipFile):
        with zipfile.ZipFile(io.BytesIO(bytes(corrupted)), "r") as zf:
            for name in zf.namelist():
                zf.read(name)

    # Verify MarkItDown can still convert it
    corrupted_result = markitdown.convert_stream(
        io.BytesIO(bytes(corrupted)),
        file_extension=".docx",
    )
    assert (
        corrupted_result.markdown.strip()
    ), "Corrupted DOCX should still produce content"
    # Content should be equivalent to the original
    assert (
        original_result.markdown.strip() == corrupted_result.markdown.strip()
    ), "Corrupted DOCX should produce the same output as original"


def test_docx_zip_filename_non_casing_mismatch_still_rejected() -> None:
    """Only case-only local/central filename disagreements are repaired.

    Equal encoded length does not imply two names differ only in case, so the
    repair must not be used to wave through archives whose local and central
    directory names genuinely disagree -- zipfile rejects those for good
    reason, and honouring that keeps the workaround scoped to issue #1812.
    """
    import struct

    from markitdown.converter_utils.docx.pre_process import (
        _fix_zip_filename_casing,
    )

    def build_zip(first_name: str) -> bytes:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr(first_name, b"payload-a")
            zf.writestr("word/document.xml", b"payload-b")
        return buf.getvalue()

    def replace_first_local_name(data: bytes, new_name: bytes) -> bytes:
        """Rewrite only the first local file header's name, leaving the central
        directory -- the authoritative copy -- untouched."""
        raw = bytearray(data)
        fname_len = struct.unpack_from("<H", raw, 26)[0]
        assert len(new_name) == fname_len, "mutation must preserve the length"
        raw[30 : 30 + fname_len] = new_name
        return bytes(raw)

    def reads_cleanly(data: bytes) -> bool:
        try:
            with zipfile.ZipFile(io.BytesIO(data), "r") as zf:
                for name in zf.namelist():
                    zf.read(name)
        except zipfile.BadZipFile:
            return False
        return True

    original = "[Content_Types].xml"

    # A case-only mismatch is repaired ...
    case_only = replace_first_local_name(build_zip(original), original.upper().encode())
    assert not reads_cleanly(case_only)
    repaired = _fix_zip_filename_casing(io.BytesIO(case_only))
    assert reads_cleanly(repaired.read())

    # ... but an equal-length mismatch that is not case-only is left alone,
    # so zipfile still refuses the archive.
    for mutated_name in (
        b"ZBnoudou^Uxqdr\\/ylm",  # unrelated, same length
        b"[Content_Types].xmy",  # a single differing character
        b"[content_types]/xml",  # differs only outside the cased characters
    ):
        data = replace_first_local_name(build_zip(original), mutated_name)
        assert not reads_cleanly(data), f"{mutated_name!r} should not be readable"
        result = _fix_zip_filename_casing(io.BytesIO(data))
        assert not reads_cleanly(
            result.read()
        ), f"{mutated_name!r} must not be silently repaired"


def test_docx_malformed_equations() -> None:
    """Malformed equations should not crash the converter (issue #1979)."""
    import zipfile
    from io import BytesIO

    docx_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
            xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
            mc:Ignorable="w14 wp14">
  <w:body>
    <w:p>
      <w:r><w:t>Normal text</w:t></w:r>
    </w:p>
    <m:oMathPara>
      <m:oMath>
        <m:r><m:t>x+1</m:t></m:r>
      </m:oMath>
    </m:oMathPara>
    <w:p>
      <w:r><w:t>After good equation</w:t></w:r>
    </w:p>
    <m:oMathPara>
      <!-- oMathPara with no oMath child -->
    </m:oMathPara>
    <w:p>
      <w:r><w:t>After empty oMathPara</w:t></w:r>
    </w:p>
    <m:oMath>
      <!-- empty inline oMath -->
    </m:oMath>
    <w:p>
      <w:r><w:t>After empty inline oMath</w:t></w:r>
    </w:p>
    <oMathPara>
      <!-- oMath outside the math namespace: BeautifulSoup matches it by local
           name, but the namespaced lookup in _convert_omath_to_latex does not
           find it, so the conversion has nothing to work with -->
      <oMath><r><t>y+2</t></r></oMath>
    </oMathPara>
    <w:p>
      <w:r><w:t>After unnamespaced oMathPara</w:t></w:r>
    </w:p>
    <oMath><r><t>z+3</t></r></oMath>
    <w:p>
      <w:r><w:t>After unnamespaced oMath</w:t></w:r>
    </w:p>
  </w:body>
</w:document>"""

    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("word/document.xml", docx_xml.encode("utf-8"))
        z.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>""",
        )
        z.writestr(
            "word/_rels/document.xml.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>""",
        )
        z.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>""",
        )

    buf.seek(0)
    markitdown = MarkItDown()
    result = markitdown.convert(buf)
    assert "Normal text" in result.markdown
    # A malformed equation must not abort the math pre-processing step, which
    # would silently drop the LaTeX conversion of every other equation too
    assert "$x+1$" in result.markdown or "$$x+1$$" in result.markdown
    assert "After empty oMathPara" in result.markdown
    assert "After empty inline oMath" in result.markdown
    assert "After unnamespaced oMathPara" in result.markdown
    assert "After unnamespaced oMath" in result.markdown


@pytest.mark.skipif(
    os.name == "nt",
    reason="The DOCX fixture embeds a POSIX file:///tmp/test_rlink.txt target.",
)
def test_doc_rlink() -> None:
    # Test for: CVE-2025-11849
    markitdown = MarkItDown()

    # Document with rlink
    docx_file = os.path.join(TEST_FILES_DIR, "rlink.docx")

    # Directory containing the target rlink file
    rlink_tmp_dir = os.path.abspath(os.sep + "tmp")

    # Ensure the tmp directory exists
    if not os.path.exists(rlink_tmp_dir):
        pytest.skip(f"Skipping rlink test; {rlink_tmp_dir} directory does not exist.")
        return

    rlink_file_path = os.path.join(rlink_tmp_dir, "test_rlink.txt")
    rlink_content = "de658225-569e-4e3d-9ed2-cfb6abf927fc"
    b64_prefix = (
        "ZGU2NTgyMjUtNTY5ZS00ZTNkLTllZDItY2ZiNmFiZjk"  # base64 prefix of rlink_content
    )

    if os.path.exists(rlink_file_path):
        with open(rlink_file_path, "r", encoding="utf-8") as f:
            existing_content = f.read()
            if existing_content != rlink_content:
                raise ValueError(
                    f"Existing {rlink_file_path} content does not match expected content."
                )
    else:
        with open(rlink_file_path, "w", encoding="utf-8") as f:
            f.write(rlink_content)

    try:
        result = markitdown.convert(docx_file, keep_data_uris=True).text_content
        assert (
            b64_prefix not in result
        )  # Make sure the target file was NOT embedded in the output
    finally:
        os.remove(rlink_file_path)


# Styles missing a type


def test_convert_docx_with_style_missing_type(tmp_path):
    """DOCX conversion should not fail when a style entry is missing w:type."""
    source_path = os.path.join(TEST_FILES_DIR, "test.docx")
    malformed_path = tmp_path / "missing_style_type.docx"

    with zipfile.ZipFile(source_path, mode="r") as zip_input:
        with zipfile.ZipFile(malformed_path, mode="w") as zip_output:
            for item in zip_input.infolist():
                content = zip_input.read(item.filename)
                if item.filename == "word/styles.xml":
                    styles_xml = content.decode("utf-8")
                    styles_xml, count = re.subn(
                        r'<w:style\s+w:type="[^"]+"(\s+w:styleId="1")',
                        r"<w:style\1",
                        styles_xml,
                    )
                    # Guard against a future fixture change silently
                    # neutralizing this test.
                    assert count == 1
                    content = styles_xml.encode("utf-8")
                zip_output.writestr(item, content)

    result = MarkItDown().convert(str(malformed_path))

    assert (
        "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation"
        in result.markdown
    )
    assert "# Abstract" in result.markdown


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
