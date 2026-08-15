# `.doc` Extension Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add optional `unword`-backed conversion for legacy `.doc` files and link it to Issue #23.

**Architecture:** Add a focused `DocConverter` that recognizes `.doc`, loads the optional parser lazily, and returns parser body text as `DocumentConverterResult`. Register it independently from `DocxConverter`, expose a `doc` optional dependency, and cover acceptance, conversion, and missing dependency behavior with unit tests.

**Tech Stack:** Python 3.10+, pytest, Hatch, `unword`, existing MarkItDown converter interfaces.

## Global Constraints

- Do not alter `.docx` behavior.
- Do not add binary fixtures or external system-command dependencies.
- Do not attempt extensionless MIME sniffing or rich layout reconstruction.
- Follow existing optional dependency and `MissingDependencyException` patterns.

---

### Task 1: Add failing converter tests

**Files:**
- Create: `packages/markitdown/tests/test_doc_converter.py`

**Interfaces:**
- Consumes: existing `DocConverter` contract and `StreamInfo`.
- Produces: executable expectations for `.doc` acceptance, text conversion, and missing dependency handling.

- [ ] **Step 1: Write the failing tests**

```python
import io
import sys
from types import SimpleNamespace

import pytest

from markitdown._exceptions import MissingDependencyException
from markitdown._stream_info import StreamInfo
from markitdown.converters._doc_converter import DocConverter


def _stream_info(extension: str) -> StreamInfo:
    return StreamInfo(mimetype=None, extension=extension, charset=None)


def test_accepts_doc_but_not_docx_or_other_extensions():
    converter = DocConverter()
    assert converter.accepts(io.BytesIO(b"binary"), _stream_info(".doc"))
    assert not converter.accepts(io.BytesIO(b"binary"), _stream_info(".docx"))
    assert not converter.accepts(io.BytesIO(b"binary"), _stream_info(".txt"))


def test_converts_body_text(monkeypatch):
    class Parsed:
        body_text = "# Heading\n\nLegacy Word text"

    monkeypatch.setitem(sys.modules, "unword", SimpleNamespace(parse_doc=lambda data: Parsed()))
    import markitdown.converters._doc_converter as module
    monkeypatch.setattr(module, "_dependency_exc_info", None)
    monkeypatch.setattr(module, "unword", sys.modules["unword"])

    result = DocConverter().convert(io.BytesIO(b"binary"), _stream_info(".doc"))
    assert result.markdown == "# Heading\n\nLegacy Word text"


def test_reports_missing_dependency(monkeypatch):
    import markitdown.converters._doc_converter as module
    monkeypatch.setattr(module, "_dependency_exc_info", (ImportError, ImportError("missing"), None))
    with pytest.raises(MissingDependencyException, match="doc"):
        DocConverter().convert(io.BytesIO(b"binary"), _stream_info(".doc"))
```

- [ ] **Step 2: Run the focused tests and verify the expected RED failure**

Run: `hatch run test:pytest tests/test_doc_converter.py -q` from `packages/markitdown`.

Expected: collection fails because `markitdown.converters._doc_converter` does not exist.

### Task 2: Implement and register the converter

**Files:**
- Create: `packages/markitdown/src/markitdown/converters/_doc_converter.py`
- Modify: `packages/markitdown/src/markitdown/converters/__init__.py`
- Modify: `packages/markitdown/src/markitdown/_markitdown.py`
- Modify: `packages/markitdown/pyproject.toml`

**Interfaces:**
- Consumes: binary stream and `StreamInfo`.
- Produces: `DocConverter.accepts(...) -> bool` and `DocConverter.convert(...) -> DocumentConverterResult`.

- [ ] **Step 1: Add the minimal converter**

Implement the existing converter pattern: import `unword` optionally, accept only lowercase `.doc`, read the stream bytes, call `unword.parse_doc`, and return `DocumentConverterResult(markdown=parsed.body_text)`; raise `MissingDependencyException` when the optional import failed.

- [ ] **Step 2: Register the converter**

Export `DocConverter`, import it in `_markitdown.py`, and register it immediately before `DocxConverter` so legacy and modern Word formats remain separate.

- [ ] **Step 3: Add dependency metadata**

Add `unword` to `all` and add `doc = ["unword"]` under optional dependencies.

- [ ] **Step 4: Run the focused tests and verify GREEN**

Run: `hatch run test:pytest tests/test_doc_converter.py -q`.

Expected: all three tests pass.

- [ ] **Step 5: Commit the implementation**

```bash
git add packages/markitdown/src/markitdown/converters/_doc_converter.py packages/markitdown/src/markitdown/converters/__init__.py packages/markitdown/src/markitdown/_markitdown.py packages/markitdown/pyproject.toml packages/markitdown/tests/test_doc_converter.py
git commit -m "feat: add legacy doc converter"
```

### Task 3: Verify repository quality

**Files:**
- Modify: only files required by formatter/type checker, if any.

- [ ] **Step 1: Run the package test suite**

Run: `hatch run test:pytest -q` from `packages/markitdown`.

- [ ] **Step 2: Run type checking**

Run: `hatch run types:check` from `packages/markitdown`.

- [ ] **Step 3: Run pre-commit checks**

Run: `pre-commit run --all-files` from the repository root.

- [ ] **Step 4: Review the final diff and status**

Run: `git diff HEAD~2..HEAD --check` and `git status --short`.

- [ ] **Step 5: Push and create the PR**

Run `gh repo fork microsoft/markitdown --remote`, push `feat/doc-extension-support`, then create a PR with title `feat: add legacy .doc conversion support` and body sections for Issue #23, implementation, compatibility, tests, unrun checks, and limitations.
