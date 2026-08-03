Dim fso
Set fso = CreateObject("Scripting.FileSystemObject")

Dim src, dst
src = "C:\Users\Kirti Verma\.gemini\antigravity-ide\brain\1c54f531-f184-4331-84c9-fe21d16a23ac\dbu_lobby_background_1779957016518.png"
dst = "C:\Users\Kirti Verma\OneDrive\Desktop\receptionist\kirti\kirti\static\dbu_lobby_background.png"

If fso.FileExists(src) Then
    fso.CopyFile src, dst, True
    MsgBox "Background image copied successfully! Now restart your Flask app.", vbInformation, "Done"
Else
    MsgBox "Source file not found: " & src, vbCritical, "Error"
End If
