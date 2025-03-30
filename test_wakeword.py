import numpy as np
import pvporcupine
import pyaudio

ACCESS_KEY = "o1UIPJZfURgtP4LEEhn2E9GIOUclKWeeR1a0lYE0jtyriRgywSqo5w=="  # Replace with your actual key
MODEL_PATH = "D:/JARVIS_AI/jarvis.ppn" 
  # Ensure correct path

def test_wake_word():
    porcupine = pvporcupine.create(access_key=ACCESS_KEY, keyword_paths=[MODEL_PATH])
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16,
                           input=True, frames_per_buffer=porcupine.frame_length)

    print("Say 'JARVIS' to test the wake word...")

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = np.frombuffer(pcm, dtype=np.int16)

        if porcupine.process(pcm) >= 0:
            print("At your service, sir.")
            break

    porcupine.delete()
    audio_stream.close()
    pa.terminate()

test_wake_word()
