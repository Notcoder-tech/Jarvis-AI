import openai
import os
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def ask_jarvis(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are JARVIS, an advanced AI assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("JARVIS: Shutting down, sir.")
        break
    response = ask_jarvis(user_input)
    print(f"JARVIS: {response}")
