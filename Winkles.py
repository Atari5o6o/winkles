import mappings as mappings
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import nltk
from config import api_key
import pyaudio
import requests
from pprint import pprint
import datetime
import time

nltk.download('omw-1.4')

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 160)


def city_weather():
    global recognizer

    api_key = "abf8e9d70c9b86e22376b620cd447646"

    #location = input("location?")   (use once ready to inplement variable location)
    weather_URL = f"http://api.openweathermap.org/data/2.5/weather?q=tokyo&appid=" #for tokyo only
    final_URL = weather_URL + api_key

    x = requests.get(final_URL).json()

    if x[""] != "404":
        y = x["main"]

        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]

        speaker.say(" The temperature is   " +
                        str(int(current_temperature) - int(273.1)) + " Degrees celcius"
                "\n Humidity is " +
                        str(current_humidity) + " Percent"
                "\n with " +
                        str(weather_description))
        speaker.runAndWait()
    else:
        speaker.say(" City Not Found ")
        speaker.runAndWait()

def create_note():
    global recognizer

    speaker.say("What should the note say?")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Choose a file name")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower

            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"Noted {filename}")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again!")
            speaker.runAndWait()

def add_todo():

    global recognizer

    speaker.say("What should i add to the to do list?")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)
                done = True

                speaker.say(f"successfully added {item} to the to do list")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again!")
            speaker.runAndWait()

def show_todos():

    speaker.say("The to do list consists of the following")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()

def tell_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M", t)

    speaker.say("It is currently")
    speaker.runAndWait()

    speaker.say(current_time)
    speaker.runAndWait()

def greeting():

    speaker.say("How may I be of service?")
    speaker.runAndWait()

def quit():
    speaker.say("Bye")
    speaker.runAndWait()
    sys.exit(0)


mappings = {
    "greeting": greeting,
    "create.note": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "exit": quit,
    "Weather": city_weather,
    "tell_time": tell_time

}




assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

while True:

    try:
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        assistant.request(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()

