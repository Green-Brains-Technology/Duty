
import os
import edge_tts
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()

def record_text():
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                # Adjust for ambient noise if needed
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.listen(source)
            MyText = r.recognize_google(audio).lower()
            return MyText
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("You have not said anything yet. Please try again.")

# Turn this into a class
class Listen:
    def __init__(self):
        self.r = sr.Recognizer()
    
    def record_text(self):
        while True:
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    # Adjust for ambient noise if needed
                    self.r.adjust_for_ambient_noise(source, duration=0.2)
                    audio = self.r.listen(source)
                MyText = self.r.recognize_google(audio).lower()
                return MyText
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
            except sr.UnknownValueError:
                print("You have not said anything yet. Please try again.")
    