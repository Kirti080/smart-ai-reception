import speech_recognition as sr
import datetime
import webbrowser
import os
import pandas as pd
import google.generativeai as genai
from difflib import get_close_matches
import requests
import base64
from pydub import AudioSegment
import simpleaudio as sa
import io

# 🌐 Setup Gemini
genai.configure(api_key="AIzaSyDwAkotliq1_HyblL9Xsv5wixbn2-wKOAE")
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# 📄 Load Excel file
qa_df = pd.read_excel("college_questions.xlsx")
qa_dict = dict(zip(qa_df['Question'].str.lower(), qa_df['Answer']))

# 🔊 Google TTS Setup
TTS_API_KEY = "AIzaSyBHbl-pCyU4q_akVo8Hiwv8Ko_RdggVF9g"

def speak_google_tts_realtime(text):
    print("Assistant:", text)
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={TTS_API_KEY}"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    payload = {
        "input": {"text": text},
        "voice": {
            "languageCode": "en-IN",
            "name": "en-IN-Wavenet-B",
            "ssmlGender": "FEMALE"
        },
        "audioConfig": {"audioEncoding": "MP3"}
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    audio_content = base64.b64decode(response.json()['audioContent'])

    # Convert MP3 bytes to AudioSegment
    audio = AudioSegment.from_file(io.BytesIO(audio_content), format="mp3")

    # Export to raw audio for simpleaudio
    raw_audio = io.BytesIO()
    audio.export(raw_audio, format="wav")
    raw_audio.seek(0)

    # Play audio using simpleaudio
    wave_obj = sa.WaveObject.from_wave_file(raw_audio)
    play_obj = wave_obj.play()
    play_obj.wait_done()

# 🧠 Listen to user input
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("🧠 Recognizing...")
        query = r.recognize_google(audio)
        print("You said:", query)
        return query.lower()
    except Exception as e:
        print("❌ Sorry, couldn't recognize.")
        return ""

# 📘 Match query with Excel
def get_custom_answer(user_query):
    questions = list(qa_dict.keys())
    match = get_close_matches(user_query, questions, n=1, cutoff=0.7)
    if match:
        return qa_dict[match[0]]
    return None

# # 🤖 Get Gemini response
# def get_gemini_reply(prompt):
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return "Sorry, Gemini API failed to respond."


def get_gemini_reply(prompt):
    try:
        full_prompt = f"{prompt}\n\nPlease answer briefly in 1-2 lines."
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return "Sorry, Gemini API failed to respond."


# 🙋 Greet the user
def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak_google_tts_realtime("Good morning!")
    elif hour < 18:
        speak_google_tts_realtime("Good afternoon!")
    else:
        speak_google_tts_realtime("Good evening!")
    speak_google_tts_realtime("I am your smart assistant. Ask me anything.")

# 🔁 Main Loop
if __name__ == "__main__":
    greet_user()
    while True:
        query = listen()
        if not query:
            continue

        # 📁 Commands
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
            # ✅ Try Excel first
            answer = get_custom_answer(query)
            if answer:
                speak_google_tts_realtime(answer)
            else:
                # 🔄 Fallback to Gemini
                reply = get_gemini_reply(query)
                speak_google_tts_realtime(reply)




# import speech_recognition as sr
# import datetime
# import webbrowser
# import os
# import pandas as pd
# import google.generativeai as genai
# from difflib import get_close_matches
# import requests
# import base64
# from pydub import AudioSegment
# import simpleaudio as sa
# import io
# import threading

# # 🌐 Setup Gemini
# genai.configure(api_key="AIzaSyBXMU6Nfrh4l9Gv_mjXF7ADlb9_iwhtHXs")
# model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# # 📄 Load Excel file
# qa_df = pd.read_excel("college_questions.xlsx")
# qa_dict = dict(zip(qa_df['Question'].str.lower(), qa_df['Answer']))

# # 🔊 Google TTS
# TTS_API_KEY = "AIzaSyBHbl-pCyU4q_akVo8Hiwv8Ko_RdggVF9g"
# play_obj = None
# stop_event = threading.Event()

