from flask import Flask, render_template, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
import boto3, os, cv2, io
from datetime import datetime
import pandas as pd
import mediapipe as mp
try:
    import mediapipe.solutions.face_mesh as mp_face_mesh
except ModuleNotFoundError:
    import mediapipe.python.solutions.face_mesh as mp_face_mesh
import threading
import time
# from human import shared_data


app = Flask(__name__)
CORS(app)

# AWS Rekognition Client (region restored)
rekognition = boto3.client('rekognition', region_name='ap-south-1')

# Configuration
image_dir = 'images'
excel_file = 'attendance.xlsx'
valid_extensions = ('.jpeg', '.jpg', '.png')

# Globals
matched_user = {
    "matched": False,
    "name": "",
    "image_url": "",
    "checkin": "",
    "checkout": "",
    "date": ""
}

latest_message = {"text": "Say something...", "photo": None}
latest_frame = None

# ---------------------- ATTENDANCE SYSTEM ----------------------
def log_attendance(name):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Read or create Excel
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
    else:
        df = pd.DataFrame(columns=["Name", "Check-in Time", "Check-out Time", "Date"])

    today_entries = df[(df['Name'] == name) & (df['Date'] == date_str)]

    if today_entries.empty:
        # First-time entry – check-in
        new_entry = pd.DataFrame([{
            "Name": name,
            "Check-in Time": time_str,
            "Check-out Time": "",
            "Date": date_str
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
        print(f"📝 Checked in: {name} at {time_str}")
    else:
        index = today_entries.index[0]
        if df.at[index, "Check-out Time"] == "" or pd.isna(df.at[index, "Check-out Time"]):
            df.at[index, "Check-out Time"] = time_str
            print(f"✅ Checked out: {name} at {time_str}")
        else:
            print(f"ℹ Already checked out for {name} today.")

    df.to_excel(excel_file, index=False)


def capture_and_compare():
    global matched_user, latest_frame
    reference_images = [f for f in os.listdir(image_dir) if f.lower().endswith(valid_extensions)]
    if not reference_images:
        print("⚠ No reference images found.")
        return

    # Wait up to 2 seconds for a frame from the background camera thread
    for _ in range(20):
        if latest_frame is not None:
            break
        time.sleep(0.1)

    if latest_frame is None:
        print("⚠ Failed to capture frame (no frame from background thread).")
        return

    frame = latest_frame.copy()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (480, 360))
    success, buffer = cv2.imencode(".jpg", resized, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
    if not success:
        print("⚠ Failed to encode image.")
        return

    captured_bytes = io.BytesIO(buffer).getvalue()

    for image_file in reference_images:
        name = os.path.splitext(image_file)[0]
        with open(os.path.join(image_dir, image_file), "rb") as ref_img:
            ref_bytes = ref_img.read()

        try:
            response = rekognition.compare_faces(
                SourceImage={'Bytes': ref_bytes},
                TargetImage={'Bytes': captured_bytes},
                SimilarityThreshold=85
            )
            if response['FaceMatches']:
                matched_user.update({
                    "matched": True,
                    "name": name,
                    "image_url": f"/profile/{image_file}"
                })
                log_attendance(name)
                return
        except Exception as e:
            print(f"❌ Error comparing with {name}: {e}")

    matched_user.update({"matched": False, "name": "", "image_url": "", "checkin": "", "checkout": "", "date": ""})

# ---------------------- ROUTES ----------------------
@app.route('/')
def home():
    return render_template('cat_ui.html')

@app.route('/attendance')
def attendance_page():
    return render_template('index.html')

@app.route('/start-match')
def start_match():
    matched_user.update({
        "matched": False,
        "name": "",
        "image_url": "",
        "checkin": "",
        "checkout": "",
        "date": ""
    })

    capture_and_compare()

    if matched_user["matched"] and os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        user_rows = df[df["Name"] == matched_user["name"]]
        if not user_rows.empty:
            latest_row = user_rows.iloc[-1]
            matched_user["checkin"] = str(latest_row.get("Check-in Time", "") or "")
            matched_user["checkout"] = str(latest_row.get("Check-out Time", "") or "")
            matched_user["date"] = str(latest_row.get("Date", "") or "")

    return jsonify(matched_user)

@app.route('/profile/<filename>')
def profile_image(filename):
    return send_from_directory(image_dir, filename)

# ---------------------- CAT UI ASSISTANT ----------------------
@app.route("/assistant")
def serve_cat_ui():
    return render_template("cat_ui.html")

@app.route("/speak", methods=["POST"])
def speak_to_ui():
    data = request.json
    print("🐱 Cat UI received:", data)
    latest_message["text"] = data.get("text", "")
    latest_message["photo"] = data.get("photo", None)
    return {"status": "ok"}

@app.route("/get-latest", methods=["GET"])
def get_latest_message():
    return jsonify(latest_message)

# Serve static images (cross-platform)
@app.route("/static/images/<filename>")
def serve_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), "images"), filename)




# =====================================================================
# CAMERA STREAMING & MEDIAPIPE SETUP
# =====================================================================

status_data = {"human": False}
latest_frame = None
cap = None

def init_camera():
    global cap
    for index in [0, 1, 2]:
        print(f"🔍 [Camera] Attempting to open index {index}...")
        temp_cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not temp_cap.isOpened():
            temp_cap = cv2.VideoCapture(index)
        if temp_cap.isOpened():
            success, frame = temp_cap.read()
            if success and frame is not None:
                cap = temp_cap
                print(f"✅ [Camera] Active on index {index}")
                return True
            temp_cap.release()
    return False

def detect_faces():
    global status_data, latest_frame, cap
    
    if cap is None or not cap.isOpened():
        if not init_camera():
            print("❌ [Camera Thread] No working webcam found.")
            return

    print("🎥 Background face detection & streaming thread active.")
    
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:
        while True:
            success, frame = cap.read()
            if not success or frame is None:
                time.sleep(0.01)
                continue

            latest_frame = frame.copy()

            # Process face mesh landmarks
            image = cv2.flip(frame, 1)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_image)

            # Update presentation state
            if results.multi_face_landmarks:
                if not status_data["human"]:
                    print("✅ Human Detected in Front of Kiosk")
                status_data["human"] = True
            else:
                if status_data["human"]:
                    print("❌ Kiosk Idle - No Human")
                status_data["human"] = False

            time.sleep(0.03)  # Cap loop processing to save CPU cycles

# Generator function for the live UI stream
def gen_frames():
    global latest_frame
    while True:
        if latest_frame is not None:
            # Resize slightly to maintain high performance in web UI
            small_frame = cv2.resize(latest_frame, (640, 480))
            ret, buffer = cv2.imencode('.jpg', small_frame)
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.04)  # Corresponds to roughly ~25 FPS stream


@app.route('/video_feed')
def video_feed():
    """Route that feeds live video directly into your HTML page."""
    return make_response(gen_frames(), {
        'Content-Type': 'multipart/x-mixed-replace; boundary=frame'
    })

@app.route("/status")
def status():
    """Return the current human presence status."""
    force_human = request.args.get('force') == 'true' or request.args.get('human') == 'true' or request.args.get('bypass') == 'true'
    if force_human:
        return jsonify({"human": True})
    return jsonify(status_data)



if __name__ == "__main__":
    # Start face detection in background thread only on the main process
    # (avoid spawning multiple threads during Flask debug reload)
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        t = threading.Thread(target=detect_faces, daemon=True)
        t.start()

    app.run(port=5005, debug=True, use_reloader=False)  # use_reloader=False stops double thread initialization bugs