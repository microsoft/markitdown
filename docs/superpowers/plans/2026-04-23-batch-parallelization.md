# Batch Parallelization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add parallel batch conversion to the `markitdown` library (`convert_batch()`) and CLI (multi-file arguments).

**Architecture:** A new `BatchConversionResult` dataclass pairs each result with its source. `convert_batch()` submits all conversions to a `ThreadPoolExecutor` and yields results in completion order via `as_completed()`. The CLI multi-file path calls `convert_batch()` and routes output to stdout or `--output-dir`.

**Tech Stack:** Python 3.10+, `concurrent.futures.ThreadPoolExecutor`, `concurrent.futures.as_completed`, `dataclasses`

---

## File Map

| File | Change |
|---|---|
| `packages/markitdown/src/markitdown/_base_converter.py` | Add `BatchConversionResult` dataclass |
| `packages/markitdown/src/markitdown/_markitdown.py` | Add `convert_batch()` method |
| `packages/markitdown/src/markitdown/__init__.py` | Export `BatchConversionResult` |
| `packages/markitdown/src/markitdown/__main__.py` | Multi-file CLI: `nargs="*"`, `--workers`, `--fail-fast`, `--output-dir` |
| `packages/markitdown/tests/test_batch.py` | New test file for library batch API |
| `packages/markitdown/tests/test_cli_misc.py` | Extend with CLI batch tests |

---

## Task 1: Add `BatchConversionResult` dataclass

**Files:**
- Modify: `packages/markitdown/src/markitdown/_base_converter.py`
- Create: `packages/markitdown/tests/test_batch.py`

- [ ] **Step 1: Write the failing test**

Create `packages/markitdown/tests/test_batch.py`:

```python
import pytest
from markitdown._base_converter import BatchConversionResult, DocumentConverterResult


def test_batch_result_success_true():
    r = BatchConversionResult(
        source="test.txt",
        result=DocumentConverterResult(markdown="# Hello"),
    )
    assert r.success is True
    assert r.result is not None
    assert r.error is None


def test_batch_result_success_false():
    r = BatchConversionResult(source="test.txt", error=ValueError("oops"))
    assert r.success is False
    assert r.result is None
    assert r.error is not None


def test_batch_result_defaults():
    r = BatchConversionResult(source="test.txt")
    assert r.result is None
    assert r.error is None
    assert r.success is True
```

- [ ] **Step 2: Run test to verify it fails**

```
cd packages/markitdown
pytest tests/test_batch.py -v
```

Expected: `ImportError` — `BatchConversionResult` does not exist yet.

- [ ] **Step 3: Add `BatchConversionResult` to `_base_converter.py`**

Add the following imports at the top of `packages/markitdown/src/markitdown/_base_converter.py`:

```python
from dataclasses import dataclass, field
```

Add this class **after** `DocumentConverterResult` and **before** `DocumentConverter`:

```python
@dataclass
class BatchConversionResult:
    """Result of a single conversion within a convert_batch() call."""

    source: Any  # The original input passed to convert_batch()
    result: Optional["DocumentConverterResult"] = None
    error: Optional[Exception] = None

    @property
    def success(self) -> bool:
        return self.error is None
```

The existing `from typing import Any, BinaryIO, Optional` import already covers `Any` and `Optional`.

- [ ] **Step 4: Run test to verify it passes**

```
cd packages/markitdown
pytest tests/test_batch.py -v
```

Expected: 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add packages/markitdown/src/markitdown/_base_converter.py packages/markitdown/tests/test_batch.py
git commit -m "feat: add BatchConversionResult dataclass"
```

---

## Task 2: Add `convert_batch()` to `MarkItDown`

**Files:**
- Modify: `packages/markitdown/src/markitdown/_markitdown.py`
- Modify: `packages/markitdown/tests/test_batch.py`

- [ ] **Step 1: Write the failing tests**

Append to `packages/markitdown/tests/test_batch.py`:

```python
import os
import concurrent.futures
from markitdown import MarkItDown, BatchConversionResult, DocumentConverterResult

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")


