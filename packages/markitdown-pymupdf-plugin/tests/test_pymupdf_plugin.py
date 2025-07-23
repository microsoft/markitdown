import io
import unittest
from unittest.mock import MagicMock

import fitz
from markitdown import MarkItDown, DocumentConverterResult, StreamInfo
from markitdown_pymupdf_plugin._plugin import PyMuPdfConverter, register_converters

class TestPyMuPdfPlugin(unittest.TestCase):
    def test_register_converters(self):
        mock_markitdown = MagicMock(spec=MarkItDown)
        register_converters(mock_markitdown)
        mock_markitdown.register_converter.assert_called_once_with(
            unittest.mock.ANY, override=True
        )
        self.assertIsInstance(
            mock_markitdown.register_converter.call_args[0][0], PyMuPdfConverter
        )

    def test_accepts(self):
        converter = PyMuPdfConverter()
        # Test with accepted extension
        self.assertTrue(
            converter.accepts(
                io.BytesIO(b""), StreamInfo(extension=".pdf", mimetype="application/pdf")
            )
        )
        # Test with accepted mimetype
        self.assertTrue(
            converter.accepts(
                io.BytesIO(b""), StreamInfo(extension=".bin", mimetype="application/pdf")
            )
        )
        # Test with unaccepted extension and mimetype
        self.assertFalse(
            converter.accepts(
                io.BytesIO(b""), StreamInfo(extension=".txt", mimetype="text/plain")
            )
        )

    def test_convert(self):
        converter = PyMuPdfConverter()
        # Create a dummy PDF in memory for testing
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((10, 10), "Hello, PyMuPDF!")
        pdf_bytes = doc.tobytes()
        doc.close()

        result = converter.convert(
            io.BytesIO(pdf_bytes), StreamInfo(extension=".pdf", mimetype="application/pdf")
        )
        self.assertIsInstance(result, DocumentConverterResult)
        self.assertIn("Hello, PyMuPDF!", result.markdown)

if __name__ == "__main__":
    unittest.main()
