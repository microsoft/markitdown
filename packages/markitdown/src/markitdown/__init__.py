# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT

from .__about__ import __version__
from ._markitdown import (
    MarkItDown,
    PRIORITY_SPECIFIC_FILE_FORMAT,
    PRIORITY_GENERIC_FILE_FORMAT,
)
from ._base_converter import DocumentConverterResult, DocumentConverter
from ._stream_info import StreamInfo
from ._exceptions import (
    MarkItDownException,
    MissingDependencyException,
    FailedConversionAttempt,
    FileConversionException,
    UnsupportedFormatException,
)
from ._progress import (
    ConversionPhase,
    ConversionProgress,
    ProgressCallback,
    ProgressTracker,
    create_progress_reporter,
)
from ._cache import (
    ConversionCache,
    enable_global_cache,
    disable_global_cache,
    get_global_cache,
    _HAS_PSUTIL,
)

# Re-export logging if available, but don't fail if not imported
try:
    from . import _logging as logging
except ImportError:
    pass

__all__ = [
    "__version__",
    "MarkItDown",
    "DocumentConverter",
    "DocumentConverterResult",
    "MarkItDownException",
    "MissingDependencyException",
    "FailedConversionAttempt",
    "FileConversionException",
    "UnsupportedFormatException",
    "StreamInfo",
    "PRIORITY_SPECIFIC_FILE_FORMAT",
    "PRIORITY_GENERIC_FILE_FORMAT",
    # Progress tracking
    "ConversionPhase",
    "ConversionProgress",
    "ProgressCallback",
    "ProgressTracker",
    "create_progress_reporter",
    # Caching
    "ConversionCache",
    "enable_global_cache",
    "disable_global_cache",
    "get_global_cache",
    # Logging
    "logging",
]
