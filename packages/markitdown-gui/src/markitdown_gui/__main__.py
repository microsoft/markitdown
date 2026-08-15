# SPDX-FileCopyrightText: 2026-present Ayush Chaugule
#
# SPDX-License-Identifier: MIT
"""Entry point for `python -m markitdown_gui`, the `markitdown-gui` console
script, and the PyInstaller build (see packaging/build_linux.sh)."""

from .app import run


def main() -> None:
    run()


if __name__ == "__main__":
    main()
