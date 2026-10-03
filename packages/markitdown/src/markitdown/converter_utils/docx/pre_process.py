import re
import struct
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
    if math_element is None:
        return ""
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


def _pre_process_strike(content: bytes) -> bytes:
    """
    Pre-processes the strikethrough content in a DOCX -> XML file by normalizing double
    strikethrough runs to single strikethrough runs.

    Word marks double strikethrough with "w:dstrike", which downstream converters do not
    recognize, causing those runs to lose their strikethrough entirely. Renaming the tag to
    "w:strike" preserves the strikethrough semantics.

    Args:
        content (bytes): The XML content of the DOCX file as bytes.

    Returns:
        bytes: The processed content with "dstrike" elements renamed to "strike", encoded as bytes.
    """
    # Double strikethrough is rare, and parsing/reserializing the XML is expensive
    # on large documents, so skip the round-trip when there is nothing to rename.
    if b"dstrike" not in content:
        return content

    soup = BeautifulSoup(content.decode(), features="xml")
    for tag in soup.find_all("dstrike"):
        tag.name = "strike"
    return str(soup).encode()


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


def _fix_zip_filename_casing(input_docx: BinaryIO) -> BinaryIO:
    """
    Fix ZIP files where local file header filenames differ in casing
    from the central directory filenames.

    Some document generators (e.g. certain Microsoft Word versions,
    legal document systems) produce .docx/.pptx files where the central
    directory records one casing (e.g. 'customXml/item2.xml') but
    the local file headers record another (e.g. 'customXML/item2.xml').
    Python's zipfile module raises BadZipFile when reading such files.

    This function patches local file header filenames to match the
    central directory, which is the authoritative source used by
    zipfile.ZipFile.
    """
    input_docx.seek(0)
    raw = bytearray(input_docx.read())

    # Read the central directory to get authoritative filenames
    try:
        with zipfile.ZipFile(BytesIO(raw), "r") as zf:
            cd_entries = {
                zi.header_offset: (zi.orig_filename, zi.flag_bits)
                for zi in zf.infolist()
            }
    except zipfile.BadZipFile:
        # Can't even read central directory — return as-is, let it fail later
        input_docx.seek(0)
        return input_docx

    patched = False
    for offset, (cd_name, flag_bits) in cd_entries.items():
        # Verify local file header signature
        if offset + 30 > len(raw) or raw[offset : offset + 4] != b"PK\x03\x04":
            continue

        local_fname_len = struct.unpack_from("<H", raw, offset + 26)[0]
        if offset + 30 + local_fname_len > len(raw):
            continue

        local_name = bytes(raw[offset + 30 : offset + 30 + local_fname_len])
        # ZIP filenames are cp437 unless flag bit 11 marks them as UTF-8, which is
        # how zipfile decoded orig_filename in the first place.
        central_name = cd_name.encode("utf-8" if flag_bits & 0x800 else "cp437")

        # Only patch if lengths match but content differs (casing mismatch)
        if (
            local_name != central_name
            and len(local_name) == len(central_name)
            and local_name.lower() == central_name.lower()
        ):
            raw[offset + 30 : offset + 30 + local_fname_len] = central_name
            patched = True

    if patched:
        return BytesIO(bytes(raw))
    input_docx.seek(0)
    return input_docx


def _pre_process_styles(content: bytes) -> bytes:
    """
    Repairs DOCX style definitions that Mammoth cannot read.

    Mammoth indexes ``w:type`` and ``w:styleId`` directly, so a ``w:style``
    element missing either attribute causes conversion to fail with a
    ``KeyError`` before any document text can be extracted.

    ``w:type`` is optional in OOXML: when it is absent the style type defaults
    to ``paragraph``, so the attribute is filled in rather than dropping the
    style, which would discard its formatting (a heading would be emitted as
    plain body text). A style with no ``w:styleId`` cannot be referenced by the
    document body, so it is removed. Double strikethrough is normalized to
    single strikethrough in the same namespace-aware pass.

    Match elements and attributes by namespace URI, preserving their qualified
    names when repairing the XML. Return the original bytes if no repair is needed.
    """
    from lxml import etree

    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    root = etree.fromstring(content, parser=parser)
    changed = False

    for style in root.findall(namespace + "style"):
        if namespace + "styleId" not in style.attrib:
            root.remove(style)
            changed = True
        elif namespace + "type" not in style.attrib:
            style.set(namespace + "type", "paragraph")
            changed = True

    for strike in root.iter(namespace + "dstrike"):
        strike.tag = namespace + "strike"
        changed = True

    if not changed:
        return content

    return etree.tostring(root.getroottree(), encoding="utf-8", xml_declaration=True)


