import zipfile
from io import BytesIO
from struct import unpack_from

import pytest

from markitdown.converter_utils.docx.pre_process import pre_process_docx


def _docx_with_case_mismatched_local_header() -> BytesIO:
    stream = BytesIO()
    with zipfile.ZipFile(stream, mode="w") as zip_output:
        zip_output.writestr("customXml/item2.xml", b"<item />")

    raw = bytearray(stream.getvalue())
    with zipfile.ZipFile(BytesIO(raw), mode="r") as zip_input:
        info = zip_input.getinfo("customXml/item2.xml")

    offset = info.header_offset
    file_name_length = unpack_from("<H", raw, offset + 26)[0]
    local_name_start = offset + 30
    local_name_end = local_name_start + file_name_length
    local_name = b"customXML/item2.xml"
    assert len(local_name) == file_name_length

    raw[local_name_start:local_name_end] = local_name
    return BytesIO(bytes(raw))


def test_pre_process_docx_repairs_case_mismatched_local_headers() -> None:
    stream = _docx_with_case_mismatched_local_header()

    with pytest.raises(zipfile.BadZipFile):
        with zipfile.ZipFile(stream, mode="r") as zip_input:
            zip_input.read("customXml/item2.xml")

    output = pre_process_docx(stream)

    with zipfile.ZipFile(output, mode="r") as zip_input:
        assert zip_input.read("customXml/item2.xml") == b"<item />"
