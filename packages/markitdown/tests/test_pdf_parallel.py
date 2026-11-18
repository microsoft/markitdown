"""Opt-in parallel PDF page extraction (``pdf_workers``)."""

import faulthandler
import hashlib
import io
import json
import multiprocessing
import os
import subprocess
import sys
import threading
import warnings
from concurrent.futures import ProcessPoolExecutor
from types import SimpleNamespace

import pytest

from markitdown import FileConversionException, MarkItDown, StreamInfo
from markitdown.converters import PdfConverter, _pdf_parallel
from markitdown.converters._pdf_parallel import PdfParallelWarning

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")
MiB = 1024 * 1024

EQUIVALENCE_FIXTURES = [
    "pdf_cleanup_plain.pdf",  # plain text only: per-range pdfminer path
    "REPAIR-2022-INV-001_multipage.pdf",  # form pages
    "SPARSE-2024-INV-1234_borderless_table.pdf",
    "MEDRPT-2024-PAT-3847_medical_report_scan.pdf",  # scanned: no text layer
]  # pdf_cleanup_mixed.pdf is covered through MarkItDown in TestParallelOutput


def _text_pdf(pages: list[list[str]]) -> bytes:
    """Build a minimal PDF with one Helvetica text line per list entry."""
    objects: list[bytes] = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"",  # page tree, filled in below
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    kids = []
    for lines in pages:
        ops = ["BT /F1 12 Tf 72 720 Td 16 TL"]
        for line in lines:
            escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            ops.append(f"({escaped}) Tj T*")
        ops.append("ET")
        stream = "\n".join(ops).encode("latin-1")
        objects.append(
            b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream)
        )
        objects.append(
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 3 0 R >> >> /Contents %d 0 R >>" % len(objects)
        )
        kids.append(len(objects))
    objects[1] = b"<< /Type /Pages /Kids [%s] /Count %d >>" % (
        b" ".join(b"%d 0 R" % kid for kid in kids),
        len(kids),
    )
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n%s\nendobj\n" % (number, body)
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    for offset in offsets:
        out += b"%010d 00000 n \n" % offset
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
        len(objects) + 1,
        xref,
    )
    return bytes(out)


def _read_fixture(name: str) -> bytes:
    with open(os.path.join(TEST_FILES_DIR, name), "rb") as f:
        return f.read()


def _convert(data: bytes, **kwargs) -> str:
    return (
        PdfConverter()
        .convert(io.BytesIO(data), StreamInfo(extension=".pdf"), **kwargs)
        .markdown
    )


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# Worker replacements for fault injection. They are module-level so that spawned
# workers can import them by name, exactly like the real worker functions.
def _raising_range(start, stop):
    raise RuntimeError("injected worker failure")


def _exiting_range(start, stop):
    os._exit(3)


def _exiting_init(shm_name, size):
    os._exit(4)


def _convert_in_worker(path):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        markdown = MarkItDown().convert(path, pdf_workers=2).markdown
    return markdown, [
        str(w.message) for w in caught if issubclass(w.category, PdfParallelWarning)
    ]


@pytest.fixture
def parallel(monkeypatch, recwarn):
    """Deterministic resources; records pools and shared-memory blocks.

    Teardown fails the test on any unexpected fallback warning and on any
    shared-memory block that was not released, after success or failure.
    """
    monkeypatch.setattr(_pdf_parallel, "_disabled_reason", None)
    monkeypatch.setattr(_pdf_parallel, "_cpu_count", lambda: 4)
    monkeypatch.setattr(
        _pdf_parallel, "_memory_headroom", lambda: (64 * 1024 * MiB, None)
    )
    state = SimpleNamespace(pools=[], blocks=[])

    class RecordingPool(ProcessPoolExecutor):
        def __init__(self, *args, **kwargs):
            state.pools.append(kwargs["max_workers"])
            super().__init__(*args, **kwargs)

    class RecordingSharedMemory(_pdf_parallel.SharedMemory):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.unlinked = False
            state.blocks.append(self)

        def unlink(self):
            self.unlinked = True
            super().unlink()

    monkeypatch.setattr(_pdf_parallel, "ProcessPoolExecutor", RecordingPool)
    monkeypatch.setattr(_pdf_parallel, "SharedMemory", RecordingSharedMemory)
    yield state
    assert all(block.unlinked for block in state.blocks)
    if sys.platform.startswith("linux"):
        assert not any(os.path.exists(f"/dev/shm/{b.name}") for b in state.blocks)
    # Warnings a test expects are consumed by its pytest.warns block.
    unexpected = [
        str(w.message) for w in recwarn if issubclass(w.category, PdfParallelWarning)
    ]
    assert not unexpected, unexpected


