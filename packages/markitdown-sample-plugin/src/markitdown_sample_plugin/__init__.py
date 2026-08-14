# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT

from ._plugin import __plugin_interface_version__, register_converters, RtfConverter
from .__about__ import __version__

__all__ = [
    "__version__",
    "__plugin_interface_version__",
    "register_converters",
    "RtfConverter",
]
