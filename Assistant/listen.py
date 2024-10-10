
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

class Listen:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 4000
        self.recognizer.pause_threshold = 1.0
    
    def record_text(self):
        while True:
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=None)
                
                text = self.recognizer.recognize_google(audio).lower()
                print("You said:", text)
                return text
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand that. Please try again.")
            except sr.RequestError:
                print("Sorry, there was an error with the speech recognition service. Please try again.")
            except sr.WaitTimeoutError:
                print("No speech detected. Please try again.")
    