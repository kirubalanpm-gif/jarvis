import os
import datetime

def open_chrome():
    os.system("start chrome")
    return "Opening Chrome."

def open_vscode():
    os.system("start code")
    return "Opening Visual Studio Code."

def open_notepad():
    os.system("start notepad")
    return "Opening Notepad."

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

def tell_time():
    now = datetime.datetime.now()
    time_string = now.strftime("%I:%M %p")  # e.g., "02:30 PM"
    return f"The time is {time_string}."

def tell_date():
    now = datetime.datetime.now()
    date_string = now.strftime("%A, %B %d, %Y")  # e.g., "Friday, August 01, 2026"
    return f"Today is {date_string}."

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
    elif "folder" in text:
        for name in ["documents", "downloads", "desktop", "pictures", "jarvis"]:
            if name in text:
                return open_folder(name)
        return "Which folder would you like me to open?"
    else:
        return f"I heard you say: {command_text}. I don't know that command yet."