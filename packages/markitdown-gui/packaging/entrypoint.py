# SPDX-FileCopyrightText: 2026-present Ayush Chaugule
#
# SPDX-License-Identifier: MIT
"""PyInstaller's entry script.

Why this file exists instead of pointing PyInstaller straight at
`markitdown_gui/__main__.py`: PyInstaller runs its entry script as the
top-level `__main__` module, which breaks `__main__.py`'s own `from .app
import run` (a relative import needs a real parent package, and a script run
directly has none). Importing `markitdown_gui` as an installed package from
here sidesteps that -- `__main__.py` is then loaded as a submodule, where the
relative import works normally.
"""

from markitdown_gui.__main__ import main

if __name__ == "__main__":
    main()
