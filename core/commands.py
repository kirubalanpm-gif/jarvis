import os
import datetime
import random
import requests
from dotenv import load_dotenv

load_dotenv()

def open_chrome():
    os.system("start chrome")
    return "Opening Chrome."

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
    elif "joke" in text:
        return tell_joke()
    elif "weather" in text:
        return get_weather()
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
        return f"I heard you say: {command_text}. I don't know that command yet."