import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the module path to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'packages/markitdown/src'))

from markitdown.converters._cu_converter import CUConverter

@pytest.mark.parametrize("api_key_payload", [
    # Exact exploit case: API key in environment variable
    "sk-live-1234567890abcdef1234567890abcdef",
    # Boundary case: Empty API key (should not expose anything)
    "",
    # Valid input: Non-sensitive placeholder
    "placeholder_key",
    # Attack payload: Attempt to extract key via error message
    "../../../etc/passwd",
    # Attack payload: SQL injection style pattern
    "' OR '1'='1' --",
])
def test_api_keys_not_exposed_in_output_or_errors(api_key_payload):
    """Invariant: Converter must never expose API keys in output, logs, or error messages."""
    
    with patch.dict(os.environ, {'AZURE_API_KEY': api_key_payload}):
        # Initialize converter with mocked dependencies to prevent actual API calls
        with patch('azure.ai.documentintelligence.DocumentIntelligenceClient') as mock_client:
            mock_client.return_value = MagicMock()
            
            converter = CUConverter(
                endpoint="https://fake-endpoint.cognitiveservices.azure.com/",
                analyzer_id=None,
                file_types=None
            )
            
            # Test that the API key is not accessible through any public attribute
            assert not hasattr(converter, 'api_key'), "Converter should not store API key as public attribute"
            
            # Test that string representation doesn't contain the key
            converter_str = str(converter)
            assert api_key_payload not in converter_str, f"API key leaked in string representation: {converter_str}"
            
            # Test that repr doesn't contain the key
            converter_repr = repr(converter)
            assert api_key_payload not in converter_repr, f"API key leaked in repr: {converter_repr}"
            
            # Test error handling doesn't expose the key
            try:
                # Force an error by calling convert with invalid input
                converter.convert(None)
            except Exception as e:
                error_str = str(e)
                assert api_key_payload not in error_str, f"API key leaked in error message: {error_str}"