# def play_audio(audio_bytes):
#     global play_obj
#     raw_audio = io.BytesIO()
#     audio_bytes.export(raw_audio, format="wav")
#     raw_audio.seek(0)
#     wave_obj = sa.WaveObject.from_wave_file(raw_audio)
#     play_obj = wave_obj.play()
#     while play_obj.is_playing():
#         if stop_event.is_set():
#             play_obj.stop()
#             break

# def speak_google_tts_realtime(text):
#     print("Assistant:", text)
#     stop_event.clear()

#     url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={TTS_API_KEY}"
#     headers = {"Content-Type": "application/json; charset=utf-8"}
#     payload = {
#         "input": {"text": text},
#         "voice": {
#             "languageCode": "en-IN",
#             "name": "en-IN-Wavenet-B",
#             "ssmlGender": "FEMALE"
#         },
#         "audioConfig": {"audioEncoding": "MP3"}
#     }

#     response = requests.post(url, headers=headers, json=payload)
#     response.raise_for_status()
#     audio_content = base64.b64decode(response.json()['audioContent'])
#     audio = AudioSegment.from_file(io.BytesIO(audio_content), format="mp3")

#     # Play in separate thread
#     t = threading.Thread(target=play_audio, args=(audio,))
#     t.start()

#     # Start listening for 'stop'
#     listen_for_stop()

#     t.join()

# def listen_for_stop():
#     r = sr.Recognizer()
#     mic = sr.Microphone()
#     with mic as source:
#         r.adjust_for_ambient_noise(source)
#         print("🎤 Say 'stop' to interrupt...")
#         try:
#             audio = r.listen(source, timeout=5)
#             command = r.recognize_google(audio).lower()
#             if "stop" in command:
#                 print("🛑 Stop command detected!")
#                 stop_event.set()
#         except:
#             pass  # timeout or no input

# def listen():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("🎙️ Listening...")
#         r.pause_threshold = 1
#         audio = r.listen(source)
#     try:
#         print("🧠 Recognizing...")
#         query = r.recognize_google(audio)
#         print("You said:", query)
#         return query.lower()
#     except Exception:
#         print("❌ Sorry, couldn't recognize.")
#         return ""

# def get_custom_answer(user_query):
#     questions = list(qa_dict.keys())
#     match = get_close_matches(user_query, questions, n=1, cutoff=0.7)
#     return qa_dict[match[0]] if match else None

# def get_gemini_reply(prompt):
#     try:
#         response = model.generate_content(f"{prompt}\n\nPlease answer briefly in 1-2 lines.")
#         return response.text.strip()
#     except Exception:
#         return "Sorry, Gemini API failed to respond."

# def greet_user():
#     hour = datetime.datetime.now().hour
#     if hour < 12:
#         speak_google_tts_realtime("Good morning!")
#     elif hour < 18:
#         speak_google_tts_realtime("Good afternoon!")
#     else:
#         speak_google_tts_realtime("Good evening!")
#     speak_google_tts_realtime("I am your smart assistant. Ask me anything.")

# # 🔁 Main Loop
# if __name__ == "__main__":
#     greet_user()
#     while True:
#         query = listen()
#         if not query:
#             continue

#         if "open youtube" in query:
#             webbrowser.open("https://www.youtube.com")
#             speak_google_tts_realtime("Opening YouTube.")
#         elif "open google" in query:
#             webbrowser.open("https://www.google.com")
#             speak_google_tts_realtime("Opening Google.")
#         elif "play music" in query:
#             music_dir = "/System/Library/Sounds"
#             songs = os.listdir(music_dir)
#             os.system(f"afplay '{music_dir}/{songs[0]}'")
#             speak_google_tts_realtime("Playing music.")
#         elif "exit" in query or "stop" in query:
#             speak_google_tts_realtime("Goodbye!")
#             break
#         else:
#             answer = get_custom_answer(query)
#             if answer:
#                 speak_google_tts_realtime(answer)
#             else:
#                 reply = get_gemini_reply(query)
#                 speak_google_tts_realtime(reply)
