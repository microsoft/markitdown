"""Tests for the conversion caching module."""
import os
import tempfile
import time
from pathlib import Path

import pytest

from markitdown import _cache
from markitdown._cache import (
    ConversionCache,
    CacheEntry,
    get_global_cache,
    enable_global_cache,
    disable_global_cache,
    _global_cache,
)


def setup_function():
    """Reset global cache before each test."""
    _cache._global_cache = None


def create_test_file(content: bytes = b"test content") -> str:
    """Create a temporary test file and return its path."""
    fd, path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(content)
    except Exception:
        os.close(fd)
        raise
    return path


def test_cache_entry_creation():
    """Test that CacheEntry stores data correctly."""
    entry = CacheEntry(
        result="test result",
        timestamp=12345.0,
        file_size=100,
        file_mtime=67890.0,
    )
    assert entry.result == "test result"
    assert entry.timestamp == 12345.0
    assert entry.file_size == 100
    assert entry.file_mtime == 67890.0


def test_conversion_cache_initialization():
    """Test that ConversionCache initializes with correct defaults."""
    cache = ConversionCache(max_size=50, ttl_seconds=7200)
    assert cache._max_size == 50
    assert cache._ttl == 7200
    assert cache.size == 0


def test_conversion_cache_default_params():
    """Test default parameters of ConversionCache."""
    cache = ConversionCache()
    assert cache._max_size == 100
    assert cache._ttl == 3600


def test_conversion_cache_put_and_get():
    """Test basic put and get operations."""
    cache = ConversionCache()
    file_path = create_test_file(b"Hello, World!")

    try:
        # Put a result in cache
        cache.put(file_path, "converted result")
        assert cache.size == 1

        # Get it back
        result = cache.get(file_path)
        assert result == "converted result"
    finally:
        os.unlink(file_path)


def test_conversion_cache_nonexistent_file():
    """Test get/put with nonexistent files return None without error."""
    cache = ConversionCache()
    nonexistent = "/nonexistent/path/file.txt"

    result = cache.get(nonexistent)
    assert result is None

    # Put should not raise either
    cache.put(nonexistent, "result")
    assert cache.size == 0  # Should not be added


def test_conversion_cache_ttl_expiry():
    """Test that cache entries expire after TTL."""
    cache = ConversionCache(ttl_seconds=1)  # 1 second TTL
    file_path = create_test_file(b"content")

    try:
        cache.put(file_path, "result")
        assert cache.get(file_path) == "result"  # Should be there

        # Wait for TTL to expire
        time.sleep(1.1)

        # Should be expired
        result = cache.get(file_path)
        assert result is None
        assert cache.size == 0  # Entry was removed
    finally:
        os.unlink(file_path)


def test_conversion_cache_no_ttl():
    """Test that None TTL means no expiration."""
    cache = ConversionCache(ttl_seconds=None)
    file_path = create_test_file(b"content")

    try:
        cache.put(file_path, "result")
        # Even after waiting, should still be there
        time.sleep(0.1)
        assert cache.get(file_path) == "result"
    finally:
        os.unlink(file_path)


def test_conversion_cache_file_modification_invalidates():
    """Test that modifying a file invalidates its cache entry."""
    cache = ConversionCache()
    file_path = create_test_file(b"original content")

    try:
        cache.put(file_path, "original result")
        assert cache.get(file_path) == "original result"

        # Modify the file
        time.sleep(0.01)  # Ensure mtime changes
        with open(file_path, "wb") as f:
            f.write(b"modified content")

        # Cache should miss
        result = cache.get(file_path)
        assert result is None
    finally:
        os.unlink(file_path)


def test_conversion_cache_eviction_at_capacity():
    """Test that oldest entries are evicted when cache reaches max_size."""
    cache = ConversionCache(max_size=3, ttl_seconds=None)

    files = []
    for i in range(5):
        path = create_test_file(f"content {i}".encode())
        files.append(path)
        time.sleep(0.01)  # Ensure different timestamps
        cache.put(path, f"result {i}")

    try:
        # Only 3 entries should remain
        assert cache.size == 3

        # The first 2 should have been evicted
        assert cache.get(files[0]) is None
        assert cache.get(files[1]) is None

        # The last 3 should still be there
        assert cache.get(files[2]) == "result 2"
        assert cache.get(files[3]) == "result 3"
        assert cache.get(files[4]) == "result 4"
    finally:
        for path in files:
            os.unlink(path)


def test_conversion_cache_clear():
    """Test that clear() removes all entries."""
    cache = ConversionCache()
    files = [create_test_file(f"c{i}".encode()) for i in range(5)]

    try:
        for path in files:
            cache.put(path, "result")

        assert cache.size == 5
        cache.clear()
        assert cache.size == 0

        for path in files:
            assert cache.get(path) is None
    finally:
        for path in files:
            os.unlink(path)


def test_conversion_cache_same_content_different_name():
    """Test that files with same content but different paths get different keys."""
    cache = ConversionCache()
    content = b"Same content for both files"

    path1 = create_test_file(content)
    path2 = create_test_file(content)

    try:
        cache.put(path1, "result for file 1")
        cache.put(path2, "result for file 2")

        assert cache.size == 2
        assert cache.get(path1) == "result for file 1"
        assert cache.get(path2) == "result for file 2"
    finally:
        os.unlink(path1)
        os.unlink(path2)


