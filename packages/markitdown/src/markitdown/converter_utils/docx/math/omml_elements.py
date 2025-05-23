"""
Defines classes representing OMML (Office Math Markup Language) elements.
Each class is responsible for parsing its corresponding OMML XML element
and generating its LaTeX representation.
"""

from abc import ABC, abstractmethod
from xml.etree import ElementTree as ET
from typing import List, Optional

from .latex_symbols import OMML_NAMESPACE, escape_latex_text, UNICODE_TO_LATEX, OMML_FUNCTION_NAMES_TO_LATEX
from .omml_parser import parse_omml_node, register_omml_element


class OMMLElement(ABC):
    """Base class for all OMML element representations."""

    def __init__(self, xml_element: ET.Element, parent: Optional["OMMLElement"] = None):
        self.xml_element = xml_element
        self.parent = parent
        self.children: List[OMMLElement] = []
        self._parse_properties()
        self._parse_children()

    def _parse_properties(self):
        """Parses common properties from the XML element. Subclasses can override."""
        pass

    def _parse_children(self):
        """
        Parses child XML elements and creates corresponding OMMLElement objects.
        """
        self.children = []
        for child_xml in self.xml_element:
            if isinstance(child_xml, ET.Element):
                self.children.append(parse_omml_node(child_xml, self))

    @abstractmethod
    def to_latex(self) -> str:
        """Converts the OMML element to its LaTeX string representation."""
        pass

    def _children_to_latex(self) -> str:
        """Helper method to convert all child elements to LaTeX and join them."""
        return "".join(child.to_latex() for child in self.children)

    def _get_element_text(self, element: Optional[ET.Element]) -> str:
        """Safely gets the text content of an XML element."""
        if element is not None and element.text:
            return element.text
        return ""

    def _get_child_element(self, tag_name: str) -> Optional[ET.Element]:
        """Finds a direct child element by its tag name (without namespace)."""
        return self.xml_element.find(f"{OMML_NAMESPACE}{tag_name}")


class GenericOMMLElement(OMMLElement):
    """A generic fallback for OMML elements not specifically handled."""

    def to_latex(self) -> str:
        """For generic elements, just try to convert their children."""
        return self._children_to_latex()


@register_omml_element("r")
class OMMLRun(OMMLElement):
    """Represents a run of text (<m:r>) within an OMML equation."""

    def __init__(self, xml_element: ET.Element, parent: Optional[OMMLElement] = None):
        self.text_content: str = ""
        self.is_bold: bool = False
        self.is_italic: bool = False
        self.is_script: bool = False
        self.is_fraktur: bool = False
        self.is_plain: bool = False
        super().__init__(xml_element, parent)

    def _parse_properties(self):
        super()._parse_properties()
        self.is_bold = False
        self.is_italic = False
        self.is_script = False
        self.is_fraktur = False
        self.is_plain = False

        rpr_element = self._get_child_element("rPr")
        if rpr_element is not None:
            sty_tag = rpr_element.find(f"{OMML_NAMESPACE}sty")
            sty_val: Optional[str] = None
            if sty_tag is not None:
                sty_val = sty_tag.get(f"{OMML_NAMESPACE}val") or sty_tag.get("val")

            if sty_val:
                if sty_val == "p":
                    self.is_plain = True
                elif sty_val == "b":
                    self.is_bold = True
                elif sty_val == "i":
                    self.is_italic = True
                elif sty_val == "bi":
                    self.is_bold = True
                    self.is_italic = True
                elif sty_val == "sc":
                    self.is_script = True
                elif sty_val == "fr":
                    self.is_fraktur = True

            if sty_val == "nor" or sty_val is None or sty_val == "p":
                if not self.is_script and rpr_element.find(f"{OMML_NAMESPACE}scr") is not None:
                    self.is_script = True
                if not self.is_fraktur and rpr_element.find(f"{OMML_NAMESPACE}frak") is not None:
                    self.is_fraktur = True

                if not self.is_script and not self.is_fraktur:
                    b_tag = rpr_element.find(f"{OMML_NAMESPACE}b")
                    if b_tag is not None:
                        b_val_attr = b_tag.get(f"{OMML_NAMESPACE}val", "on")
                        if b_val_attr not in ["0", "off"]:
                            self.is_bold = True

                    i_tag = rpr_element.find(f"{OMML_NAMESPACE}i")
                    if i_tag is not None:
                        i_val_attr = i_tag.get(f"{OMML_NAMESPACE}val", "on")
                        if i_val_attr not in ["0", "off"]:
                            self.is_italic = True

        t_element = self._get_child_element("t")
        raw_text = self._get_element_text(t_element)

        processed_text = []
        for char_val in raw_text:
            char_code = ord(char_val)
            if char_code in UNICODE_TO_LATEX:
                processed_text.append(UNICODE_TO_LATEX[char_code])
                if UNICODE_TO_LATEX[char_code].startswith("\\\\"):
                    processed_text.append(" ")
            else:
                processed_text.append(char_val)
        self.text_content = "".join(processed_text)

    def _parse_children(self):
        """OMMLRun elements do not have further OMMLElement children."""
        self.children = []

    def to_latex(self) -> str:
        latex_str = escape_latex_text(self.text_content)

        if self.is_script:
            return f"\\\\mathscr{{{latex_str}}}"
        elif self.is_fraktur:
            return f"\\\\mathfrak{{{latex_str}}}"
        else:
            processed_text = latex_str

            if self.is_plain:
                text_to_check = latex_str.strip()
                if text_to_check.isalpha() and len(text_to_check) > 1:
                    processed_text = f"\\\\mathrm{{{latex_str}}}"

            if self.is_italic:
                processed_text = f"\\\\textit{{{processed_text}}}"
            if self.is_bold:
                processed_text = f"\\\\mathbf{{{processed_text}}}"

            return processed_text


