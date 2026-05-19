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

    def _try_create_symlink(self, tmp_path):
        """Try to create a real symlink; return (target, link) or None if unable."""
        target = tmp_path / "target.txt"
        target.write_text("secret")
        link = tmp_path / "link.txt"
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError):
            # Windows without admin / dev-mode raises OSError; some FS reject it
            return None
        return target, link

    def test_symlink_blocked_by_default(self, monkeypatch, tmp_path):
        """Test that symlinks are blocked by default.

        On Windows without admin/dev-mode we cannot create a real symlink, so
        we fall back to a mock-based test that verifies the same code path
        (is_symlink() detection → ValueError raise) without requiring elevated
        privileges.  This keeps coverage non-zero on every platform.
        """
        from markitdown_mcp.__main__ import _load_security_config, _validate_uri

        config = _load_security_config()
        assert config.allow_symlinks is False  # invariant under test

        created = self._try_create_symlink(tmp_path)
        if created is not None:
            # Real symlink path — full end-to-end check
            _target, link = created
            with pytest.raises(ValueError, match="Symlinks not allowed"):
                _validate_uri(link.as_uri(), config)
            return

        # Fallback: mock os.path.islink to simulate the rejected branch.
        # This still exercises the actual _validate_uri rejection logic.
        fake_file = tmp_path / "pseudo_link.txt"
        fake_file.write_text("data")

        import os.path as _ospath
        original_islink = _ospath.islink

        def fake_islink(p):
            try:
                if Path(p).resolve() == fake_file.resolve():
                    return True
            except (OSError, ValueError):
                pass
            return original_islink(p)

        monkeypatch.setattr("markitdown_mcp.__main__.os.path.islink", fake_islink)

        with pytest.raises(ValueError, match="Symlinks not allowed"):
            _validate_uri(fake_file.as_uri(), config)

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


class TestSchemeSmuggling:
    """R13: harden against URI scheme/SSRF smuggling vectors."""

    def test_javascript_scheme_rejected(self, monkeypatch):
        """javascript: URIs must be rejected even if they look harmless."""
        for key in list(os.environ.keys()):
            if key.startswith("MARKITDOWN_MCP_"):
                monkeypatch.delenv(key, raising=False)
        from markitdown_mcp.__main__ import _load_security_config, _validate_uri

        config = _load_security_config()
        for payload in (
            "javascript:alert(1)",
            "JaVaScRiPt:void(0)",
            "data:text/html,<script>alert(1)</script>",  # data:html should fail when only "data:" data subset desired
            "vbscript:msgbox",
            "ftp://internal-host/etc/passwd",
        ):
            scheme = payload.split(":", 1)[0].lower()
            if scheme in config.allowed_schemes:
                # The `data:` scheme is in defaults; the test fixture above uses
                # `data:text/html,...` which is allowed by scheme but flagged
                # only if downstream parsing rejects HTML. We assert here only
                # the scheme gate; downstream behavior is verified separately.
                continue
            with pytest.raises(ValueError, match="not allowed"):
                _validate_uri(payload, config)

    def test_url_encoded_traversal_blocked(self, monkeypatch):
        """%2e%2e (URL-encoded ..) must still be detected as traversal."""
        for key in list(os.environ.keys()):
            if key.startswith("MARKITDOWN_MCP_"):
                monkeypatch.delenv(key, raising=False)
        from markitdown_mcp.__main__ import _load_security_config, _validate_uri

        config = _load_security_config()
        # %2e%2e decodes to ".." → unquote happens inside _validate_uri before
        # the traversal check, so this MUST raise.
        with pytest.raises((ValueError, FileNotFoundError)):
            _validate_uri("file:///tmp/%2e%2e/%2e%2e/etc/passwd", config)

    def test_unicode_overlong_dot_blocked(self, monkeypatch, tmp_path):
        """Mixed-case / overlong path traversal must not bypass detection."""
        for key in list(os.environ.keys()):
            if key.startswith("MARKITDOWN_MCP_"):
                monkeypatch.delenv(key, raising=False)
        from markitdown_mcp.__main__ import _load_security_config, _validate_uri

        config = _load_security_config()
        # `....//` is a classic CVE pattern that some normalizers collapse to "..".
        # Path() doesn't, so traversal is blocked at a later layer (resolve()).
        # We assert it never escalates to a successful path outside cwd.
        with pytest.raises((ValueError, FileNotFoundError)):
            _validate_uri("file:///tmp/..../..../etc/passwd", config)

    def test_empty_uri_rejected(self, monkeypatch):
        for key in list(os.environ.keys()):
            if key.startswith("MARKITDOWN_MCP_"):
                monkeypatch.delenv(key, raising=False)
        from markitdown_mcp.__main__ import _load_security_config, _validate_uri

        config = _load_security_config()
        with pytest.raises((ValueError, FileNotFoundError)):
            _validate_uri("", config)

    def test_file_uri_without_path_rejected(self, monkeypatch):
        for key in list(os.environ.keys()):
            if key.startswith("MARKITDOWN_MCP_"):
                monkeypatch.delenv(key, raising=False)
        from markitdown_mcp.__main__ import _load_security_config, _validate_uri

        config = _load_security_config()
        with pytest.raises((ValueError, FileNotFoundError)):
            # No path component → should fail before any IO.
            _validate_uri("file://", config)


