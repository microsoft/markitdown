#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026-present Ayush Chaugule
#
# SPDX-License-Identifier: MIT
#
# One-command launcher for the MarkItDown GUI. This is what end users run
# after downloading a release zip (or `git clone`-ing / "Download ZIP"-ing
# this repo) -- no manual pip install, no manual venv, nothing.
#
#   ./run.sh
#
# What it does, in priority order:
#
#   1. If a prebuilt standalone binary is sitting next to this script (the
#      layout of the GitHub Release zip -- see .github/workflows/build-gui-release.yml),
#      or already built locally via packages/markitdown-gui/packaging/build_linux.sh,
#      just run it directly. Nothing to install; this is the fast, fully
#      self-contained path (Python and Tk are baked into that binary).
#
#   2. Otherwise (a plain source checkout with no prebuilt binary attached --
#      e.g. GitHub's "Download ZIP" on the repo itself, or `git clone`), fall
#      back to bootstrapping a local, throwaway venv and installing the
#      handful of packages the GUI needs into it. Silent and one-time: later
#      runs detect the venv is already set up and start immediately.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.markitdown-gui-venv"
MARKER="$VENV_DIR/.install-ok"

if [[ "${1:-}" == "--clean" ]]; then
    echo "==> --clean requested, removing bootstrapped venv"
    rm -rf "$VENV_DIR"
fi

# --- Path 1: a prebuilt standalone binary is available -----------------

for candidate in \
    "$SCRIPT_DIR/markitdown-gui" \
    "$SCRIPT_DIR/packages/markitdown-gui/packaging/dist/markitdown-gui"
do
    if [[ -x "$candidate" ]]; then
        exec "$candidate" "$@"
    fi
done

# --- Path 2: no prebuilt binary -- bootstrap a local venv ---------------

echo "No prebuilt binary found next to this script; setting up a local"
echo "environment instead (one-time; later runs will be instant)."

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 was not found on your PATH." >&2
    echo "Install Python 3.10+ (e.g. 'sudo apt install python3') and re-run this script." >&2
    exit 1
fi

if [[ ! -f "$MARKER" ]]; then
    rm -rf "$VENV_DIR"
    echo "==> Creating a local virtual environment (this does not touch your system Python)"
    if ! python3 -m venv "$VENV_DIR" 2>/tmp/markitdown-gui-venv-error.$$; then
        # Debian/Ubuntu/Mint often ship Python without the stdlib `venv` module's
        # ensurepip support out of the box (the fix normally is
        # `sudo apt install python3-venv`). Rather than dead-end here, fall back
        # to the `virtualenv` PyPI package, installed into the user's own
        # ~/.local (never system-wide, never needs sudo) via pip's
        # --user flag. This is the one place this project reaches outside a
        # venv to install something -- it's safe because --user confines it to
        # your home directory, same as any other user-local tool install.
        echo "    (stdlib venv unavailable here -- trying a user-local fallback, no sudo needed)"
        if ! python3 -m pip install --user --quiet virtualenv 2>/dev/null \
            && ! python3 -m pip install --user --break-system-packages --quiet virtualenv 2>/tmp/markitdown-gui-venv-error.$$; then
            cat /tmp/markitdown-gui-venv-error.$$ >&2
            rm -f /tmp/markitdown-gui-venv-error.$$
            echo "" >&2
            echo "ERROR: could not create a Python virtual environment." >&2
            echo "On Debian/Ubuntu/Mint this usually means the venv module isn't installed:" >&2
            echo "    sudo apt install python3-venv" >&2
            echo "then re-run ./run.sh. (Alternatively, grab the prebuilt standalone binary" >&2
            echo "from this project's GitHub Releases page instead -- it needs nothing installed.)" >&2
            exit 1
        fi
        if ! python3 -m virtualenv --quiet "$VENV_DIR" 2>/tmp/markitdown-gui-venv-error.$$; then
            cat /tmp/markitdown-gui-venv-error.$$ >&2
            rm -f /tmp/markitdown-gui-venv-error.$$
            echo "ERROR: could not create a Python virtual environment (fallback also failed)." >&2
            exit 1
        fi
    fi
    rm -f /tmp/markitdown-gui-venv-error.$$

    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"

    if ! python -c "import tkinter" >/dev/null 2>&1; then
        echo "" >&2
        echo "ERROR: this Python doesn't have Tk (the GUI toolkit) available." >&2
        echo "On Debian/Ubuntu/Mint, install it with:" >&2
        echo "    sudo apt install python3-tk" >&2
        echo "then re-run ./run.sh." >&2
        deactivate
        rm -rf "$VENV_DIR"
        exit 1
    fi

    echo "==> Installing MarkItDown GUI and its dependencies (this can take a minute)"
    python -m pip install --quiet --upgrade pip wheel
    pip install --quiet "$SCRIPT_DIR/packages/markitdown[pptx,docx,xlsx,xls,pdf,outlook,audio-transcription]"
    pip install --quiet "$SCRIPT_DIR/packages/markitdown-gui"

    touch "$MARKER"
    deactivate
    echo "==> Setup complete"
fi

exec "$VENV_DIR/bin/python" -m markitdown_gui