class TestDefaultBehaviour:
    def test_sequential_by_default(self, monkeypatch):
        def fail(*args, **kwargs):
            raise AssertionError("parallel path used without pdf_workers")

        monkeypatch.setattr(_pdf_parallel, "extract_markdown", fail)
        path = os.path.join(TEST_FILES_DIR, "pdf_cleanup_mixed.pdf")
        assert MarkItDown().convert(path).markdown
        assert MarkItDown().convert(path, pdf_workers=None).markdown
        assert MarkItDown().convert(path, pdf_workers=1).markdown

    @pytest.mark.parametrize("value", [0, -2])
    def test_invalid_worker_count(self, value):
        with pytest.raises(ValueError, match="pdf_workers"):
            _convert(_read_fixture("pdf_cleanup_plain.pdf"), pdf_workers=value)

    @pytest.mark.parametrize("value", ["2", 2.0, True])
    def test_invalid_worker_type(self, value):
        with pytest.raises(TypeError, match="pdf_workers"):
            _convert(_read_fixture("pdf_cleanup_plain.pdf"), pdf_workers=value)

    def test_invalid_value_reported_through_markitdown(self):
        path = os.path.join(TEST_FILES_DIR, "pdf_cleanup_plain.pdf")
        with pytest.raises(FileConversionException, match="pdf_workers"):
            MarkItDown().convert(path, pdf_workers=0)


class TestParallelOutput:
    @pytest.mark.parametrize("name", EQUIVALENCE_FIXTURES)
    def test_matches_sequential(self, parallel, name):
        data = _read_fixture(name)
        assert _convert(data, pdf_workers=2) == _convert(data)
        assert parallel.pools == [2]

    def test_page_order_and_numbering_across_worker_ranges(self, parallel):
        pages = [[f"Marker for page {n}", "Body text."] for n in range(1, 6)]
        # Ranges for 5 pages and 3 workers are pages 1-2, 3-4 and 5, so the
        # numbering ".1" ends the first range and its text starts the second.
        pages[1].append(".1")
        pages[2].insert(0, "The intent of this Request for Proposal.")
        data = _text_pdf(pages)
        markdown = _convert(data, pdf_workers=3)
        assert markdown == _convert(data)
        assert parallel.pools == [3]
        positions = [markdown.index(f"Marker for page {n}") for n in range(1, 6)]
        assert positions == sorted(positions)
        assert ".1 The intent of this Request for Proposal." in markdown

    def test_through_markitdown_from_a_thread(self, parallel):
        path = os.path.join(TEST_FILES_DIR, "pdf_cleanup_mixed.pdf")
        expected = MarkItDown().convert(path).markdown
        results = []
        thread = threading.Thread(
            target=lambda: results.append(
                MarkItDown().convert(path, pdf_workers=2).markdown
            )
        )
        thread.start()
        thread.join()
        assert results == [expected]
        assert parallel.pools == [2]


