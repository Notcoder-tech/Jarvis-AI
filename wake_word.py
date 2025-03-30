import pvporcupine
import pyaudio
import struct

# Replace this with your Porcupine Access Key
ACCESS_KEY = "o1UIPJZfURgtP4LEEhn2E9GIOUclKWeeR1a0lYE0jtyriRgywSqo5w=="

# Initialize Porcupine Wake Word Detector
porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=["jarvis.ppn"]  # Pre-trained wake word model
)

# Start Audio Stream
pa = pyaudio.PyAudio()
stream = pa.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=porcupine.sample_rate,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("Listening for 'JARVIS'...")

while True:
    pcm = stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

    result = porcupine.process(pcm)
    if result >= 0:
        print("Wake Word Detected! JARVIS is now active.")
        break  # Exit loop once wake word is detected

# Cleanup
stream.close()
pa.terminate()
porcupine.delete()
