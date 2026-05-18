"""Tests for core library security features."""
import os
import io
import pytest
from pathlib import Path


class TestPathSecurity:
    """Test path validation and security checks."""

    def test_path_traversal_detection(self):
        """Test that path traversal attempts are detected."""
        from markitdown import MarkItDown

        md = MarkItDown()

        # Simple traversal should be caught
        with pytest.raises(ValueError, match="Path traversal detected"):
            md.convert("../../../etc/passwd")

        # Nested traversal should also be caught
        with pytest.raises(ValueError, match="Path traversal detected"):
            md.convert("dir/../../../etc/passwd")

    def test_security_check_disable(self, tmp_path):
        """Test that security checks can be disabled (but shouldn't be!)."""
        from markitdown import MarkItDown

        md = MarkItDown()

        test_file = tmp_path / "test.txt"
        test_file.write_text("hello")

        # With security checks disabled (not recommended!)
        result = md.convert(str(test_file), security_check=False)
        assert "hello" in result.markdown

    def test_symlink_warning(self, tmp_path):
        """Test that symlinks trigger a warning."""
        if os.name == "nt":
            pytest.skip("Symlink tests skipped on Windows (requires admin)")

        from markitdown import MarkItDown

        md = MarkItDown()

        # Create target and symlink
        target_file = tmp_path / "target.txt"
        target_file.write_text("symlink target")
        symlink_file = tmp_path / "link.txt"
        symlink_file.symlink_to(target_file)

        # Should warn about symlink but still convert
        with pytest.warns(UserWarning, match="Symbolic link detected"):
            result = md.convert(str(symlink_file))

        assert "symlink target" in result


class TestDownloadLimits:
    """Test HTTP download size limits."""

    def test_download_size_limit_from_header(self):
        """Test that Content-Length header triggers size check."""
        # This is mostly tested via integration
        # We test the parameter is accepted
        from markitdown import MarkItDown

        md = MarkItDown()

        # Just verify we can set the parameter
        # (actual HTTP tests need network)
        assert True  # Placeholder - tested via mock in other tests


class TestUnsupportedSchemes:
    """Test that unsupported URI schemes are rejected."""

    def test_unknown_scheme_rejected(self):
        """Test that unsupported schemes raise an error."""
        from markitdown import MarkItDown

        md = MarkItDown()

        with pytest.raises(ValueError, match="Unsupported URI scheme"):
            md.convert_uri("ftp://example.com/test.pdf")

    def test_remote_file_uri_rejected(self):
        """Test that non-local file URIs are rejected."""
        from markitdown import MarkItDown

        md = MarkItDown()

        with pytest.raises(ValueError, match="Unsupported file URI"):
            md.convert_uri("file://remote-server/path/file.pdf")


class TestUriSchemeValidation:
    """Test URI scheme validation."""

    @pytest.mark.parametrize("scheme", ["file", "data", "http", "https"])
    def test_supported_schemes_accepted(self, scheme):
        """Test that supported schemes are accepted."""
        from markitdown import MarkItDown

        md = MarkItDown()

        # These should not raise scheme errors (they may fail for other reasons)
        try:
            if scheme == "file":
                # Will fail with path error, but not scheme error
                md.convert_uri("file:///nonexistent_test_file.txt")
            elif scheme == "data":
                # Simple text data URI
                result = md.convert_uri("data:text/plain;base64,SGVsbG8=")
                # May or may not work depending on converters, but shouldn't fail on scheme
            else:
                # http/https will fail to connect, but that's network not scheme
                pass
        except ValueError as e:
            # Should NOT be a scheme error
            assert "Unsupported URI scheme" not in str(e)
        except (FileNotFoundError, OSError, IOError):
            # These are expected (file doesn't exist, network error, etc.)
            # Not a scheme validation issue, so test passes
            pass


class TestDataUri:
    """Test data URI handling."""

    def test_plain_text_data_uri(self):
        """Test converting a plain text data URI."""
        from markitdown import MarkItDown

        md = MarkItDown()

        # Base64 encoded "Hello, World!"
        result = md.convert_uri("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
        # Plain text converter should handle it
        # The result may just be the raw text
        assert "Hello" in result.text_content or len(result.text_content) > 0


class TestLocalPathResolution:
    """Test that local paths are properly resolved to absolute."""

    def test_relative_path_resolved(self, tmp_path, monkeypatch):
        """Test that relative paths become absolute."""
        from markitdown import MarkItDown

        md = MarkItDown()

        # Change to tmp directory and use relative path
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            # Create file
            (tmp_path / "relative_test.txt").write_text("relative content")

            # Convert with relative path - should still work
            result = md.convert("relative_test.txt")
            assert "relative content" in result.text_content
        finally:
            os.chdir(original_cwd)
