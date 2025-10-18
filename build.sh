#!/bin/bash
set -e

# Install all project dependencies, including optional ones for docx and pdf
pip install -e packages/markitdown[all]

# Install PyInstaller
pip install pyinstaller

# Run PyInstaller to create the executable
pyinstaller --onefile --windowed --name MarkitdownGUI packages/markitdown/src/markitdown/run_gui.py --clean

echo "Build successful! The executable can be found in the 'dist' directory."