class TestFailures:
    """Every failure converts sequentially, with the same output, and warns.

    The ``parallel`` fixture also verifies that shared memory was released.
    """

    def test_worker_exception(self, parallel, monkeypatch):
        data = _read_fixture("pdf_cleanup_mixed.pdf")
        monkeypatch.setattr(_pdf_parallel, "_plumber_range", _raising_range)
        with pytest.warns(PdfParallelWarning, match="injected worker failure"):
            markdown = _convert(data, pdf_workers=2)
        assert markdown == _convert(data)
        assert _pdf_parallel._disabled_reason is None  # the pool itself was healthy
        assert len(parallel.blocks) == 1 and parallel.blocks[0].unlinked

    def test_worker_crash_disables_parallel_conversion(self, parallel, monkeypatch):
        data = _read_fixture("pdf_cleanup_plain.pdf")
        monkeypatch.setattr(_pdf_parallel, "_pdfminer_range", _exiting_range)
        with pytest.warns(PdfParallelWarning, match="exited unexpectedly"):
            markdown = _convert(data, pdf_workers=2)
        assert markdown == _convert(data)
        assert _pdf_parallel._disabled_reason is not None
        with pytest.warns(PdfParallelWarning, match="disabled after an earlier"):
            assert _convert(data, pdf_workers=2) == markdown
        assert parallel.pools == [2]  # no second pool
        assert len(parallel.blocks) == 1 and parallel.blocks[0].unlinked

    def test_worker_dies_during_startup(self, parallel, monkeypatch):
        # With the PDF in the start-up arguments this case blocked forever on
        # some platforms; fail loudly instead of hanging the test run.
        data = _read_fixture("REPAIR-2022-INV-001_multipage.pdf")
        monkeypatch.setattr(_pdf_parallel, "_init_worker", _exiting_init)
        faulthandler.dump_traceback_later(120, exit=True)
        try:
            with pytest.warns(PdfParallelWarning, match="exited unexpectedly"):
                markdown = _convert(data, pdf_workers=2)
        finally:
            faulthandler.cancel_dump_traceback_later()
        assert markdown == _convert(data)

    @pytest.mark.parametrize("error", [OSError(5, "injected"), KeyboardInterrupt()])
    def test_shared_memory_copy_failure(self, parallel, monkeypatch, error):
        class FailingBuffer:
            def __setitem__(self, key, value):
                raise error

        class FailingSharedMemory(_pdf_parallel.SharedMemory):  # still recording
            @property
            def buf(self):
                return FailingBuffer()

        monkeypatch.setattr(_pdf_parallel, "SharedMemory", FailingSharedMemory)
        data = _read_fixture("pdf_cleanup_mixed.pdf")
        if isinstance(error, OSError):
            with pytest.warns(PdfParallelWarning, match="could not be copied"):
                assert _convert(data, pdf_workers=2) == _convert(data)
        else:  # interrupts are not swallowed
            with pytest.raises(KeyboardInterrupt):
                _convert(data, pdf_workers=2)
        assert parallel.pools == []
        assert len(parallel.blocks) == 1 and parallel.blocks[0].unlinked
        assert _pdf_parallel._disabled_reason is None

    def test_inside_a_multiprocessing_worker(self):
        path = os.path.join(TEST_FILES_DIR, "pdf_cleanup_plain.pdf")
        context = multiprocessing.get_context("spawn")
        with ProcessPoolExecutor(1, mp_context=context) as pool:
            markdown, messages = pool.submit(_convert_in_worker, path).result()
        assert markdown == MarkItDown().convert(path).markdown
        assert messages and "inside a multiprocessing worker" in messages[0]


