from gtts import gTTS
from pydub import AudioSegment
import os

# Create and save TTS
tts = gTTS("Hello there!", lang='en')
tts.save("output.mp3")

# Load and change speed
sound = AudioSegment.from_file("output.mp3")

# Speed up (e.g., 1.5x)
faster_sound = sound._spawn(sound.raw_data, overrides={
    "frame_rate": int(sound.frame_rate * 1.5)
}).set_frame_rate(sound.frame_rate)

# Save sped-up version
faster_sound.export("faster_output.mp3", format="mp3")