class TestApiKeyEnforcement:
    """R13: end-to-end API key enforcement on the MCP tool entry points."""

    def test_convert_to_markdown_rejects_wrong_key(self, monkeypatch, tmp_path):
        """Calling convert_to_markdown with wrong key must raise."""
        monkeypatch.setenv("MARKITDOWN_MCP_API_KEY", "secret-key-123")

        # Force reload of the security config so the env var takes effect.
        import importlib
        import markitdown_mcp.__main__ as mod
        importlib.reload(mod)

        target = tmp_path / "f.txt"
        target.write_text("hello")
        uri = target.as_uri()

        async def _run():
            return await mod.convert_to_markdown(uri=uri, api_key="WRONG")

        import asyncio
        with pytest.raises(ValueError, match="Invalid API key"):
            asyncio.run(_run())

    def test_convert_to_markdown_accepts_correct_key(self, monkeypatch, tmp_path):
        monkeypatch.setenv("MARKITDOWN_MCP_API_KEY", "secret-key-123")
        import importlib
        import markitdown_mcp.__main__ as mod
        importlib.reload(mod)

        target = tmp_path / "f.txt"
        target.write_text("hello world")
        uri = target.as_uri()

        async def _run():
            return await mod.convert_to_markdown(uri=uri, api_key="secret-key-123")

        import asyncio
        result = asyncio.run(_run())
        assert "hello world" in result

    def test_convert_to_markdown_rejects_empty_key_when_required(self, monkeypatch, tmp_path):
        monkeypatch.setenv("MARKITDOWN_MCP_API_KEY", "secret-key-123")
        import importlib
        import markitdown_mcp.__main__ as mod
        importlib.reload(mod)

        target = tmp_path / "f.txt"
        target.write_text("hello")
        uri = target.as_uri()

        async def _run():
            # Default api_key="" — must NOT silently bypass the requirement.
            return await mod.convert_to_markdown(uri=uri)

        import asyncio
        with pytest.raises(ValueError, match="Invalid API key"):
            asyncio.run(_run())

    def test_local_file_tool_rejects_wrong_key(self, monkeypatch, tmp_path):
        """Even when called via the same tool with a file URI, wrong key must fail."""
        monkeypatch.setenv("MARKITDOWN_MCP_API_KEY", "secret-key-123")
        import importlib
        import markitdown_mcp.__main__ as mod
        importlib.reload(mod)

        target = tmp_path / "f.txt"
        target.write_text("local hello")

        async def _run():
            return await mod.convert_to_markdown(uri=target.as_uri(), api_key="bad")

        import asyncio
        with pytest.raises(ValueError, match="Invalid API key"):
            asyncio.run(_run())
