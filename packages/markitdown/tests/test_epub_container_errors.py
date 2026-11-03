import io
import zipfile

import pytest

from markitdown import MarkItDown
from markitdown._exceptions import FileConversionException


def _epub(container_xml: str, extra: dict[str, str] | None = None) -> io.BytesIO:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("mimetype", "application/epub+zip")
        archive.writestr("META-INF/container.xml", container_xml)
        for name, content in (extra or {}).items():
            archive.writestr(name, content)
    buffer.seek(0)
    return buffer


def test_epub_without_rootfile_raises_a_named_error():
    container = '<?xml version="1.0"?><container><rootfiles></rootfiles></container>'

    with pytest.raises(FileConversionException, match="no <rootfile> element"):
        MarkItDown().convert_stream(_epub(container), stream_info=None)


def test_epub_with_missing_opf_member_raises_a_named_error():
    container = (
        '<?xml version="1.0"?><container><rootfiles>'
        '<rootfile full-path="OEBPS/content.opf"/></rootfiles></container>'
    )

    with pytest.raises(FileConversionException, match="not a member of the archive"):
        MarkItDown().convert_stream(_epub(container), stream_info=None)
