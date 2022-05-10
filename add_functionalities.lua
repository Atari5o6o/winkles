- show weather  (done)
- set alarm     (cant figure out how to get audio input as integer)
def set_alarm():
    global recognizer

    speaker.say("Specify the hour in a 24 hour format")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                hour = int(recognizer.recognize_google(audio))

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again!")
            speaker.runAndWait()

    speaker.say("Specify the minutes")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                minute = int(recognizer.recognize_google(audio))

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again!")
            speaker.runAndWait()

    while True:
        if hour == datetime.datetime.now().hour and minute == datetime.datetime.now().minute:

            speaker.say("It is now" + hour + minute)
            speaker.runAndWait()

- set reminder
- search wikipedia
- whats the time   (done)
- add activation voice command
- add to calendar
-