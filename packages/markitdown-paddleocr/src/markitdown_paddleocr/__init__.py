# SPDX-FileCopyrightText: 2026-present Contributors
# SPDX-License-Identifier: MIT

"""PaddleOCR plugin for MarkItDown."""

from .__about__ import __version__
from ._ocr_service import OCRResult, PaddleOCRService
from ._pdf_converter import PdfConverterWithPaddleOCR
from ._plugin import __plugin_interface_version__, register_converters

__all__ = [
    "__version__",
    "__plugin_interface_version__",
    "register_converters",
    "OCRResult",
    "PaddleOCRService",
    "PdfConverterWithPaddleOCR",
]