@register_omml_element("f")
class OMMLFraction(OMMLElement):
    """Represents a fraction (<m:f>)."""

    def __init__(self, xml_element: ET.Element, parent: Optional[OMMLElement] = None):
        self.numerator_element: Optional[OMMLElement] = None
        self.denominator_element: Optional[OMMLElement] = None
        self.fraction_type: Optional[str] = None
        super().__init__(xml_element, parent)

    def _parse_properties(self):
        super()._parse_properties()
        f_pr_element = self._get_child_element("fPr")
        if f_pr_element is not None:
            type_element = f_pr_element.find(f".//{OMML_NAMESPACE}type")
            if type_element is not None:
                val_attr = type_element.get(f"{OMML_NAMESPACE}val")
                if val_attr is None:
                    val_attr = type_element.get("val")
                self.fraction_type = val_attr

    def _parse_children(self):
        super()._parse_children()
        num_container: Optional[OMMLElement] = None
        den_container: Optional[OMMLElement] = None
        for child_omml_element in self.children:
            child_xml_tag_local = child_omml_element.xml_element.tag.replace(
                OMML_NAMESPACE, ""
            )
            if child_xml_tag_local == "num":
                num_container = child_omml_element
            elif child_xml_tag_local == "den":
                den_container = child_omml_element
        if num_container and num_container.children:
            self.numerator_element = num_container.children[0]
        if den_container and den_container.children:
            self.denominator_element = den_container.children[0]

    def to_latex(self) -> str:
        if not self.numerator_element or not self.denominator_element:
            return "{ERROR: Incomplete Fraction}"
        num_latex = self.numerator_element.to_latex()
        den_latex = self.denominator_element.to_latex()
        frac_command = "\\\\frac"
        if self.fraction_type == "skw":
            return f"{{{num_latex}}}/{{{den_latex}}}"
        elif self.fraction_type == "lin":
            return f"{{{num_latex}}} \\\\\\\\over {{{den_latex}}}"
        elif self.fraction_type == "noBar":
            frac_command = "\\\\binom"
        return f"{frac_command}{{{num_latex}}}{{{den_latex}}}"


class OMMLScript(OMMLElement):
    """Handles script elements like superscript, subscript, and sub-superscript."""

    def __init__(self, xml_element: ET.Element, parent: Optional[OMMLElement] = None):
        super().__init__(xml_element, parent)
        self.base_element: OMMLElement | None = None
        self.sub_script_element: OMMLElement | None = None
        self.super_script_element: OMMLElement | None = None
        self._parse_specific_script_children()

    def _parse_specific_script_children(self):
        children_count = len(self.children)
        if children_count == 0:
            return

        base_container = self.children[0]
        if base_container and base_container.children:
            self.base_element = base_container.children[0]
        elif base_container:
            self.base_element = base_container

        tag_name = self.xml_element.tag.replace(OMML_NAMESPACE, "")

        if tag_name == "sSub":
            if children_count >= 2:
                sub_container = self.children[1]
                if sub_container and sub_container.children:
                    self.sub_script_element = sub_container.children[0]
                elif sub_container:
                    self.sub_script_element = sub_container
        elif tag_name == "sSup":
            if children_count >= 2:
                sup_container = self.children[1]
                if sup_container and sup_container.children:
                    self.super_script_element = sup_container.children[0]
                elif sup_container:
                    self.super_script_element = sup_container
        elif tag_name == "sSubSup":
            if children_count >= 2:
                sub_container = self.children[1]
                if sub_container and sub_container.children:
                    self.sub_script_element = sub_container.children[0]
                elif sub_container:
                    self.sub_script_element = sub_container
            if children_count >= 3:
                sup_container = self.children[2]
                if sup_container and sup_container.children:
                    self.super_script_element = sup_container.children[0]
                elif sup_container:
                    self.super_script_element = sup_container

    def to_latex(self) -> str:
        base_latex = self.base_element.to_latex() if self.base_element else "{}"

        if self.sub_script_element and self.super_script_element:
            sub_latex = self.sub_script_element.to_latex()
            sup_latex = self.super_script_element.to_latex()
            return f"{{{base_latex}}}_{{{sub_latex}}}^{{{sup_latex}}}"
        elif self.sub_script_element:
            sub_latex = self.sub_script_element.to_latex()
            return f"{{{base_latex}}}_{{{sub_latex}}}"
        elif self.super_script_element:
            sup_latex = self.super_script_element.to_latex()
            return f"{{{base_latex}}}^{{{sup_latex}}}"
        else:
            return base_latex


