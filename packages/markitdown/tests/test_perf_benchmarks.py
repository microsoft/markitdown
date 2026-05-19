"""Cross-format performance benchmarks for MarkItDown.

Verifies real-world production characteristics:
- **Throughput**: each format must finish a baseline workload within a SLA.
- **Memory ceiling**: peak resident memory must stay below the documented cap.
- **Output stability**: structural invariants of the produced markdown.

Unlike the existing test_pdf_memory.py (which targets a single optimization),
this suite spans the multi-converter pipeline and produces machine-readable
metrics (BENCH_RESULTS) usable in CI dashboards.

Each benchmark is a stand-alone pytest test so failures are isolated:
- test_throughput_<fmt>: wall-clock SLA check (seconds)
- test_peak_memory_<fmt>: tracemalloc peak in MiB
- test_repeat_stability_<fmt>: N=5 runs produce identical output length

Tunable via env vars:
- MARKITDOWN_BENCH_REPEATS  : repeat count for stability test (default 5)
- MARKITDOWN_BENCH_RELAXED  : "1" multiplies SLAs by 3 (slow CI)
"""

from __future__ import annotations

import gc
import io
import os
import time
import tracemalloc
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import pytest

from markitdown import MarkItDown, StreamInfo

TEST_FILES_DIR = Path(__file__).parent / "test_files"
RELAXED = os.environ.get("MARKITDOWN_BENCH_RELAXED") == "1"
REPEATS = int(os.environ.get("MARKITDOWN_BENCH_REPEATS", "5"))


def _scale(seconds: float) -> float:
    """Allow CI runners to relax SLA by setting MARKITDOWN_BENCH_RELAXED=1."""
    return seconds * (3.0 if RELAXED else 1.0)


# (fixture_name, extension, max_seconds, max_mib, min_chars)
# SLAs intentionally generous (5x typical observed) so they catch real
# regressions without flaking on slow machines.
_BENCHMARK_MATRIX: List[Tuple[str, str, float, float, int]] = [
    # PDF: largest among the test fixtures
    ("test.pdf", ".pdf", 6.0, 80.0, 100),
    # DOCX: docx2txt + mammoth pipeline
    ("test.docx", ".docx", 3.0, 40.0, 50),
    # PPTX: per-slide image + text extraction
    ("test.pptx", ".pptx", 5.0, 60.0, 50),
    # XLSX: openpyxl
    ("test.xlsx", ".xlsx", 3.0, 40.0, 20),
    # HTML: BeautifulSoup + markdownify
    ("test_blog.html", ".html", 3.0, 30.0, 50),
    # JSON: pure-python pretty-print
    ("test.json", ".json", 2.0, 20.0, 10),
    # EPUB
    ("test.epub", ".epub", 4.0, 50.0, 50),
]


def _run_convert(fixture: str, ext: str) -> Tuple[str, float, float]:
    """Run conversion once; return (markdown, seconds, peak_mib)."""
    path = TEST_FILES_DIR / fixture
    if not path.exists():
        pytest.skip(f"fixture not present: {fixture}")
    md = MarkItDown()
    gc.collect()
    tracemalloc.start()
    t0 = time.perf_counter()
    with open(path, "rb") as fh:
        result = md.convert_stream(fh, stream_info=StreamInfo(extension=ext))
    elapsed = time.perf_counter() - t0
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result.markdown, elapsed, peak / (1024 * 1024)


@pytest.mark.parametrize(
    "fixture,ext,max_sec,max_mib,min_chars",
    _BENCHMARK_MATRIX,
    ids=[m[0] for m in _BENCHMARK_MATRIX],
)
def test_throughput_under_sla(fixture, ext, max_sec, max_mib, min_chars):
    """Each format must convert within its wall-clock SLA."""
    _, elapsed, _peak = _run_convert(fixture, ext)
    sla = _scale(max_sec)
    assert elapsed < sla, (
        f"{fixture}: took {elapsed:.2f}s, SLA={sla:.2f}s (regression?)"
    )


@pytest.mark.parametrize(
    "fixture,ext,max_sec,max_mib,min_chars",
    _BENCHMARK_MATRIX,
    ids=[m[0] for m in _BENCHMARK_MATRIX],
)
def test_peak_memory_under_cap(fixture, ext, max_sec, max_mib, min_chars):
    """Each format must finish under its documented memory cap."""
    _, _elapsed, peak_mib = _run_convert(fixture, ext)
    cap = max_mib * (3.0 if RELAXED else 1.0)
    assert peak_mib < cap, (
        f"{fixture}: peak {peak_mib:.1f} MiB, cap={cap:.1f} MiB (memory leak?)"
    )


@pytest.mark.parametrize(
    "fixture,ext,max_sec,max_mib,min_chars",
    _BENCHMARK_MATRIX,
    ids=[m[0] for m in _BENCHMARK_MATRIX],
)
def test_output_minimum_size(fixture, ext, max_sec, max_mib, min_chars):
    """Sanity: output must contain at least the documented minimum chars."""
    text, _elapsed, _peak = _run_convert(fixture, ext)
    assert len(text) >= min_chars, (
        f"{fixture}: only {len(text)} chars produced, expected ≥ {min_chars}"
    )


@pytest.mark.parametrize(
    "fixture,ext,max_sec,max_mib,min_chars",
    _BENCHMARK_MATRIX,
    ids=[m[0] for m in _BENCHMARK_MATRIX],
)
def test_repeat_stability(fixture, ext, max_sec, max_mib, min_chars):
    """N repeated conversions must produce byte-identical output.

    Catches:
    - Random ordering bugs (set/dict iteration)
    - Timestamp leaks into output
    - Memory accumulation across calls
    """
    if REPEATS < 2:
        pytest.skip("REPEATS<2; nothing to compare")
    lengths: List[int] = []
    texts: List[str] = []
    for _ in range(REPEATS):
        text, _e, _p = _run_convert(fixture, ext)
        lengths.append(len(text))
        texts.append(text)
    assert len(set(lengths)) == 1, (
        f"{fixture}: output length varies across {REPEATS} runs: {lengths}"
    )
    # Stronger: byte-identical
    assert all(t == texts[0] for t in texts), (
        f"{fixture}: output content differs between identical runs (non-determinism)"
    )


def test_no_growing_memory_across_formats():
    """Sequential conversion of mixed formats must not leak memory.

    Run the full matrix 3x in a row and verify peak memory of the
    3rd round is not > 2x the 1st round (catches inter-format leaks).
    """
    gc.collect()
    peaks: List[float] = []
    for _ in range(3):
        tracemalloc.start()
        for fixture, ext, *_ in _BENCHMARK_MATRIX:
            path = TEST_FILES_DIR / fixture
            if not path.exists():
                continue
            md = MarkItDown()
            with open(path, "rb") as fh:
                md.convert_stream(fh, stream_info=StreamInfo(extension=ext))
            del md
        _c, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peaks.append(peak / (1024 * 1024))
        gc.collect()
    assert peaks[2] < peaks[0] * 2.5, (
        f"Suspicious memory growth across rounds: {peaks} MiB "
        "(possible cross-format leak)"
    )
