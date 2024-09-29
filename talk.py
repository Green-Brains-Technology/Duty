import os
import edge_tts
import sounddevice as sd
import soundfile as sf

# Female Voices
VOICE1 = "en-US-AvaNeural"
VOICE2 = "en-IE-EmilyNeural"
VOICE3 = "en-US-EmmaNeural"
VOICE4 = "en-GB-SoniaNeural"
VOICE5 = "en-AU-NatashaNeural"

# Male Voices
VOICE6 = "en-GB-RyanNeural"
VOICE7 = "en-CA-LiamNeural"


OUTPUT_FOLDER = "Lib\\audtemp"  # Specify the folder here
    
# Turn this into a class
class Talk:
    def __init__(self):
        self.voice = VOICE2
        self.output_file = os.path.join(OUTPUT_FOLDER, "audio.wav")
        
    async def speak_text(self, text):
        """Convert text to speech and play it."""
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(self.output_file)

        # Read the audio file
        audio_data, sample_rate = sf.read(self.output_file, dtype='float32')

        # Play the audio
        sd.play(audio_data, sample_rate)
        sd.wait()

        os.remove(self.output_file)

# Implementation
# talk = Talk()
# asyncio.run(talk.speak_text("Hello, World!"))