@register_omml_element("sSub")
class OMMLSubscript(OMMLScript):
    pass


@register_omml_element("sSup")
class OMMLSuperscript(OMMLScript):
    pass


@register_omml_element("sSubSup")
class OMMLSubSuperscript(OMMLScript):
    pass


@register_omml_element("rad")
class OMMLRadical(OMMLElement):
    """Handles radical elements like square roots."""

    def __init__(self, xml_element: ET.Element, parent: Optional[OMMLElement] = None):
        super().__init__(xml_element, parent)
        self.base_element: OMMLElement | None = None
        self.degree_element: OMMLElement | None = None
        self.hide_degree: bool = False
        self._parse_specific_radical_children()
        self._parse_radical_properties()

    def _parse_radical_properties(self):
        rad_pr_element = self._get_child_element("radPr")
        if rad_pr_element is not None:
            deg_hide_element = rad_pr_element.find(f"{OMML_NAMESPACE}degHide")
            if deg_hide_element is not None:
                val = deg_hide_element.get(f"{OMML_NAMESPACE}val")
                if val in ("on", "1"):
                    self.hide_degree = True

    def _parse_specific_radical_children(self):
        deg_container: Optional[OMMLElement] = None
        base_container: Optional[OMMLElement] = None
        for child_wrapper in self.children:
            child_tag_local = child_wrapper.xml_element.tag.replace(OMML_NAMESPACE, "")
            if child_tag_local == "e":
                base_container = child_wrapper
            elif child_tag_local == "deg":
                deg_container = child_wrapper
        if base_container and base_container.children:
            self.base_element = base_container.children[0]
        elif base_container:
            self.base_element = base_container
        if deg_container and deg_container.children:
            self.degree_element = deg_container.children[0]
        elif deg_container:
            self.degree_element = deg_container

    def to_latex(self) -> str:
        if not self.base_element:
            return "{ERROR: Incomplete Radical}"
        base_latex = self.base_element.to_latex()
        if self.degree_element and not self.hide_degree:
            degree_latex = self.degree_element.to_latex()
            if degree_latex.strip() == "2":
                return f"\\\\sqrt{{{base_latex}}}"
            return f"\\\\sqrt[{degree_latex}]{{{base_latex}}}"
        else:
            return f"\\\\sqrt{{{base_latex}}}"


