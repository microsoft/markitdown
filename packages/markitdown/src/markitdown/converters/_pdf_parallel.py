"""Opt-in parallel page extraction for ``PdfConverter`` (``pdf_workers=N``).

Pages are split into contiguous ranges and extracted in ``spawn`` worker
processes using exactly the same pdfplumber / pdfminer calls as the sequential
converter, then reassembled in page order, so the output is identical.

``extract_markdown`` returns ``None`` whenever parallel extraction is not used
or does not complete (too little memory, a worker failed, ...). The caller then
runs the unchanged sequential converter, so a failure never produces partial or
reordered output. Each such case emits a ``PdfParallelWarning`` that says why,
except for PDFs with fewer than two pages or that pdfplumber cannot open, which
the sequential converter handles exactly as before.

Notes:
- The PDF is passed to workers through ``multiprocessing.shared_memory``; only
  its name and size travel through the worker start-up pipe. CPython writes the
  start-up data to that pipe while still holding the pipe's read end, so if a
  worker died before reading a large payload, the parent would block forever.
- ``spawn`` re-imports the caller's ``__main__`` module in every worker, so
  scripts must call the converter under ``if __name__ == "__main__":``.
- Supported on Linux and Windows, where available memory (including cgroup and
  job-object limits) can be determined; elsewhere conversion stays sequential.
  The memory check is a conservative estimate, not a guarantee: the operating
  system can still terminate the process.
- One parallel conversion runs per process at a time; concurrent calls convert
  sequentially. Other processes on the machine are not coordinated with.
"""

from __future__ import annotations

import io
import multiprocessing
import os
import posixpath
import sys
import threading
import warnings
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from multiprocessing.shared_memory import SharedMemory
from typing import Any, Callable, Optional

_MiB = 1024 * 1024

# Per-worker estimates, rounded up from measured peak worker memory (RSS of
# 97-107 MB for ~10 MB / 100-page PDFs and 145-179 MB for ~45-55 MB / 500-page
# PDFs).
_WORKER_BASE_BYTES = 100 * _MiB
_WORKER_PDF_FACTOR = 2.5  # the worker's copy of the PDF plus parser buffers
_PARENT_PDF_FACTOR = 2.0  # shared-memory copy plus transient buffers in the parent
# On Windows, every process that imports numpy (markitdown does, via magika)
# commits about 32 MiB per BLAS thread, without touching it. Commit, not
# physical memory, is then the binding limit.
_WINDOWS_COMMIT_PER_BLAS_THREAD = 32 * _MiB
_SAFETY_MARGIN_MIN = 256 * _MiB
_SAFETY_MARGIN_FRACTION = 0.25
_SHM_SLACK = 16 * _MiB

_ENTRY_POINT_ERROR = (
    "pdf_workers was used while a worker process was importing the main module. "
    "The calling script converts PDFs at import time, so every worker would run "
    'the conversion again. Call the converter under `if __name__ == "__main__":` '
    "(see 'Safe importing of main module' in the multiprocessing documentation)."
)


class PdfParallelWarning(RuntimeWarning):
    """``pdf_workers`` was requested, but the PDF was converted sequentially."""


# After a pool-level failure (a worker died or could not start), parallel
# conversion stays disabled for the rest of the process, so a broken
# environment is not retried for every document.
_disabled_reason: Optional[str] = None
_pool_lock = threading.Lock()


class _PoolFailure(Exception):
    """The worker pool itself failed."""


class _TaskFailure(Exception):
    """A worker raised while extracting pages; the pool is healthy."""


def extract_markdown(pdf: bytes, pdf_workers: int) -> Optional[str]:
    """Return the joined page text, or None to use the sequential converter.

    The returned text corresponds to what ``PdfConverter.convert`` produces
    before its empty-result fallback and numbering post-processing.
    """
    import pdfplumber

    reason = _environment_reason()
    if reason is not None:
        _warn(reason)
        return None

    try:
        with pdfplumber.open(io.BytesIO(pdf)) as document:
            n_pages = len(document.pages)
    except Exception:
        return None  # the sequential converter handles unreadable PDFs as before
    if n_pages < 2:
        return None

    # One pool per process at a time: concurrent calls would otherwise each
    # plan against the same free memory. Others convert sequentially.
    if not _pool_lock.acquire(blocking=False):
        _warn("another parallel PDF conversion is already running in this process")
        return None
    try:
        return _plan_and_extract(pdf, pdf_workers, n_pages)
    finally:
        _pool_lock.release()


