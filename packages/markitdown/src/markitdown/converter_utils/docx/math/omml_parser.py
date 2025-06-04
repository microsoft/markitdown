"""
OMML (Office Math Markup Language) Parser.

This module provides the core parsing functionality to convert OMML XML nodes
into a structured tree of `OMMLElement` objects. It uses a decorator-based
registration system to map OMML tags to their corresponding Python classes.
"""

from xml.etree import ElementTree as ET
from typing import Dict, Type, TYPE_CHECKING, Optional

from .latex_symbols import OMML_NAMESPACE

if TYPE_CHECKING:
    from .omml_elements import OMMLElement

# Global registry mapping OMML tag names (local names) to OMMLElement subclasses.
TAG_TO_CLASS_MAP: Dict[str, Type["OMMLElement"]] = {}


def register_omml_element(tag_name: str):
    """
    Decorator to register an OMMLElement subclass for a specific OMML tag.

    Args:
        tag_name: The local name of the OMML tag (e.g., "r", "f", "sSup").
    """

    def decorator(element_class: Type["OMMLElement"]) -> Type["OMMLElement"]:
        if tag_name in TAG_TO_CLASS_MAP:
            pass
        TAG_TO_CLASS_MAP[tag_name] = element_class
        return element_class

    return decorator


def parse_omml_node(
    xml_node: ET.Element, parent: Optional["OMMLElement"] = None
) -> "OMMLElement":
    """
    Parses a single XML element and returns an instance of the corresponding
    OMMLElement subclass.

    If the tag is not specifically registered, it defaults to `GenericOMMLElement`.
    If the element is not in the OMML namespace, it also defaults to `GenericOMMLElement`.

    Args:
        xml_node: The `xml.etree.ElementTree.Element` to parse.
        parent: The parent `OMMLElement` in the tree, if any.

    Returns:
        An instance of an `OMMLElement` subclass.
    """
    # Import GenericOMMLElement here to avoid circular dependencies at module load time,
    # as omml_elements might import from omml_parser (e.g., for parse_omml_node itself).
    from .omml_elements import GenericOMMLElement

    if not isinstance(xml_node, ET.Element) or not xml_node.tag.startswith(OMML_NAMESPACE):
        # Handles non-element nodes (e.g. comments, PIs if they were to appear)
        # or elements not in the OMML namespace.
        return GenericOMMLElement(xml_node, parent)

    tag_local_name = xml_node.tag.replace(OMML_NAMESPACE, "")
    element_class = TAG_TO_CLASS_MAP.get(tag_local_name)

    if element_class:
        return element_class(xml_node, parent)
    else:
        return GenericOMMLElement(xml_node, parent)
