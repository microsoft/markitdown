# Builds the OPTIONAL Python fallback engine on Windows.
# See build_binary.sh / README.md for what this is and when you need it.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

python -m venv .venv
& .venv\Scripts\Activate.ps1

pip install --quiet --upgrade pip
pip install --quiet pyinstaller "markitdown[all]"

@"
from markitdown.__main__ import main

if __name__ == "__main__":
    main()
"@ | Set-Content -Encoding utf8 _entry.py

pyinstaller --onefile --name markitdown-py `
    --collect-all magika `
    --collect-data charset_normalizer `
    --copy-metadata markitdown `
    _entry.py

Write-Host ""
Write-Host "Built: $PSScriptRoot\dist\markitdown-py.exe"
Write-Host 'Enable it with:  $env:MARKITDOWN_PY_BIN = "' + "$PSScriptRoot\dist\markitdown-py.exe" + '"'
