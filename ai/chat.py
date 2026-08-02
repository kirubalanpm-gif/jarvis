import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_ai(question):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=question
        )
        return response.text
    except Exception as e:
        return "I'm having trouble reaching my AI brain right now."