import os
import datetime
import random
import requests
import wikipedia
import screen_brightness_control as sbc
import pyautogui
import pyperclip
from dotenv import load_dotenv
from ai.chat import ask_ai
from database.db import get_connection
from plyer import notification
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

load_dotenv()

def open_chrome():
    os.system("start chrome")
    return "Opening Chrome."

def remember_fact(key, value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()
    return f"I'll remember that {key} is {value}."

def recall_fact(key):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM memory WHERE key = ?", (key,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return f"{key} is {result[0]}."
    return f"I don't know {key} yet."

def save_note(content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (content, created_at) VALUES (?, ?)", (content, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return "Note saved."

def save_reminder(content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reminders (content, created_at) VALUES (?, ?)", (content, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return "Reminder saved."

def read_clipboard():
    content = pyperclip.paste()
    if content:
        return f"Your clipboard contains: {content}"
    return "Your clipboard is empty."

def copy_to_clipboard(text):
    pyperclip.copy(text)
    return f"Copied to clipboard: {text}"


def lock_pc():
    os.system("rundll32.exe user32.dll,LockWorkStation")
    return "Locking the PC."

def shutdown_pc():
    os.system("shutdown /s /t 5")
    return "Shutting down in 5 seconds."

def restart_pc():
    os.system("shutdown /r /t 5")
    return "Restarting in 5 seconds."

def sleep_pc():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    return "Going to sleep."

def take_screenshot():
    screenshots_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
    os.makedirs(screenshots_folder, exist_ok=True)
    filename = datetime.datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.png")
    filepath = os.path.join(screenshots_folder, filename)
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    return f"Screenshot saved."

def set_brightness(level):
    try:
        sbc.set_brightness(level)
        return f"Brightness set to {level} percent."
    except Exception:
        return "I couldn't change the brightness. Your display may not support this."

def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def set_volume(level):
    volume = get_volume_interface()
    volume.SetMasterVolumeLevelScalar(level / 100, None)
    return f"Volume set to {level} percent."

def mute_volume():
    volume = get_volume_interface()
    volume.SetMute(1, None)
    return "Muted."

def unmute_volume():
    volume = get_volume_interface()
    volume.SetMute(0, None)
    return "Unmuted."

def show_notification(title, message):
    notification.notify(title=title, message=message, timeout=5)
    return f"Notification sent: {message}"

def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"That could mean several things: {', '.join(e.options[:3])}. Can you be more specific?"
    except wikipedia.exceptions.PageError:
        return f"I couldn't find anything on Wikipedia about {query}."
    except Exception:
        return "I'm having trouble reaching Wikipedia right now."

def open_vscode():
    os.system("start code")
    return "Opening Visual Studio Code."

def open_notepad():
    os.system("start notepad")
    return "Opening Notepad."

def get_weather(city="Chennai"):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"The weather in {city} is currently {description}, with a temperature of {temp} degrees Celsius."
        else:
            return f"I couldn't get the weather for {city}. Please check the city name."
    except Exception as e:
        return "I'm having trouble reaching the weather service right now."

def open_calculator():
    os.system("start calc")
    return "Opening Calculator."

def open_folder(folder_name):
    folder_paths = {
        "documents": os.path.expanduser("~/Documents"),
        "downloads": os.path.expanduser("~/Downloads"),
        "desktop": os.path.expanduser("~/Desktop"),
        "pictures": os.path.expanduser("~/Pictures"),
        "jarvis": os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    }

    path = folder_paths.get(folder_name)
    if path and os.path.exists(path):
        os.startfile(path)
        return f"Opening the {folder_name} folder."
    else:
        return f"I don't know a folder called {folder_name}."
import webbrowser

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searching Google for {query}."

def search_youtube(query):
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    return f"Searching YouTube for {query}."

def extract_search_term(text):
    """
    Pulls out everything after the word 'for' in the sentence.
    Example: 'search google for cute cats' -> 'cute cats'
    """
    if " for " in text:
        return text.split(" for ", 1)[1].strip()
    return None
def tell_time():
    now = datetime.datetime.now()
    time_string = now.strftime("%I:%M %p")  # e.g., "02:30 PM"
    return f"The time is {time_string}."

def tell_date():
    now = datetime.datetime.now()
    date_string = now.strftime("%A, %B %d, %Y")  # e.g., "Friday, August 01, 2026"
    return f"Today is {date_string}."

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I told my computer I needed a break, and it said no problem, it'll go to sleep.",
    "Why do Java developers wear glasses? Because they don't see sharp.",
    "There are 10 types of people in the world: those who understand binary, and those who don't.",
    "I would tell you a joke about UDP, but you might not get it."
]

def tell_joke():
    return random.choice(JOKES)
def process_command(command_text):
    """
    Looks at the command text and decides which function to call.
    Returns a response string for JARVIS to speak.
    """
    text = command_text.lower()

    if "chrome" in text:
        return open_chrome()
    elif "vs code" in text or "visual studio code" in text or "vscode" in text:
        return open_vscode()
    elif "notepad" in text:
        return open_notepad()
    elif "calculator" in text:
        return open_calculator()
    elif "time" in text:
        return tell_time()
    elif "date" in text:
        return tell_date()
    elif "mute" in text:
        return mute_volume()
    elif "screenshot" in text:
        return take_screenshot()
    elif "unmute" in text:
        return unmute_volume()
    elif "lock" in text:
        return lock_pc()
    elif "shutdown" in text or "shut down" in text:
        return shutdown_pc()
    elif "restart" in text:
        return restart_pc()
    elif "sleep" in text:
        return sleep_pc()
    elif "clipboard" in text or "what did i copy" in text:
        return read_clipboard()
    elif "remember my name is" in text:
        name = text.split("remember my name is", 1)[1].strip()
        return remember_fact("name", name)
    elif "what is my name" in text or "what's my name" in text:
        return recall_fact("name")
    elif "remember that" in text:
        fact = text.split("remember that", 1)[1].strip()
        return remember_fact("note", fact)
    elif "take a note" in text or "save a note" in text:
        term = extract_search_term(text)
        content = term if term else text.split("note", 1)[1].strip()
        return save_note(content)
    elif "add a reminder" in text or "set a reminder" in text:
        term = extract_search_term(text)
        content = term if term else text.split("reminder", 1)[1].strip()
        return save_reminder(content)
    elif "brightness" in text:
        import re
        numbers = re.findall(r'\d+', text)
        if numbers:
            return set_brightness(int(numbers[0]))
        else:
            return "What brightness level would you like?"
    elif "volume" in text:
        import re
        numbers = re.findall(r'\d+', text)
        if numbers:
            return set_volume(int(numbers[0]))
        else:
            return "What volume level would you like?"
    elif "joke" in text:
        return tell_joke()
    elif "weather" in text:
        return get_weather()
    elif "remind me" in text or "notify me" in text:
        term = extract_search_term(text)
        message = term if term else "Reminder from JARVIS"
        return show_notification("JARVIS Reminder", message)
    elif "wikipedia" in text or "who is" in text or "what is" in text or "tell me about" in text:
        term = extract_search_term(text)
        if not term:
            # If there's no "for", try removing common trigger phrases instead
            for phrase in ["tell me about", "wikipedia", "who is", "what is"]:
                if phrase in text:
                    term = text.split(phrase, 1)[1].strip()
                    break
        if term:
            return search_wikipedia(term)
        else:
            return "What would you like to know about?"
    elif "folder" in text:
        for name in ["documents", "downloads", "desktop", "pictures", "jarvis"]:
            if name in text:
                return open_folder(name)
    if "search google" in text or "google search" in text:
        term = extract_search_term(text)
        if term:
            return search_google(term)
        else:
            return "What would you like me to search on Google?"
    elif "search youtube" in text or "youtube search" in text:
        term = extract_search_term(text)
        if term:
            return search_youtube(term)
        else:
            return "What would you like me to search on YouTube?"
    elif "chrome" in text:
        return "Which folder would you like me to open?"
    else:
        return ask_ai(command_text)