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


OUTPUT_FOLDER = "audtemp"  # Specify the folder here
    
# Turn this into a class
class Talk:
    def __init__(self):
        self.voice = VOICE2
        self.output_folder = OUTPUT_FOLDER
        
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        self.output_file = os.path.join(self.output_folder, "audio.wav")
        
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