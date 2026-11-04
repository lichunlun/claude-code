@echo off
REM Research Command Center - one-click database backup (Windows)
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
if not exist ".venv\Scripts\python.exe" (
    echo [RCC] Please run start.bat once first.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" scripts\backup_db.py %*
pause
endlocal
