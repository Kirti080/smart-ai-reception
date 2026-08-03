@echo off
title Recreate Virtual Environment
echo ===================================================
echo * Recreating Python Virtual Environment *
echo ===================================================
echo.

echo [INFO] Deleting old, broken virtual environment...
if exist ".venv" rmdir /s /q .venv
if exist ".venv311" rmdir /s /q .venv311

echo.
echo [INFO] Creating a fresh virtual environment in this folder...
python -m venv .venv
if %errorlevel% neq 0 (
    echo.
    echo ❌ [ERROR] Failed to create virtual environment!
    echo Please make sure you have Python installed and in your system PATH.
    pause
    exit /b
)

echo.
echo [INFO] Installing all required libraries from requirements.txt...
.venv\Scripts\pip.exe install -r kirti\requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ❌ [ERROR] Failed to install dependencies!
    pause
    exit /b
)

echo.
echo ===================================================
echo ✅ Virtual environment successfully recreated!
echo ✅ All dependencies installed!
echo ===================================================
echo.
pause
run_project.bat
