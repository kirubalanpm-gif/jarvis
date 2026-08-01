import asyncio
import edge_tts
import sys
import os
from playsound import playsound

# Allow this file to import config.py from the parent (JARVIS root) folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

async def speak(text):
    """
    Converts the given text into speech using Edge TTS,
    saves it as an mp3, and plays it silently in the background.
    """
    communicate = edge_tts.Communicate(
        text,
        config.EDGE_VOICE,
        rate=f"{int((config.VOICE_SPEED - 1) * 100):+d}%",
        volume=f"{int((config.VOICE_VOLUME - 1) * 100):+d}%"
    )
    output_file = "temp_voice.mp3"
    await communicate.save(output_file)

    # Play the audio file directly, no popup window
    playsound(output_file)

    # Clean up the temporary file after playing
    os.remove(output_file)

if __name__ == "__main__":
    asyncio.run(speak(config.GREETING))