def _pre_process_fields(content: bytes) -> bytes:
    """
    Preserves the display text of Word fields, which Mammoth otherwise drops.

    Mammoth has no handler for ``w:fldSimple``, so the element is ignored along
    with the child runs holding its cached result. It also never emits field
    instructions (``w:instrText``), which loses MACROBUTTON fields entirely:
    their display text is the trailing argument of the instruction and they
    have no result runs (issue #1247, common in standards-body templates for
    "Proposal N:"/"Observation N:" lines).

    ``w:fldSimple`` elements are unwrapped so their cached result runs are
    converted like ordinary content. MACROBUTTON instructions — in a
    ``w:fldSimple`` with no cached result, or in the ``w:instrText`` runs of a
    complex field with no "separate" marker — are rewritten as text runs
    holding only the display-text argument. Other instructions are never
    emitted, and complex fields with a separator are left untouched: Mammoth
    already converts their result runs.

    Args:
        content (bytes): The XML content of the DOCX file as bytes.

    Returns:
        bytes: The processed content with field display text preserved, encoded as bytes.
    """
    from lxml import etree

    # Parsing/reserializing the XML is expensive on large documents, so skip
    # the round-trip when the document contains no fields.
    if b"fldSimple" not in content and b"instrText" not in content:
        return content

    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    xml_space = "{http://www.w3.org/XML/1998/namespace}space"
    macrobutton = re.compile(r"\s*MACROBUTTON\s+\S+\s(.*)", re.DOTALL)
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    root = etree.fromstring(content, parser=parser)
    changed = False

    def make_text_run(text: str) -> "etree._Element":
        run = etree.Element(namespace + "r")
        t_element = etree.SubElement(run, namespace + "t")
        t_element.set(xml_space, "preserve")
        t_element.text = text
        return run

    # Rewrite the instruction text of complex MACROBUTTON fields (no
    # "separate" marker, hence no result runs) as ordinary text runs holding
    # only the display-text argument. A stack tracks nested fields; the
    # instruction of any other field is simply left for Mammoth to ignore.
    # Each entry holds a "separate" marker flag and the instrText elements.
    field_stack: list[list] = []
    for element in root.iter(namespace + "fldChar", namespace + "instrText"):
        if element.tag == namespace + "instrText":
            if field_stack and not field_stack[-1][0]:
                field_stack[-1][1].append(element)
            continue
        fld_char_type = element.get(namespace + "fldCharType")
        if fld_char_type == "begin":
            field_stack.append([False, []])
        elif fld_char_type == "separate" and field_stack:
            field_stack[-1][0] = True
        elif fld_char_type == "end" and field_stack:
            has_separator, instr_elements = field_stack.pop()
            if has_separator:
                continue
            instruction = "".join(instr.text or "" for instr in instr_elements)
            match = macrobutton.match(instruction)
            if match is None:
                continue
            # Convert the instrText elements overlapping the display-text
            # argument to w:t elements, preserving their runs' formatting,
            # and drop the ones covering only the instruction prefix.
            position = 0
            for instr in instr_elements:
                text = instr.text or ""
                keep = text[max(match.start(1) - position, 0) :]
                position += len(text)
                if keep:
                    instr.tag = namespace + "t"
                    instr.set(xml_space, "preserve")
                    instr.text = keep
                else:
                    instr.getparent().remove(instr)
                changed = True

    # Unwrap simple fields so their cached result runs are converted like
    # ordinary content. A MACROBUTTON field with no cached result gets a text
    # run synthesized from its instruction's display-text argument.
    for field in reversed(list(root.iter(namespace + "fldSimple"))):
        if not "".join(field.itertext()):
            match = macrobutton.match(field.get(namespace + "instr", ""))
            if match is not None and match.group(1):
                field.append(make_text_run(match.group(1)))
        parent = field.getparent()
        index = parent.index(field)
        children = list(field)
        for offset, child in enumerate(children):
            parent.insert(index + offset, child)
        if field.tail:
            if children:
                children[-1].tail = (children[-1].tail or "") + field.tail
            elif index > 0:
                previous = parent[index - 1]
                previous.tail = (previous.tail or "") + field.tail
            else:
                parent.text = (parent.text or "") + field.tail
        parent.remove(field)
        changed = True

    if not changed:
        return content

    return etree.tostring(root.getroottree(), encoding="utf-8", xml_declaration=True)


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
    # Fix ZIP filename casing mismatch before any processing
    input_docx = _fix_zip_filename_casing(input_docx)

    output_docx = BytesIO()
    # The pre-processing steps to apply to each file in the .docx
    pre_process_enable_files = {
        "word/document.xml": (
            _pre_process_strike,
            _pre_process_math,
            _pre_process_fields,
        ),
        "word/footnotes.xml": (
            _pre_process_strike,
            _pre_process_math,
            _pre_process_fields,
        ),
        "word/endnotes.xml": (
            _pre_process_strike,
            _pre_process_math,
            _pre_process_fields,
        ),
        "word/styles.xml": (_pre_process_styles,),
    }
    with zipfile.ZipFile(input_docx, mode="r") as zip_input:
        files = {name: zip_input.read(name) for name in zip_input.namelist()}
        with zipfile.ZipFile(output_docx, mode="w") as zip_output:
            zip_output.comment = zip_input.comment
            for name, content in files.items():
                updated_content = content
                # Each step is applied independently, so one failing step does
                # not discard the results of the others.
                for pre_process_step in pre_process_enable_files.get(name, ()):
                    try:
                        updated_content = pre_process_step(updated_content)
                    except Exception:
                        pass
                zip_output.writestr(name, updated_content)
    output_docx.seek(0)
    return output_docx