def test_convert_batch_basic():
    md = MarkItDown()
    sources = [
        os.path.join(TEST_FILES_DIR, "test.docx"),
        os.path.join(TEST_FILES_DIR, "test.pdf"),
        os.path.join(TEST_FILES_DIR, "test.pptx"),
    ]
    results = list(md.convert_batch(sources))
    assert len(results) == 3
    assert all(isinstance(r, BatchConversionResult) for r in results)
    assert all(r.success for r in results)
    assert all(isinstance(r.result, DocumentConverterResult) for r in results)
    assert {r.source for r in results} == set(sources)


def test_convert_batch_on_error_collect():
    md = MarkItDown()
    sources = [
        os.path.join(TEST_FILES_DIR, "test.docx"),
        os.path.join(TEST_FILES_DIR, "nonexistent_file_xyz.docx"),
    ]
    results = list(md.convert_batch(sources, on_error="collect"))
    assert len(results) == 2
    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]
    assert len(successful) == 1
    assert len(failed) == 1
    assert failed[0].error is not None


def test_convert_batch_on_error_raise():
    md = MarkItDown()
    sources = [os.path.join(TEST_FILES_DIR, "nonexistent_file_xyz.docx")]
    with pytest.raises(Exception):
        list(md.convert_batch(sources, on_error="raise"))


def test_convert_batch_invalid_on_error():
    md = MarkItDown()
    with pytest.raises(ValueError, match="on_error"):
        list(md.convert_batch([], on_error="bad_value"))


def test_convert_batch_empty():
    md = MarkItDown()
    results = list(md.convert_batch([]))
    assert results == []


