# -*- coding: utf-8 -*-
"""Every OMML element's properties child is optional.

``<m:f>`` without ``<m:fPr>`` is a fraction with default properties, and the
same goes for ``<m:d>``, ``<m:acc>``, ``<m:bar>`` and ``<m:groupChr>``. Word
always writes the child, because it carries the control run's formatting, but
other producers have no reason to. The handlers indexed it directly, so an
equation that omits it raised ``KeyError``. ``_pre_process_math`` runs over the
whole of ``word/document.xml`` inside a blanket ``except Exception``, so the
crash discards the OMML rewrite for the entire part and every equation in the
document is lost.
"""

import io
import os
import re
import zipfile

import pytest
from xml.etree import ElementTree as ET

from markitdown import MarkItDown, StreamInfo
from markitdown.converter_utils.docx.math.omml import OMML_NS, oMath2Latex

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")
EQUATIONS_DOCX = os.path.join(TEST_FILES_DIR, "equations.docx")

MATH_NS_DECL = f'xmlns:m="{OMML_NS[1:-1]}"'


def _latex(xml_fragment: str) -> str:
    element = ET.fromstring(f"<m:oMath {MATH_NS_DECL}>{xml_fragment}</m:oMath>")
    return oMath2Latex(element).latex


FRACTION = "<m:f>{pr}<m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>2</m:t></m:r></m:den></m:f>"
DELIMITER = "<m:d>{pr}<m:e><m:r><m:t>x</m:t></m:r></m:e></m:d>"
ACCENT = "<m:acc>{pr}<m:e><m:r><m:t>x</m:t></m:r></m:e></m:acc>"
BAR = "<m:bar>{pr}<m:e><m:r><m:t>x</m:t></m:r></m:e></m:bar>"
GROUP_CHAR = "<m:groupChr>{pr}<m:e><m:r><m:t>x</m:t></m:r></m:e></m:groupChr>"


@pytest.mark.parametrize(
    "template, properties",
    [
        (FRACTION, "<m:fPr><m:ctrlPr/></m:fPr>"),
        (DELIMITER, "<m:dPr><m:ctrlPr/></m:dPr>"),
        (ACCENT, "<m:accPr><m:ctrlPr/></m:accPr>"),
        (BAR, "<m:barPr><m:ctrlPr/></m:barPr>"),
        (GROUP_CHAR, "<m:groupChrPr><m:ctrlPr/></m:groupChrPr>"),
    ],
    ids=["f", "d", "acc", "bar", "groupChr"],
)
def test_omitted_properties_convert_like_default_properties(
    template: str, properties: str
) -> None:
    """Omitting the child must read the same as a child that sets nothing."""
    assert _latex(template.format(pr="")) == _latex(template.format(pr=properties))


def test_fraction_without_properties_still_converts() -> None:
    assert _latex(FRACTION.format(pr="")) == r"\frac{1}{2}"


def test_delimiter_without_properties_uses_the_default_parentheses() -> None:
    assert _latex(DELIMITER.format(pr="")) == r"\left(x\right)"


def test_explicit_properties_are_still_honored() -> None:
    """A property that is set must still win over the default."""
    latex = _latex(
        DELIMITER.format(pr='<m:dPr><m:begChr m:val="["/><m:endChr m:val="]"/></m:dPr>')
    )

    assert latex == r"\left[x\right]"


def _docx_without(element_name: str) -> io.BytesIO:
    """Rebuild the equations fixture with every ``<m:NAME>`` element removed."""
    pattern = re.compile(
        f"<m:{element_name}>.*?</m:{element_name}>".encode("utf-8"), re.S
    )
    buffer = io.BytesIO()
    with zipfile.ZipFile(EQUATIONS_DOCX) as source:
        with zipfile.ZipFile(buffer, "w") as target:
            for item in source.infolist():
                data = source.read(item.filename)
                if item.filename == "word/document.xml":
                    data, removed = pattern.subn(b"", data)
                    assert removed > 0, f"fixture has no <m:{element_name}> to remove"
                target.writestr(item, data)
    buffer.seek(0)
    return buffer


def _latex_line_count(stream) -> int:
    markdown = (
        MarkItDown()
        .convert_stream(stream, stream_info=StreamInfo(extension=".docx"))
        .markdown
    )
    return len([line for line in markdown.splitlines() if "$" in line])


@pytest.mark.parametrize("element_name", ["fPr", "dPr"])
def test_document_keeps_its_equations_without_the_properties_child(
    element_name: str,
) -> None:
    """The damage is not local: one such equation loses all of them."""
    with open(EQUATIONS_DOCX, "rb") as fixture:
        expected = _latex_line_count(fixture)
    assert expected > 0

    assert _latex_line_count(_docx_without(element_name)) == expected
