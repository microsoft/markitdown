# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT

from .__about__ import __version__
from typing import TYPE_CHECKING

if TYPE_CHECKING:
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


def __getattr__(name: str):
    # Keep package imports lightweight for CLI help and version requests.
    if name in (
        "MarkItDown",
        "PRIORITY_SPECIFIC_FILE_FORMAT",
        "PRIORITY_GENERIC_FILE_FORMAT",
    ):
        from . import _markitdown

        value = getattr(_markitdown, name)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(set(globals()) | set(__all__))