def test_conversion_cache_partial_read_for_hash():
    """Test that cache uses only first 64KB for hashing (performance)."""
    cache = ConversionCache()
    # Create a file larger than 64KB
    large_content = b"x" * 100000  # ~100KB
    file_path = create_test_file(large_content)

    try:
        cache.put(file_path, "large result")
        assert cache.get(file_path) == "large result"
    finally:
        os.unlink(file_path)


def test_global_cache_initially_none():
    """Test that global cache is None by default."""
    assert get_global_cache() is None


def test_enable_global_cache():
    """Test that enable_global_cache creates and returns a cache."""
    enable_global_cache(max_size=50, ttl_seconds=1800)

    cache = get_global_cache()
    assert isinstance(cache, ConversionCache)
    assert cache._max_size == 50
    assert cache._ttl == 1800


def test_disable_global_cache():
    """Test that disable_global_cache removes the global cache."""
    enable_global_cache()
    assert get_global_cache() is not None

    disable_global_cache()
    assert get_global_cache() is None


def test_global_cache_is_shared():
    """Test that all calls to get_global_cache return the same instance."""
    enable_global_cache()

    cache1 = get_global_cache()
    cache2 = get_global_cache()

    assert cache1 is cache2

    # Put something in one, get it from the other
    file_path = create_test_file(b"test")
    try:
        cache1.put(file_path, "shared result")
        assert cache2.get(file_path) == "shared result"
    finally:
        os.unlink(file_path)


def test_compute_key_uses_content():
    """Test that cache key is based on file content hash."""
    cache = ConversionCache()

    # Create two files with same content
    path1 = create_test_file(b"same content")
    path2 = create_test_file(b"same content")

    try:
        # Read first 64KB to compute keys
        with open(path1, "rb") as f:
            content1 = f.read(65536)
        with open(path2, "rb") as f:
            content2 = f.read(65536)

        key1 = cache._compute_key(path1, content1)
        key2 = cache._compute_key(path2, content2)

        # Same content -> same hash part of key
        # But different basename -> different full keys
        hash1 = key1.split(":")[1]
        hash2 = key2.split(":")[1]
        assert hash1 == hash2
    finally:
        os.unlink(path1)
        os.unlink(path2)


def test_empty_file_cache():
    """Test caching works with empty files."""
    cache = ConversionCache()
    path = create_test_file(b"")

    try:
        cache.put(path, "empty result")
        assert cache.get(path) == "empty result"
    finally:
        os.unlink(path)


def test_cache_size_property():
    """Test that size property returns correct count."""
    cache = ConversionCache()
    assert cache.size == 0

    paths = [create_test_file(b"a"), create_test_file(b"b")]
    try:
        for i, path in enumerate(paths):
            cache.put(path, f"result {i}")

        assert cache.size == 2
    finally:
        for path in paths:
            os.unlink(path)


def test_cache_estimated_memory_usage():
    """Test that estimated_memory_usage returns reasonable value."""
    cache = ConversionCache()
    assert cache.estimated_memory_usage == 0

    path = create_test_file(b"test content")
    try:
        cache.put(path, "result" * 1000)  # Large-ish result
        assert cache.estimated_memory_usage > 0  # Should have some size
    finally:
        os.unlink(path)


def test_cache_get_stats():
    """Test that get_stats returns all expected fields."""
    cache = ConversionCache(max_size=50, ttl_seconds=7200)
    stats = cache.get_stats()

    assert "entry_count" in stats
    assert "max_entries" in stats
    assert "ttl_seconds" in stats
    assert "estimated_memory_bytes" in stats
    assert "memory_pressure_detected" in stats
    assert stats["entry_count"] == 0
    assert stats["max_entries"] == 50
    assert stats["ttl_seconds"] == 7200


def test_cache_clear_resets_memory_counter():
    """Test that clear() resets memory usage counter."""
    cache = ConversionCache()
    path = create_test_file(b"content")

    try:
        cache.put(path, "result")
        assert cache.estimated_memory_usage > 0

        cache.clear()
        assert cache.estimated_memory_usage == 0
        assert cache.size == 0
    finally:
        os.unlink(path)


def test_cache_overwrite_updates_memory():
    """Test that overwriting an entry correctly updates memory counter."""
    cache = ConversionCache()
    path = create_test_file(b"content")

    try:
        cache.put(path, "small result")
        size_before = cache.estimated_memory_usage
        assert size_before > 0

        # Overwrite with much larger result
        cache.put(path, "large result" * 1000)
        size_after = cache.estimated_memory_usage
        assert size_after > size_before
    finally:
        os.unlink(path)


def test_memory_pressure_check_no_crash():
    """Test that _check_memory_pressure doesn't crash even without psutil."""
    cache = ConversionCache()
    # Just verify it returns a bool and doesn't raise
    result = cache._check_memory_pressure()
    assert isinstance(result, bool)


def test_evict_oldest_works():
    """Test that _evict_oldest removes entries correctly."""
    cache = ConversionCache(max_size=10)
    paths = [create_test_file(f"content{i}".encode()) for i in range(5)]

    try:
        for path in paths:
            time.sleep(0.01)  # Ensure different timestamps
            cache.put(path, "result")

        assert cache.size == 5

        cache._evict_oldest(2)
        assert cache.size == 3  # 5 - 2 = 3
    finally:
        for path in paths:
            os.unlink(path)


def test_evict_oldest_empty_cache_no_crash():
    """Test that _evict_oldest on empty cache doesn't crash."""
    cache = ConversionCache()
    cache._evict_oldest(5)  # Should not raise
    assert cache.size == 0
