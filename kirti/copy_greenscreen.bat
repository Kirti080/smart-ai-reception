@echo off
title Copy Kiosk Receptionist Green Screen Asset
echo ===================================================
echo * Installing Kiosk Receptionist Green Screen Image *
echo ===================================================
echo.

set SOURCE_IMAGE=C:\Users\Kirti Verma\.gemini\antigravity-ide\brain\83b8a687-d78c-48ba-9c8c-2f571b928d23\receptionist_greenscreen_1779860993808.png
set TARGET_DIR=kirti\static
set TARGET_IMAGE=%TARGET_DIR%\receptionist_greenscreen.png

if not exist "%SOURCE_IMAGE%" (
    echo [ERROR] Source green-screen image not found!
    pause
    exit /b
)

if not exist "%TARGET_DIR%" (
    mkdir "%TARGET_DIR%"
)

echo [INFO] Copying green screen asset...
copy "%SOURCE_IMAGE%" "%TARGET_IMAGE%" > nul

if %errorlevel% equ 0 (
    echo [SUCCESS] Green screen image successfully saved to: %TARGET_IMAGE%
) else (
    echo [ERROR] Failed to copy image.
)

echo.
echo ===================================================
echo * Copy Complete!
echo ===================================================
echo.
pause
