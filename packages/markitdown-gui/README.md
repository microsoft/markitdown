# MarkItDown GUI

A small, fixed-size Tkinter desktop app for [MarkItDown](../markitdown), styled to look at
home on a Linux Mint / Cinnamon desktop (Mint-Y-Dark-Purple). Pick a file, convert it to
Markdown, save the result -- nothing more.

This package is source; see [`../../run.sh`](../../run.sh) at the repo root for how end users
are meant to launch it without installing anything themselves.

## Running from source (development)

```bash
cd packages/markitdown-gui
python3 -m venv .venv && source .venv/bin/activate
pip install -e '.[bundle]'
python -m markitdown_gui
```

`python3-tk` must be importable by whichever Python runs this (it's part of the stdlib but
often ships as a separate OS package -- on Debian/Ubuntu/Mint: `sudo apt install python3-tk`).
This only matters for running from source; the packaged/bundled distribution (see the repo
root `run.sh` and `packaging/build_linux.sh`) has Tk's runtime baked in and does not require
`python3-tk` on the end user's machine.

## Package layout

- `theme.py` -- the Mint-Y-Dark-Purple color palette and font resolution (values read
  directly from the installed Cinnamon theme's CSS, not guessed).
- `formats.py` -- introspects a live `MarkItDown()` instance to build the "Supports: ..."
  label from the converters actually registered, instead of a hand-maintained list.
- `widgets.py` -- small Canvas-based widgets (`RoundedButton`, `ProgressBar`) styled to match
  the theme, since `ttk` can't do real rounded corners portably.
- `convert.py` -- a thin wrapper around `markitdown.MarkItDown().convert_local()`.
- `app.py` -- the main window: wires the widgets together, runs conversion on a background
  thread so the UI never blocks, and drives the progress bar animation.
- `about.py` -- the About dialog (app name, version, source link).
- `__main__.py` -- `python -m markitdown_gui` entry point (also the PyInstaller entry point).

## Packaging

See `packaging/build_linux.sh` to build a standalone onefile Linux executable with PyInstaller.
