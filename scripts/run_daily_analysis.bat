@echo off
REM Daily Stock Analysis Runner
REM Runs the Python stock fetcher script

setlocal enabledelayedexpansion

echo.
echo ====================
echo Daily Stock Analysis
echo ====================
echo.

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0

REM Run Python script from workspace root
cd /d "%SCRIPT_DIR%.."
python scripts\fetch_stock_analysis.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Stock analysis failed with code %errorlevel%
    exit /b %errorlevel%
)

echo.
echo Analysis completed successfully!
pause
