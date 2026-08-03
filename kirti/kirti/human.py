import cv2
import mediapipe as mp
import mediapipe.solutions.face_mesh as mp_face_mesh
shared_data = {"status_data": {"human_detected": False}}


# Initialize mediapipe face mesh


cap = cv2.VideoCapture(0)  # Use webcam

with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:

    while cap.isOpened():
        success, image = cap.read()
        if not success:

            # print(" human is detected.")
            continue

        # Flip image horizontally for natural selfie view
        image = cv2.flip(image, 1)

        # Convert the BGR image to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image and find face landmarks
        results = face_mesh.process(rgb_image)

        # Check if a face is detected
        if results.multi_face_landmarks:
            print("✅ Human Present")
            shared_data["status_data"]["human_detected"] = True
        else:
            print("❌ No Human")
            shared_data["status_data"]["human_detected"] = False

        # Show the webcam feed
        cv2.imshow('Face Detection', image)

        if cv2.waitKey(5) & 0xFF == 27:  # ESC to exit
            break

cap.release()
cv2.destroyAllWindows()