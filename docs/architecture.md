# MarkItDown Architecture Overview

## Core Modules

MarkItDown's architecture is organized into modular components that can be used independently or together:

### 1. Core Conversion Engine (`_markitdown.py`)
- Main `MarkItDown` class that orchestrates the conversion pipeline
- Manages converter registration and priority ordering
- Provides the public API for conversion operations
- **New**: Integrated caching support for local file conversions

### 2. Progress Tracking (`_progress.py`)
Track conversion progress with granular phase information:

```python
from markitdown import ConversionPhase, create_progress_reporter

def my_callback(progress):
    print(f"Phase: {progress.phase}, {progress.current}/{progress.total}")
    print(f"Message: {progress.message}")
    print(f"Percent: {progress.percentage:.1f}%")

tracker = create_progress_reporter(my_callback)
tracker.set_phase(ConversionPhase.CONVERTING, total=100)
tracker.update(50, message="Halfway done!")
```

**Features:**
- `ConversionPhase` enum: `detecting`, `converting`, `extracting_images`, `ocr`, `finalizing`
- Thread-safe progress updates
- Callback-based notification
- Percentage calculation

### 3. Caching (`_cache.py`)
Optional caching to avoid re-processing the same files:

```python
from markitdown import enable_global_cache, ConversionCache

# Enable global caching (100 entries, 1 hour TTL)
enable_global_cache(max_size=100, ttl_seconds=3600)

# From now on, MarkItDown.convert() will use cache automatically
md = MarkItDown()
result1 = md.convert("large_file.pdf")  # Converts and caches
result2 = md.convert("large_file.pdf")  # Returns cached result (fast!)

# Create a custom cache instance
custom_cache = ConversionCache(max_size=50, ttl_seconds=7200)
stats = custom_cache.get_stats()
print(f"Cache size: {stats['entry_count']} entries")
print(f"Memory usage: {stats['estimated_memory_bytes'] / 1024:.1f} KB")
```

**Memory-Aware Features:**
- Automatic eviction when system memory is low (< 10% available)
- Per-process memory threshold (500MB by default)
- Garbage collection triggered on memory pressure
- Estimated memory usage tracking

**Cache Statistics:**
```python
cache = ConversionCache()
stats = cache.get_stats()
# Returns:
# {
#   "entry_count": 0,
#   "max_entries": 100,
#   "ttl_seconds": 3600,
#   "estimated_memory_bytes": 0,
#   "memory_pressure_detected": False
# }
```

### 4. Logging (`_logging.py`)
Unified logging facade for consistent logging behavior:

```python
from markitdown import logging

# Configure logging
logging.configure_logging(
    level=logging.logging.DEBUG,
    format="%(levelname)s:%(name)s:%(message)s"
)

# Log messages
logging.debug("Debug information")
logging.info("Conversion started")
logging.warning("Low disk space")
logging.error("Conversion failed")

# Check if logging has been configured
if logging.is_configured():
    print("Logging is ready")
```

**Features:**
- NullHandler by default (no output unless configured)
- Configurable log levels and formats
- Custom handler support
- Works with standard Python logging ecosystem

## Converter Architecture

### Base Converter (`_base_converter.py`)
Abstract base class that all converters implement:
- `accept()` - Check if this converter can handle the stream
- `convert()` - Perform the actual conversion
- Returns `DocumentConverterResult` with markdown and metadata

### Converter Pipeline

1. **Stream Detection** - Identify file type using magika + extension
2. **Converter Matching** - Try converters in priority order
3. **Conversion** - Process stream into structured markdown
4. **Caching** - Store result (if caching enabled)

## Security Model

See [`SECURITY.md`](../SECURITY.md) for complete security documentation:

- Path traversal protection
- MCP server authentication
- Path whitelisting
- Scheme restrictions
- Plugin security

## Performance Optimizations

### PDF Memory Management
- Per-page cleanup with `page.close()` after processing
- Avoids O(n) memory growth with document size
- Works with both pdfplumber and pdfminer backends

### Stream Handling
- Non-seekable streams are buffered in memory
- 64KB content hashing for cache keys (efficient for large files)

### Memory-Aware Caching
- Monitors system memory pressure
- Automatic eviction of 50% of entries when memory is low
- Triggers garbage collection after eviction
- `psutil`-enhanced detection (falls back gracefully if not installed)

## Usage Patterns

### Basic Conversion
```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("document.pdf")
print(result.markdown)
```

### With Caching Enabled
```python
from markitdown import MarkItDown, enable_global_cache, get_global_cache

enable_global_cache(max_size=200, ttl_seconds=7200)
md = MarkItDown()

# First call: converts and caches
result1 = md.convert("large_document.pdf")

# Second call: returns cached result instantly
result2 = md.convert("large_document.pdf")

# Inspect cache stats
cache = get_global_cache()
print(cache.get_stats())
```

### With Progress Tracking
```python
from markitdown import MarkItDown, create_progress_reporter

def show_progress(progress):
    print(f"\r{progress.phase}: {progress.percentage:.1f}%", end="")

tracker = create_progress_reporter(show_progress)
md = MarkItDown()
result = md.convert("document.pdf")
```

### With Logging
```python
import logging as pylogging
from markitdown import logging as md_logging

md_logging.configure_logging(
    level=pylogging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

md = MarkItDown()
result = md.convert("document.pdf")
```

## Extending MarkItDown

### Custom Converters
1. Subclass `DocumentConverter`
2. Implement `accept()` and `convert()` methods
3. Register with `MarkItDown.register_converter()`

### Plugins
1. Create a package with `register_converters()` entry point
2. Install in environment
3. Enable with `MarkItDown(enable_plugins=True)`

## Module Dependencies

```
markitdown/
├── _markitdown.py        # Core engine (depends on converters, _cache)
├── _cache.py             # Caching (no internal dependencies)
├── _progress.py          # Progress tracking (no dependencies)
├── _logging.py           # Logging (no dependencies)
├── _stream_info.py       # Stream metadata (no dependencies)
├── _exceptions.py        # Exception hierarchy (no dependencies)
├── _base_converter.py    # Converter base class (no dependencies)
└── converters/           # Individual format converters
    ├── _pdf_converter.py
    ├── _docx_converter.py
    ├── _xlsx_converter.py
    └── ...
```
