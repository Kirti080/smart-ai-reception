@echo off
title Launch Kiosk Fullscreen Mode
echo ===================================================
echo * Starting DBU Kiosk in Fullscreen Mode *
echo ===================================================

:: Give servers time to launch if starting simultaneously
timeout /t 3 /nobreak > nul

:: Try Chrome Kiosk Mode first
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo [INFO] Launching Chrome in Kiosk Mode...
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --kiosk --app=http://localhost:5005/ --user-data-dir="%LOCALAPPDATA%\KioskChromeProfile" --no-first-run
    exit /b
)

if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    echo [INFO] Launching Chrome (x86) in Kiosk Mode...
    start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --kiosk --app=http://localhost:5005/ --user-data-dir="%LOCALAPPDATA%\KioskChromeProfile" --no-first-run
    exit /b
)

:: Fallback to Microsoft Edge Kiosk Mode
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    echo [INFO] Launching Edge in Kiosk Mode...
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --kiosk http://localhost:5005/ --edge-kiosk-type=fullscreen
    exit /b
)

:: Generic browser fallback
echo [INFO] Opening default browser...
start http://localhost:5005/
