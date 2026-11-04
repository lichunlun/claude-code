@echo off
REM Research Command Center - stop (Windows)
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
if not exist ".venv\Scripts\python.exe" (
    echo [RCC] Not installed yet.
    exit /b 0
)
".venv\Scripts\python.exe" scripts\launcher.py stop
endlocal
