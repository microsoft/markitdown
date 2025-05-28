"""
Main entry point for OMML to LaTeX conversion.
"""

from xml.etree import ElementTree as ET
from typing import List

from .omml_parser import parse_omml_node
from .latex_symbols import OMML_NAMESPACE


def convert_omml_to_latex(omml_root_xml_string: str) -> str:
    """
    Converts an OMML XML string (typically the content of an <m:oMath> element)
    to its LaTeX representation.

    Args:
        omml_root_xml_string: A string containing the OMML XML.
                              This string should represent the content *inside* an <m:oMath> tag,
                              or a full <m:oMath> tag itself.

    Returns:
        The LaTeX string representation of the input OMML.
    """
    try:
        omml_element = ET.fromstring(omml_root_xml_string)

        if omml_element.tag == f"{OMML_NAMESPACE}oMath":
            # If the root is an oMath element, process its children
            return "".join(
                parse_omml_node(child_xml, parent=None).to_latex()
                for child_xml in omml_element
                if isinstance(child_xml, ET.Element)
            )
        else:
            # If the root is a single OMML element (e.g. <m:r>, <m:f>), process it directly
            # This path might be less common if pre_process.py always sends oMath
            omml_node = parse_omml_node(omml_element, parent=None)
            return omml_node.to_latex()

    except ET.ParseError:
        return "[OMML Parse Error]"
    except Exception:
        return "[OMML Conversion Error]"


def convert_omml_element_to_latex(omml_omath_element: ET.Element) -> str:
    """
    Converts an <m:oMath> ET.Element to its LaTeX representation.
    This is the primary entry point for the new conversion logic.
    """
    if omml_omath_element.tag != f"{OMML_NAMESPACE}oMath":
        # Consider logging: logging.warning(f"Expected <m:oMath> element, got {omml_omath_element.tag}")
        return "[Error: Not an oMath element]"

    latex_parts: List[str] = []
    for child_xml_element in omml_omath_element:
        if isinstance(
            child_xml_element, ET.Element
        ):  # Ensure it's an element, not comment/PI
            omml_node = parse_omml_node(
                child_xml_element, parent=None
            )  # Parent is the conceptual oMath
            latex_parts.append(omml_node.to_latex())

    return "".join(latex_parts)
