@echo off
title Smart AI Receptionist Launcher
echo ===================================================
echo * Launching Smart AI Receptionist Project *
echo ===================================================
echo.

:: Detect virtual environment
set VENV_PATH=.venv
if not exist "%VENV_PATH%\Scripts\python.exe" (
    set VENV_PATH=.venv311
)

if not exist "%VENV_PATH%\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found in .venv or .venv311!
    echo Please make sure you have a python virtual environment set up.
    pause
    exit /b
)

echo [INFO] Using virtual environment: %VENV_PATH%
echo [INFO] Verifying required libraries...
echo.

:: Check if required libraries are installed
"%VENV_PATH%\Scripts\python.exe" -c "import flask, flask_cors, boto3, cv2, pandas, mediapipe.python.solutions.face_mesh, groq, speech_recognition, playsound" 2>nul
if %errorlevel%==0 goto :launch

echo ===================================================
echo [WARNING] Some required libraries are missing!
echo ===================================================
echo.

set /p install="Would you like to automatically install all dependencies now? (Y/N): "
if /i "%install%"=="Y" goto :install_deps
goto :skip_install

:install_deps
echo.
echo [INFO] Installing dependencies from kirti\requirements.txt...
"%VENV_PATH%\Scripts\pip.exe" install -r kirti\requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Dependency installation failed! Please run 'pip install -r kirti\requirements.txt' manually.
    pause
    exit /b
)
echo.
echo [SUCCESS] Dependencies installed successfully!
echo.
goto :launch

:skip_install
echo [INFO] Skipping installation. The application may fail to start if modules are missing.
echo.

:launch
:: Start Flask UI Server
echo [INFO] Starting Flask UI Server in a new window...
start "Flask UI Server" cmd /k "cd kirti && ..\%VENV_PATH%\Scripts\python.exe cat_ui_server.py"

:: Give the server a few seconds to start
ping -n 4 127.0.0.1 > nul

:: Start Assistant
echo [INFO] Starting AI Assistant in a new window...
start "AI Assistant" cmd /k "cd kirti && ..\%VENV_PATH%\Scripts\python.exe assistant.py"

echo.
echo ===================================================
echo * Both services have been launched!
echo * Flask UI Server: http://localhost:5005
echo * Smart Kiosk Receptionist: http://localhost:5005/
echo * Attendance Scanner Page: http://localhost:5005/attendance
echo ===================================================
echo.
pause