def _plan_and_extract(pdf: bytes, pdf_workers: int, n_pages: int) -> Optional[str]:
    global _disabled_reason
    workers, reason = _plan_workers(
        pdf_workers, n_pages, len(pdf), _cpu_count(), *_memory_headroom()
    )
    if reason is not None:
        _warn(reason)
        return None
    if not _shared_memory_has_room(len(pdf)):
        _warn("/dev/shm has too little free space for the PDF")
        return None

    try:
        shm = SharedMemory(create=True, size=len(pdf))
    except (OSError, ValueError) as exc:
        _warn(f"shared memory is unavailable ({type(exc).__name__}: {exc})")
        return None
    try:
        try:
            buffer = shm.buf
            assert buffer is not None  # only None after close()
            buffer[: len(pdf)] = pdf
        except (OSError, ValueError, BufferError) as exc:
            _warn(f"the PDF could not be copied to shared memory ({exc!r})")
            return None
        return _extract_in_pool(shm.name, len(pdf), n_pages, workers)
    except _PoolFailure as exc:
        _disabled_reason = str(exc)
        _warn(
            f"{exc}. Parallel PDF conversion is disabled for the rest of this "
            "process. Possible causes: the operating system terminated a worker "
            "(for example for lack of memory), worker processes cannot be "
            "started here, or the main script lacks an "
            '`if __name__ == "__main__":` guard'
        )
        return None
    except _TaskFailure as exc:
        _warn(f"a worker failed ({exc})")
        return None
    finally:
        shm.close()
        try:
            shm.unlink()  # no-op on Windows, where the last close frees it
        except FileNotFoundError:
            pass


def _extract_in_pool(shm_name: str, size: int, n_pages: int, workers: int) -> str:
    ranges = _page_ranges(n_pages, workers)
    try:
        pool = ProcessPoolExecutor(
            max_workers=workers,
            mp_context=multiprocessing.get_context("spawn"),
            initializer=_init_worker,
            initargs=(shm_name, size),
        )
    except Exception as exc:
        raise _PoolFailure(f"the worker pool could not be created ({exc})") from exc
    try:
        pages = [p for chunk in _run(pool, _plumber_range, ranges) for p in chunk]
        # Same global decision as the sequential converter: without any
        # form-style page, the whole document is extracted with pdfminer.
        if not any(is_form for is_form, _ in pages):
            return "".join(_run(pool, _pdfminer_range, ranges))
        return "\n\n".join(text for _, text in pages if text is not None).strip()
    finally:
        pool.shutdown(wait=True, cancel_futures=True)


def _run(pool: ProcessPoolExecutor, fn: Callable, ranges: list[tuple[int, int]]):
    try:
        futures = [pool.submit(fn, start, stop) for start, stop in ranges]
    except Exception as exc:  # submit() starts the worker processes
        raise _PoolFailure(f"a worker failed to start ({type(exc).__name__})") from exc
    results = []
    for future, (start, stop) in zip(futures, ranges):
        try:
            result = future.result()
        except BrokenProcessPool as exc:
            raise _PoolFailure("a worker process exited unexpectedly") from exc
        except Exception as exc:
            raise _TaskFailure(f"{type(exc).__name__}: {exc}") from exc
        if isinstance(result, list) and len(result) != stop - start:
            raise _TaskFailure(f"pages {start}-{stop} returned {len(result)} results")
        results.append(result)
    return results


def _page_ranges(n_pages: int, n_chunks: int) -> list[tuple[int, int]]:
    """Split [0, n_pages) into n_chunks contiguous, near-equal ranges."""
    base, extra = divmod(n_pages, n_chunks)
    ranges, start = [], 0
    for i in range(n_chunks):
        stop = start + base + (1 if i < extra else 0)
        ranges.append((start, stop))
        start = stop
    return ranges


