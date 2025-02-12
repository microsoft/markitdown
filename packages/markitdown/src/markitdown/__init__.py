# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT

from .__about__ import __version__
from ._markitdown import MarkItDown
from ._exceptions import (
    MarkItDownException,
    ConverterPrerequisiteException,
    FileConversionException,
    UnsupportedFormatException,
)
from .converters import DocumentConverter, DocumentConverterResult

__all__ = [
    "__version__",
    "MarkItDown",
    "DocumentConverter",
    "DocumentConverterResult",
    "MarkItDownException",
    "ConverterPrerequisiteException",
    "FileConversionException",
    "UnsupportedFormatException",
]
