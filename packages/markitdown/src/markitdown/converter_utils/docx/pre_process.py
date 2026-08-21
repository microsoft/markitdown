import zipfile
from io import BytesIO
from typing import BinaryIO
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


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# mammoth's default style map only defines list nesting up to five levels (see
# "p:ordered-list(5)" in mammoth.options). A paragraph promoted past the last
# mapped level matches no rule at all and drops out of the list entirely, so
# nesting is capped at the deepest level mammoth can still represent.
MAX_LIST_LEVEL = 4

# Word's default indentation step between consecutive list levels, in twips.
# Used only when a level definition carries no explicit indentation.
DEFAULT_LEVEL_INDENT = 720


def _read_indent(element: Tag | None) -> int | None:
    """
    Reads the left indentation (in twips) from the "w:ind" child of an element.

    Args:
        element (Tag | None): The element whose "w:ind" child should be read.

    Returns:
        int | None: The left indentation, or None if it is absent or malformed.
    """
    if element is None:
        return None
    ind = element.find("ind", recursive=False)
    if ind is None:
        return None
    # "w:start" is the ISO/strict equivalent of the transitional "w:left".
    for attribute in ("w:left", "w:start"):
        value = ind.get(attribute)
        if value is not None:
            try:
                return int(value)
            except ValueError:
                pass
    return None


def _read_numbering_definitions(numbering_soup: BeautifulSoup) -> dict:
    """
    Resolves every "w:num" in numbering.xml to its per-level indentation and format.

    Args:
        numbering_soup (BeautifulSoup): The parsed numbering.xml.

    Returns:
        dict: Maps num_id -> level_index -> {"indent": int | None, "fmt": str | None}.
    """
    abstract_nums = {}
    for abstract_num in numbering_soup.find_all("abstractNum"):
        levels = {}
        for lvl in abstract_num.find_all("lvl"):
            num_fmt = lvl.find("numFmt")
            levels[lvl.get("w:ilvl")] = {
                "indent": _read_indent(lvl.find("pPr")),
                "fmt": num_fmt.get("w:val") if num_fmt is not None else None,
            }
        abstract_nums[abstract_num.get("w:abstractNumId")] = levels

    nums = {}
    for num in numbering_soup.find_all("num"):
        abstract_num_id = num.find("abstractNumId")
        if abstract_num_id is None:
            continue
        levels = dict(abstract_nums.get(abstract_num_id.get("w:val"), {}))
        # A "w:lvlOverride" replaces the inherited definition for a single level.
        for override in num.find_all("lvlOverride"):
            lvl = override.find("lvl")
            if lvl is None:
                continue
            num_fmt = lvl.find("numFmt")
            level_index = lvl.get("w:ilvl", override.get("w:ilvl"))
            levels[level_index] = {
                "indent": _read_indent(lvl.find("pPr")),
                "fmt": num_fmt.get("w:val") if num_fmt is not None else None,
            }
        nums[num.get("w:numId")] = levels
    return nums


def _iter_list_paragraphs(document_soup: BeautifulSoup):
    """
    Yields each paragraph of a document alongside its numbering reference.

    Args:
        document_soup (BeautifulSoup): The parsed document.xml.

    Yields:
        tuple: (paragraph, ilvl_tag, num_id_tag). The tags are None for any
            paragraph that does not carry direct numbering.
    """
    for paragraph in document_soup.find_all("p"):
        p_pr = paragraph.find("pPr", recursive=False)
        num_pr = p_pr.find("numPr", recursive=False) if p_pr is not None else None
        if num_pr is None:
            yield paragraph, None, None
            continue
        ilvl_tag = num_pr.find("ilvl", recursive=False)
        num_id_tag = num_pr.find("numId", recursive=False)
        # A "w:numId" of 0 explicitly removes numbering from the paragraph.
        if num_id_tag is None or num_id_tag.get("w:val") == "0":
            yield paragraph, None, None
            continue
        yield paragraph, ilvl_tag, num_id_tag


