import io
import zipfile
import pytest
from markitdown import MarkItDown
from markitdown.converter_utils.docx.math.omml import OMML_NS

# Minimal Word Document XML structure with a math run having no text child
# (an <m:r> with formatting tags but no <m:t>)
# This simulates the math XML structure inside a DOCX document
DOCUMENT_XML_CONTENT = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
    <w:body>
        <w:p>
            <m:oMath>
                <m:r>
                    <m:rPr/>
                </m:r>
                <m:r>
                    <m:t>x</m:t>
                </m:r>
            </m:oMath>
        </w:p>
    </w:body>
</w:document>
"""

def test_math_run_no_text_child():
    # Build a minimal docx in-memory
    docx_buffer = io.BytesIO()
    with zipfile.ZipFile(docx_buffer, "w") as z:
        # docx needs word/document.xml to be valid
        z.writestr("word/document.xml", DOCUMENT_XML_CONTENT)
        # minimal content types
        z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?><Types><Default Extension="xml" ContentType="application/xml"/></Types>')
        
    docx_buffer.seek(0)
    
    # We should be able to convert this without a TypeError crash,
    # and the valid math run ('x') should still be preserved/rendered.
    markitdown = MarkItDown()
    result = markitdown.convert_stream(docx_buffer, file_extension=".docx")
    assert "$x$" in result.text_content
