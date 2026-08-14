@echo off
setlocal
cd /d "%~dp0"

title Promote User to Admin

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found at .venv\Scripts\python.exe
    echo.
    echo Create and install dependencies first:
    echo   py -3.11 -m venv .venv
    echo   .venv\Scripts\python -m pip install -e ".[dev]"
    echo.
    pause
    exit /b 1
)

if "%~1"=="" (
    echo ==========================================================
    echo   Promote a user to admin
    echo   Usage: promote_admin.bat [username]
    echo   If no username is given you will be prompted.
    echo ==========================================================
    echo.
    ".venv\Scripts\python.exe" promote_admin.py
) else (
    ".venv\Scripts\python.exe" promote_admin.py %1
)

echo.
pause
