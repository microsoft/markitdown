import io
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from markitdown import MarkItDown
from markitdown.converters import _pdf_converter as module

FILES = Path(__file__).parent / "test_files"


@pytest.mark.parametrize("compressed", [False, True])
def test_real_inline_image_recovers_following_text(compressed, monkeypatch):
    pytest.importorskip("pymupdf")
    path = FILES / f"inline-truncated-{compressed}.pdf"
    recovered = MarkItDown().convert(str(path)).markdown
    assert "AFTER_IMAGE: line 11" in recovered
    monkeypatch.setitem(sys.modules, "pymupdf", None)
    primary = MarkItDown().convert(str(path)).markdown
    assert "BEFORE_IMAGE" in primary
    assert "AFTER_IMAGE" not in primary


def test_mixed_document_preserves_table_and_long_neighbor(monkeypatch):
    pytest.importorskip("pymupdf")
    path = FILES / "inline-truncated-mixed.pdf"
    recovered = MarkItDown().convert(str(path)).markdown
    monkeypatch.setitem(sys.modules, "pymupdf", None)
    primary = MarkItDown().convert(str(path)).markdown
    assert len(primary) > 2048
    assert "AFTER_IMAGE: line 11" in recovered
    table = primary[primary.index("| Item") :]
    assert table in recovered
    assert "Healthy prose line 44" in recovered


@pytest.mark.parametrize(
    "primary,candidate,expected",
    [
        ("", "recovered text", True),
        ("prefix text", "prefix text more words", True),
        ("prefix text", "unrelated much longer candidate text", False),
        ("same text", "same   text", False),
    ],
)
def test_only_strict_text_continuations_are_selected(
    monkeypatch, primary, candidate, expected
):
    page = MagicMock()
    page.get_image_info.return_value = [{"xref": 0}]
    page.get_text.return_value = candidate
    document = MagicMock()
    document.__enter__.return_value = document
    document.__getitem__.return_value = page
    monkeypatch.setitem(
        sys.modules, "pymupdf", SimpleNamespace(open=lambda **kw: document)
    )
    result = module._recover_inline_image_pages(io.BytesIO(b"pdf"), {0: primary})
    assert result == ({0: candidate} if expected else {})
    document.__exit__.assert_called_once()


def test_missing_backend_is_optional(monkeypatch):
    monkeypatch.setitem(sys.modules, "pymupdf", None)
    assert module._recover_inline_image_pages(io.BytesIO(b"pdf"), {0: ""}) == {}


def test_backend_failure_preserves_primary(monkeypatch):
    backend = MagicMock()
    backend.open.side_effect = RuntimeError("broken backend")
    monkeypatch.setitem(sys.modules, "pymupdf", backend)
    assert module._recover_inline_image_pages(io.BytesIO(b"pdf"), {0: "primary"}) == {}
