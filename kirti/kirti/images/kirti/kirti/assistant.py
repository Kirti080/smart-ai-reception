# import speech_recognition as sr
# import pyttsx3
# import datetime
# import webbrowser
# import os

# # Initialize speech engine
# engine = pyttsx3.init()
# engine.setProperty('rate', 180)  # speaking speed
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)  # Mac uses built-in voice

# def speak(text):
#     print("Assistant:", text)
#     engine.say(text)
#     engine.runAndWait()

# def listen():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         r.pause_threshold = 1
#         audio = r.listen(source)
#     try:
#         print("Recognizing...")
#         query = r.recognize_google(audio)
#         print("You said:", query)
#         return query.lower()
#     except Exception as e:
#         print("Sorry, could not recognize.")
#         return ""

# def greet_user():
#     hour = datetime.datetime.now().hour
#     if hour < 12:
#         speak("Good morning!")
#     elif hour < 18:
#         speak("Good afternoon!")
#     else:
#         speak("Good evening!")
#     speak("I am your assistant. How can I help you?")

# def execute_command(query):
#     if "time" in query:
#         time = datetime.datetime.now().strftime("%I:%M %p")
#         speak(f"The current time is {time}")
    
#     elif "open youtube" in query:
#         webbrowser.open("https://www.youtube.com")
#         speak("Opening YouTube")

#     elif "open google" in query:
#         webbrowser.open("https://www.google.com")
#         speak("Opening Google")

#     elif "play music" in query:
#         music_dir = "/System/Library/Sounds"
#         songs = os.listdir(music_dir)
#         os.system(f"afplay '{music_dir}/{songs[0]}'")

#     elif "quit" in query or "stop" in query:
#         speak("Goodbye!")
#         exit()

#     else:
#         speak("Sorry, I didn't understand that.")

# # 🔁 Main Loop
# if __name__ == "__main__":
#     greet_user()
#     while True:
#         query = listen()
#         if query:
#             execute_command(query)





# import speech_recognition as sr
# import pyttsx3
# import datetime
# import webbrowser
# import os
# import google.generativeai as genai

# # # 🌐 Setup Gemini
# # genai.configure(api_key="AIzaSyD5dGbgHTWLhvgINIpgKaN0NRwCaHGkPGQ")  # <--- Use your real key here
# # # model = genai.GenerativeModel("gemini-pro")
# # model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# # --- Configure your API keys ---
# GENAI_API_KEY = "AIzaSyBXMU6Nfrh4l9Gv_mjXF7ADlb9_iwhtHXs"

# # --- Configure Gemini ---
# genai.configure(api_key=GENAI_API_KEY)
# model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# # 🔊 TTS Engine Setup
# engine = pyttsx3.init()
# engine.setProperty('rate', 180)
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)

# def speak(text):
#     print("Assistant:", text)
#     engine.say(text)
#     engine.runAndWait()

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
#     except Exception as e:
#         print("❌ Sorry, couldn't recognize.")
#         return ""

# def get_gemini_reply(prompt):
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return "Sorry, Gemini API failed to respond."

# def greet_user():
#     hour = datetime.datetime.now().hour
#     if hour < 12:
#         speak("Good morning!")
#     elif hour < 18:
#         speak("Good afternoon!")
#     else:
#         speak("Good evening!")
#     speak("I am your smart assistant. How can I help you today?")

# # 🔁 Main loop
# if __name__ == "__main__":
#     greet_user()
#     while True:
#         query = listen()
#         if not query:
#             continue

#         # Special commands
#         if "open youtube" in query:
#             webbrowser.open("https://www.youtube.com")
#             speak("Opening YouTube.")
#         elif "open google" in query:
#             webbrowser.open("https://www.google.com")
#             speak("Opening Google.")
#         elif "play music" in query:
#             music_dir = "/System/Library/Sounds"
#             songs = os.listdir(music_dir)
#             os.system(f"afplay '{music_dir}/{songs[0]}'")
#             speak("Playing music.")
#         elif "exit" in query or "stop" in query:
#             speak("Goodbye!")
#             break
#         else:
#             # 💬 Ask Gemini
#             reply = get_gemini_reply(query)
#             speak(reply)





import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import pandas as pd
import google.generativeai as genai
from difflib import get_close_matches


# # # 🌐 Setup Gemini
# # genai.configure(api_key="AIzaSyD5dGbgHTWLhvgINIpgKaN0NRwCaHGkPGQ")  # <--- Use your real key here
# # # model = genai.GenerativeModel("gemini-pro")
# # model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# 🌐 Setup Gemini
genai.configure(api_key="AIzaSyBXMU6Nfrh4l9Gv_mjXF7ADlb9_iwhtHXs")
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# 📄 Load Excel file
qa_df = pd.read_excel("college_questions.xlsx")
qa_dict = dict(zip(qa_df['Question'].str.lower(), qa_df['Answer']))

# 🔊 TTS Engine Setup
engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

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

def get_custom_answer(user_query):
    questions = list(qa_dict.keys())
    match = get_close_matches(user_query, questions, n=1, cutoff=0.7)
    if match:
        return qa_dict[match[0]]
    return None

def get_gemini_reply(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Sorry, Gemini API failed to respond."

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your smart assistant. Ask me anything.")

# 🔁 Main loop
if __name__ == "__main__":
    greet_user()
    while True:
        query = listen()
        if not query:
            continue

        # Special commands
        if "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube.")
        elif "open google" in query:
            webbrowser.open("https://www.google.com")
            speak("Opening Google.")
        elif "play music" in query:
            music_dir = "/System/Library/Sounds"
            songs = os.listdir(music_dir)
            os.system(f"afplay '{music_dir}/{songs[0]}'")
            speak("Playing music.")
        elif "exit" in query or "stop" in query:
            speak("Goodbye!")
            break
        else:
            # 🧠 Try custom Excel questions
            answer = get_custom_answer(query)
            if answer:
                speak(answer)
            else:
                # 💬 Fallback to Gemini
                reply = get_gemini_reply(query)
                speak(reply)




import requests
import base64
from pydub import AudioSegment
import simpleaudio as sa
import io

TTS_API_KEY = "AIzaSyBHbl-pCyU4q_akVo8Hiwv8Ko_RdggVF9g"

def speak_google_tts_realtime(text):
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

# ✅ Example usage
speak_google_tts_realtime("Hello Arun! Your assistant is ready.")
