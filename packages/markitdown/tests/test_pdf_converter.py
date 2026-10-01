#!/usr/bin/env python3 -m pytest

import io
import os
import pytest
from unittest.mock import Mock, patch
import sys

#import marItDown framework, pdf converter
from markitdown import MarkItDown, StreamInfo
from markitdown.converters._pdf_converter import (
    PdfConverter,
    ACCEPTED_MIME_TYPE_PREFIXES,
    ACCEPTED_FILE_EXTENSIONS,
)
from markitdown._exceptions import MissingDependencyException

# Paths and setup for locating test assets
TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")
PDF_TEST_FILE = os.path.join(TEST_FILES_DIR, "test.pdf")

# Unit tests for PdfConverter.accepts()
# To verify that converter correctly recognizes PDF files based on extension and MIME types, rejecting invalid ones
class TestPdfConverterAccepts:

    #Test that .pdf extension is accepted.
    def test_accepts_pdf_extension(self):
        converter = PdfConverter()
        stream_info = StreamInfo(extension=".pdf")
        assert converter.accepts(io.BytesIO(), stream_info) is True

    #Test that .PDF extension is accepted (case insensitive).
    def test_accepts_pdf_extension_uppercase(self):
        converter = PdfConverter()
        stream_info = StreamInfo(extension=".PDF")
        assert converter.accepts(io.BytesIO(), stream_info) is True

    #Test that application/pdf mimetype is accepted.
    def test_accepts_application_pdf_mimetype(self):
        converter = PdfConverter()
        stream_info = StreamInfo(mimetype="application/pdf")
        assert converter.accepts(io.BytesIO(), stream_info) is True

    #Test that  application/pdf with charset is accepted.
    def test_accepts_application_pdf_with_charset(self):
        converter = PdfConverter()
        stream_info = StreamInfo(mimetype="application/pdf; charset=utf-8")
        assert converter.accepts(io.BytesIO(), stream_info) is True

    #Test that application/x-pdf mimetype is accepted
    def test_accepts_application_x_pdf_mimetype(self):
        converter = PdfConverter()
        stream_info = StreamInfo(mimetype="application/x-pdf")
        assert converter.accepts(io.BytesIO(), stream_info) is True

    #Test that mimetype matching is case insensitive.
    def test_accepts_mimetype_case_insensitive(self):
        converter = PdfConverter()
        stream_info = StreamInfo(mimetype="APPLICATION/PDF")
        assert converter.accepts(io.BytesIO(), stream_info) is True

    #Test that non-PDF extensions are rejected.
    def test_rejects_wrong_extension(self):
        converter = PdfConverter()
        stream_info = StreamInfo(extension=".txt")
        assert converter.accepts(io.BytesIO(), stream_info) is False

    #Test that non-PDF mimetypes are rejected.
    def test_rejects_wrong_mimetype(self):
        converter = PdfConverter()
        stream_info = StreamInfo(mimetype="text/plain")
        assert converter.accepts(io.BytesIO(), stream_info) is False

    #Test that empty StreamInfo is rejected.
    def test_rejects_empty_stream_info(self):
        converter = PdfConverter()
        stream_info = StreamInfo()
        assert converter.accepts(io.BytesIO(), stream_info) is False

# Unit tests for PdfConverter.convert()
class TestPdfConverterConvert:
  
    #Test that MissingDependencyException is raised when pdfminer is not available.
    def test_convert_missing_dependency(self):
        # Mock the dependency check to simulate missing pdfminer
        with patch("markitdown.converters._pdf_converter._dependency_exc_info") as mock_exc_info:
            # Create a fake ImportError
            try:
                raise ImportError("No module named 'pdfminer'")
            except ImportError:
                mock_exc_info.__bool__ = Mock(return_value=True)
                mock_exc_info.__getitem__ = Mock(side_effect=lambda x: sys.exc_info()[x])

                converter = PdfConverter()
                stream_info = StreamInfo(extension=".pdf")

                with pytest.raises(MissingDependencyException) as exc_info:
                    converter.convert(io.BytesIO(b"fake pdf content"), stream_info)

                # Check the exception message
                assert "pdf" in str(exc_info.value).lower()
                assert ".pdf" in str(exc_info.value)

    
#Tests for constants to ensure accepted extensions and MIME types are correclty defined and non-empty
class TestPdfConverterConstants:
    #Test that ACCEPTED_MIME_TYPE_PREFIXES contains expected values.
    def test_accepted_mime_type_prefixes(self):
        assert "application/pdf" in ACCEPTED_MIME_TYPE_PREFIXES
        assert "application/x-pdf" in ACCEPTED_MIME_TYPE_PREFIXES
        assert len(ACCEPTED_MIME_TYPE_PREFIXES) >= 2

    #Test that ACCEPTED_FILE_EXTENSIONS contains expected values.
    def test_accepted_file_extensions(self):
        assert ".pdf" in ACCEPTED_FILE_EXTENSIONS
        assert len(ACCEPTED_FILE_EXTENSIONS) >= 1

# Allows this file to be executed directly with python test_pdf_converter.py
# Runs tests in verbode mode
if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    pytest.main([__file__, "-v"])
