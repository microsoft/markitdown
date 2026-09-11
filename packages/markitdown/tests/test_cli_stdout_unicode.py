"""Regression tests for #1802 / #1788.

The CLI's stdout output path historically raised
``UnicodeEncodeError: 'charmap' codec can't encode characters`` on
Windows when the converted markdown contained Unicode characters the
local console codepage couldn't represent (bullets, em-dashes, CJK).
A subsequent fix re-encoded with ``errors="replace"`` to silence the
crash, but at the cost of silently substituting ``?`` for any
unencodable character — users redirecting to a file got corrupted
output.

The current fix reconfigures ``sys.stdout`` to UTF-8 before printing,
preserving every character. The ``errors="replace"`` round-trip
remains as a defensive fallback for stdout objects that don't support
reconfiguration.
"""

from __future__ import annotations

import io
import sys
from unittest.mock import MagicMock

from markitdown.__main__ import _handle_output


class _FakeResult:
    def __init__(self, markdown: str) -> None:
        self.markdown = markdown


def _make_args(output: str | None) -> MagicMock:
    args = MagicMock()
    args.output = output
    return args


def test_handle_output_to_file_preserves_unicode(tmp_path):
    """File output already used utf-8 — pin that contract."""
    out = tmp_path / "out.md"
    args = _make_args(str(out))
    payload = "Bullet • em–dash 中文 日本語 한글"
    _handle_output(args, _FakeResult(payload))

    written = out.read_text(encoding="utf-8")
    assert written == payload


def test_handle_output_to_stdout_reconfigures_to_utf8(monkeypatch, capsys):
    """When stdout supports ``reconfigure``, the CLI must switch it to
    UTF-8 so unicode characters survive instead of being replaced.

    pytest's ``capsys`` already binds stdout to a UTF-8 wrapper, but the
    point of this test is to assert the CLI *invokes* ``reconfigure``
    rather than rely on the runtime defaults. We patch
    ``sys.stdout.reconfigure`` to record the call.
    """
    calls: list[dict] = []
    real_reconfigure = getattr(sys.stdout, "reconfigure", None)

    def _spy(**kwargs):
        calls.append(kwargs)
        if real_reconfigure is not None:
            try:
                real_reconfigure(**kwargs)
            except (OSError, ValueError):
                pass

    monkeypatch.setattr(sys.stdout, "reconfigure", _spy, raising=False)

    args = _make_args(None)
    payload = "Bullet • em–dash 中文"
    _handle_output(args, _FakeResult(payload))

    captured = capsys.readouterr()
    assert payload in captured.out, (
        "regression #1802: unicode characters must survive stdout output, "
        "not be replaced with '?'"
    )
    assert calls and calls[0].get("encoding") == "utf-8", (
        "expected sys.stdout.reconfigure(encoding='utf-8') to be invoked"
    )


def test_handle_output_falls_back_when_reconfigure_unavailable(monkeypatch, capsys):
    """If stdout exposes no ``reconfigure`` (older Python or unusual
    stdout objects), the helper must still avoid crashing — the
    ``errors="replace"`` path is the legacy safety net."""

    class _NoReconfigureWriter(io.TextIOBase):
        encoding = "ascii"

        def __init__(self) -> None:
            self._lines: list[str] = []

        def writable(self) -> bool:  # type: ignore[override]
            return True

        def write(self, s: str) -> int:  # type: ignore[override]
            # Simulate a strict ASCII codec that rejects non-ASCII.
            s.encode("ascii")
            self._lines.append(s)
            return len(s)

        def flush(self) -> None:  # type: ignore[override]
            return None

    fake = _NoReconfigureWriter()
    monkeypatch.setattr(sys, "stdout", fake)
    monkeypatch.setattr(sys.stdout, "encoding", "ascii", raising=False)

    args = _make_args(None)
    # Should not raise even though the payload has non-ASCII characters
    # and stdout has no reconfigure().
    _handle_output(args, _FakeResult("hi • there"))
    # The lossy replacement path is acceptable here — non-ASCII becomes ?
    assert "hi" in "".join(fake._lines)
    assert "there" in "".join(fake._lines)
