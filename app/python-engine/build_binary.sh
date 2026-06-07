#!/usr/bin/env bash
# Builds the OPTIONAL Python fallback engine: a self-contained PyInstaller
# binary of the original Python markitdown (with all optional extras).
#
# You do NOT need this for normal use — the Rust binary handles all default
# markitdown formats by itself. Build this only if you want the long tail:
# OCR for scanned documents (via plugins), audio transcription, Azure
# converters, or Python plugins.
#
# Usage:  ./build_binary.sh                 # one-file binary (portable, 1-3s cold start)
#         BUILD_MODE=onedir ./build_binary.sh   # folder build (~50ms cold start — best
#                                               # for Auto-fallback on many files)
# Result: dist/markitdown-py  (onefile)  or  dist/markitdown-py/markitdown-py (onedir)
# Point MARKITDOWN_PY_BIN at the produced executable.
set -euo pipefail
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"
MODE="${BUILD_MODE:-onefile}"

echo "==> creating venv"
"$PY" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

echo "==> installing markitdown[all] + pyinstaller"
pip install --quiet --upgrade pip
pip install --quiet pyinstaller "markitdown[all]"
# Optional: local OCR plugin from this repo (uncomment to include):
# pip install --quiet ../../packages/markitdown-ocr

echo "==> writing entry point"
cat > _entry.py <<'EOF'
from markitdown.__main__ import main

if __name__ == "__main__":
    main()
EOF

echo "==> building $MODE binary (this takes a few minutes)"
pyinstaller "--$MODE" --name markitdown-py \
    --collect-all magika \
    --collect-data charset_normalizer \
    --copy-metadata markitdown \
    _entry.py

echo
if [ "$MODE" = "onedir" ]; then
    BIN="$(pwd)/dist/markitdown-py/markitdown-py"
else
    BIN="$(pwd)/dist/markitdown-py"
fi
echo "Built: $BIN ($(du -sh "$(dirname "$BIN")" | cut -f1) total)"
echo
echo "Enable it for the Rust tools with:"
echo "  export MARKITDOWN_PY_BIN=$BIN"
echo "or pass --engine python / --python-bin to the markitdown CLI."
echo "(--engine auto is the default: Rust converts everything it can; the"
echo " Python engine is only invoked for fidelity gaps like OCR.)"
