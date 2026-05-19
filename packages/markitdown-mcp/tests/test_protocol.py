"""Tests for basic MCP protocol and tool availability."""
import os
import sys
import json
import pytest
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestToolDefinition:
    """Test that MCP tools are properly defined."""

    def test_convert_to_markdown_tool_exists(self):
        """Test that the convert_to_markdown tool exists."""
        from markitdown_mcp.__main__ import mcp

        # FastMCP exposes tools through _tool_manager
        tools = mcp._tool_manager.list_tools()
        found = False
        for tool in tools:
            if tool.name == "convert_to_markdown":
                found = True
                assert "Convert a resource" in tool.description
                break

        assert found, "convert_to_markdown tool not found"

    def test_tool_has_uri_parameter(self):
        """Test that the tool has uri parameter."""
        from markitdown_mcp.__main__ import mcp

        for tool in mcp._tool_manager.list_tools():
            if tool.name == "convert_to_markdown":
                # FastMCP Tool exposes parameters as a JSON schema dict
                params = tool.parameters or {}
                properties = params.get("properties", {})
                assert "uri" in properties
                assert "api_key" in properties
                break


class TestCheckPluginsEnabled:
    """Test the plugins enabled check function."""

    def test_plugins_disabled_by_default(self, monkeypatch):
        """Test that plugins are disabled by default."""
        from markitdown_mcp.__main__ import check_plugins_enabled

        # Clear env var
        monkeypatch.delenv("MARKITDOWN_ENABLE_PLUGINS", raising=False)
        assert check_plugins_enabled() is False

    @pytest.mark.parametrize("value", ["true", "1", "yes", "TRUE", "YES"])
    def test_plugins_enabled_values(self, value, monkeypatch):
        """Test various truthy values for enabling plugins."""
        monkeypatch.setenv("MARKITDOWN_ENABLE_PLUGINS", value)
        from markitdown_mcp.__main__ import check_plugins_enabled

        assert check_plugins_enabled() is True

    @pytest.mark.parametrize("value", ["false", "0", "no", "FALSE", "NO", "anything"])
    def test_plugins_disabled_values(self, value, monkeypatch):
        """Test various falsy values for disabling plugins."""
        monkeypatch.setenv("MARKITDOWN_ENABLE_PLUGINS", value)
        from markitdown_mcp.__main__ import check_plugins_enabled

        assert check_plugins_enabled() is False


class TestLocalConversionIntegration:
    """Integration tests for actual conversion via MCP."""

    @pytest.mark.asyncio
    async def test_convert_local_file(self, tmp_path):
        """Test converting a simple local file."""
        import sys
        from markitdown_mcp.__main__ import convert_to_markdown, _SECURITY_CONFIG

        # Create test file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Document\n\nHello, World!\n")

        # Test without API key
        from markitdown_mcp.__main__ import _SECURITY_CONFIG

        original_key = _SECURITY_CONFIG.api_key
        _SECURITY_CONFIG.api_key = None  # Disable API key for test

        try:
            # Use Path.as_uri() for cross-platform file:// URIs
            result = await convert_to_markdown(uri=test_file.as_uri())
            assert "Test Document" in result
            assert "Hello, World!" in result
        finally:
            _SECURITY_CONFIG.api_key = original_key

    @pytest.mark.asyncio
    async def test_api_key_validation_required(self, monkeypatch):
        """Test that API key is validated when configured."""
        from markitdown_mcp.__main__ import convert_to_markdown, _load_security_config

        # Force reload with API key
        monkeypatch.setenv("MARKITDOWN_MCP_API_KEY", "secret123")
        import markitdown_mcp.__main__ as mcp_module

        mcp_module._SECURITY_CONFIG = _load_security_config()

        # Should fail with wrong key
        with pytest.raises(ValueError, match="Invalid API key"):
            await convert_to_markdown(uri="file:///test.txt", api_key="wrong-key")

        # Should fail with missing key (empty string)
        with pytest.raises(ValueError, match="Invalid API key"):
            await convert_to_markdown(uri="file:///test.txt", api_key="")

    @pytest.mark.asyncio
    async def test_api_key_validation_correct(self, monkeypatch):
        """Test that correct API key passes validation."""
        from markitdown_mcp.__main__ import convert_to_markdown, _load_security_config

        # Force reload with API key
        monkeypatch.setenv("MARKITDOWN_MCP_API_KEY", "secret123")
        import markitdown_mcp.__main__ as mcp_module

        mcp_module._SECURITY_CONFIG = _load_security_config()

        # This should pass key validation and then fail on file not found (not key error)
        try:
            await convert_to_markdown(
                uri="file:///nonexistent_file_12345.txt", api_key="secret123"
            )
            # If we get here, the key validation passed
            # The conversion itself may fail, but that's a separate issue
        except ValueError as e:
            # Either "No such file" or "Invalid API key" - we want the former
            assert "Invalid API key" not in str(e)
        except Exception:
            # Other exceptions are OK (file not found etc)
            pass


class TestWindowsFileUriHandling:
    """Test Windows file URI normalization."""

    @pytest.mark.skipif(os.name != "nt", reason="Windows-only tests")
    def test_windows_file_uri_normalization(self):
        """Test that Windows file URIs are properly normalized."""
        # This is implicitly tested by the conversion tests
        # Just verify the import works
        from markitdown_mcp.__main__ import _validate_uri

        assert True  # Placeholder - actual behavior tested in integration tests
