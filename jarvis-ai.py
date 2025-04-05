import os
import time
import requests
from dotenv import load_dotenv
import google.generativeai as genai
import openai

# Load environment variables
load_dotenv()

# --- API Keys ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# --- Configure Gemini ---
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# --- Configure OpenRouter ---
openai.api_key = OPENROUTER_API_KEY
openai.base_url = "https://openrouter.ai/api/v1"

# --- Weather API Logic ---
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        res = requests.get(url).json()

        if res["cod"] != 200:
            return f"Couldn't find weather for '{city}'."

        temp = res["main"]["temp"]
        description = res["weather"][0]["description"]
        return f"The weather in {city} is {description} with a temperature of {temp}°C."
    except Exception as e:
        return f"Weather error: {str(e)}"

# --- Ask Gemini (Primary AI) ---
def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"GEMINI_ERROR: {str(e)}"

# --- Ask OpenRouter (Fallback AI) ---
def ask_openrouter(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="mistral/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are JARVIS, an advanced AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"OPENROUTER_ERROR: {str(e)}"

# --- JARVIS Main Loop ---
while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("JARVIS: Shutting down, sir.")
        break

    if "weather" in user_input.lower():
        words = user_input.split()
        city = "your city"
        for i, word in enumerate(words):
            if word.lower() == "in" and i + 1 < len(words):
                city = words[i + 1]
                break
        response = get_weather(city)
        print(f"JARVIS: {response}")
        continue

    # First try Gemini
    reply = ask_gemini(user_input)
    if reply.startswith("GEMINI_ERROR"):
        print("JARVIS: Gemini failed, trying backup...")
        reply = ask_openrouter(user_input)

    print(f"JARVIS: {reply}")
