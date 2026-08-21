# MarkItDown GUI Setup and Run Guide

This guide explains how to install dependencies and run the `markitdown-gui` desktop app.

## 1. Prerequisites

- Python 3.10+
- PowerShell (Windows)
- This repository cloned locally

## 2. Open the Project Folder

```powershell
cd D:\develpment\FileConverterToMD
```

## 3. Create and Activate Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If script execution is blocked in PowerShell, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 4. Install MarkItDown with GUI + DOCX Support

Recommended for GUI and Word files (`.docx`):

```powershell
pip install -e "packages/markitdown[gui,docx]"
```

Install all optional converters instead:

```powershell
pip install -e "packages/markitdown[all,gui]"
```

## 5. Run the GUI

Option A (dedicated command):

```powershell
markitdown-gui
```

Option B (through main CLI):

```powershell
markitdown --gui
```

## 6. Convert Files in the GUI

1. Click **Select Files** and choose one or more files.
2. Choose output mode:
   - Keep **Save next to each source file** enabled, or
   - Disable it and select an **Output folder**.
3. Click **Convert to Markdown**.
4. Check the log panel for success/error messages.

Each selected input file produces one `.md` output file.

## 7. Quick Verification (Optional)

Check CLI install:

```powershell
markitdown --version
```

Quick single-file conversion test:

```powershell
markitdown "D:\path\to\file.docx" -o "D:\path\to\file.md"
```

## Troubleshooting

### Error: MissingDependencyException for `.docx`

Install DOCX dependencies:

```powershell
pip install -e "packages/markitdown[docx]"
```

or

```powershell
pip install -e "packages/markitdown[gui,docx]"
```

### Error on reinstall: Access denied for `markitdown-gui.exe`

Close any running GUI window, then reinstall:

```powershell
pip install -e "packages/markitdown[gui,docx]"
```

### Command not found (`markitdown-gui`)

- Ensure virtual environment is activated.
- Reinstall package in editable mode:

```powershell
pip install -e "packages/markitdown[gui,docx]"
```