@register_omml_element("d")
class OMMLDelimiter(OMMLElement):
    """Handles delimiter elements like parentheses, brackets, etc."""

    def __init__(self, xml_element: ET.Element, parent: Optional[OMMLElement] = None):
        super().__init__(xml_element, parent)
        self.beg_char: Optional[str] = None
        self.end_char: Optional[str] = None
        self.sep_char: Optional[str] = None
        self.grow: bool = False
        self._parse_delimiter_properties()

    def _parse_delimiter_properties(self):
        d_pr_element = self._get_child_element("dPr")
        if d_pr_element is not None:
            beg_chr_el = d_pr_element.find(f"{OMML_NAMESPACE}begChr")
            if beg_chr_el is not None:
                self.beg_char = beg_chr_el.get(f"{OMML_NAMESPACE}val")
            end_chr_el = d_pr_element.find(f"{OMML_NAMESPACE}endChr")
            if end_chr_el is not None:
                self.end_char = end_chr_el.get(f"{OMML_NAMESPACE}val")
            sep_chr_el = d_pr_element.find(f"{OMML_NAMESPACE}sepChr")
            if sep_chr_el is not None:
                self.sep_char = sep_chr_el.get(f"{OMML_NAMESPACE}val")
            grow_el = d_pr_element.find(f"{OMML_NAMESPACE}grow")
            if grow_el is not None:
                val = grow_el.get(f"{OMML_NAMESPACE}val")
                self.grow = val in ("1", "on")

        if self.beg_char is None:
            self.beg_char = self.xml_element.get(f"{OMML_NAMESPACE}begChr")
        if self.end_char is None:
            self.end_char = self.xml_element.get(f"{OMML_NAMESPACE}endChr")

        if self.beg_char is None:
            self.beg_char = "("
        if self.end_char is None:
            self.end_char = ")"

    def to_latex(self) -> str:
        from .latex_symbols import DELIMITER_MAP

        content_parts = []
        current_segment_elements = []
        for child_element_wrapper in self.children:
            if child_element_wrapper.xml_element.tag == f"{OMML_NAMESPACE}sep":
                content_parts.append("".join(el.to_latex() for el in current_segment_elements))
                current_segment_elements = []
            else:
                if child_element_wrapper.xml_element.tag == f"{OMML_NAMESPACE}e" and child_element_wrapper.children:
                    current_segment_elements.append(child_element_wrapper.children[0])
                elif child_element_wrapper.xml_element.tag != f"{OMML_NAMESPACE}sep":
                    current_segment_elements.append(child_element_wrapper)

        content_parts.append("".join(el.to_latex() for el in current_segment_elements))

        separator_latex = escape_latex_text(self.sep_char) if self.sep_char else ", "

        if len(content_parts) <= 1:
            content_latex = content_parts[0] if content_parts else ""
        else:
            content_latex = separator_latex.join(content_parts)

        bc = self.beg_char if self.beg_char is not None else "("
        ec = self.end_char if self.end_char is not None else ")"

        open_delim = DELIMITER_MAP.get(bc, escape_latex_text(bc))
        close_delim = DELIMITER_MAP.get(ec, escape_latex_text(ec))

        if self.grow:
            open_latex = f"\\\\left{open_delim if open_delim else '.'}"
            close_latex = f"\\\\right{close_delim if close_delim else '.'}"
            return f"{{{open_latex}{content_latex}{close_latex}}}"
        else:
            return f"{{{open_delim}{content_latex}{close_delim}}}"


@register_omml_element("func")
class OMMLFunction(OMMLElement):
    """Represents an OMML function element (<m:func>)."""

    def __init__(self, xml_element: ET.Element, parent: Optional[OMMLElement] = None):
        self.function_name_element: Optional[OMMLElement] = None
        self.argument_elements: List[OMMLElement] = []
        super().__init__(xml_element, parent)

    def _parse_properties(self):
        super()._parse_properties()
        # func_pr_element = self._get_child_element("funcPr")
        # if func_pr_element:
        #     pass

    def _parse_children(self):
        super()._parse_children()

        for child_omml_obj in self.children:
            child_xml_tag_local = child_omml_obj.xml_element.tag.replace(OMML_NAMESPACE, "")

            if child_xml_tag_local == "fName":
                if child_omml_obj.children:
                    self.function_name_element = child_omml_obj.children[0]
            elif child_xml_tag_local == "e":
                if child_omml_obj.children:
                    self.argument_elements.append(child_omml_obj.children[0])

    def to_latex(self) -> str:
        if not self.function_name_element:
            args_only_latex = "".join(arg.to_latex() for arg in self.argument_elements)
            return f"{{ERROR: Missing function name; args: {args_only_latex}}}" if args_only_latex else "{ERROR: Missing function name}"

        func_name_str = self.function_name_element.to_latex().strip()

        if func_name_str in OMML_FUNCTION_NAMES_TO_LATEX:
            latex_func_name = OMML_FUNCTION_NAMES_TO_LATEX[func_name_str]
        elif func_name_str.startswith("\\\\") and "operatorname" not in func_name_str:
            latex_func_name = func_name_str
        else:
            latex_func_name = f"\\\\operatorname{{{func_name_str}}}"

        args_latex = [arg.to_latex() for arg in self.argument_elements]

        if not args_latex:
            return latex_func_name

        if latex_func_name == "\\\\lim" and len(args_latex) == 1:
            return f"{latex_func_name}_{{{args_latex[0]}}}"

        return f"{latex_func_name}({', '.join(args_latex)})"


