import os
from unittest.mock import Mock
from markitdown import MarkItDown

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

def test_llm_describber_is_called():
    """Tests that the llm_describber is called when provided."""
    # Create a mock llm_describber
    mock_describber = Mock(return_value="A description from the mock.")

    # Initialize MarkItDown with the mock describber
    md = MarkItDown(llm_describber=mock_describber)

    # Convert an image
    image_path = os.path.join(TEST_FILES_DIR, "test.jpg")
    result = md.convert(image_path)

    # Assert that the mock was called
    mock_describber.assert_called_once()

    # Assert that the description is in the markdown
    assert "A description from the mock." in result.markdown
