import asyncio
from voice.speak import speak
from voice.listen import listen
import config

WAKE_WORD = "jarvis"
STOP_WORDS = ["stop listening", "shut down", "goodbye jarvis"]

async def handle_command(command_text):
    print(f"Handling command: {command_text}")
    await speak(f"You said: {command_text}")

async def main_loop():
    await speak(config.GREETING)

    while True:
        heard_text = listen()

        if heard_text is None:
            continue

        heard_text_lower = heard_text.lower()
       

        if any(stop_word in heard_text_lower for stop_word in STOP_WORDS):
            await speak("Goodbye.")
            break  # exits the while loop, ending the program

        if WAKE_WORD in heard_text_lower:
            await speak("Yes?")
            command_text = listen()
            if command_text:
                await handle_command(command_text)

if __name__ == "__main__":
    asyncio.run(main_loop())