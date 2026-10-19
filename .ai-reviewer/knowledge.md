# smart-ai-reception reviewer notes

## Architecture

This is a Python-based kiosk receptionist combining a Flask web UI, webcam/MediaPipe presence detection, AWS Rekognition attendance matching, and a voice assistant. `kirti/kirti/cat_ui_server.py` owns the HTTP routes, camera thread, face detection, and Excel attendance persistence; `kirti/kirti/assistant.py` runs the voice loop and communicates with that server over localhost. Older standalone assistant implementations and platform-specific experiments are kept under `kirti/kirti/images/kirti/kirti/`.

## Conventions

- Configuration is loaded from environment variables with `python-dotenv`; the active assistant uses `GEMINI_API_KEY`/`GOOGLE_API_KEY`, `TTS_API_KEY`, and `GROQ_API_KEY` in `kirti/kirti/assistant.py`.
- The assistant prioritizes local Excel answers, then calls Gemini, then Groq as a fallback. Preserve this order and the brief-response prompt in `get_custom_answer`, `get_gemini_reply`, and `get_groq_reply`.
- Excel files are the primary persistence/data source: `college_questions.xlsx` supplies Q&A and photos, while `attendance.xlsx` stores `Name`, `Check-in Time`, `Check-out Time`, and `Date` as used by `cat_ui_server.py`.
- User questions are normalized with `.strip().str.lower()`, and approximate matching uses `difflib.get_close_matches(..., cutoff=0.7)`; changes to matching should retain normalization and account for fuzzy-match behavior.
- Flask endpoints use JSON for stateful interactions: `/start-match`, `/status`, `/speak`, and `/get-latest`. Image assets are served through `/profile/<filename>` and `/static/images/<filename>`.
- Camera processing runs in a daemon background thread and communicates through module-level state such as `latest_frame`, `status_data`, and `matched_user`. The Flask server deliberately uses `use_reloader=False` to avoid duplicate camera threads (`kirti/kirti/cat_ui_server.py`).
- The assistant is activated only when `/status` reports `"human": true`; it polls `http://localhost:5005/status` and sends UI speech updates to `/speak` (`kirti/kirti/assistant.py`).
- Runtime dependencies are duplicated in the root `requirements.txt` and `kirti/kirti/requirements.txt`; the packaged `images/kirti` environment additionally pins many macOS/PyObjC and audio dependencies.

## Intentional non-standard choices

- MediaPipe face mesh import compatibility is handled through several fallback import paths in `cat_ui_server.py` and separately tested by `kirti/diagnose.py`; do not simplify this solely because `mp.solutions.face_mesh` is unavailable in some installations.
- The application intentionally supports both cloud Google TTS and offline `pyttsx3` fallback in `assistant.py`.
- The `/status` route intentionally supports `force`, `human`, and `bypass` query parameters for manually forcing kiosk activation.

## Watch out for

- Never add or retain API keys in source files. Archived `final.py` and `assistant.py` copies contain hardcoded Gemini/TTS credentials and should be treated as sensitive even though they are under `__MACOSX`/backup-style paths.
- Flag changes that expose Flask endpoints, attendance records, webcam frames, or Rekognition functionality without authentication or input validation. `CORS(app)` is currently fully permissive.
- `latest_frame`, `status_data`, `matched_user`, and `latest_message` are shared across threads without locks; review concurrent reads/writes for races or partially updated state.
- Preserve the camera/assistant contract on port `5005`, including `/status` and `/speak`; changing route names or payload fields can silently disable voice activation or UI updates.
- Flag new dependence on the process working directory: Excel files and `images` are resolved relatively, so launching from another directory can break startup or asset lookup.
- Review changes to attendance toggling carefully: a second match on the same day changes check-in into check-out, while later matches are ignored (`log_attendance`).