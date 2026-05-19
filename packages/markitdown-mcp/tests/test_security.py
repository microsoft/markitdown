"""Tests for MCP server security features."""
import os
import sys
import pytest
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestSecurityConfig:
    """Test security configuration loading."""

    def test_default_config(self, monkeypatch):
        """Test default security configuration."""
        # Clear all security env vars
        for key in list(os.environ.keys()):
            if key.startswith("MARKITDOWN_MCP_"):
                monkeypatch.delenv(key, raising=False)

        from markitdown_mcp.__main__ import _load_security_config

        config = _load_security_config()
        assert config.api_key is None
        assert config.allowed_paths is None
        assert config.allowed_schemes == ["file", "http", "https", "data"]
        assert config.max_file_size == 50 * 1024 * 1024  # 50MB
        assert config.allow_symlinks is False

    def test_api_key_config(self, monkeypatch):
        """Test API key configuration."""
        monkeypatch.setenv("MARKITDOWN_MCP_API_KEY", "test-secret-key")
        from markitdown_mcp.__main__ import _load_security_config

        config = _load_security_config()
        assert config.api_key == "test-secret-key"

    def test_allowed_paths_config(self, monkeypatch, tmp_path):
        """Test allowed paths whitelist."""
        path1 = tmp_path / "docs"
        path2 = tmp_path / "reports"
        path1.mkdir()
        path2.mkdir()

        separator = ";" if os.name == "nt" else ":"
        monkeypatch.setenv("MARKITDOWN_MCP_ALLOWED_PATHS", f"{path1}{separator}{path2}")

        from markitdown_mcp.__main__ import _load_security_config

        config = _load_security_config()
        assert config.allowed_paths is not None
        assert len(config.allowed_paths) == 2
        assert path1.resolve() in config.allowed_paths
        assert path2.resolve() in config.allowed_paths

    def test_allowed_schemes_config(self, monkeypatch):
        """Test allowed URI schemes."""
        monkeypatch.setenv("MARKITDOWN_MCP_ALLOWED_SCHEMES", "file,https")

        from markitdown_mcp.__main__ import _load_security_config

        config = _load_security_config()
        assert config.allowed_schemes == ["file", "https"]

    def test_max_file_size_config(self, monkeypatch):
        """Test max file size configuration."""
        monkeypatch.setenv("MARKITDOWN_MCP_MAX_FILE_SIZE", "10485760")  # 10MB

        from markitdown_mcp.__main__ import _load_security_config

        config = _load_security_config()
        assert config.max_file_size == 10 * 1024 * 1024


class TestUriValidation:
    """Test URI validation security."""

    def test_disallowed_scheme(self, monkeypatch):
        """Test that disallowed schemes are rejected."""
        monkeypatch.setenv("MARKITDOWN_MCP_ALLOWED_SCHEMES", "file,https")

        from markitdown_mcp.__main__ import _load_security_config, _validate_uri

        config = _load_security_config()

        # http: should be rejected (only https allowed)
        with pytest.raises(ValueError, match="scheme.*not allowed"):
            _validate_uri("http://example.com/test.pdf", config)

        # file: should work
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"test")
            f.flush()
            path = f.name

        try:
            normalized = _validate_uri(Path(path).as_uri(), config)
            assert normalized == Path(path).as_uri()
        finally:
            os.unlink(path)

    def test_path_traversal_blocked(self, monkeypatch):
        """Test that path traversal attempts are blocked."""
        from markitdown_mcp.__main__ import _load_security_config, _validate_uri

        config = _load_security_config()

        # This should be caught by Path.resolve() normalizing out the ".."
        # but we still test for it
        with pytest.raises((ValueError, FileNotFoundError)):
            _validate_uri("file:///etc/../../../etc/passwd", config)

    def test_file_size_limit(self, monkeypatch, tmp_path):
        """Test that files exceeding size limit are rejected."""
        monkeypatch.setenv("MARKITDOWN_MCP_MAX_FILE_SIZE", "100")  # 100 bytes

        from markitdown_mcp.__main__ import _load_security_config, _validate_uri

        config = _load_security_config()

        # Small file should pass
        small_file = tmp_path / "small.txt"
        small_file.write_text("x" * 50)
        result = _validate_uri(small_file.as_uri(), config)
        assert result == small_file.as_uri()

        # Large file should be rejected
        large_file = tmp_path / "large.txt"
        large_file.write_text("x" * 200)
        with pytest.raises(ValueError, match="too large"):
            _validate_uri(large_file.as_uri(), config)

    def test_symlink_blocked_by_default(self, monkeypatch, tmp_path):
        """Test that symlinks are blocked by default."""
        if os.name == "nt":
            pytest.skip("Symlink tests skipped on Windows (requires admin)")

        from markitdown_mcp.__main__ import _load_security_config, _validate_uri

        config = _load_security_config()

        # Create target file and symlink
        target_file = tmp_path / "target.txt"
        target_file.write_text("secret")
        symlink_path = tmp_path / "link.txt"
        symlink_path.symlink_to(target_file)

        # Symlink should be blocked
        with pytest.raises(ValueError, match="Symlinks not allowed"):
            _validate_uri(f"file://{symlink_path}", config)

    def test_whitelist_path_restriction(self, monkeypatch, tmp_path):
        """Test that only whitelisted paths are allowed."""
        allowed_dir = tmp_path / "allowed"
        forbidden_dir = tmp_path / "forbidden"
        allowed_dir.mkdir()
        forbidden_dir.mkdir()

        monkeypatch.setenv("MARKITDOWN_MCP_ALLOWED_PATHS", str(allowed_dir))

        from markitdown_mcp.__main__ import _load_security_config, _validate_uri

        config = _load_security_config()

        # File in allowed directory should work
        allowed_file = allowed_dir / "test.txt"
        allowed_file.write_text("test")
        result = _validate_uri(allowed_file.as_uri(), config)
        assert result == allowed_file.as_uri()

        # File outside allowed directory should be blocked
        forbidden_file = forbidden_dir / "test.txt"
        forbidden_file.write_text("test")
        with pytest.raises(ValueError, match="not in allowed list"):
            _validate_uri(forbidden_file.as_uri(), config)


class TestShowSecurityConfig:
    """Test the --show-security-config flag."""

    def test_help_includes_security_flag(self, capsys):
        """Test that --show-security-config appears in help."""
        from markitdown_mcp.__main__ import main

        with pytest.raises(SystemExit):
            sys.argv = ["markitdown-mcp", "--help"]
            main()

        captured = capsys.readouterr()
        assert "--show-security-config" in captured.out
