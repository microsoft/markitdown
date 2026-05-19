"""Auto-validate CONVERTER_MATRIX.md against the actual source tree.

CONVERTER_MATRIX.md is hand-maintained documentation that easily drifts when
converters are added/removed/renamed. This test parses both the doc and the
source tree, then asserts they agree on:

  1. Every converter file has a corresponding matrix row
  2. Every matrix row points to a real `*Converter` class on disk
  3. Class names declared in the matrix actually exist in the source
  4. No orphan matrix rows (referencing dead converters)

Run on every CI build → guarantees the docs never silently rot.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
MATRIX_PATH = REPO_ROOT / "CONVERTER_MATRIX.md"
CONVERTERS_DIR = (
    REPO_ROOT / "packages" / "markitdown" / "src" / "markitdown" / "converters"
)

# Files that live in converters/ but are not user-facing converters.
_INFRA_FILES = {
    "__init__.py",
    "_exiftool.py",
    "_markdownify.py",
    "_converter_error_utils.py",
}

# Utility classes that are correctly documented in the matrix but are NOT
# stand-alone Converter subclasses (e.g. caption helpers used by other
# converters). They live in regular source files but the matrix marks them
# with `††` to indicate utility status. The validator should not require a
# 1:1 file→matrix mapping for these.
_UTILITY_ROW_NAMES = {"LlmCaption", "Transcribe", "LLM Caption"}


# ---------------------------------------------------------------------------
# Source-tree parsing
# ---------------------------------------------------------------------------


def _list_converter_files() -> List[Path]:
    """Return all real converter source files (excluding infra)."""
    if not CONVERTERS_DIR.exists():
        pytest.skip(f"Converters dir not found: {CONVERTERS_DIR}")
    return sorted(
        p
        for p in CONVERTERS_DIR.glob("_*.py")
        if p.name not in _INFRA_FILES
    )


def _extract_converter_class_names(path: Path) -> List[str]:
    """Find all class names ending in 'Converter' inside a source file.

    Uses AST so we never get fooled by occurrences in docstrings/comments.
    """
    src = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(src)
    except SyntaxError as e:  # pragma: no cover
        pytest.fail(f"Cannot parse {path.name}: {e}")
    names: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name.endswith("Converter"):
            names.append(node.name)
    return names


def _all_converter_classes() -> Dict[str, Path]:
    """Map class name → source file for every *Converter class on disk."""
    mapping: Dict[str, Path] = {}
    for f in _list_converter_files():
        for cls in _extract_converter_class_names(f):
            mapping[cls] = f
    return mapping


# ---------------------------------------------------------------------------
# Matrix parsing
# ---------------------------------------------------------------------------

# Row format (column 3 = class, in `backticks`):
# | 1 | **Audio** | `AudioConverter` | ...
# Accept fractional row numbers like "5.5" for insertions between rows.
_MATRIX_ROW_RE = re.compile(
    r"^\|\s*[\d.]+\s*\|\s*\*\*(?P<name>[^*]+)\*\*\s*\|\s*`(?P<cls>[^`]+)`",
    re.MULTILINE,
)


def _parse_matrix_rows() -> List[Tuple[str, str]]:
    """Return list of (display_name, class_name) tuples from the matrix."""
    if not MATRIX_PATH.exists():
        pytest.skip(f"CONVERTER_MATRIX.md not found at {MATRIX_PATH}")
    md = MATRIX_PATH.read_text(encoding="utf-8")
    rows = [(m.group("name").strip(), m.group("cls").strip()) for m in _MATRIX_ROW_RE.finditer(md)]
    if not rows:
        pytest.fail("CONVERTER_MATRIX.md has no parseable rows — format changed?")
    return rows


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_matrix_file_exists():
    assert MATRIX_PATH.is_file(), f"CONVERTER_MATRIX.md missing: {MATRIX_PATH}"


def test_matrix_has_rows():
    rows = _parse_matrix_rows()
    assert len(rows) >= 15, f"Matrix only has {len(rows)} rows — looks broken"


def test_every_matrix_row_points_to_real_class():
    """All `ClassConverter` cells must exist as actual Python classes."""
    rows = _parse_matrix_rows()
    classes = _all_converter_classes()
    missing: List[Tuple[str, str]] = []
    for display, cls in rows:
        if display in _UTILITY_ROW_NAMES or cls in _UTILITY_ROW_NAMES:
            continue
        if cls not in classes:
            missing.append((display, cls))
    assert not missing, (
        "Matrix references classes that don't exist on disk: "
        + ", ".join(f"{d}({c})" for d, c in missing)
    )


def test_every_source_converter_appears_in_matrix():
    """Every *Converter class in source must be documented in the matrix.

    Catches: "I added a new converter but forgot to update the doc."
    """
    rows = _parse_matrix_rows()
    classes = _all_converter_classes()
    # Allow utility classes to be skipped (matrix marks them with ††)
    matrix_classes: Set[str] = {cls for _d, cls in rows}
    orphaned: List[str] = []
    for cls_name in classes:
        if cls_name in matrix_classes:
            continue
        # The base class itself isn't a converter row
        if cls_name == "DocumentConverter":
            continue
        orphaned.append(cls_name)
    assert not orphaned, (
        f"These converter classes are not documented in CONVERTER_MATRIX.md: "
        f"{sorted(orphaned)}"
    )


def test_no_duplicate_class_in_matrix():
    rows = _parse_matrix_rows()
    seen: Set[str] = set()
    dupes: List[str] = []
    for _d, cls in rows:
        if cls in seen:
            dupes.append(cls)
        seen.add(cls)
    assert not dupes, f"Matrix has duplicate class entries: {dupes}"