def test_convert_batch_custom_executor():
    md = MarkItDown()
    sources = [
        os.path.join(TEST_FILES_DIR, "test.docx"),
        os.path.join(TEST_FILES_DIR, "test.pdf"),
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = list(md.convert_batch(sources, executor=executor))
    assert len(results) == 2
    assert all(r.success for r in results)


def test_convert_batch_workers_param():
    md = MarkItDown()
    sources = [
        os.path.join(TEST_FILES_DIR, "test.docx"),
        os.path.join(TEST_FILES_DIR, "test.pdf"),
    ]
    results = list(md.convert_batch(sources, workers=1))
    assert len(results) == 2
    assert all(r.success for r in results)
```

- [ ] **Step 2: Run tests to verify they fail**

```
cd packages/markitdown
pytest tests/test_batch.py -v
```

Expected: `AttributeError` — `MarkItDown` has no `convert_batch`.

- [ ] **Step 3: Add imports to `_markitdown.py`**

At the top of `packages/markitdown/src/markitdown/_markitdown.py`, add to the existing imports:

```python
import concurrent.futures
from typing import Any, List, Dict, Optional, Union, BinaryIO, Iterator, Iterable
```

(Replace the existing `from typing import Any, List, Dict, Optional, Union, BinaryIO` line — just add `Iterator, Iterable` to it.)

Also add to the `_base_converter` import line:

```python
from ._base_converter import DocumentConverter, DocumentConverterResult, BatchConversionResult
```

- [ ] **Step 4: Add `convert_batch()` method to `MarkItDown`**

Add this method to the `MarkItDown` class in `_markitdown.py`, after the `convert()` method (around line 300):

```python
def convert_batch(
    self,
    sources: Iterable[Union[str, Path, BinaryIO, "requests.Response"]],
    *,
    on_error: str = "collect",
    workers: Optional[int] = None,
    executor: Optional[concurrent.futures.Executor] = None,
    **kwargs: Any,
) -> Iterator[BatchConversionResult]:
    """Convert multiple sources concurrently.

    Yields BatchConversionResult instances in completion order.

    Args:
        sources: Iterable of inputs accepted by convert().
        on_error: "collect" wraps errors and continues; "raise" re-raises the first error.
        workers: Thread count when no executor is provided. Defaults to min(32, cpu_count+4).
        executor: If provided, used directly; caller owns its lifecycle.
        **kwargs: Passed through to each convert() call.
    """
    if on_error not in ("collect", "raise"):
        raise ValueError(f"on_error must be 'collect' or 'raise', got {on_error!r}")

    own_executor = executor is None
    _executor = executor or concurrent.futures.ThreadPoolExecutor(
        max_workers=workers or min(32, (os.cpu_count() or 1) + 4)
    )

    try:
        future_to_source = {
            _executor.submit(self.convert, source, **kwargs): source
            for source in sources
        }

        for future in concurrent.futures.as_completed(future_to_source):
            source = future_to_source[future]
            exc = future.exception()
            if exc is not None:
                if on_error == "raise":
                    for f in future_to_source:
                        f.cancel()
                    raise exc
                yield BatchConversionResult(source=source, error=exc)
            else:
                yield BatchConversionResult(source=source, result=future.result())
    finally:
        if own_executor:
            _executor.shutdown(wait=False, cancel_futures=True)
```

- [ ] **Step 5: Run tests to verify they pass**

```
cd packages/markitdown
pytest tests/test_batch.py -v
```

Expected: All tests PASS.

- [ ] **Step 6: Commit**

```bash
git add packages/markitdown/src/markitdown/_markitdown.py packages/markitdown/tests/test_batch.py
git commit -m "feat: add convert_batch() method to MarkItDown"
```

---

## Task 3: Export `BatchConversionResult` from `__init__.py`

**Files:**
- Modify: `packages/markitdown/src/markitdown/__init__.py`
- Modify: `packages/markitdown/tests/test_batch.py`

- [ ] **Step 1: Write the failing test**

Add to `packages/markitdown/tests/test_batch.py`:

```python
def test_batch_result_public_import():
    from markitdown import BatchConversionResult as BCR
    assert BCR is BatchConversionResult
```

- [ ] **Step 2: Run test to verify it fails**

```
cd packages/markitdown
pytest tests/test_batch.py::test_batch_result_public_import -v
```

Expected: `ImportError` — `BatchConversionResult` not in `markitdown.__init__`.

- [ ] **Step 3: Update `__init__.py`**

In `packages/markitdown/src/markitdown/__init__.py`:

Change:
```python
from ._base_converter import DocumentConverterResult, DocumentConverter
```
To:
```python
from ._base_converter import DocumentConverterResult, DocumentConverter, BatchConversionResult
```

Add `"BatchConversionResult"` to the `__all__` list:
```python
__all__ = [
    "__version__",
    "MarkItDown",
    "DocumentConverter",
    "DocumentConverterResult",
    "BatchConversionResult",
    "MarkItDownException",
    "MissingDependencyException",
    "FailedConversionAttempt",
    "FileConversionException",
    "UnsupportedFormatException",
    "StreamInfo",
    "PRIORITY_SPECIFIC_FILE_FORMAT",
    "PRIORITY_GENERIC_FILE_FORMAT",
]
```

- [ ] **Step 4: Run test to verify it passes**

```
cd packages/markitdown
pytest tests/test_batch.py -v
```

Expected: All tests PASS.

- [ ] **Step 5: Commit**

```bash
git add packages/markitdown/src/markitdown/__init__.py packages/markitdown/tests/test_batch.py
git commit -m "feat: export BatchConversionResult from public API"
```

---

## Task 4: Update CLI for multi-file batch support

**Files:**
- Modify: `packages/markitdown/src/markitdown/__main__.py`
- Modify: `packages/markitdown/tests/test_cli_misc.py`

- [ ] **Step 1: Write the failing tests**

Append to `packages/markitdown/tests/test_cli_misc.py`:

```python
import os
import tempfile

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")


def test_cli_multi_file_stdout():
    result = subprocess.run(
        [
            "python", "-m", "markitdown",
            os.path.join(TEST_FILES_DIR, "test.docx"),
            os.path.join(TEST_FILES_DIR, "test.pdf"),
        ],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    assert "--- " in result.stdout


def test_cli_multi_file_output_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        result = subprocess.run(
            [
                "python", "-m", "markitdown",
                os.path.join(TEST_FILES_DIR, "test.docx"),
                os.path.join(TEST_FILES_DIR, "test.pdf"),
                "--output-dir", tmp_dir,
            ],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"CLI failed: {result.stderr}"
        assert os.path.exists(os.path.join(tmp_dir, "test.docx.md"))
        assert os.path.exists(os.path.join(tmp_dir, "test.pdf.md"))


def test_cli_multi_file_fail_fast():
    result = subprocess.run(
        [
            "python", "-m", "markitdown",
            os.path.join(TEST_FILES_DIR, "nonexistent_xyz.pdf"),
            "--fail-fast",
        ],
        capture_output=True, text=True,
    )
    assert result.returncode == 1


def test_cli_multi_file_collect_errors():
    result = subprocess.run(
        [
            "python", "-m", "markitdown",
            os.path.join(TEST_FILES_DIR, "test.docx"),
            os.path.join(TEST_FILES_DIR, "nonexistent_xyz.pdf"),
        ],
        capture_output=True, text=True,
    )
    assert result.returncode == 1
    assert "Error" in result.stderr


def test_cli_workers_flag():
    result = subprocess.run(
        [
            "python", "-m", "markitdown",
            os.path.join(TEST_FILES_DIR, "test.docx"),
            os.path.join(TEST_FILES_DIR, "test.pdf"),
            "--workers", "2",
        ],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
```

- [ ] **Step 2: Run tests to verify they fail**

```
cd packages/markitdown
pytest tests/test_cli_misc.py -v
```

Expected: The new tests FAIL — `--output-dir`, `--workers`, `--fail-fast` are unknown flags; `filename` only accepts one value.

- [ ] **Step 3: Update `__main__.py`**

Replace the entire `main()` function in `packages/markitdown/src/markitdown/__main__.py` with:

```python
def main():
    parser = argparse.ArgumentParser(
        description="Convert various file formats to markdown.",
        prog="markitdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=dedent(
            """
            SYNTAX:

                markitdown <OPTIONAL: FILENAME [FILENAME ...]>
                If FILENAME is empty, markitdown reads from stdin.

            EXAMPLES:

                markitdown example.pdf

                markitdown file1.pdf file2.docx file3.html

                cat example.pdf | markitdown

                markitdown example.pdf -o example.md

                markitdown file1.pdf file2.docx --output-dir ./output/
            """
        ).strip(),
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="show the version number and exit",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output file name. Only valid for single-file conversion.",
    )

    parser.add_argument(
        "--output-dir",
        help="Output directory for batch conversion. Each file is written to <dir>/<filename>.md.",
    )

    parser.add_argument(
        "-x",
        "--extension",
        help="Provide a hint about the file extension (e.g., when reading from stdin).",
    )

    parser.add_argument(
        "-m",
        "--mime-type",
        help="Provide a hint about the file's MIME type.",
    )

    parser.add_argument(
        "-c",
        "--charset",
        help="Provide a hint about the file's charset (e.g, UTF-8).",
    )

    parser.add_argument(
        "-d",
        "--use-docintel",
        action="store_true",
        help="Use Document Intelligence to extract text instead of offline conversion.",
    )

    parser.add_argument(
        "-e",
        "--endpoint",
        type=str,
        help="Document Intelligence Endpoint.",
    )

    parser.add_argument(
        "-p",
        "--use-plugins",
        action="store_true",
        help="Use 3rd-party plugins to convert files.",
    )

    parser.add_argument(
        "--list-plugins",
        action="store_true",
        help="List installed 3rd-party plugins.",
    )

    parser.add_argument(
        "--keep-data-uris",
        action="store_true",
        help="Keep data URIs in the output.",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Number of parallel threads for batch conversion.",
    )

    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Abort batch conversion on the first error (default: collect errors and continue).",
    )

    parser.add_argument("filename", nargs="*")
    args = parser.parse_args()

    # Parse the extension hint
    extension_hint = args.extension
    if extension_hint is not None:
        extension_hint = extension_hint.strip().lower()
        if len(extension_hint) > 0:
            if not extension_hint.startswith("."):
                extension_hint = "." + extension_hint
        else:
            extension_hint = None

    # Parse the mime type
    mime_type_hint = args.mime_type
    if mime_type_hint is not None:
        mime_type_hint = mime_type_hint.strip()
        if len(mime_type_hint) > 0:
            if mime_type_hint.count("/") != 1:
                _exit_with_error(f"Invalid MIME type: {mime_type_hint}")
        else:
            mime_type_hint = None

    # Parse the charset
    charset_hint = args.charset
    if charset_hint is not None:
        charset_hint = charset_hint.strip()
        if len(charset_hint) > 0:
            try:
                charset_hint = codecs.lookup(charset_hint).name
            except LookupError:
                _exit_with_error(f"Invalid charset: {charset_hint}")
        else:
            charset_hint = None

    stream_info = None
    if (
        extension_hint is not None
        or mime_type_hint is not None
        or charset_hint is not None
    ):
        stream_info = StreamInfo(
            extension=extension_hint, mimetype=mime_type_hint, charset=charset_hint
        )

    if args.list_plugins:
        print("Installed MarkItDown 3rd-party Plugins:\n")
        plugin_entry_points = list(entry_points(group="markitdown.plugin"))
        if len(plugin_entry_points) == 0:
            print("  * No 3rd-party plugins installed.")
            print(
                "\nFind plugins by searching for the hashtag #markitdown-plugin on GitHub.\n"
            )
        else:
            for entry_point in plugin_entry_points:
                print(f"  * {entry_point.name:<16}\t(package: {entry_point.value})")
            print(
                "\nUse the -p (or --use-plugins) option to enable 3rd-party plugins.\n"
            )
        sys.exit(0)

    if args.use_docintel:
        if args.endpoint is None:
            _exit_with_error(
                "Document Intelligence Endpoint is required when using Document Intelligence."
            )
        elif not args.filename:
            _exit_with_error("Filename is required when using Document Intelligence.")
        markitdown = MarkItDown(
            enable_plugins=args.use_plugins, docintel_endpoint=args.endpoint
        )
    else:
        markitdown = MarkItDown(enable_plugins=args.use_plugins)

    # Stdin mode
    if not args.filename:
        result = markitdown.convert_stream(
            sys.stdin.buffer,
            stream_info=stream_info,
            keep_data_uris=args.keep_data_uris,
        )
        _handle_output(args, result)
        return

    # Single-file mode (preserves original behaviour exactly)
    if len(args.filename) == 1 and args.output_dir is None:
        result = markitdown.convert(
            args.filename[0],
            stream_info=stream_info,
            keep_data_uris=args.keep_data_uris,
        )
        _handle_output(args, result)
        return

    # Batch mode
    on_error = "raise" if args.fail_fast else "collect"
    exit_code = 0
    try:
        for batch_result in markitdown.convert_batch(
            args.filename,
            on_error=on_error,
            workers=args.workers,
            stream_info=stream_info,
            keep_data_uris=args.keep_data_uris,
        ):
            if not batch_result.success:
                print(
                    f"Error converting {batch_result.source}: {batch_result.error}",
                    file=sys.stderr,
                )
                exit_code = 1
            elif args.output_dir:
                os.makedirs(args.output_dir, exist_ok=True)
                source_name = os.path.basename(str(batch_result.source))
                out_path = os.path.join(args.output_dir, source_name + ".md")
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(batch_result.result.markdown)
                print(f"Converted: {batch_result.source} -> {out_path}", file=sys.stderr)
            else:
                print(f"\n--- {batch_result.source} ---\n")
                print(
                    batch_result.result.markdown.encode(
                        sys.stdout.encoding, errors="replace"
                    ).decode(sys.stdout.encoding)
                )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        exit_code = 1

    sys.exit(exit_code)
```

Note: also add `import os` at the top of `__main__.py` if it's not already there. Check first with `grep "^import os" packages/markitdown/src/markitdown/__main__.py`.

- [ ] **Step 4: Run tests to verify they pass**

```
cd packages/markitdown
pytest tests/test_cli_misc.py -v
```

Expected: All tests PASS (including the original `test_version` and `test_invalid_flag`).

- [ ] **Step 5: Run the full test suite**

```
cd packages/markitdown
pytest tests/ -v --ignore=tests/test_docintel_html.py
```

Expected: All tests PASS (docintel tests require credentials, skip them).

- [ ] **Step 6: Commit**

```bash
git add packages/markitdown/src/markitdown/__main__.py packages/markitdown/tests/test_cli_misc.py
git commit -m "feat: add batch CLI support with --workers, --fail-fast, --output-dir"
```

---

## Done

The full batch parallelization feature is complete:
- `BatchConversionResult` in public API
- `MarkItDown.convert_batch()` with pluggable executor
- CLI accepts multiple files with `--workers`, `--fail-fast`, `--output-dir`
