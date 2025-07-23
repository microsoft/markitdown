import io
import os
import shutil
import warnings
from pathlib import Path
import pytest

import pymupdf as pymupdf
from markitdown import DocumentConverterResult, StreamInfo
from markitdown_pymupdf_plugin._plugin import PyMuPdfConverter

# Suppress specific DeprecationWarning messages from SWIG-generated code in PyMuPDF
warnings.filterwarnings("ignore", message="builtin type SwigPyPacked has no __module__ attribute", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="builtin type SwigPyObject has no __module__ attribute", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="builtin type swigvarlink has no __module__ attribute", category=DeprecationWarning)

@pytest.fixture
def setup_teardown_pdf_and_dirs():
    converter = PyMuPdfConverter()
    image_source_path = "packages/markitdown/tests/test_files/test.jpg"
    text_content_default = "Hello, PyMuPDF with image!"
    text_content_custom = "Hello, PyMuPDF with custom image!"
    temp_pdf_path = "temp_test_file.pdf"
    default_img_dir = os.path.join(os.path.dirname(temp_pdf_path), "img")
    custom_img_dir = "custom_images_output"

    # Create a dummy PDF with an image
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((10, 10), text_content_default)
    page.insert_image(page.rect, filename=image_source_path)
    pdf_bytes = doc.tobytes()
    doc.close()

    with open(temp_pdf_path, "wb") as f:
        f.write(pdf_bytes)

    yield converter, pdf_bytes, temp_pdf_path, default_img_dir, custom_img_dir, text_content_default, text_content_custom, image_source_path

    if os.path.exists(temp_pdf_path):
        os.remove(temp_pdf_path)
    if os.path.exists(default_img_dir):
        shutil.rmtree(default_img_dir)
    if os.path.exists(custom_img_dir):
        shutil.rmtree(custom_img_dir)

class TestPyMuPdfImageExtraction:

    def test_convert_with_image_extraction_default_dir(self, setup_teardown_pdf_and_dirs):
        converter, pdf_bytes, temp_pdf_path, default_img_dir, _, text_content_default, _, _ = setup_teardown_pdf_and_dirs
        result = converter.convert(
            io.BytesIO(pdf_bytes), 
            StreamInfo(extension=".pdf", mimetype="application/pdf", local_path=temp_pdf_path)
        )
        assert isinstance(result, DocumentConverterResult)
        assert text_content_default in result.markdown
        assert result.extracted_image_paths is not None
        assert len(result.extracted_image_paths) == 1
        
        expected_image_path = os.path.join(default_img_dir, "page_1_image_1.jpeg")
        assert os.path.exists(expected_image_path)
        assert result.extracted_image_paths[0] == expected_image_path

    def test_convert_with_image_extraction_custom_dir(self, setup_teardown_pdf_and_dirs):
        converter, _, _, _, custom_img_dir, _, text_content_custom, image_source_path = setup_teardown_pdf_and_dirs
        # Re-create PDF with custom text for this test
        doc = pymupdf.open()
        page = doc.new_page()
        page.insert_text((10, 10), text_content_custom)
        page.insert_image(page.rect, filename=image_source_path)
        custom_pdf_bytes = doc.tobytes()
        doc.close()

        result = converter.convert(
            io.BytesIO(custom_pdf_bytes), 
            StreamInfo(extension=".pdf", mimetype="application/pdf"),
            images_output_dir=custom_img_dir
        )
        assert isinstance(result, DocumentConverterResult)
        assert text_content_custom in result.markdown
        assert result.extracted_image_paths is not None
        assert len(result.extracted_image_paths) == 1
        
        expected_image_path = os.path.join(custom_img_dir, "page_1_image_1.jpeg")
        assert os.path.exists(expected_image_path)
        assert result.extracted_image_paths[0] == expected_image_path
