import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import threading

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_and_respond():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        update_status("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)
            query = r.recognize_google(audio).lower()
            user_input.set(query)
            update_status("Recognized")
            respond(query)
        except Exception as e:
            user_input.set("")
            response_text.set("Sorry, could not recognize.")
            update_status("Try Again")

def respond(query):
    response = ""
    
    if "time" in query:
        time = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The current time is {time}"
    
    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
        response = "Opening YouTube"

    elif "open google" in query:
        webbrowser.open("https://www.google.com")
        response = "Opening Google"

    elif "play music" in query:
        music_dir = "/System/Library/Sounds"
        songs = os.listdir(music_dir)
        os.system(f"afplay '{music_dir}/{songs[0]}'")
        response = "Playing music"

    elif "stop" in query or "exit" in query:
        response = "Goodbye!"
        speak(response)
        root.destroy()
        return

    else:
        response = "Sorry, I didn't understand that."

    response_text.set(response)
    speak(response)

def threaded_listen():
    threading.Thread(target=listen_and_respond).start()

def update_status(msg):
    status_text.set(f"Status: {msg}")

# ---------------- UI ----------------
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="Voice Assistant", font=("Helvetica", 18, "bold")).pack(pady=10)

user_input = tk.StringVar()
response_text = tk.StringVar()
status_text = tk.StringVar(value="Status: Idle")

tk.Label(root, text="You said:", font=("Helvetica", 12)).pack()
tk.Label(root, textvariable=user_input, fg="blue", font=("Helvetica", 12)).pack(pady=5)

tk.Label(root, text="Assistant:", font=("Helvetica", 12)).pack()
tk.Label(root, textvariable=response_text, fg="green", font=("Helvetica", 12)).pack(pady=5)

tk.Label(root, textvariable=status_text, font=("Helvetica", 10, "italic")).pack(pady=5)

tk.Button(root, text="🎤 Speak", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=threaded_listen).pack(pady=15)

root.mainloop()



# AIzaSyD5dGbgHTWLhvgINIpgKaN0NRwCaHGkPGQ