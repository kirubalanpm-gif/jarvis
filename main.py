import asyncio
from voice.speak import speak
from voice.listen import listen
from core.commands import process_command
import config

WAKE_WORD = "jarvis"
STOP_WORDS = ["stop listening", "shut down", "goodbye jarvis"]

async def handle_command(command_text):
    response = process_command(command_text)
    print(f"JARVIS: {response}")
    await speak(response)

async def main_loop():
    await speak(config.GREETING)

    while True:
        heard_text = listen()

        if heard_text is None:
            continue

        heard_text_lower = heard_text.lower()

        if any(stop_word in heard_text_lower for stop_word in STOP_WORDS):
            await speak("Goodbye.")
            break

        if WAKE_WORD in heard_text_lower:
            # Extract whatever comes AFTER the wake word in the same sentence
            wake_index = heard_text_lower.find(WAKE_WORD)
            remainder = heard_text[wake_index + len(WAKE_WORD):].strip()

            if remainder:
                # The command was said in the same sentence as "jarvis"
                await handle_command(remainder)
            else:
                # Only "jarvis" was said alone — ask for the command separately
                await speak("Yes?")
                command_text = listen()
                if command_text:
                    await handle_command(command_text)

if __name__ == "__main__":
    asyncio.run(main_loop())