# --------------------------------------------------------------------- workers

_worker_pdf: bytes = b""


def _init_worker(shm_name: str, size: int) -> None:
    global _worker_pdf
    kwargs: dict[str, Any] = {"track": False} if sys.version_info >= (3, 13) else {}
    shm = SharedMemory(name=shm_name, **kwargs)
    try:
        buffer = shm.buf
        assert buffer is not None  # only None after close()
        _worker_pdf = bytes(buffer[:size])
    finally:
        shm.close()


def _plumber_range(start: int, stop: int) -> list[tuple[bool, Optional[str]]]:
    """The sequential converter's per-page loop body for pages [start, stop)."""
    import pdfplumber

    from ._pdf_converter import _extract_form_content_from_words

    results: list[tuple[bool, Optional[str]]] = []
    pages = list(range(start + 1, stop + 1))  # pdfplumber page numbers are 1-based
    with pdfplumber.open(io.BytesIO(_worker_pdf), pages=pages) as document:
        for page in document.pages:
            content = _extract_form_content_from_words(page)
            if content is not None:
                results.append((True, content if content.strip() else None))
            else:
                text = page.extract_text()
                results.append((False, text.strip() if text and text.strip() else None))
            page.close()
    return results


def _pdfminer_range(start: int, stop: int) -> str:
    import pdfminer.high_level

    return pdfminer.high_level.extract_text(
        io.BytesIO(_worker_pdf), page_numbers=set(range(start, stop))
    )


# ------------------------------------------------------------ resource checks


def _environment_reason() -> Optional[str]:
    """Why worker processes must not be started here, or None."""
    if getattr(multiprocessing.current_process(), "_inheriting", False):
        # The same condition multiprocessing itself rejects: this process is
        # still importing the parent's __main__ module. Raise instead of
        # converting a second time inside the worker.
        raise RuntimeError(_ENTRY_POINT_ERROR)
    if multiprocessing.parent_process() is not None:
        return "already running inside a multiprocessing worker"
    if getattr(sys, "frozen", False):
        return "not supported in frozen executables"
    if _disabled_reason is not None:
        return f"disabled after an earlier failure ({_disabled_reason})"
    return None


def _plan_workers(
    requested: int,
    n_pages: int,
    pdf_size: int,
    cpus: int,
    headroom: Optional[int],
    commit_headroom: Optional[int],
    blas_threads: Optional[int] = None,
) -> tuple[int, Optional[str]]:
    """Return (workers, None), or (1, reason) to convert sequentially.

    ``headroom`` is the physical memory available (None if unknown);
    ``commit_headroom`` is the Windows commit available (None elsewhere).
    """
    workers = min(requested, cpus, n_pages)
    if workers < 2:
        return 1, "fewer than 2 CPUs are available"
    if headroom is None:
        return 1, "available memory cannot be determined on this platform"
    resident = _WORKER_BASE_BYTES + _WORKER_PDF_FACTOR * pdf_size
    committed = resident
    if commit_headroom is not None:
        committed += _WINDOWS_COMMIT_PER_BLAS_THREAD * (blas_threads or _blas_threads())
    parent = _PARENT_PDF_FACTOR * pdf_size

    def needed(per_worker: float, n: int) -> float:
        total = n * per_worker + parent
        return total + max(_SAFETY_MARGIN_MIN, _SAFETY_MARGIN_FRACTION * total)

    while workers >= 2 and (
        needed(resident, workers) > headroom
        or (
            commit_headroom is not None and needed(committed, workers) > commit_headroom
        )
    ):
        workers -= 1
    if workers < 2:
        return 1, "not enough memory for 2 worker processes"
    return workers, None


