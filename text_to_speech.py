import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)  # Adjust speed (default ~200)
    engine.setProperty('volume', 1.0)  # Max volume
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Change index for different voices
    engine.say(text)
    engine.runAndWait()

# Test Jarvis voice
speak("Hello sir, text-to-speech is now working.")
