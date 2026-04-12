# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT

from .__about__ import __version__
from ._base_converter import DocumentConverter, DocumentConverterResult
from ._exceptions import (
    FailedConversionAttempt,
    FileConversionException,
    MarkItDownException,
    MissingDependencyException,
    UnsupportedFormatException,
)
from ._markitdown import (
    PRIORITY_GENERIC_FILE_FORMAT,
    PRIORITY_SPECIFIC_FILE_FORMAT,
    MarkItDown,
)
from ._stream_info import StreamInfo

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
]
