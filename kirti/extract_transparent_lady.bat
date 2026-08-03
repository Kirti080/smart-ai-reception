@echo off
title Extract Transparent Kiosk Receptionist Lady
echo ===================================================
echo * Generating Transparent Kiosk Receptionist Lady  *
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

echo [INFO] Running automated chroma-key background removal...
"%VENV_PATH%\Scripts\python.exe" -c "import os; from PIL import Image; source = r'C:\Users\Kirti Verma\.gemini\antigravity-ide\brain\83b8a687-d78c-48ba-9c8c-2f571b928d23\receptionist_greenscreen_1779860993808.png'; target = r'kirti\static\receptionist.png'; backup = r'kirti\static\receptionist_old.png'; img = Image.open(source).convert('RGBA'); datas = img.getdata(); newData = []; [newData.append((255, 255, 255, 0) if (item[1] > 140 and item[0] < 110 and item[2] < 110) else item) for item in datas]; img.putdata(newData); os.rename(target, backup) if os.path.exists(target) and not os.path.exists(backup) else (os.remove(target) if os.path.exists(target) else None); img.save(target, 'PNG'); print('[SUCCESS] Chroma-key successful! Saved transparent lady to kirti\\static\\receptionist.png')"

echo.
echo ===================================================
echo * Extraction and Background Removal Complete!
echo ===================================================
echo.
pause
