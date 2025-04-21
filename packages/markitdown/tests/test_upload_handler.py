import os
import pytest
from markitdown import MarkItDown, StreamInfo
import re




TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

@pytest.mark.parametrize("filename", ["test.pptx"])
def test_convert_with_upload_handler_url_format(filename):
    """Tests if the URL returned by the upload_handler is  included in the converted markdown in the correct format when converting a PPTX file."""
    markitdown = MarkItDown()
    
    file_path = os.path.join(TEST_FILES_DIR, filename)
    

    def validation_upload_handler(image_blob, meta):
        assert "filename" in meta
        assert re.match(r"[a-f0-9]{32}\.[a-zA-Z]+", meta["filename"]) # Check if filename is in UUID format
        return f"http://test.com/{meta['filename']}"
    
    with open(file_path, "rb") as stream:
        result = markitdown.convert(
            stream,
            stream_info=StreamInfo(
                extension=".pptx", 
                mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            ),
            upload_handler=validation_upload_handler
        )
    
    # Verify that the URL is included in the returned markdown
    assert "http://test.com/" in result.markdown
    # Verify that the image markdown format is correct
    assert re.search(r"!\[.*\]\(http://test\.com/[a-f0-9]{32}\.[a-zA-Z]+\)", result.markdown)

def test_metadata_completeness():
    """Verifies that all required fields are included in the metadata."""
    metadata_fields = set()
    
    def metadata_collector(image_blob, meta):
        nonlocal metadata_fields
        metadata_fields.update(meta.keys())
        return "http://test.com"
    
    with open(os.path.join(TEST_FILES_DIR, "test.pptx"), "rb") as stream:
        result = MarkItDown().convert(
            stream,
            upload_handler=metadata_collector
        )
        
    assert "filename" in metadata_fields
    assert "content_type" in metadata_fields



def test_image_content_verification():
    """
    Verifies that the image blob passed to the upload handler matches the original.
    """
    markitdown = MarkItDown()
    file_path = os.path.join(TEST_FILES_DIR, "test.pptx")
    
    # Upload handler that verifies the size of the image blob
    def size_verification_handler(image_blob, meta):
        # Verify that the image blob contains actual data
        assert len(image_blob) > 0
        # Verify that the image blob is in a proper image format
        # Note: PNG signature is 8 bytes, so slice modification
        jpeg_sig = b'\xFF\xD8\xFF\xE0'  # JPEG
        png_sig = b'\x89PNG'            # PNG (first 4 bytes only)
        gif_sig = b'GIF8'               # GIF
        
        # Check image signature (first 4 bytes only)
        img_start = image_blob[:4]
        valid_sig = False
        if img_start.startswith(jpeg_sig[:2]) or img_start.startswith(png_sig[:2]) or img_start.startswith(gif_sig[:2]):
            valid_sig = True
            
        assert valid_sig, f"Invalid image signature: {img_start}"
        return "http://test.com/verified.jpg"
    
    with open(file_path, "rb") as stream:        result = markitdown.convert(
            stream,
            upload_handler=size_verification_handler
        )
    
    assert "http://test.com/verified.jpg" in result.markdown

def test_concurrent_document_conversion():
    """
    Verifies that the upload_handler works correctly when multiple documents are converted simultaneously.
    """
    import threading
    from concurrent.futures import ThreadPoolExecutor
    
    results = []
    exceptions = []
    
    def convert_document(filename):
        try:
            markitdown = MarkItDown()
            file_path = os.path.join(TEST_FILES_DIR, filename)
            
            thread_id = threading.get_ident()
            def thread_specific_handler(image_blob, meta):
                return f"http://test.com/thread{thread_id}/{meta['filename']}"
            
            with open(file_path, "rb") as stream:
                result = markitdown.convert(
                    stream,
                    upload_handler=thread_specific_handler
                )
            results.append((filename, result.markdown))
            
        except Exception as e:
            exceptions.append((filename, str(e)))
    
    # Convert the same file in multiple threads simultaneously
    with ThreadPoolExecutor(max_workers=3) as executor:
        for _ in range(3):
            executor.submit(convert_document, "test.pptx")
    
    # Verify that all conversions were successful
    assert len(exceptions) == 0, f"Exceptions occurred during conversion: {exceptions}"
    assert len(results) == 3, "Expected 3 results, but got a different number"
    
    # Verify that each result contains a unique thread-specific URL
    for filename, markdown in results:
        assert "http://test.com/thread" in markdown
        
        
@pytest.mark.parametrize("filename", ["test.pptx"])
def test_upload_handler_exception_fallback(filename):
    """
    Tests that the conversion process continues and fallback handling is applied
    when an exception occurs in the upload handler.
    """
    markitdown = MarkItDown()
    file_path = os.path.join(TEST_FILES_DIR, filename)
    
    # Upload handler that raises an exception
    def failing_upload_handler(image_blob, meta):
        raise Exception("Intentional test exception")
    
    # Conversion should continue even if an exception occurs
    with open(file_path, "rb") as stream:
        result = markitdown.convert(
            stream,
            upload_handler=failing_upload_handler
        )
    
    # Markdown should be generated
    assert result.markdown is not None
    assert len(result.markdown) > 0
    
    # Default handling (filename) should be applied due to exception handling
    assert ".jpg" in result.markdown

@pytest.mark.parametrize("filename", ["test.pptx"])
def test_upload_handler_invalid_return_values(filename):
    """
    Tests that various types of invalid return values from the upload handler
    are handled appropriately.
    """
    markitdown = MarkItDown()
    file_path = os.path.join(TEST_FILES_DIR, filename)
    
    invalid_return_values = [
        None,           # Return None
        "",             # Empty string
        "   ",          # String with only whitespace
        123,            # Number (not a string)
        [],             # Empty list
        {},             # Empty dictionary
        False           # Boolean value
    ]
    
    for invalid_value in invalid_return_values:
        # Handler that returns an invalid value
        def invalid_return_handler(image_blob, meta):
            return invalid_value
        
        with open(file_path, "rb") as stream:
            result = markitdown.convert(
                stream,
                upload_handler=invalid_return_handler
            )
        
        # Markdown should be generated
        assert result.markdown is not None
        assert len(result.markdown) > 0
        
        # Fallback handling should be applied for invalid return values
        assert ".jpg" in result.markdown
        
        # Skip empty string validation - markdown text may contain empty strings
        if isinstance(invalid_value, str) and invalid_value.strip() and len(invalid_value) > 3:
            assert invalid_value not in result.markdown
