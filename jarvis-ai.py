import os 
import google.generativeai as genai
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Main Gemini Chat Function
def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return None

# Fallback using OpenRouter (uses GPT-3.5 / Mixtral / Claude)
def ask_openrouter(prompt, model="mistralai/mixtral-8x7b"):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are JARVIS, an advanced AI assistant."},
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[OpenRouter Error] {str(e)}"

# JARVIS Handler
def ask_jarvis(prompt):
    gemini_reply = ask_gemini(prompt)
    if gemini_reply:
        return gemini_reply.strip()
    else:
        print("[JARVIS] Switching to backup model (OpenRouter)...")
        return ask_openrouter(prompt).strip()

# Command Loop
if __name__ == "__main__":
    print("JARVIS: Online and ready, sir.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("JARVIS: Powering down, sir.")
            break
        response = ask_jarvis(user_input)
        print(f"JARVIS: {response}")