class TestResourceLimits:
    def test_insufficient_memory(self, parallel, monkeypatch):
        monkeypatch.setattr(
            _pdf_parallel, "_memory_headroom", lambda: (200 * MiB, None)
        )
        data = _read_fixture("pdf_cleanup_mixed.pdf")
        with pytest.warns(PdfParallelWarning, match="not enough memory"):
            markdown = _convert(data, pdf_workers=4)
        assert markdown == _convert(data)
        assert parallel.pools == []  # no worker process was started

    def test_unknown_memory(self, parallel, monkeypatch):
        monkeypatch.setattr(_pdf_parallel, "_memory_headroom", lambda: (None, None))
        data = _read_fixture("pdf_cleanup_mixed.pdf")
        with pytest.warns(PdfParallelWarning, match="cannot be determined"):
            assert _convert(data, pdf_workers=4) == _convert(data)
        assert parallel.pools == []

    def test_one_parallel_conversion_at_a_time(self, parallel):
        data = _read_fixture("pdf_cleanup_mixed.pdf")
        assert _pdf_parallel._pool_lock.acquire(blocking=False)
        try:
            with pytest.warns(PdfParallelWarning, match="already running"):
                assert _convert(data, pdf_workers=2) == _convert(data)
        finally:
            _pdf_parallel._pool_lock.release()
        assert parallel.pools == []

    @pytest.mark.parametrize(
        "kwargs, expected",
        [
            (dict(cpus=8, headroom=8192 * MiB, commit_headroom=None), 4),
            (dict(cpus=2, headroom=8192 * MiB, commit_headroom=None), 2),
            (dict(cpus=1, headroom=8192 * MiB, commit_headroom=None), 1),
            (dict(cpus=8, headroom=None, commit_headroom=None), 1),
            (dict(cpus=8, headroom=300 * MiB, commit_headroom=None), 1),
            (dict(cpus=8, headroom=600 * MiB, commit_headroom=None), 2),
            (dict(cpus=8, headroom=700 * MiB, commit_headroom=None), 3),
            # Windows: physical memory is ample but commit is the binding limit.
            (
                dict(
                    cpus=8, headroom=8 << 30, commit_headroom=1100 * MiB, blas_threads=8
                ),
                2,
            ),
            (
                dict(
                    cpus=8, headroom=8 << 30, commit_headroom=500 * MiB, blas_threads=8
                ),
                1,
            ),
        ],
    )
    def test_plan_workers(self, kwargs, expected):
        workers, reason = _pdf_parallel._plan_workers(4, 100, 10 * MiB, **kwargs)
        assert workers == expected
        assert (reason is None) == (expected > 1)

    def test_page_count_caps_workers(self):
        assert _pdf_parallel._plan_workers(8, 3, MiB, 8, 8192 * MiB, None) == (3, None)

    @pytest.mark.parametrize(
        "flags, limit, peak, expected_mib",
        [
            (0, 0, 0, 5000),  # in a job without limits
            (0x200, 1500 * MiB, 1200 * MiB, 300),  # job-wide memory limit
            (0x200, 1000 * MiB, 1200 * MiB, 0),  # already over the limit
            (0x100, 0, 0, 0),  # per-process memory limit: not evaluated
            (0x008, 0, 0, 0),  # process-count limit: not evaluated
        ],
    )
    def test_job_limits(self, flags, limit, peak, expected_mib):
        assert _pdf_parallel._apply_job_limits(5000 * MiB, flags, limit, peak) == (
            expected_mib * MiB
        )

    @pytest.mark.parametrize(
        "files, expected_mib",
        [
            ({}, 4000),  # no cgroup information: host memory
            (
                {  # cgroup v2: tightest limit on the path wins; inactive cache is free
                    "/proc/self/cgroup": "0::/app.slice/job.scope",
                    "/sys/fs/cgroup/cgroup.controllers": "cpu memory pids",
                    "/sys/fs/cgroup/app.slice/cgroup.controllers": "cpu memory",
                    "/sys/fs/cgroup/app.slice/cgroup.type": "domain",
                    "/sys/fs/cgroup/app.slice/job.scope/cgroup.controllers": "memory",
                    "/sys/fs/cgroup/app.slice/job.scope/cgroup.type": "domain",
                    "/sys/fs/cgroup/app.slice/job.scope/memory.high": "max",
                    "/sys/fs/cgroup/app.slice/job.scope/memory.max": str(1024 * MiB),
                    "/sys/fs/cgroup/app.slice/job.scope/memory.current": str(300 * MiB),
                    "/sys/fs/cgroup/app.slice/job.scope/memory.stat": (
                        f"anon 1\ninactive_file {100 * MiB}"
                    ),
                    "/sys/fs/cgroup/app.slice/memory.high": str(600 * MiB),
                    "/sys/fs/cgroup/app.slice/memory.max": "max",
                    "/sys/fs/cgroup/app.slice/memory.current": str(500 * MiB),
                    # the root cgroup has no cgroup.type and no limit files
                },
                100,
            ),
            (
                {  # cgroup v2, explicitly unlimited (WSL and most desktops)
                    "/proc/self/cgroup": "0::/user",
                    "/sys/fs/cgroup/cgroup.controllers": "memory",
                    "/sys/fs/cgroup/user/cgroup.controllers": "memory",
                    "/sys/fs/cgroup/user/cgroup.type": "domain",
                    "/sys/fs/cgroup/user/memory.max": "max",
                    "/sys/fs/cgroup/user/memory.high": "max",
                },
                4000,
            ),
            (
                {  # cgroup v2 without the memory controller below the root
                    "/proc/self/cgroup": "0::/user",
                    "/sys/fs/cgroup/cgroup.controllers": "memory",
                    "/sys/fs/cgroup/user/cgroup.controllers": "cpu",
                    "/sys/fs/cgroup/user/cgroup.type": "domain",
                },
                4000,
            ),
            ({"/proc/self/cgroup": "0::/job"}, None),  # v2, nothing readable
            (
                {  # v2: the memory controller is enabled but memory.max is unreadable
                    "/proc/self/cgroup": "0::/job",
                    "/sys/fs/cgroup/cgroup.controllers": "memory",
                    "/sys/fs/cgroup/job/cgroup.controllers": "memory",
                    "/sys/fs/cgroup/job/cgroup.type": "domain",
                },
                None,
            ),
            (
                {  # v2: unparsable limit
                    "/proc/self/cgroup": "0::/job",
                    "/sys/fs/cgroup/cgroup.controllers": "memory",
                    "/sys/fs/cgroup/job/cgroup.controllers": "memory",
                    "/sys/fs/cgroup/job/cgroup.type": "domain",
                    "/sys/fs/cgroup/job/memory.max": "",
                    "/sys/fs/cgroup/job/memory.high": "max",
                },
                None,
            ),
            ({"/proc/self/cgroup": "4:memory:/docker/abc\n0::/"}, None),  # v1, none
            (
                {  # cgroup v1
                    "/proc/self/cgroup": "4:memory:/docker/abc\n0::/",
                    "/sys/fs/cgroup/memory/docker/abc/memory.limit_in_bytes": str(
                        512 * MiB
                    ),
                    "/sys/fs/cgroup/memory/docker/abc/memory.usage_in_bytes": str(
                        112 * MiB
                    ),
                    "/sys/fs/cgroup/memory/memory.limit_in_bytes": str(2**63 - 4096),
                },
                400,
            ),
        ],
    )
    def test_linux_headroom(self, files, expected_mib):
        meminfo = f"MemTotal: 8000000 kB\nMemAvailable: {4000 * 1024} kB"
        files = {"/proc/meminfo": meminfo, **files}
        expected = None if expected_mib is None else expected_mib * MiB
        assert _pdf_parallel._linux_headroom(files.get) == expected

    def test_linux_headroom_unknown_usage(self):
        files = {
            "/proc/meminfo": "MemAvailable: 4096000 kB",
            "/proc/self/cgroup": "0::/job",
            "/sys/fs/cgroup/job/cgroup.controllers": "memory",
            "/sys/fs/cgroup/job/memory.max": str(512 * MiB),
            "/sys/fs/cgroup/job/memory.high": "max",
        }
        assert _pdf_parallel._linux_headroom(files.get) is None

    @pytest.mark.skipif(
        not (sys.platform.startswith("linux") or sys.platform == "win32"),
        reason="memory is only probed on Linux and Windows",
    )
    def test_real_probes(self):
        headroom, _ = _pdf_parallel._memory_headroom()
        assert headroom is not None and headroom > 0
        assert _pdf_parallel._cpu_count() >= 1


