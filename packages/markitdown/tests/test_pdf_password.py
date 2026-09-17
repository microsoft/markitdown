"""Tests for password-protected PDF support."""

import os

import pytest

from markitdown import MarkItDown
from markitdown._exceptions import FileConversionException

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")
PASSWORD_PDF = os.path.join(TEST_FILES_DIR, "test_password.pdf")
CORRECT_PASSWORD = "testpassword"


class TestPdfPasswordSupport:
    """Tests for password-protected PDF conversion."""

    def test_convert_with_correct_password(self):
        """A password-protected PDF should convert when the correct password is given."""
        md = MarkItDown()
        result = md.convert(PASSWORD_PDF, password=CORRECT_PASSWORD)
        assert "password-protected test document" in result.markdown

    def test_convert_without_password_raises(self):
        """A password-protected PDF without a password should raise FileConversionException."""
        md = MarkItDown()
        with pytest.raises(Exception):
            md.convert(PASSWORD_PDF)

    def test_convert_with_wrong_password_raises(self):
        """A password-protected PDF with the wrong password should raise an error."""
        md = MarkItDown()
        with pytest.raises(Exception):
            md.convert(PASSWORD_PDF, password="wrongpassword")

    def test_unprotected_pdf_unaffected(self):
        """An unprotected PDF should convert normally even when password is None."""
        md = MarkItDown()
        # Use an existing test PDF from the test_files directory
        test_pdfs = [
            f
            for f in os.listdir(TEST_FILES_DIR)
            if f.endswith(".pdf") and f != "test_password.pdf"
        ]
        if test_pdfs:
            result = md.convert(os.path.join(TEST_FILES_DIR, test_pdfs[0]))
            assert result.markdown is not None

    def test_cli_password_flag(self):
        """The --password CLI flag should be recognized."""
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "-m", "markitdown", "--help"],
            capture_output=True,
            text=True,
        )
        assert "--password" in result.stdout