@register_omml_element("nary")
class OMMLNAry(OMMLElement):
    """Represents an N-ary operator like summation or integration (<m:nary>)."""

    def __init__(self, xml_element: ET.Element, parent: Optional[OMMLElement] = None):
        self.nary_char: Optional[str] = None
        self.sub_script_element: Optional[OMMLElement] = None
        self.super_script_element: Optional[OMMLElement] = None
        self.base_element: Optional[OMMLElement] = None
        self.nary_pr_props: dict = {}
        super().__init__(xml_element, parent)

    def _parse_properties(self):
        super()._parse_properties()
        nary_pr_element = self._get_child_element("naryPr")
        if nary_pr_element is not None:
            chr_element = nary_pr_element.find(f" .//{OMML_NAMESPACE}chr")
            if chr_element is not None:
                val_attr = chr_element.get(f"{OMML_NAMESPACE}val")
                if val_attr is None:
                    val_attr = chr_element.get("val")
                self.nary_char = val_attr

            for child_prop in nary_pr_element:
                prop_tag = child_prop.tag.replace(OMML_NAMESPACE, "")
                val = child_prop.get(f"{OMML_NAMESPACE}val")
                if val is None:
                    val = child_prop.get("val")
                if val is not None:
                    self.nary_pr_props[prop_tag] = val

    def _parse_children(self):
        super()._parse_children()

        for child_wrapper_omml_obj in self.children:
            child_wrapper_tag_local = child_wrapper_omml_obj.xml_element.tag.replace(OMML_NAMESPACE, "")

            if child_wrapper_tag_local == "sub":
                if child_wrapper_omml_obj.children:
                    self.sub_script_element = child_wrapper_omml_obj.children[0]
            elif child_wrapper_tag_local == "sup":
                if child_wrapper_omml_obj.children:
                    self.super_script_element = child_wrapper_omml_obj.children[0]
            elif child_wrapper_tag_local == "e":
                if child_wrapper_omml_obj.children:
                    self.base_element = child_wrapper_omml_obj.children[0]

    def to_latex(self) -> str:
        if not self.base_element:
            return "{ERROR: N-ary operator missing base element}"

        base_latex = self.base_element.to_latex()
        op_char_latex = ""

        if self.nary_char:
            if len(self.nary_char) == 1 and ord(self.nary_char) in UNICODE_TO_LATEX:
                op_char_latex = UNICODE_TO_LATEX[ord(self.nary_char)]
            else:
                op_char_latex = escape_latex_text(self.nary_char)
        else:
            op_char_latex = "\\\\sum"  # Default if char is missing

        sub_latex_content = self.sub_script_element.to_latex() if self.sub_script_element else ""
        sup_latex_content = self.super_script_element.to_latex() if self.super_script_element else ""

        limits_location = self.nary_pr_props.get("limsLoc")
        # Check for char or unicode escape for integral
        is_integral_char = self.nary_char == "\\u222B" or self.nary_char == "∫"

        operator_part = op_char_latex
        scripts_part = ""

        if limits_location == "undOvr":
            if is_integral_char:
                operator_part += "\\\\limits"
            if sub_latex_content:
                scripts_part += f"_{{{sub_latex_content}}}"
            if sup_latex_content:
                scripts_part += f"^{{{sup_latex_content}}}"
            return f"{operator_part}{scripts_part} {base_latex}"
        elif limits_location == "subSup":
            if sub_latex_content:
                scripts_part += f"_{{{sub_latex_content}}}"
            if sup_latex_content:
                scripts_part += f"^{{{sup_latex_content}}}"
            return f"{operator_part}{scripts_part} {base_latex}"
        else:  # Default behavior
            if is_integral_char:  # Integrals default to sub/sup
                if sub_latex_content:
                    scripts_part += f"_{{{sub_latex_content}}}"
                if sup_latex_content:
                    scripts_part += f"^{{{sup_latex_content}}}"
            else:  # Other N-ary operators (like sum, prod) default to undOvr in display style
                if sub_latex_content:
                    scripts_part += f"_{{{sub_latex_content}}}"
                if sup_latex_content:
                    scripts_part += f"^{{{sup_latex_content}}}"
            return f"{operator_part}{scripts_part} {base_latex}"


