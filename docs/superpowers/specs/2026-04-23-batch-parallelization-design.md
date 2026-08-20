# Batch Parallelization Design

**Date:** 2026-04-23
**Scope:** Add parallel batch conversion to the `markitdown` library and CLI.

---

## Goals

- Convert multiple local files concurrently from both the library API and CLI.
- Return results in arrival order (completion order, not input order).
- Let callers choose between fail-fast and collect-and-continue error handling.
- Default to `ThreadPoolExecutor`; allow callers to plug in any `concurrent.futures.Executor`.

## Out of Scope

- Parallelism _within_ a single document.
- Async / `asyncio` interface.
- Remote URL batch fetching (future work).

---

## Library API

### New dataclass: `BatchConversionResult`

Added to `_base_converter.py` alongside the existing `DocumentConverterResult`.

```python
from dataclasses import dataclass
from typing import Optional, Union
from pathlib import Path

@dataclass
class BatchConversionResult:
    source: Union[str, Path]                  # original input value
    result: Optional[DocumentConverterResult] = None
    error: Optional[Exception] = None

    @property
    def success(self) -> bool:
        return self.error is None
```

### New method: `MarkItDown.convert_batch()`

```python
def convert_batch(
    self,
    sources: Iterable[Union[str, Path, BinaryIO, requests.Response]],
    *,
    on_error: Literal["raise", "collect"] = "collect",
    workers: Optional[int] = None,
    executor: Optional[concurrent.futures.Executor] = None,
    **kwargs,
) -> Iterator[BatchConversionResult]:
```

**Parameters:**

| Parameter | Default | Description |
|---|---|---|
| `sources` | required | Any iterable of inputs accepted by `convert()` |
| `on_error` | `"collect"` | `"collect"` wraps errors and continues; `"raise"` re-raises the first error |
| `workers` | `min(32, cpu_count + 4)` | Thread count when no `executor` is provided |
| `executor` | `None` | If provided, used directly; caller owns its lifecycle |
| `**kwargs` | — | Passed through to each `convert()` call |

**Behaviour:**

- Yields `BatchConversionResult` instances in **completion order** via `concurrent.futures.as_completed()`.
- When `on_error="collect"`: exceptions are caught per-future and wrapped in `BatchConversionResult(source=..., error=...)`.
- When `on_error="raise"`: first exception is re-raised; remaining futures are cancelled.
- When `executor` is `None`: a `ThreadPoolExecutor(max_workers=workers)` is created internally and shut down after all futures resolve.
- When `executor` is provided: `convert_batch()` submits work to it but does **not** call `shutdown()`.

**Note on `ProcessPoolExecutor`:** Passing a `ProcessPoolExecutor` is unsupported — `MarkItDown` is not reliably picklable. No helper or workaround is provided.

---

## CLI Changes

### Updated argument: `filename`

Changed from `nargs="?"` to `nargs="*"`. Stdin mode activates when no filenames are given (unchanged).

### New flags

| Flag | Description |
|---|---|
| `--workers N` | Number of parallel threads (default: library default) |
| `--fail-fast` | Exit on first conversion error (default: collect and continue) |
| `--output-dir DIR` | Write each result to `<DIR>/<stem>.md` instead of stdout |

### Output rules

| Scenario | Behaviour |
|---|---|
| Single file, no `--output-dir` | Unchanged: stdout or `-o file` |
| Multiple files, no `--output-dir` | Results printed to stdout in arrival order, each preceded by `--- <source> ---` |
| Multiple files, `--output-dir` | Each result written to `<DIR>/<original_filename>.md` (e.g., `report.pdf` → `report.pdf.md`) to avoid collisions; progress lines printed to stderr |
| Error in collect mode | Error message printed to stderr; processing continues |
| Error in fail-fast mode | Error printed to stderr; exit code 1 |

---

## Thread Safety

| Shared state | Assessment |
|---|---|
| `self._converters` | Read-only after construction. Safe. |
| `self._requests_session` | `requests.Session` is documented thread-safe. Safe. |
| `self._magika` | ONNX inference is safe for concurrent reads. Safe. |
| Individual converters | All stateless per-call; no mutable instance state. Safe. |

No locks are required.

---

## Files to Change

| File | Change |
|---|---|
| `packages/markitdown/src/markitdown/_base_converter.py` | Add `BatchConversionResult` dataclass |
| `packages/markitdown/src/markitdown/_markitdown.py` | Add `convert_batch()` method; export `BatchConversionResult` |
| `packages/markitdown/src/markitdown/__init__.py` | Export `BatchConversionResult` |
| `packages/markitdown/src/markitdown/__main__.py` | Multi-file CLI: `nargs="*"`, `--workers`, `--fail-fast`, `--output-dir` |
