# -*- coding: utf-8 -*-
"""
Regression tests for the OMML delimiter (<m:d>) with several arguments.

`<m:e>` may repeat inside `<m:d>`, with `<m:sepChr>` naming the separator.
Previously only the last argument was kept and `sepChr` was never read.
"""

from xml.etree import ElementTree as ET

from markitdown.converter_utils.docx.math.omml import OMML_NS, oMath2Latex

MATH_NS_DECL = f'xmlns:m="{OMML_NS[1:-1]}"'


def _latex(xml_fragment: str) -> str:
    element = ET.fromstring(f"<m:oMath {MATH_NS_DECL}>{xml_fragment}</m:oMath>")
    return oMath2Latex(element).latex


def _r(text: str) -> str:
    return f"<m:r><m:t>{text}</m:t></m:r>"


def test_explicit_separator_keeps_every_argument():
    xml = (
        _r("f")
        + '<m:d><m:dPr><m:sepChr m:val=","/></m:dPr>'
        + f"<m:e>{_r('x')}</m:e><m:e>{_r('y')}</m:e></m:d>"
    )
    assert _latex(xml) == "f\\left(x,y\\right)"


def test_default_separator_is_vertical_bar():
    xml = (
        '<m:d><m:dPr><m:begChr m:val="{"/><m:endChr m:val="}"/></m:dPr>'
        f"<m:e>{_r('x')}</m:e><m:e>{_r('x>0')}</m:e></m:d>"
    )
    assert _latex(xml) == "\\left\\{x|x>0\\right\\}"


def test_three_arguments_with_semicolon():
    xml = (
        '<m:d><m:dPr><m:sepChr m:val=";"/></m:dPr>'
        f"<m:e>{_r('a')}</m:e><m:e>{_r('b')}</m:e><m:e>{_r('c')}</m:e></m:d>"
    )
    assert _latex(xml) == "\\left(a;b;c\\right)"


def test_empty_separator_means_no_separator():
    xml = (
        '<m:d><m:dPr><m:sepChr m:val=""/></m:dPr>'
        f"<m:e>{_r('a')}</m:e><m:e>{_r('b')}</m:e></m:d>"
    )
    assert _latex(xml) == "\\left(ab\\right)"


def test_single_argument_is_unchanged():
    xml = f"<m:d><m:dPr/><m:e>{_r('x')}</m:e></m:d>"
    assert _latex(xml) == "\\left(x\\right)"
