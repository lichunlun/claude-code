@echo off
REM Research Command Center - one-click start (Windows)
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1

if exist ".venv\Scripts\python.exe" goto :have_venv
echo [RCC] First run: creating Python virtual environment in .venv ...
py -3 -m venv .venv >nul 2>nul
if not exist ".venv\Scripts\python.exe" python -m venv .venv
if not exist ".venv\Scripts\python.exe" (
    echo [RCC] ERROR: Python 3.11 or newer was not found.
    echo [RCC] Install it from https://www.python.org/downloads/ and tick "Add python.exe to PATH".
    pause
    exit /b 1
)
:have_venv
".venv\Scripts\python.exe" scripts\launcher.py start %*
if errorlevel 1 pause
endlocal
