import zipfile
from io import BytesIO
from typing import BinaryIO, Callable, Optional
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup, Tag

from .math.omml import OMML_NS, oMath2Latex

MATH_ROOT_TEMPLATE = "".join(
    (
        "<w:document ",
        'xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" ',
        'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" ',
        'xmlns:o="urn:schemas-microsoft-com:office:office" ',
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ',
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" ',
        'xmlns:v="urn:schemas-microsoft-com:vml" ',
        'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" ',
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" ',
        'xmlns:w10="urn:schemas-microsoft-com:office:word" ',
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" ',
        'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" ',
        'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" ',
        'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" ',
        'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" ',
        'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" mc:Ignorable="w14 wp14">',
        "{0}</w:document>",
    )
)


def _convert_omath_to_latex(tag: Tag) -> str:
    """
    Converts an OMML (Office Math Markup Language) tag to LaTeX format.

    Args:
        tag (Tag): A BeautifulSoup Tag object representing the OMML element.

    Returns:
        str: The LaTeX representation of the OMML element.
    """
    # Format the tag into a complete XML document string
    math_root = ET.fromstring(MATH_ROOT_TEMPLATE.format(str(tag)))
    # Find the 'oMath' element within the XML document
    math_element = math_root.find(OMML_NS + "oMath")
    # Convert the 'oMath' element to LaTeX using the oMath2Latex function
    latex = oMath2Latex(math_element).latex
    return latex


def _get_omath_tag_replacement(tag: Tag, block: bool = False) -> Tag:
    """
    Creates a replacement tag for an OMML (Office Math Markup Language) element.

    Args:
        tag (Tag): A BeautifulSoup Tag object representing the "oMath" element.
        block (bool, optional): If True, the LaTeX will be wrapped in double dollar signs for block mode. Defaults to False.

    Returns:
        Tag: A BeautifulSoup Tag object representing the replacement element.
    """
    t_tag = Tag(name="w:t")
    t_tag.string = (
        f"$${_convert_omath_to_latex(tag)}$$"
        if block
        else f"${_convert_omath_to_latex(tag)}$"
    )
    r_tag = Tag(name="w:r")
    r_tag.append(t_tag)
    return r_tag


def _replace_equations(tag: Tag):
    """
    Replaces OMML (Office Math Markup Language) elements with their LaTeX equivalents.

    Args:
        tag (Tag): A BeautifulSoup Tag object representing the OMML element. Could be either "oMathPara" or "oMath".

    Raises:
        ValueError: If the tag is not supported.
    """
    if tag.name == "oMathPara":
        # Create a new paragraph tag
        p_tag = Tag(name="w:p")
        # Replace each 'oMath' child tag with its LaTeX equivalent as block equations
        for child_tag in tag.find_all("oMath"):
            p_tag.append(_get_omath_tag_replacement(child_tag, block=True))
        # Replace the original 'oMathPara' tag with the new paragraph tag
        tag.replace_with(p_tag)
    elif tag.name == "oMath":
        # Replace the 'oMath' tag with its LaTeX equivalent as inline equation
        tag.replace_with(_get_omath_tag_replacement(tag, block=False))
    else:
        raise ValueError(f"Not supported tag: {tag.name}")


def _pre_process_math(content: bytes) -> bytes:
    """
    Pre-processes the math content in a DOCX -> XML file by converting OMML (Office Math Markup Language) elements to LaTeX.
    This preprocessed content can be directly replaced in the DOCX file -> XMLs.

    Args:
        content (bytes): The XML content of the DOCX file as bytes.

    Returns:
        bytes: The processed content with OMML elements replaced by their LaTeX equivalents, encoded as bytes.
    """
    soup = BeautifulSoup(content.decode(), features="xml")
    for tag in soup.find_all("oMathPara"):
        _replace_equations(tag)
    for tag in soup.find_all("oMath"):
        _replace_equations(tag)
    return str(soup).encode()


def _build_indent_lookup(
    numbering_content: bytes,
) -> Callable[[str, str], Optional[int]]:
    """
    Builds a lookup of list level indentation from a numbering.xml part.

    Args:
        numbering_content (bytes): The XML content of the numbering part.

    Returns:
        Callable: A function mapping (numId, ilvl) to the left indent of that
        list level, or None when either the numbering definition or the level
        is not defined.
    """
    soup = BeautifulSoup(numbering_content.decode(), features="xml")
    num_to_abstract = {
        num["w:numId"]: num.abstractNumId["w:val"] for num in soup.find_all("num")
    }
    level_indents: dict[tuple[str, str], int] = {}
    for abstract in soup.find_all("abstractNum"):
        for level in abstract.find_all("lvl"):
            ind = level.find("ind")
            if ind is not None:
                indent = ind.get("w:left") or ind.get("w:start")
                if indent is not None:
                    level_indents[(abstract["w:abstractNumId"], level["w:ilvl"])] = int(
                        indent
                    )

    def indent_of(num_id: str, ilvl: str) -> Optional[int]:
        abstract = num_to_abstract.get(num_id)
        if abstract is None:
            return None
        return level_indents.get((abstract, ilvl))

    return indent_of


