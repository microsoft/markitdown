@echo off
REM Helper script to build the markitdown-mcp Docker image
REM This script ensures fresh builds that pick up code changes

cd /d "%~dp0..\.."

echo Building markitdown-mcp Docker image...

REM Build with cache-busting argument to force rebuild of Python packages
docker build -f packages/markitdown-mcp/Dockerfile --build-arg CACHE_BUST=%TIME:~0,2%%TIME:~3,2%%TIME:~6,2% -t markitdown-mcp:latest .

echo.
echo Build complete!
echo.
echo To restart the service with the new image:
echo   cd packages\markitdown-mcp
echo   docker compose down
echo   docker compose up -d
