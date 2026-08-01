import speech_recognition as sr

def listen():
    """
    Captures audio from the microphone and converts it to text
    using Google's free speech recognition service.
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for background noise... please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = recognizer.listen(source)

    print("Recognizing...")
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError:
        print("Speech recognition service is unavailable right now.")
        return None

if __name__ == "__main__":
    listen()