def _is_parent_of(candidate: dict, item: dict) -> bool:
    """
    Determines whether an open list level is an ancestor of the current item.

    Within a single "w:numId" the declared "w:ilvl" is authoritative, because
    Word uses it directly and levels of one list are directly comparable.
    Across different "w:numId" values the levels are unrelated, so only the
    rendered indentation can establish which list is nested inside the other.

    Args:
        candidate (dict): An open level from the stack.
        item (dict): The list paragraph being placed.

    Returns:
        bool: True if candidate is strictly shallower than item.
    """
    if candidate["num_id"] == item["num_id"]:
        return candidate["ilvl"] < item["ilvl"]
    return candidate["indent"] < item["indent"]


def _resolve_list_depths(document_soup: BeautifulSoup, numbering: dict) -> list:
    """
    Computes the true nesting depth of every numbered paragraph in a document.

    Word represents a nested list in either of two ways: as a deeper "w:ilvl"
    within the parent's "w:numId", or as an entirely new "w:numId" at
    "w:ilvl" 0 that is simply indented further. Both render identically, but
    mammoth derives nesting from "w:ilvl" alone and so flattens the second
    form. Walking the document while tracking the open levels recovers the
    nesting that indentation implies.

    Args:
        document_soup (BeautifulSoup): The parsed document.xml.
        numbering (dict): Numbering definitions from _read_numbering_definitions.

    Returns:
        list: One (paragraph, ilvl_tag, num_id_tag, depth) tuple per paragraph
            whose depth differs from its declared level.
    """
    remappings = []
    stack: list[dict] = []

    for paragraph, ilvl_tag, num_id_tag in _iter_list_paragraphs(document_soup):
        if num_id_tag is None:
            # Body text interrupts the surrounding list, exactly as it does for
            # mammoth, so no level stays open across it.
            stack.clear()
            continue

        num_id = num_id_tag.get("w:val")
        # A missing "w:ilvl" means the first level.
        raw_ilvl = ilvl_tag.get("w:val") if ilvl_tag is not None else "0"
        try:
            ilvl = int(raw_ilvl)
        except (TypeError, ValueError):
            ilvl = 0

        level = numbering.get(num_id, {}).get(str(ilvl), {})
        indent = level.get("indent")
        if indent is None:
            indent = ilvl * DEFAULT_LEVEL_INDENT
        # Indentation applied directly to the paragraph overrides the level's.
        paragraph_indent = _read_indent(paragraph.find("pPr", recursive=False))
        if paragraph_indent is not None:
            indent = paragraph_indent

        item = {"num_id": num_id, "ilvl": ilvl, "indent": indent}
        while stack and not _is_parent_of(stack[-1], item):
            stack.pop()

        implied_depth = stack[-1]["depth"] + 1 if stack else 0
        # Indentation is only ever used to reveal nesting the declared levels
        # missed, never to remove nesting a document states outright. This
        # keeps documents that mammoth already handles correctly untouched.
        depth = min(max(implied_depth, ilvl), MAX_LIST_LEVEL)

        item["depth"] = depth
        stack.append(item)

        if depth != ilvl:
            remappings.append((paragraph, ilvl_tag, num_id_tag, depth))

    return remappings


