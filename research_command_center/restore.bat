@echo off
REM Research Command Center - restore from backup (Windows). Stop the app first.
REM   restore.bat --list | --latest | --file "path\to\backup.db"
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
if not exist ".venv\Scripts\python.exe" (
    echo [RCC] Please run start.bat once first.
    pause
    exit /b 1
)
if "%~1"=="" (
    ".venv\Scripts\python.exe" scripts\restore_db.py --list
    echo.
    echo Usage: restore.bat --latest   or   restore.bat --file "backup file path"
) else (
    ".venv\Scripts\python.exe" scripts\restore_db.py %*
)
pause
endlocal