_JOB_SCRIPT = """\
import ctypes, hashlib, json, sys, warnings
from ctypes import wintypes
from markitdown import MarkItDown
from markitdown.converters import _pdf_parallel


class Limits(ctypes.Structure):  # JOBOBJECT_EXTENDED_LIMIT_INFORMATION
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_int64),
        ("PerJobUserTimeLimit", ctypes.c_int64),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
        ("IoInfo", ctypes.c_ulonglong * 6),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


def main():
    path, extra_mib, force = sys.argv[1], int(sys.argv[2]), sys.argv[3] == "force"
    md = MarkItDown()  # load converters before the limit applies
    k32 = ctypes.WinDLL("kernel32")
    k32.CreateJobObjectW.restype = wintypes.HANDLE
    k32.GetCurrentProcess.restype = wintypes.HANDLE
    handle, info = [wintypes.HANDLE, ctypes.c_int], [ctypes.c_void_p, wintypes.DWORD]
    k32.SetInformationJobObject.argtypes = handle + info
    k32.QueryInformationJobObject.argtypes = handle + info + [ctypes.c_void_p]
    k32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    job = k32.CreateJobObjectW(None, None)
    limits = Limits(LimitFlags=0x200, JobMemoryLimit=1 << 40)  # JOB_MEMORY
    size = ctypes.sizeof(limits)
    assert k32.SetInformationJobObject(job, 9, ctypes.byref(limits), size)
    assert k32.AssignProcessToJobObject(job, k32.GetCurrentProcess())
    assert k32.QueryInformationJobObject(job, 9, ctypes.byref(limits), size, None)
    # Commit limit: what this process has committed so far plus extra_mib.
    limits.JobMemoryLimit = limits.PeakJobMemoryUsed + extra_mib * 2**20
    assert k32.SetInformationJobObject(job, 9, ctypes.byref(limits), size)
    commit = _pdf_parallel._memory_headroom()[1]
    if force:  # bypass the budget: workers must fail to start, not hang
        _pdf_parallel._memory_headroom = lambda: (1 << 40, 1 << 40)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        markdown = md.convert(path, pdf_workers=4).markdown
    print(json.dumps(dict(
        sha=hashlib.sha256(markdown.encode()).hexdigest(),
        commit=commit,
        warnings=[str(w.message) for w in caught
                  if issubclass(w.category, _pdf_parallel.PdfParallelWarning)],
    )))


if __name__ == "__main__":
    main()
"""


