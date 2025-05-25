import unittest
from unittest.mock import patch, MagicMock
import asyncio # Required for IsolatedAsyncioTestCase if not automatically handled

# Import the function to test
from packages.markitdown_mcp.src.markitdown_mcp.__main__ import convert_to_markdown
# Import DocumentConverterResult for type hinting if needed, though mocking might bypass direct need
# from markitdown import DocumentConverterResult # Assuming it's accessible

class TestMcpTool(unittest.IsolatedAsyncioTestCase):

    async def test_uri_with_prefix(self):
        mock_converter_result = MagicMock()
        mock_converter_result.markdown = "some markdown from prefixed uri"

        with patch('packages.markitdown_mcp.src.markitdown_mcp.__main__.MarkItDown') as MockMarkItDown:
            mock_instance = MockMarkItDown.return_value
            mock_instance.convert_uri.return_value = mock_converter_result
            
            await convert_to_markdown(uri="test.txt", prefix="myprefix/")
            
            mock_instance.convert_uri.assert_called_once_with("myprefix/test.txt")

    async def test_uri_without_prefix(self):
        mock_converter_result = MagicMock()
        mock_converter_result.markdown = "some markdown from non-prefixed uri"

        with patch('packages.markitdown_mcp.src.markitdown_mcp.__main__.MarkItDown') as MockMarkItDown:
            mock_instance = MockMarkItDown.return_value
            mock_instance.convert_uri.return_value = mock_converter_result
            
            await convert_to_markdown(uri="test.txt", prefix=None)
            
            mock_instance.convert_uri.assert_called_once_with("test.txt")

    async def test_uri_with_empty_prefix(self):
        mock_converter_result = MagicMock()
        mock_converter_result.markdown = "some markdown from empty prefix uri"

        with patch('packages.markitdown_mcp.src.markitdown_mcp.__main__.MarkItDown') as MockMarkItDown:
            mock_instance = MockMarkItDown.return_value
            mock_instance.convert_uri.return_value = mock_converter_result
            
            await convert_to_markdown(uri="test.txt", prefix="")
            
            mock_instance.convert_uri.assert_called_once_with("test.txt")

if __name__ == '__main__':
    unittest.main()
