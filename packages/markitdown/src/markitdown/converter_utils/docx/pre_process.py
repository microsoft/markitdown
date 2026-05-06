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


def _fix_zip_name_casing(input_docx: BinaryIO) -> BinaryIO:
    """Repair .docx zips whose local file headers disagree with the central
    directory only in case (e.g. ``customXML/item2.xml`` locally vs
    ``customXml/item2.xml`` in the central directory).

    Some .docx producers emit such files. Most zip tools accept them, but
    Python's :mod:`zipfile` strictly validates and raises ``BadZipFile``.
    The central directory is authoritative per APPNOTE; we patch the local
    file header bytes in-memory to match it. The patch is byte-length
    preserving (case-only differences in ASCII paths never change length),
    so no offset recomputation is needed.

    If no fix is required the original stream is returned unchanged
    (rewound to position 0). See markitdown #1812.
    """
    input_docx.seek(0)
    raw = bytearray(input_docx.read())
    patched = False
    try:
        zf = zipfile.ZipFile(BytesIO(raw), mode="r")
    except zipfile.BadZipFile:
        # Not even the central directory parses — nothing we can patch here.
        # Let the caller see the same error the unfixed code path would.
        input_docx.seek(0)
        return input_docx
    try:
        for info in zf.infolist():
            offset = info.header_offset
            # Local file header signature is "PK\x03\x04". If we don't see
            # it we have a malformed zip beyond what this fixer targets.
            if raw[offset : offset + 4] != b"PK\x03\x04":
                continue
            # Per APPNOTE local file header layout:
            #   bytes  0..3  signature
            #   bytes 26..27 file name length (little-endian uint16)
            #   bytes 30..   file name
            fname_len = struct.unpack_from("<H", raw, offset + 26)[0]
            local_name = bytes(raw[offset + 30 : offset + 30 + fname_len])
            try:
                central_name = info.filename.encode("utf-8")
            except UnicodeEncodeError:
                continue
            if (
                local_name != central_name
                and local_name.lower() == central_name.lower()
                and len(local_name) == len(central_name)
            ):
                raw[offset + 30 : offset + 30 + fname_len] = central_name
                patched = True
    finally:
        zf.close()
    if patched:
        return BytesIO(bytes(raw))
    input_docx.seek(0)
    return input_docx


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
    # Repair .docx zips whose local headers disagree with the central
    # directory only in case — Python's zipfile rejects these but most other
    # zip tools accept them, so .docx producers occasionally emit them
    # (markitdown #1812).
    input_docx = _fix_zip_name_casing(input_docx)
    output_docx = BytesIO()
    # The files that need to be pre-processed from .docx
    pre_process_enable_files = [
        "word/document.xml",
        "word/footnotes.xml",
        "word/endnotes.xml",
    ]
    with zipfile.ZipFile(input_docx, mode="r") as zip_input:
        files = {name: zip_input.read(name) for name in zip_input.namelist()}
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