@register_omml_element("m")
class OMMLMatrix(OMMLElement):
    """Represents a matrix (<m:m>)."""

    def __init__(self, xml_element: ET.Element, parent: Optional[OMMLElement] = None):
        self.rows: List[List[OMMLElement]] = []
        self.matrix_pr_props: dict = {}
        super().__init__(xml_element, parent)

    def _parse_properties(self):
        super()._parse_properties()
        m_pr_element = self._get_child_element("mPr")
        if m_pr_element is not None:
            for child_prop in m_pr_element:
                prop_tag = child_prop.tag.replace(OMML_NAMESPACE, "")
                val = child_prop.get(f"{OMML_NAMESPACE}val")
                if val is None:
                    val = child_prop.get("val")
                if val is not None:
                    self.matrix_pr_props[prop_tag] = val

    def _parse_children(self):
        super()._parse_children()

        for child_omml_obj in self.children:
            child_xml_tag_local = child_omml_obj.xml_element.tag.replace(OMML_NAMESPACE, "")
            if child_xml_tag_local == "mr":  # OMMLMatrixRow
                current_row_elements: List[OMMLElement] = []
                for e_wrapper_in_mr in child_omml_obj.children:  # <m:e> wrappers
                    if e_wrapper_in_mr.children:  # Actual content within <m:e>
                        current_row_elements.append(e_wrapper_in_mr.children[0])
                if current_row_elements:
                    self.rows.append(current_row_elements)

    def to_latex(self) -> str:
        if not self.rows:
            return ""

        matrix_env = "matrix"  # Default
        if isinstance(self.parent, OMMLDelimiter):
            beg_char = self.parent.beg_char if self.parent.beg_char is not None else ""
            end_char = self.parent.end_char if self.parent.end_char is not None else ""

            if beg_char == '(' and end_char == ')':
                matrix_env = "pmatrix"
            elif beg_char == '[' and end_char == ']':
                matrix_env = "bmatrix"
            elif beg_char == '{' and end_char == '}':
                matrix_env = "Bmatrix"
            elif beg_char == '|' and end_char == '|':
                if self.parent.xml_element.find(f".//{OMML_NAMESPACE}sepChr") is None:
                    matrix_env = "vmatrix"
                else:
                    matrix_env = "Vmatrix"

        rows_latex = []
        for row_elements in self.rows:
            row_latex = " & ".join(el.to_latex() for el in row_elements)
            rows_latex.append(row_latex)

        matrix_content = " \\\\\\\\ \\\\n".join(rows_latex)
        return f"\\\\begin{{{matrix_env}}}\\n{matrix_content}\\n\\\\end{{{matrix_env}}}"


@register_omml_element("mr")
class OMMLMatrixRow(OMMLElement):
    """Represents a matrix row (<m:mr>). Its children are <m:e> elements."""
    def to_latex(self) -> str:
        # This class is a container; LaTeX is generated by OMMLMatrix.
        return " & ".join(child.to_latex() for child in self.children)


@register_omml_element("acc")
class OMMLAccent(OMMLElement):
    """Represents an accent character (<m:acc>)."""
    def __init__(self, xml_element: ET.Element, parent: Optional[OMMLElement] = None):
        self.accent_char: Optional[str] = None
        self.base_element: Optional[OMMLElement] = None
        super().__init__(xml_element, parent)

    def _parse_properties(self):
        super()._parse_properties()
        acc_pr_element = self._get_child_element("accPr")
        if acc_pr_element is not None:
            chr_element = acc_pr_element.find(f".//{OMML_NAMESPACE}chr")
            if chr_element is not None:
                val_attr = chr_element.get(f"{OMML_NAMESPACE}val")
                if val_attr is None:
                    val_attr = chr_element.get("val")
                self.accent_char = val_attr

    def _parse_children(self):
        super()._parse_children()  # Populates self.children with <m:e> wrapper
        if self.children:  # Should be one <m:e> element
            e_wrapper = self.children[0]
            if e_wrapper.children:  # The actual base element
                self.base_element = e_wrapper.children[0]

    def to_latex(self) -> str:
        from .latex_symbols import ACCENT_CHAR_TO_LATEX
        if not self.base_element or not self.accent_char:
            return self.base_element.to_latex() if self.base_element else "{ERROR: Accent missing base or char}"

        base_latex = self.base_element.to_latex()

        if len(self.accent_char) == 1 and self.accent_char in ACCENT_CHAR_TO_LATEX:
            accent_command_template = ACCENT_CHAR_TO_LATEX[self.accent_char]
        elif self.accent_char.upper() in ACCENT_CHAR_TO_LATEX:  # Hex string
            accent_command_template = ACCENT_CHAR_TO_LATEX[self.accent_char.upper()]
        else:
            simple_accents = {
                "^": "\\\\hat{{{0}}}", "~": "\\\\tilde{{{0}}}", "-": "\\\\bar{{{0}}}",
                "\\u00AF": "\\\\bar{{{0}}}",  # Macron
                "\\u2192": "\\\\vec{{{0}}}",  # Right arrow for vector
                ".": "\\\\dot{{{0}}}", "..": "\\\\ddot{{{0}}}",
                "'": "\\\\acute{{{0}}}", "`": "\\\\grave{{{0}}}",
                "\\u02D8": "\\\\breve{{{0}}}",  # Breve
                "\\u02C7": "\\\\check{{{0}}}"  # Caron / Check
            }
            if self.accent_char in simple_accents:
                accent_command_template = simple_accents[self.accent_char]
            else:
                # print(f"Warning: Unknown accent character \'{self.accent_char}\'")
                return f"\\\\text{{Accent?}}{{{base_latex}}}"

        if "{0}" in accent_command_template:
            return accent_command_template.format(base_latex)
        else:
            return f"{accent_command_template}{{{base_latex}}}"


