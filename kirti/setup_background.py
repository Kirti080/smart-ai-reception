import shutil, os

src = r"C:\Users\Kirti Verma\.gemini\antigravity-ide\brain\1c54f531-f184-4331-84c9-fe21d16a23ac\dbu_lobby_background_1779957016518.png"
dst = r"C:\Users\Kirti Verma\OneDrive\Desktop\receptionist\kirti\kirti\static\dbu_lobby_background.png"

if os.path.exists(src):
    shutil.copy(src, dst)
    print(f"✅ Background image copied successfully to:\n   {dst}")
else:
    print("❌ Source image not found. Please regenerate background image.")

input("\nPress Enter to close...")
