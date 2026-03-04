@echo off
echo ========================================
echo MarkItDown Batch Converter
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv .venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo.

REM Check if requirements are installed
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements-server.txt
    echo.
)

REM Start the server
echo Starting MarkItDown Batch Converter Server...
echo.
echo ========================================
echo Server will be available at:
echo http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python server.py

pause
