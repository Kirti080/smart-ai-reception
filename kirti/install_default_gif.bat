@echo off
title Install Default Kiosk Speaking GIF
echo ===================================================
echo * Installing Default Kiosk Speaking GIF Asset    *
echo ===================================================
echo.

set SOURCE_GIF=kirti\static\kriti.gif
set TARGET_GIF=kirti\static\receptionist.gif

if not exist "%SOURCE_GIF%" (
    echo [ERROR] Source GIF 'kirti\static\kriti.gif' not found!
    pause
    exit /b
)

echo [INFO] Copying default speaking GIF...
copy "%SOURCE_GIF%" "%TARGET_GIF%" > nul

if %errorlevel% equ 0 (
    echo [SUCCESS] Default speaking GIF installed successfully to: %TARGET_GIF%
) else (
    echo [ERROR] Failed to install GIF.
)

echo.
echo ===================================================
echo * Installation Complete!
echo ===================================================
echo.
pause