@pytest.mark.skipif(sys.platform != "win32", reason="Windows job objects")
@pytest.mark.parametrize(
    "extra_mib, force, expected_warning",
    [
        (200, False, "not enough memory"),
        (300, False, "not enough memory"),
        (300, True, "worker"),  # workers cannot commit memory: fall back
    ],
)
def test_windows_job_memory_limit(tmp_path, extra_mib, force, expected_warning):
    script = tmp_path / "job_limited.py"
    script.write_text(_JOB_SCRIPT)
    path = os.path.join(TEST_FILES_DIR, "pdf_cleanup_plain.pdf")
    mode = "force" if force else "budget"
    completed = subprocess.run(
        [sys.executable, str(script), path, str(extra_mib), mode],
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert completed.returncode == 0, completed.stderr
    result = json.loads(completed.stdout.strip().splitlines()[-1])
    assert result["sha"] == _sha(MarkItDown().convert(path).markdown)
    assert result["commit"] <= extra_mib * MiB
    assert len(result["warnings"]) == 1 and expected_warning in result["warnings"][0]


_UNGUARDED_SCRIPT = """\
import hashlib, sys, warnings
warnings.simplefilter("always")
from markitdown import MarkItDown

# Deliberately no `if __name__ == "__main__":` guard.
result = MarkItDown().convert(sys.argv[1], pdf_workers=2)
with open(sys.argv[2], "a") as f:
    f.write(hashlib.sha256(result.markdown.encode()).hexdigest() + "\\n")
"""


@pytest.mark.skipif(_pdf_parallel._cpu_count() < 2, reason="needs 2 CPUs")
def test_unguarded_script_does_not_convert_in_workers(tmp_path):
    """spawn re-imports the calling script in every worker.

    Guarded entry points are exercised by every other test in this module,
    which run under pytest's guarded main module.
    """
    script = tmp_path / "unguarded.py"
    script.write_text(_UNGUARDED_SCRIPT)
    marker = tmp_path / "results.txt"
    path = os.path.join(TEST_FILES_DIR, "pdf_cleanup_mixed.pdf")
    completed = subprocess.run(
        [sys.executable, str(script), path, str(marker)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert completed.returncode == 0, completed.stderr
    # Only the parent completed a conversion; it fell back and said why.
    assert marker.read_text().splitlines() == [
        _sha(MarkItDown().convert(path).markdown)
    ]
    assert "PdfParallelWarning" in completed.stderr
    assert "__main__" in completed.stderr
