import sys
import traceback
print("Python executable:", sys.executable)
print("Python version:", sys.version)

try:
    import mediapipe as mp
    print("Mediapipe version:", getattr(mp, '__version__', 'No version'))
    print("Mediapipe file:", getattr(mp, '__file__', 'No __file__ attribute'))
except Exception as e:
    print("Failed to import mediapipe:", e)

try:
    print("Attempting to import mediapipe.python.solutions.face_mesh...")
    import mediapipe.python.solutions.face_mesh as mp_face_mesh
    print("[SUCCESS] Successfully imported mediapipe.python.solutions.face_mesh!")
except Exception as e:
    print("[ERROR] Failed to import mediapipe.python.solutions.face_mesh:")
    traceback.print_exc()

try:
    print("Attempting to access mp.solutions.face_mesh...")
    import mediapipe as mp
    mp_face_mesh = mp.solutions.face_mesh
    print("[SUCCESS] Successfully accessed mp.solutions.face_mesh!")
except Exception as e:
    print("[ERROR] Failed to access mp.solutions.face_mesh:")
    traceback.print_exc()