@register_omml_element("bar")
class OMMLBar(OMMLElement):
    """Represents a bar over or under an element (<m:bar>)."""
    def __init__(self, xml_element: ET.Element, parent: Optional[OMMLElement] = None):
        self.base_element: Optional[OMMLElement] = None
        self.position: str = "top"  # Default to overbar
        super().__init__(xml_element, parent)

    def _parse_properties(self):
        super()._parse_properties()
        bar_pr_element = self._get_child_element("barPr")
        if bar_pr_element is not None:
            pos_element = bar_pr_element.find(f".//{OMML_NAMESPACE}pos")
            if pos_element is not None:
                val_attr = pos_element.get(f"{OMML_NAMESPACE}val")
                if val_attr is None:
                    val_attr = pos_element.get("val")
                if val_attr == "bot":
                    self.position = "bottom"

    def _parse_children(self):
        super()._parse_children()
        if self.children:  # Should be one <m:e> element
            e_wrapper = self.children[0]
            if e_wrapper.children:
                self.base_element = e_wrapper.children[0]

    def to_latex(self) -> str:
        if not self.base_element:
            return "{ERROR: Bar missing base element}"
        base_latex = self.base_element.to_latex()
        if self.position == "bottom":
            return f"\\\\underline{{{base_latex}}}"
        else:  # Default to top
            return f"\\\\overline{{{base_latex}}}"


@register_omml_element("box")
class OMMLBox(OMMLElement):
    """Represents a boxed element (<m:box>)."""
    def __init__(self, xml_element: ET.Element, parent: Optional[OMMLElement] = None):
        self.base_element: Optional[OMMLElement] = None
        super().__init__(xml_element, parent)

    def _parse_children(self):
        super()._parse_children()
        if self.children:  # Should be one <m:e> element
            e_wrapper = self.children[0]
            if e_wrapper.children:
                self.base_element = e_wrapper.children[0]

    def to_latex(self) -> str:
        if not self.base_element:
            return "{ERROR: Box missing base element}"
        base_latex = self.base_element.to_latex()
        return f"\\\\boxed{{{base_latex}}}"  # Requires amsmath


@register_omml_element("groupChr")
class OMMLGroupChar(OMMLElement):
    """Represents a grouping character (e.g., top/bottom brace) (<m:groupChr>)."""
    def __init__(self, xml_element: ET.Element, parent: Optional[OMMLElement] = None):
        self.base_element: Optional[OMMLElement] = None
        self.char: Optional[str] = None
        self.pos: Optional[str] = None  # top or bot
        self.vert_just: Optional[str] = None
        super().__init__(xml_element, parent)

    def _parse_properties(self):
        super()._parse_properties()
        gc_pr_element = self._get_child_element("groupChrPr")
        if gc_pr_element is not None:
            chr_element = gc_pr_element.find(f".//{OMML_NAMESPACE}chr")
            if chr_element is not None:
                self.char = chr_element.get(f"{OMML_NAMESPACE}val") or chr_element.get("val")
            pos_element = gc_pr_element.find(f".//{OMML_NAMESPACE}pos")
            if pos_element is not None:
                self.pos = pos_element.get(f"{OMML_NAMESPACE}val") or pos_element.get("val")
            vert_just_element = gc_pr_element.find(f".//{OMML_NAMESPACE}vertJc")
            if vert_just_element is not None:
                self.vert_just = vert_just_element.get(f"{OMML_NAMESPACE}val") or vert_just_element.get("val")

    def _parse_children(self):
        super()._parse_children()
        if self.children:  # Should be one <m:e> element
            e_wrapper = self.children[0]
            if e_wrapper.children:
                self.base_element = e_wrapper.children[0]

    def to_latex(self) -> str:
        if not self.base_element or not self.char:
            return self.base_element.to_latex() if self.base_element else "{ERROR: GroupChar missing base or char}"

        base_latex = self.base_element.to_latex()
        command = None
        # Common chars: { (U+007B), } (U+007D), [ (U+005B), ] (U+005D)
        # Word might use specific grouping characters like U+23DE (Top Curly Bracket)
        if self.char == "{" or self.char == "\\u007B" or self.char == "\\u23DE":  # Top brace
            command = "\\\\overbrace" if self.pos == "top" else "\\\\underbrace"
        elif self.char == "[" or self.char == "\\u005B":
            # No standard LaTeX for over/under bracket
            pass

        if command:
            return f"{command}{{{base_latex}}}"
        else:
            return base_latex


