"""
Quick diagnostic: shows live microphone volume.
Clap, talk, snap your fingers, and watch the numbers.
"""

import numpy as np
import sounddevice as sd


SAMPLE_RATE = 44100
BLOCK_SIZE = 1024


def rms(audio_block):
    return float(np.sqrt(np.mean(np.square(audio_block))))


def callback(indata, frames, time_info, status):
    if status:
        return
    volume = rms(indata)
    # Simple bar visual
    bar = "#" * int(volume * 100)
    print(f"{volume:.3f}  {bar}")


print("Listening... clap, talk, snap. Watch the numbers.")
print("Press Ctrl+C to stop.\n")

with sd.InputStream(
    samplerate=SAMPLE_RATE,
    blocksize=BLOCK_SIZE,
    channels=1,
    callback=callback,
):
    try:
        while True:
            sd.sleep(100)
    except KeyboardInterrupt:
        print("\nStopped.")