def _cpu_count() -> int:
    """CPUs usable by this process, including affinity and cgroup v2 quotas."""
    process_cpu_count = getattr(os, "process_cpu_count", None)  # Python 3.13+
    if process_cpu_count is not None:
        count = process_cpu_count()
    elif hasattr(os, "sched_getaffinity"):
        count = len(os.sched_getaffinity(0))
    else:
        count = os.cpu_count()
    count = count or 1
    if sys.platform == "win32":
        count = min(count, 61)  # ProcessPoolExecutor's limit on Windows
    for directory in _cgroup_dirs(_read_text, v2=True):
        quota, _, period = (
            _read_text(posixpath.join(directory, "cpu.max")) or ""
        ).partition(" ")
        if quota.isdigit() and period.isdigit() and int(period) > 0:
            count = min(count, max(1, -(-int(quota) // int(period))))
    return count


def _blas_threads() -> int:
    for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS"):
        value = os.environ.get(name, "").strip()
        if value.isdigit() and int(value) > 0:
            return int(value)
    return os.cpu_count() or 1


def _memory_headroom() -> tuple[Optional[int], Optional[int]]:
    """(physical bytes available, Windows commit bytes available or None)."""
    try:
        if sys.platform.startswith("linux"):
            return _linux_headroom(_read_text), None
        if sys.platform == "win32":
            return _windows_headroom()
    except Exception:
        pass  # any probe failure means "unknown", which keeps conversion sequential
    return None, None


def _linux_headroom(read: Callable[[str], Optional[str]]) -> Optional[int]:
    """min(MemAvailable, every cgroup limit on this process's path minus usage).

    Reclaimable inactive page cache is not counted as used; swap is never
    counted as available. Returns None (unknown) when this process is in a
    memory cgroup whose limits cannot be read, rather than assuming none.
    """
    available = None
    for line in (read("/proc/meminfo") or "").splitlines():
        if line.startswith("MemAvailable:"):
            available = int(line.split()[1]) * 1024
    if available is None:
        return None
    v2 = bool(_cgroup_dirs(read, v2=True)) and not _cgroup_dirs(read, v2=False)
    limit_files: tuple[str, ...]
    if v2:
        limit_files, usage_file, inactive = (
            ("memory.max", "memory.high"),
            "memory.current",
            "inactive_file",
        )
    else:
        limit_files, usage_file, inactive = (
            ("memory.limit_in_bytes",),
            "memory.usage_in_bytes",
            "total_inactive_file",
        )
    directories = _cgroup_dirs(read, v2=v2)
    if not directories:
        return max(available, 0)  # not in a memory cgroup
    visible = False
    for directory in directories:
        values = [read(posixpath.join(directory, name)) for name in limit_files]
        if v2:
            controllers = read(posixpath.join(directory, "cgroup.controllers"))
            if controllers is None:
                continue  # level not visible here (container without cgroupns)
            visible = True
            if "memory" not in controllers.split():
                continue  # memory controller not enabled at this level
            if values[0] is None and not read(posixpath.join(directory, "cgroup.type")):
                continue  # the root cgroup, which has no limit files
        else:
            if values[0] is None:
                continue  # level not visible here (container without cgroupns)
            visible = True
        limits = []
        for value in values:
            if value is None or not value.isdigit():
                if v2 and value == "max":
                    continue  # unlimited
                return None  # the limit cannot be read
            if int(value) < 2**60:  # v1 reports "unlimited" as ~2**63
                limits.append(int(value))
        if not limits:
            continue
        usage = read(posixpath.join(directory, usage_file)) or ""
        if not usage.isdigit():
            return None  # limited, but usage is unknown
        reclaimable = 0
        for line in (read(posixpath.join(directory, "memory.stat")) or "").splitlines():
            key, _, value = line.partition(" ")
            if key == inactive and value.strip().isdigit():
                reclaimable = int(value)
        available = min(available, min(limits) - max(0, int(usage) - reclaimable))
    if not visible:
        return None  # in a memory cgroup, but none of its levels can be read
    return max(available, 0)


def _cgroup_dirs(read: Callable[[str], Optional[str]], v2: bool) -> list[str]:
    """This process's memory/cpu cgroup directory and its ancestors, leaf first.

    In containers without a cgroup namespace the leaf may not exist under the
    mount; missing levels are skipped by the callers (reads return None), and
    the mount root, which is the container's own cgroup, is still checked. The
    memory check treats a path with no readable level as unknown.
    """
    root = "/sys/fs/cgroup" if v2 else "/sys/fs/cgroup/memory"
    for line in (read("/proc/self/cgroup") or "").splitlines():
        hierarchy, controllers, path = (line.split(":", 2) + ["", ""])[:3]
        if (v2 and hierarchy == "0" and not controllers) or (
            not v2 and "memory" in controllers.split(",")
        ):
            parts = [p for p in path.split("/") if p]
            return [posixpath.join(root, *parts[:i]) for i in range(len(parts), -1, -1)]
    return []


_JOB_LIMIT_ACTIVE_PROCESS = 0x0008
_JOB_LIMIT_PROCESS_MEMORY = 0x0100
_JOB_LIMIT_JOB_MEMORY = 0x0200


def _apply_job_limits(commit: int, flags: int, job_limit: int, peak_used: int) -> int:
    """Commit headroom under a Windows job object's limits.

    A job-wide memory limit caps commit; its peak usage is used because the
    current usage is not reported (peak >= current, so this is conservative).
    Per-process memory and process-count limits are not evaluated: they
    return 0, which keeps conversion sequential.
    """
    if flags & (_JOB_LIMIT_ACTIVE_PROCESS | _JOB_LIMIT_PROCESS_MEMORY):
        return 0
    if flags & _JOB_LIMIT_JOB_MEMORY:
        commit = min(commit, job_limit - peak_used)
    return max(commit, 0)


def _windows_headroom() -> tuple[Optional[int], Optional[int]]:
    """(available physical memory, available commit) for this process.

    Only the process's immediate job object can be queried; limits of an
    enclosing job are not visible.
    """
    if sys.platform != "win32":
        return None, None
    import ctypes
    from ctypes import wintypes

    class MemoryStatusEx(ctypes.Structure):
        _fields_ = [("dwLength", wintypes.DWORD), ("dwMemoryLoad", wintypes.DWORD)] + [
            (name, ctypes.c_ulonglong)
            for name in (
                "ullTotalPhys",
                "ullAvailPhys",
                "ullTotalPageFile",
                "ullAvailPageFile",
                "ullTotalVirtual",
                "ullAvailVirtual",
                "ullAvailExtendedVirtual",
            )
        ]

    class ExtendedLimitInformation(ctypes.Structure):  # JOBOBJECT_EXTENDED_LIMIT_...
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

    kernel32 = ctypes.WinDLL("kernel32")
    status = MemoryStatusEx()
    status.dwLength = ctypes.sizeof(status)
    if not kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
        return None, None

    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    kernel32.IsProcessInJob.argtypes = [
        wintypes.HANDLE,
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.BOOL),
    ]
    in_job = wintypes.BOOL()
    if not kernel32.IsProcessInJob(
        kernel32.GetCurrentProcess(), None, ctypes.byref(in_job)
    ):
        return None, None
    if not in_job.value:
        return status.ullAvailPhys, status.ullAvailPageFile
    limits = ExtendedLimitInformation()
    kernel32.QueryInformationJobObject.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.c_void_p,
    ]
    if not kernel32.QueryInformationJobObject(  # 9: JobObjectExtendedLimitInformation
        None, 9, ctypes.byref(limits), ctypes.sizeof(limits), None
    ):
        return None, None  # in a job whose limits cannot be read
    commit = _apply_job_limits(
        status.ullAvailPageFile,
        limits.LimitFlags,
        limits.JobMemoryLimit,
        limits.PeakJobMemoryUsed,
    )
    return status.ullAvailPhys, commit


def _shared_memory_has_room(size: int) -> bool:
    """On Linux, shared memory lives in /dev/shm (often only 64 MiB in
    containers), and writing past its free space raises SIGBUS, which kills the
    process, instead of an exception. So check first."""
    if not sys.platform.startswith("linux"):
        return True
    try:
        stat = os.statvfs("/dev/shm")
    except OSError:
        return False
    return stat.f_bavail * stat.f_frsize >= size + _SHM_SLACK


def _read_text(path: str) -> Optional[str]:
    try:
        with open(path) as f:
            return f.read().strip()
    except OSError:
        return None


def _warn(reason: str) -> None:
    warnings.warn(
        f"pdf_workers: {reason}; converting sequentially.",
        PdfParallelWarning,
        stacklevel=3,
    )