@register_omml_element("limLow")
class OMMLLimLow(OMMLElement):
    """Represents a lower limit (<m:limLow>)."""
    def __init__(self, xml_element: ET.Element, parent: Optional[OMMLElement] = None):
        self.base_element: Optional[OMMLElement] = None
        self.limit_element: Optional[OMMLElement] = None
        super().__init__(xml_element, parent)

    def _parse_children(self):
        """Expects two <m:e> children: first is base, second is limit."""
        super()._parse_children()
        if len(self.children) >= 2:
            e1_wrapper = self.children[0]
            e2_wrapper = self.children[1]
            if e1_wrapper and e1_wrapper.children:
                self.base_element = e1_wrapper.children[0]
            if e2_wrapper and e2_wrapper.children:
                self.limit_element = e2_wrapper.children[0]
        elif len(self.children) == 1 and self.xml_element.tag.replace(OMML_NAMESPACE, "") == "lim":  # Check if it's an <m:lim> tag
            # This case is typically handled by OMMLFunction for \\lim_{sub}
            pass

    def to_latex(self) -> str:
        if not self.base_element or not self.limit_element:
            return (self.base_element.to_latex() if self.base_element else "") + \
                   (self.limit_element.to_latex() if self.limit_element else "{ERROR: LimLow incomplete}")

        base_latex = self.base_element.to_latex()
        limit_latex = self.limit_element.to_latex()
        return f"{{{base_latex}}}_{{{limit_latex}}}"


@register_omml_element("limUpp")
class OMMLLimUpp(OMMLElement):
    """Represents an upper limit (<m:limUpp>)."""
    def __init__(self, xml_element: ET.Element, parent: Optional[OMMLElement] = None):
        self.base_element: Optional[OMMLElement] = None
        self.limit_element: Optional[OMMLElement] = None
        super().__init__(xml_element, parent)

    def _parse_children(self):
        """Expects two <m:e> children: first is base, second is limit."""
        super()._parse_children()
        if len(self.children) >= 2:
            e1_wrapper = self.children[0]
            e2_wrapper = self.children[1]
            if e1_wrapper and e1_wrapper.children:
                self.base_element = e1_wrapper.children[0]
            if e2_wrapper and e2_wrapper.children:
                self.limit_element = e2_wrapper.children[0]
        elif len(self.children) == 1 and self.xml_element.tag.replace(OMML_NAMESPACE, "") == "lim":  # Check if it's an <m:lim> tag
            if self.children[0].children:
                self.limit_element = self.children[0].children[0]

    def to_latex(self) -> str:
        if not self.base_element or not self.limit_element:
            if self.limit_element and not self.base_element:
                return f"^{{{self.limit_element.to_latex()}}}"  # Render as superscript if base is missing
            return (self.base_element.to_latex() if self.base_element else "") + \
                   (self.limit_element.to_latex() if self.limit_element else "{ERROR: LimUpp incomplete}")

        base_latex = self.base_element.to_latex()
        limit_latex = self.limit_element.to_latex()
        return f"{{{base_latex}}}^{{{limit_latex}}}"


@register_omml_element("eqArr")
class OMMLEqArr(OMMLElement):
    """Represents an equation array (<m:eqArr>)."""
    def __init__(self, xml_element: ET.Element, parent: Optional[OMMLElement] = None):
        self.elements_in_rows: List[List[OMMLElement]] = []
        super().__init__(xml_element, parent)

    def _parse_children(self):
        super()._parse_children()  # Populates self.children with <m:e> wrappers

        current_row: List[OMMLElement] = []
        for e_wrapper_omml_obj in self.children:
            if e_wrapper_omml_obj.children:
                current_row.append(e_wrapper_omml_obj)  # Store the <m:e> wrapper
                self.elements_in_rows.append(current_row)
                current_row = []  # Start a new row

    def to_latex(self) -> str:
        if not self.elements_in_rows:
            return ""

        lines_latex = []
        for row_list in self.elements_in_rows:
            line_content_latex = "".join(e_wrapper.to_latex() for e_wrapper in row_list)
            lines_latex.append(line_content_latex)

        parent_is_cases_like = False
        if isinstance(self.parent, OMMLDelimiter):
            delim_parent = self.parent
            if delim_parent.xml_element.tag == f"{OMML_NAMESPACE}d":  # Ensure it's the direct parent 'd'
                dpr = delim_parent._get_child_element("dPr")
                if dpr:
                    beg_el = dpr.find(f"{OMML_NAMESPACE}begChr")
                    end_el = dpr.find(f"{OMML_NAMESPACE}endChr")
                    beg_val = beg_el.get(f"{OMML_NAMESPACE}val") if beg_el is not None else None
                    end_val = end_el.get(f"{OMML_NAMESPACE}val") if end_el is not None else None
                    if beg_val == "{" and (end_val is None or end_val.strip() == ""):
                        parent_is_cases_like = True

        if parent_is_cases_like:
            array_content = " \\\\\\\\ \\\\n".join(lines_latex)
            return f"\\\\begin{{cases}}\\n{array_content}\\n\\\\end{{cases}}"
        else:
            array_content = " \\\\\\\\ \\\\n".join(lines_latex)
            return f"\\\\begin{{align}}\\n{array_content}\\n\\\\end{{align}}"