def _set_numbering(p: Tag, num_id: str, ilvl: int) -> None:
    """Rewrites the numbering reference (numId, ilvl) of a paragraph."""
    num_id_tag = p.find("numId")
    if num_id_tag is None:
        return
    num_id_tag["w:val"] = num_id
    ilvl_tag = p.find("ilvl")
    if ilvl_tag is None:
        num_pr = p.find("numPr")
        if num_pr is None:
            return
        ilvl_tag = Tag(name="ilvl")
        num_pr.insert(0, ilvl_tag)
    ilvl_tag["w:val"] = str(ilvl)


def _pre_process_nested_lists(
    content: bytes, numbering_content: Optional[bytes]
) -> bytes:
    """
    Rewrites visually-nested lists that use a separate numbering definition.

    Word frequently renders sub-lists (e.g. "a) ... b) ..." below a numbered
    item) as an independent top-level numbering definition whose visual
    nesting comes only from its indentation in numbering.xml. Conversion
    libraries such as mammoth flatten such lists, because the paragraphs
    reference their own numbering definition at ilvl 0. Rewriting those
    paragraphs to continue the parent list at a deeper ilvl preserves the
    nesting during conversion.

    A run of paragraphs is rewritten when it starts at ilvl 0 with a numId
    different from the immediately preceding numbered paragraph, and the
    indent of the new list level is strictly greater than the indent of the
    preceding one.

    Args:
        content (bytes): The XML content of the document part as bytes.
        numbering_content (Optional[bytes]): The XML content of numbering.xml,
        or None when the document has no numbering part (the content is
        returned unchanged in that case).

    Returns:
        bytes: The processed XML content, encoded as bytes.
    """
    if numbering_content is None:
        return content
    indent_of = _build_indent_lookup(numbering_content)
    soup = BeautifulSoup(content.decode(), features="xml")

    parent: Optional[tuple[str, int]] = None  # (numId, ilvl) of previous list item
    rewrite_num_id: Optional[str] = None  # numId of the run being rewritten
    rewrite_target: tuple[str, int] = ("", 0)  # (numId, level shift) to apply

    for p in soup.find_all("p"):
        num_id_tag = p.find("numId")
        if num_id_tag is None:
            parent = None
            rewrite_num_id = None
            continue
        num_id = num_id_tag["w:val"]
        ilvl_tag = p.find("ilvl")
        ilvl = int(ilvl_tag["w:val"]) if ilvl_tag is not None else 0

        if rewrite_num_id is not None and num_id == rewrite_num_id:
            # Continue the nested run, shifting all of its levels.
            new_ilvl = ilvl + rewrite_target[1]
            _set_numbering(p, rewrite_target[0], new_ilvl)
            parent = (rewrite_target[0], new_ilvl)
            continue

        parent_indent = (
            indent_of(parent[0], str(parent[1])) if parent is not None else None
        )
        run_indent = indent_of(num_id, "0")
        if (
            parent is not None
            and parent[0] != num_id
            and ilvl == 0
            and parent_indent is not None
            and run_indent is not None
            and run_indent > parent_indent
        ):
            rewrite_num_id = num_id
            rewrite_target = (parent[0], parent[1] + 1)
            new_ilvl = ilvl + rewrite_target[1]
            _set_numbering(p, rewrite_target[0], new_ilvl)
            parent = (rewrite_target[0], new_ilvl)
        else:
            rewrite_num_id = None
            parent = (num_id, ilvl)

    return str(soup).encode()


def pre_process_docx(input_docx: BinaryIO) -> BinaryIO:
    """
    Pre-processes a DOCX file with provided steps.

    The process works by unzipping the DOCX file in memory, transforming specific XML files
    (such as converting OMML elements to LaTeX), and then zipping everything back into a
    DOCX file without writing to disk.

    Args:
        input_docx (BinaryIO): A binary input stream representing the DOCX file.

    Returns:
        BinaryIO: A binary output stream representing the processed DOCX file.
    """
    output_docx = BytesIO()
    # The files that need to be pre-processed from .docx
    pre_process_enable_files = [
        "word/document.xml",
        "word/footnotes.xml",
        "word/endnotes.xml",
    ]
    with zipfile.ZipFile(input_docx, mode="r") as zip_input:
        files = {name: zip_input.read(name) for name in zip_input.namelist()}
        numbering_content = files.get("word/numbering.xml")
        with zipfile.ZipFile(output_docx, mode="w") as zip_output:
            zip_output.comment = zip_input.comment
            for name, content in files.items():
                if name in pre_process_enable_files:
                    try:
                        # Pre-process the content
                        updated_content = _pre_process_math(content)
                        updated_content = _pre_process_nested_lists(
                            updated_content, numbering_content
                        )
                        # In the future, if there are more pre-processing steps, they can be added here
                        zip_output.writestr(name, updated_content)
                    except Exception:
                        # If there is an error in processing the content, write the original content
                        zip_output.writestr(name, content)
                else:
                    zip_output.writestr(name, content)
    output_docx.seek(0)
    return output_docx