def _apply_list_depths(
    document_soup: BeautifulSoup, numbering_soup: BeautifulSoup, remappings: list
) -> None:
    """
    Rewrites paragraphs whose nesting depth was mis-declared, in place.

    Simply raising "w:ilvl" would make the paragraph resolve against whatever
    unrelated level its numbering happens to define at that index, which can
    silently flip an ordered list to a bulleted one. Instead each remapped
    (num_id, ilvl, depth) combination gets a minimal generated definition that
    places the original format at the required depth.

    Args:
        document_soup (BeautifulSoup): The parsed document.xml.
        numbering_soup (BeautifulSoup): The parsed numbering.xml.
        remappings (list): Output of _resolve_list_depths.
    """
    numbering_root = numbering_soup.find("numbering")
    if numbering_root is None:
        return

    existing_num_ids = {
        int(num.get("w:numId"))
        for num in numbering_soup.find_all("num")
        if (num.get("w:numId") or "").isdigit()
    }
    existing_abstract_ids = {
        int(abstract_num.get("w:abstractNumId"))
        for abstract_num in numbering_soup.find_all("abstractNum")
        if (abstract_num.get("w:abstractNumId") or "").isdigit()
    }
    next_num_id = max(existing_num_ids, default=0) + 1
    next_abstract_id = max(existing_abstract_ids, default=0) + 1

    numbering = _read_numbering_definitions(numbering_soup)
    generated: dict = {}

    for paragraph, ilvl_tag, num_id_tag, depth in remappings:
        num_id = num_id_tag.get("w:val")
        ilvl = ilvl_tag.get("w:val") if ilvl_tag is not None else "0"
        key = (num_id, ilvl, depth)

        if key not in generated:
            num_fmt = numbering.get(num_id, {}).get(ilvl, {}).get("fmt")

            abstract_num = numbering_soup.new_tag(
                "abstractNum", namespace=W_NS, nsprefix="w"
            )
            abstract_num["w:abstractNumId"] = str(next_abstract_id)
            lvl = numbering_soup.new_tag("lvl", namespace=W_NS, nsprefix="w")
            lvl["w:ilvl"] = str(depth)
            if num_fmt is not None:
                num_fmt_tag = numbering_soup.new_tag(
                    "numFmt", namespace=W_NS, nsprefix="w"
                )
                num_fmt_tag["w:val"] = num_fmt
                lvl.append(num_fmt_tag)
            abstract_num.append(lvl)

            num = numbering_soup.new_tag("num", namespace=W_NS, nsprefix="w")
            num["w:numId"] = str(next_num_id)
            abstract_num_id = numbering_soup.new_tag(
                "abstractNumId", namespace=W_NS, nsprefix="w"
            )
            abstract_num_id["w:val"] = str(next_abstract_id)
            num.append(abstract_num_id)

            # "w:abstractNum" elements must precede "w:num" elements.
            first_num = numbering_root.find("num", recursive=False)
            if first_num is not None:
                first_num.insert_before(abstract_num)
            else:
                numbering_root.append(abstract_num)
            numbering_root.append(num)

            generated[key] = str(next_num_id)
            next_abstract_id += 1
            next_num_id += 1

        num_id_tag["w:val"] = generated[key]
        if ilvl_tag is None:
            num_pr = num_id_tag.parent
            ilvl_tag = document_soup.new_tag("ilvl", namespace=W_NS, nsprefix="w")
            num_pr.insert(0, ilvl_tag)
        ilvl_tag["w:val"] = str(depth)


def _pre_process_lists(document_content: bytes, numbering_content: bytes) -> tuple:
    """
    Restores list nesting that is expressed through indentation rather than levels.

    Args:
        document_content (bytes): The XML content of word/document.xml.
        numbering_content (bytes): The XML content of word/numbering.xml.

    Returns:
        tuple: The processed (document_content, numbering_content) as bytes.
    """
    document_soup = BeautifulSoup(document_content.decode(), features="xml")
    numbering_soup = BeautifulSoup(numbering_content.decode(), features="xml")

    numbering = _read_numbering_definitions(numbering_soup)
    remappings = _resolve_list_depths(document_soup, numbering)
    if not remappings:
        return document_content, numbering_content

    _apply_list_depths(document_soup, numbering_soup, remappings)
    return str(document_soup).encode(), str(numbering_soup).encode()


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

        # List nesting spans document.xml and numbering.xml, so both are
        # rewritten together rather than one file at a time below.
        if "word/document.xml" in files and "word/numbering.xml" in files:
            try:
                (
                    files["word/document.xml"],
                    files["word/numbering.xml"],
                ) = _pre_process_lists(
                    files["word/document.xml"], files["word/numbering.xml"]
                )
            except Exception:
                # If there is an error in processing the content, keep the original content
                pass

        with zipfile.ZipFile(output_docx, mode="w") as zip_output:
            zip_output.comment = zip_input.comment
            for name, content in files.items():
                if name in pre_process_enable_files:
                    try:
                        # Pre-process the content
                        updated_content = _pre_process_math(content)
                        # In the future, if there are more pre-processing steps, they can be added here
                        zip_output.writestr(name, updated_content)
                    except Exception:
                        # If there is an error in processing the content, write the original content
                        zip_output.writestr(name, content)
                else:
                    zip_output.writestr(name, content)
    output_docx.seek(0)
    return output_docx
