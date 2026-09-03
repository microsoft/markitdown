from bs4 import BeautifulSoup
from defusedxml import ElementTree as ET

from markitdown.converter_utils.docx.math.omml import oMath2Latex
from markitdown.converter_utils.docx.pre_process import _convert_omath_to_latex


def test_convert_omath_without_namespaced_child_returns_text() -> None:
    soup = BeautifulSoup(b"<oMath><r><t>x</t></r></oMath>", "xml")

    assert _convert_omath_to_latex(soup.find("oMath")) == "x"


def test_unknown_omml_function_uses_operatorname() -> None:
    root = ET.fromstring(
        """
        <m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
          <m:func>
            <m:fName><m:r><m:t>log</m:t></m:r></m:fName>
            <m:e><m:r><m:t>x</m:t></m:r></m:e>
          </m:func>
        </m:oMath>
        """
    )

    assert oMath2Latex(root).latex == r"\operatorname{log}(x)"
