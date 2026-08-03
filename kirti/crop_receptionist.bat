@echo off
title Crop Receptionist Lady Asset
echo ===================================================
echo * Extracting Kiosk Receptionist Lady from Mockup *
echo ===================================================
echo.

set VENV_PATH=.venv
if not exist "%VENV_PATH%\Scripts\python.exe" (
    set VENV_PATH=.venv311
)

if not exist "%VENV_PATH%\Scripts\python.exe" (
    echo [ERROR] Python environment not found!
    pause
    exit /b
)

echo [INFO] Running extraction script using %VENV_PATH%...
"%VENV_PATH%\Scripts\python.exe" -c "import os; from PIL import Image; img = Image.open(r'C:\Users\Kirti Verma\.gemini\antigravity-ide\brain\83b8a687-d78c-48ba-9c8c-2f571b928d23\natural_standing_ui_1779858706037.png'); w, h = img.size; cropped = img.crop((int(w*0.25), int(h*0.22), int(w*0.75), int(h*0.76))); target = r'kirti\static\receptionist.png'; backup = r'kirti\static\receptionist_old.png'; os.rename(target, backup) if os.path.exists(target) and not os.path.exists(backup) else (os.remove(target) if os.path.exists(target) else None); cropped.save(target, 'PNG'); print('[SUCCESS] Beautiful receptionist lady extracted and saved to kirti\\static\\receptionist.png!')"

echo.
echo ===================================================
echo * Extraction Complete!
echo ===================================================
echo.
pause
