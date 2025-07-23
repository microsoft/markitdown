import io
import os
import shutil
import warnings
from unittest.mock import MagicMock, ANY

import pymupdf as pymupdf
from markitdown import MarkItDown, DocumentConverterResult, StreamInfo
from markitdown_pymupdf_plugin._plugin import PyMuPdfConverter, register_converters

# Suppress specific DeprecationWarning messages from SWIG-generated code in PyMuPDF
warnings.filterwarnings("ignore", message="builtin type SwigPyPacked has no __module__ attribute", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="builtin type SwigPyObject has no __module__ attribute", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="builtin type swigvarlink has no __module__ attribute", category=DeprecationWarning)

class TestPyMuPdfPlugin:
    def test_register_converters(self):
        """
        Check whether registration is called properly 
        """
        mock_markitdown = MagicMock(spec=MarkItDown)
        register_converters(mock_markitdown)
        mock_markitdown.register_converter.assert_called_once_with(
            ANY, override=True
        )
        assert isinstance(
            mock_markitdown.register_converter.call_args[0][0], PyMuPdfConverter
        )

    def test_accepts(self):
        """
        Test detection of situations where this converter applies
        """
        converter = PyMuPdfConverter()
        # Test with accepted extension
        assert converter.accepts(
            io.BytesIO(b""), StreamInfo(extension=".pdf", mimetype="application/pdf")
        )
        # Test with accepted mimetype
        assert converter.accepts(
            io.BytesIO(b""), StreamInfo(extension=".bin", mimetype="application/pdf")
        )
        # Test with unaccepted extension and mimetype
        assert not converter.accepts(
            io.BytesIO(b""), StreamInfo(extension=".txt", mimetype="text/plain")
        )

    def test_convert(self):
        """
        Test pure textual conversion to markdown
        """
        converter = PyMuPdfConverter()
        # Create a dummy PDF in memory for testing
        doc = pymupdf.open()
        page = doc.new_page()
        page.insert_text((10, 10), "Hello, PyMuPDF!")
        pdf_bytes = doc.tobytes()
        doc.close()

        result = converter.convert(
            io.BytesIO(pdf_bytes), StreamInfo(extension=".pdf", mimetype="application/pdf", local_path=None)
        )
        assert isinstance(result, DocumentConverterResult)
        assert "Hello, PyMuPDF!" in result.markdown
        assert result.extracted_image_paths == [] # No images extracted in this test
