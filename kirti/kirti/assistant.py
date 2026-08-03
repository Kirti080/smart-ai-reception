from dotenv import load_dotenv
import speech_recognition as sr
import datetime
import webbrowser
import os
import pandas as pd
import google.generativeai as genai
from groq import Groq
from difflib import get_close_matches
import requests
import base64
from playsound import playsound
import tempfile
import time

# 🔐 Load Environment Variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
TTS_API_KEY = os.getenv("TTS_API_KEY") or GEMINI_API_KEY
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# 🤖 Gemini model (use valid gemini-1.5-flash)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# 🔄 Groq client (fallback)
if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
else:
    groq_client = None
# 📌 Load Excel Q/A
qa_df = pd.read_excel("college_questions.xlsx")
qa_df['Question'] = qa_df['Question'].str.strip().str.lower()
qa_df['Answer'] = qa_df['Answer'].fillna("").str.strip()
qa_df['Photos'] = qa_df['Photos'].fillna("").str.strip()

qa_dict = dict(zip(qa_df['Question'], qa_df['Answer']))
photo_dict = dict(zip(qa_df['Question'], qa_df['Photos']))

IMAGE_BASE_URL = "http://localhost:5005/static/images/"


# 🔊 Speak without FFmpeg
def speak_google_tts_realtime(text, photo=None):
    print("Assistant:", text, "| 📷", photo)

    # UI send
    try:
        payload = {"text": text}
        if photo:
            payload["photo"] = IMAGE_BASE_URL + photo
        requests.post("http://localhost:5005/speak", json=payload)
    except:
        print("⚠ UI server not reachable.")

    try:
        url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={TTS_API_KEY}"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        payload = {
            "input": {"text": text},
            "voice": {
                "languageCode": "en-IN",
                "name": "en-IN-Wavenet-A",
                "ssmlGender": "FEMALE"
            },
            "audioConfig": {"audioEncoding": "MP3"}
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        audio_content = base64.b64decode(response.json()['audioContent'])

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(audio_content)
            temp_audio_file = f.name

        playsound(temp_audio_file)
    except Exception as e:
        print(f"⚠ Google TTS failed ({e}). Falling back to pyttsx3 offline TTS...")
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            
            # Find and set a female voice
            female_voice = None
            for voice in voices:
                name_lower = voice.name.lower()
                if "female" in name_lower or "zira" in name_lower or "hazel" in name_lower or "elena" in name_lower:
                    female_voice = voice.id
                    break
            if female_voice:
                engine.setProperty('voice', female_voice)
            elif len(voices) > 1:
                engine.setProperty('voice', voices[1].id) # Fallback to Zira (usually index 1)
                
            engine.say(text)
            engine.runAndWait()
        except Exception as ex:
            print(f"❌ Offline TTS also failed: {ex}")


# 🎧 Listen
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("🧠 Recognizing...")
        query = r.recognize_google(audio)
        print("You said:", query)
        return query.lower()
    except:
        print("❌ Sorry, couldn't recognize.")
        return ""


# Search custom answers
def get_custom_answer(user_query):
    match = get_close_matches(user_query, list(qa_dict.keys()), n=1, cutoff=0.7)
    if match:
        q = match[0]
        return qa_dict[q], photo_dict.get(q)
    return None, None


# 🤖 Groq AI answer (fallback)
def get_groq_reply(prompt):
    """Fallback to Groq when Gemini fails or quota exceeded."""
    if not groq_client:
        return None
    
    full_prompt = f"{prompt}\n\nPlease answer briefly in 1-2 lines."
    
    # Try current production models for Groq
    for groq_model in ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]:
        try:
            message = groq_client.chat.completions.create(
                messages=[
                    {"role": "user", "content": full_prompt}
                ],
                model=groq_model,
                max_tokens=100,
                temperature=0.7
            )
            print(f"✅ Using Groq model: {groq_model}")
            return message.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ Groq model {groq_model} error: {e}")
            continue

    return None


# Gemini AI answer (with Groq fallback)
def get_gemini_reply(prompt):
    try:
        full_prompt = f"{prompt}\n\nPlease answer briefly in 1-2 lines."
        response = model.generate_content(full_prompt)
        print("✅ Using Gemini API")
        return response.text.strip()
    except Exception as e:
        print(f"⚠ Gemini API failed: {e}")
        print("🔄 Falling back to Groq API...")
        
        # Try Groq as fallback
        groq_reply = get_groq_reply(prompt)
        if groq_reply:
            print("✅ Using Groq API (fallback)")
            return groq_reply
        
        return "Sorry, both AI services failed. Please try again later."


# Greeting
def greet_user():
    hour = datetime.datetime.now().hour
    greeting = "Good morning!" if hour < 12 else "Good afternoon!" if hour < 18 else "Good evening!"
    
    speak_google_tts_realtime(greeting)
    speak_google_tts_realtime("I am your smart assistant. Ask me anything.")


# Main Loop
if __name__ == "__main__":
    greet_user()
    is_active = False

    while True:
        try:
            # Check the Flask server status to see if a human is physically present
            status_check = requests.get("http://localhost:5005/status").json()
            human_present = status_check.get("human", False)
        except Exception as e:
            print("⚠ Unable to reach Flask UI server to pull human status.")
            human_present = False

        if not human_present:
            if is_active:
                print("💤 Returning to standby mode...")
                is_active = False
            time.sleep(1)  # Sleep quietly until someone stands in front of the kiosk
            continue

        if not is_active:
            print("🔔 User detected! Voice activation ready.")
            is_active = True

        query = listen()
        if not query:
            continue

        if "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
            speak_google_tts_realtime("Opening YouTube.")
        elif "open google" in query:
            webbrowser.open("https://www.google.com")
            speak_google_tts_realtime("Opening Google.")
        elif "play music" in query:
            music_dir = "/System/Library/Sounds"
            songs = os.listdir(music_dir)
            os.system(f"afplay '{music_dir}/{songs[0]}'")
            speak_google_tts_realtime("Playing music.")
        elif "exit" in query or "stop" in query:
            speak_google_tts_realtime("Goodbye!")
            break
        else:
            answer, photo = get_custom_answer(query)
            if answer:
                speak_google_tts_realtime(answer, photo)
            else:
                reply = get_gemini_reply(query)
                speak_google_tts_realtime(reply)
