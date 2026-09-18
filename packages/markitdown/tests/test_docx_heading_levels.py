"""Word Heading 7-9 must clamp to markdown h6, not drop structure."""
import io

from docx import Document

from markitdown import MarkItDown, StreamInfo


def test_docx_heading_levels_1_to_9():
    doc = Document()
    for level in range(1, 10):
        doc.add_heading(f"H{level}", level=level)
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    result = MarkItDown().convert_stream(buf, stream_info=StreamInfo(extension=".docx"))
    lines = [line for line in result.markdown.splitlines() if line.strip()]
    assert lines[0] == "# H1"
    assert lines[5] == "###### H6"
    # 7-9 clamp to h6 instead of losing heading structure entirely
    assert lines[6] == "###### H7"
    assert lines[8] == "###### H9"
