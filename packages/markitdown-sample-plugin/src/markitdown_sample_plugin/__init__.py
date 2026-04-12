# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT

from .__about__ import __version__
from ._plugin import RtfConverter, __plugin_interface_version__, register_converters

__all__ = [
    "__version__",
    "__plugin_interface_version__",
    "register_converters",
    "RtfConverter",
]
