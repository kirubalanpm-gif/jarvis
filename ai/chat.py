import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

conversation_history = []

def ask_ai(question):
    try:
        conversation_history.append(
            types.Content(role="user", parts=[types.Part(text=question)])
        )

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=conversation_history
        )

        conversation_history.append(
            types.Content(role="model", parts=[types.Part(text=response.text)])
        )

        if len(conversation_history) > 20:
            conversation_history[:] = conversation_history[-20:]

        return response.text
    except Exception as e:
        print(f"[DEBUG] AI Error: {e}")
        return "I'm having trouble reaching my AI brain right now."