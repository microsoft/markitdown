# SPDX-FileCopyrightText: 2026-present Aryan Kaushik <aryankaushik251@gmail.com>
#
# SPDX-License-Identifier: MIT

from ._plugin import __plugin_interface_version__, register_converters
from ._dicom_converter import DicomConverter
from .__about__ import __version__

__all__ = [
    "__version__",
    "__plugin_interface_version__",
    "register_converters",
    "DicomConverter",
]
