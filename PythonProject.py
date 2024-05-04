import speech_recognition as sr
import webbrowser
import time
from time import ctime
import playsound
import random
import os
from gtts import gTTS
import datetime

r = sr.Recognizer()

# Define the timetable dataset
timetable = {
    "Monday": [
        "8:25 AM to 9:30 AM  -  Computing systems architecture",
        "11:35 AM to 12:30 PM -  ITPD",
        "4:35 PM to 5:30 PM  -  CN",
        
    ],
    "Tuesday": [
        "10:35 AM to 11:30 AM- Computing systems architecture",
        "11:35 AM to 12:30 PM - Myths and indian literature",
        "1:35 PM to 2:30 PM -  VLSI",
        "2:35 PM to 3:30 PM -  ITPD",
        "3:35 PM  to 4:30 PM-  VLSI Lab",
    ],
    "Wednesday": [
        "9:25 AM to 10:20 AM - VLSI",
    ],
    "Thursday": [
        "11:35 AM to 12:30 PM - NLP",
        "1:35 PM to 2:30 PM - CN",
        "2:35 PM to 4:30 PM - Computing systems architecture"
        "4:35 PM to 5:30 PM - CN lab",
    ],
    "Friday": [
        "11:35 AM to 12:30 PM- Myths and indian literature",
        "1:35 PM to 2:30 PM - CN",
        "2:35 PM to 3:30 PM- NLP",
    ],
    "Saturday": [
        "No classes for today"
    ],
    "Sunday": [
        "No classes for today"
    ]
    
}

def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            elmo_speak(ask)
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening....")
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
            print(voice_data)
        except sr.UnknownValueError:
            elmo_speak("Sorry could not recognize your voice\n")
        except sr.RequestError:
            elmo_speak("Sorry. My speech service is down")
        return voice_data

def elmo_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio- ' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

def get_today_schedule():
    today = datetime.datetime.now().strftime("%A")
    if today in timetable:
        return timetable[today]
    else:
        return ["No schedule available for today."]

def respond(voice_data):
    if 'what is your name' in voice_data:
        elmo_speak('My name is Elmo')
    elif 'time' in voice_data:
        elmo_speak(ctime())
    elif 'search' in voice_data:
        search = record_audio("What do you want to search for? ")
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        elmo_speak("Here is what I found for " + search)
    elif 'location' in voice_data:
        location = record_audio("What is the location? ")
        url = 'https://google.nl/maps/place/' + location + '/&amp'
        webbrowser.get().open(url)
        elmo_speak("Here is the location of " + location)
    elif 'schedule' in voice_data and ('today' in voice_data or 'for today' in voice_data):
        schedule = get_today_schedule()
        elmo_speak("Your schedule for today is as follows:")
        for event in schedule:
            elmo_speak(event)
    elif 'schedule' in voice_data:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days:
            if day.lower() in voice_data.lower():
                if day in timetable:
                    elmo_speak(f"Your schedule for {day} is as follows:")
                    for event in timetable[day]:
                        elmo_speak(event)
                    break
                else:
                    elmo_speak(f"No schedule available for {day}.")
                    break
        else:
            elmo_speak("I'm sorry, I didn't catch that day. Can you please repeat?")
    elif 'exit' in voice_data:
        elmo_speak("Goodbye!")
        exit(0)

time.sleep(1)
elmo_speak("Hello! My name is Elmo")
elmo_speak("How can I help you?")
while True:
    voice_data = record_audio()
    respond(voice_data)