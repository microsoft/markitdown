"""Caching for MarkItDown conversion results.

This module provides optional caching of conversion results to
avoid re-processing the same file multiple times.
"""
import hashlib
import os
import time
import gc
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any
import pickle

# Try to import psutil for memory awareness, but it's optional
try:
    import psutil

    _HAS_PSUTIL = True
except ImportError:
    _HAS_PSUTIL = False


@dataclass
class CacheEntry:
    """A single cache entry."""

    result: Any  # DocumentConverterResult
    timestamp: float
    file_size: int
    file_mtime: float
    estimated_size: int = 0  # Estimated memory size in bytes


def _estimate_object_size(obj: Any) -> int:
    """Estimate the memory size of an object (rough estimate).

    Used for memory-aware caching decisions.
    """
    try:
        # Very rough estimate based on pickle size
        return len(pickle.dumps(obj))
    except (pickle.PicklingError, TypeError):
        return 1024  # Default estimate: 1KB


class ConversionCache:
    """Caches conversion results based on file content hash.

    Memory-aware: automatically evicts entries when system memory is low.
    """

    # Memory threshold: evict if available memory is below this (percentage)
    MEMORY_THRESHOLD_PERCENT = 10.0
    # Per-process memory threshold (in MB) - evict if process exceeds this
    PROCESS_MEMORY_THRESHOLD_MB = 500

    def __init__(self, max_size: int = 100, ttl_seconds: Optional[int] = 3600):
        """Initialize cache.

        Args:
            max_size: Maximum number of entries to keep (default: 100)
            ttl_seconds: Time-to-live in seconds, None = no expiry (default: 1h)
        """
        self._cache: Dict[str, CacheEntry] = {}
        self._max_size = max_size
        self._ttl = ttl_seconds
        self._total_cached_size = 0  # Estimated total cache size in bytes

    def _check_memory_pressure(self) -> bool:
        """Check if system is under memory pressure.

        Returns:
            True if memory is low and we should evict entries.
        """
        if not _HAS_PSUTIL:
            return False

        try:
            # Check system-wide memory
            mem = psutil.virtual_memory()
            if mem.available / mem.total * 100 < self.MEMORY_THRESHOLD_PERCENT:
                return True

            # Check process memory
            process = psutil.Process()
            if process.memory_info().rss / (1024 * 1024) > self.PROCESS_MEMORY_THRESHOLD_MB:
                return True
        except (psutil.Error, OSError):
            pass

        return False

    def _evict_oldest(self, count: int = 1) -> None:
        """Evict the oldest N entries from cache."""
        if not self._cache:
            return

        # Sort by timestamp (oldest first)
        sorted_keys = sorted(self._cache.keys(), key=lambda k: self._cache[k].timestamp)
        for key in sorted_keys[:count]:
            entry = self._cache.pop(key)
            self._total_cached_size -= entry.estimated_size

    def _maybe_evict_for_memory(self) -> None:
        """Evict entries if memory pressure is high."""
        if not self._check_memory_pressure():
            return

        # Evict 50% of entries when under memory pressure
        evict_count = max(1, len(self._cache) // 2)
        self._evict_oldest(evict_count)

        # Also trigger garbage collection
        if evict_count > 0:
            gc.collect(generation=1)

    def _compute_key(self, file_path: str, file_content: bytes) -> str:
        """Compute cache key from file path and content."""
        h = hashlib.sha256()
        h.update(file_content)
        content_hash = h.hexdigest()[:16]
        return f"{os.path.basename(file_path)}:{content_hash}"

    def get(self, file_path: str) -> Optional[Any]:
        """Get cached result for a file.

        Args:
            file_path: Path to the file

        Returns:
            Cached DocumentConverterResult or None if not cached/invalidated
        """
        # Check memory pressure before serving
        self._maybe_evict_for_memory()

        try:
            stat = os.stat(file_path)
        except (OSError, FileNotFoundError):
            return None

        # Compute key from file content
        try:
            with open(file_path, "rb") as f:
                content = f.read(65536)  # First 64KB for hashing
        except OSError:
            return None

        key = self._compute_key(file_path, content)
        entry = self._cache.get(key)

        if entry is None:
            return None

        # Check TTL
        if self._ttl is not None and time.time() - entry.timestamp > self._ttl:
            self._total_cached_size -= entry.estimated_size
            del self._cache[key]
            return None

        # Check file changed
        if stat.st_size != entry.file_size or stat.st_mtime != entry.file_mtime:
            self._total_cached_size -= entry.estimated_size
            del self._cache[key]
            return None

        return entry.result

    def put(self, file_path: str, result: Any) -> None:
        """Store result in cache.

        Args:
            file_path: Path to the file
            result: DocumentConverterResult to cache
        """
        # Check memory pressure before adding
        self._maybe_evict_for_memory()

        try:
            stat = os.stat(file_path)
            with open(file_path, "rb") as f:
                content = f.read(65536)
        except OSError:
            return

        key = self._compute_key(file_path, content)

        # Evict oldest if at capacity
        if len(self._cache) >= self._max_size:
            self._evict_oldest(1)

        # Estimate size for memory tracking
        estimated_size = _estimate_object_size(result)

        # If already exists, subtract old size first
        if key in self._cache:
            self._total_cached_size -= self._cache[key].estimated_size

        self._cache[key] = CacheEntry(
            result=result,
            timestamp=time.time(),
            file_size=stat.st_size,
            file_mtime=stat.st_mtime,
            estimated_size=estimated_size,
        )
        self._total_cached_size += estimated_size

    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
        self._total_cached_size = 0

    @property
    def size(self) -> int:
        """Get current number of cache entries."""
        return len(self._cache)

    @property
    def estimated_memory_usage(self) -> int:
        """Get estimated memory usage of cache in bytes."""
        return self._total_cached_size

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "entry_count": len(self._cache),
            "max_entries": self._max_size,
            "ttl_seconds": self._ttl,
            "estimated_memory_bytes": self._total_cached_size,
            "memory_pressure_detected": self._check_memory_pressure(),
        }


# Global cache instance
_global_cache: Optional[ConversionCache] = None


def get_global_cache() -> Optional[ConversionCache]:
    """Get the global cache instance."""
    return _global_cache


def enable_global_cache(max_size: int = 100, ttl_seconds: int = 3600) -> None:
    """Enable global result caching.

    Args:
        max_size: Maximum number of entries (default: 100)
        ttl_seconds: TTL in seconds (default: 3600 = 1 hour)
    """
    global _global_cache
    _global_cache = ConversionCache(max_size=max_size, ttl_seconds=ttl_seconds)


def disable_global_cache() -> None:
    """Disable global result caching."""
    global _global_cache
    _global_cache = None
