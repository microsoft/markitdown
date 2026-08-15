#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026-present Ayush Chaugule
#
# SPDX-License-Identifier: MIT
#
# Builds a standalone, single-file Linux executable for the MarkItDown GUI
# using PyInstaller, so end users can run it without installing Python
# packages, a venv, or anything else themselves.
#
# Usage:
#   packages/markitdown-gui/packaging/build_linux.sh [--clean]
#
#   --clean   Wipe the build venv first (slower, but fully reproducible).
#             Without it, an existing venv is reused so repeat builds are fast.
#
# Output: packages/markitdown-gui/packaging/dist/markitdown-gui
#
# Note: ffmpeg and exiftool are external system binaries, not Python
# packages, so they are NOT bundled by this script. Audio transcription for
# non-WAV formats and image EXIF metadata extraction degrade gracefully if
# they aren't present on the machine running the built binary.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUI_PKG_DIR="$(dirname "$SCRIPT_DIR")"          # packages/markitdown-gui
PACKAGES_DIR="$(dirname "$GUI_PKG_DIR")"        # packages
VENV_DIR="$GUI_PKG_DIR/.build-venv"
DIST_DIR="$SCRIPT_DIR/dist"
BUILD_DIR="$SCRIPT_DIR/build"

if [[ "${1:-}" == "--clean" ]]; then
    echo "==> --clean requested, removing existing build venv"
    rm -rf "$VENV_DIR"
fi

echo "==> Checking for a Python with Tk support (needed to BUILD; end users won't need it)"
if ! python3 -c "import tkinter" >/dev/null 2>&1; then
    echo "ERROR: python3 -c 'import tkinter' failed." >&2
    echo "This machine's Python doesn't have Tk support, which PyInstaller needs to" >&2
    echo "find and bundle the Tcl/Tk runtime. Install it and re-run:" >&2
    echo "    sudo apt install python3-tk" >&2
    echo "(This is a one-time requirement for whoever BUILDS the binary. The binary" >&2
    echo "produced by this script does NOT require python3-tk on the machine that runs it.)" >&2
    exit 1
fi

echo "==> Setting up build venv at $VENV_DIR"
if [[ ! -d "$VENV_DIR" ]]; then
    if ! python3 -m venv "$VENV_DIR" 2>/tmp/markitdown-gui-build-venv-error.$$; then
        # See run.sh for the full explanation: some Debian/Ubuntu/Mint installs
        # ship Python without stdlib venv's ensurepip support. Fall back to the
        # `virtualenv` package installed into ~/.local (no sudo, no system changes).
        echo "    (stdlib venv unavailable here -- trying a user-local fallback, no sudo needed)"
        cat /tmp/markitdown-gui-build-venv-error.$$ >&2
        rm -f /tmp/markitdown-gui-build-venv-error.$$
        python3 -m pip install --user --quiet virtualenv 2>/dev/null \
            || python3 -m pip install --user --break-system-packages --quiet virtualenv
        python3 -m virtualenv --quiet "$VENV_DIR"
    fi
    rm -f /tmp/markitdown-gui-build-venv-error.$$
fi
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

python -m pip install --quiet --upgrade pip wheel

echo "==> Installing markitdown from THIS repo (not PyPI) with the format"
echo "    extras this GUI advertises support for, so the binary bundles"
echo "    whatever is actually in packages/markitdown right now."
pip install --quiet "$PACKAGES_DIR/markitdown[pptx,docx,xlsx,xls,pdf,outlook,audio-transcription]"

echo "==> Installing markitdown-gui itself (its 'markitdown' dependency is"
echo "    already satisfied by the local install above, so pip won't reach PyPI for it)"
pip install --quiet "$GUI_PKG_DIR"

echo "==> Installing PyInstaller"
pip install --quiet "pyinstaller>=6.0"

echo "==> Running PyInstaller"
# --onefile: a single executable, nothing else to distribute alongside it.
# --collect-all magika: bundles its ONNX content-detection model + config
#   (plain module-graph analysis only finds *code*, not this kind of package data).
# --collect-data pdfminer: bundles its CJK cmap files, needed for some PDFs.
# --collect-all speech_recognition: bundles its data *and* the statically
#   linked `flac` helper binary it ships for converting audio before transcription.
pyinstaller \
    --onefile \
    --windowed \
    --name markitdown-gui \
    --distpath "$DIST_DIR" \
    --workpath "$BUILD_DIR" \
    --specpath "$SCRIPT_DIR" \
    --collect-all magika \
    --collect-data pdfminer \
    --collect-all speech_recognition \
    --noconfirm \
    "$SCRIPT_DIR/entrypoint.py"

deactivate

BINARY="$DIST_DIR/markitdown-gui"
if [[ -f "$BINARY" ]]; then
    chmod +x "$BINARY"
    SIZE=$(du -h "$BINARY" | cut -f1)
    echo ""
    echo "==> Build succeeded: $BINARY ($SIZE)"
    echo "==> Test it standalone before shipping it, e.g. in a clean shell:"
    echo "        env -i HOME=\"\$HOME\" DISPLAY=\"\$DISPLAY\" \"$BINARY\""
    echo "    (that strips your dev PATH/PYTHONPATH/venv so you're testing what an"
    echo "    end user with no Python setup at all would actually run.)"
else
    echo "ERROR: expected output binary not found at $BINARY" >&2
    exit 1
fi
