@echo off
setlocal
cd /d "%~dp0"

title Mini Blog Server

REM ===================== 1. Virtual environment =====================
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

REM ===================== 2. .env configuration =====================
if not exist ".env" (
    echo [INFO] .env not found - creating from .env.example ...
    copy /y ".env.example" ".env" >nul
    echo [WARN] SECRET_KEY in .env is set to "change-me".
    echo        Generate a strong key and update .env before exposing on LAN:
    echo          .venv\Scripts\python -c "import secrets; print(secrets.token_hex(32))"
    echo.
)

REM =============== 3. Read host / port from .env ====================
set "APP_HOST=0.0.0.0"
set "APP_PORT=8000"
if exist ".env" (
    for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
        if /i "%%a"=="APP_HOST" set "APP_HOST=%%b"
        if /i "%%a"=="APP_PORT" set "APP_PORT=%%b"
    )
)

echo ==========================================================
echo   Mini Blog - LAN Content Platform
echo   Local:  http://127.0.0.1:%APP_PORT%
echo   LAN:    http://^<HOST_IP^>:%APP_PORT%
echo   Press Ctrl+C to stop the server.
echo ==========================================================
echo.

".venv\Scripts\python.exe" -m uvicorn app.main:app --host %APP_HOST% --port %APP_PORT% --reload

echo.
echo Server stopped.
pause
