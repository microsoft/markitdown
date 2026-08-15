# SPDX-FileCopyrightText: 2026-present Ayush Chaugule
#
# SPDX-License-Identifier: MIT

# hatch reads this for the installed package's own version (pyproject.toml's
# [tool.hatch.version] points here) -- it's also the version shown in the
# in-app About dialog (about.py), so there is exactly one place to bump it.
__version__ = "0.1.0"

# Single source of truth for the application name. Drives the window title,
# the in-window heading, and the About dialog (app.py / about.py both import
# it from here).
APP_TITLE = "MarkItDown Desktop"
