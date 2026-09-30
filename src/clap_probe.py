"""
Live mic level meter - watch the numbers while you clap.
Tells us what threshold your mic actually produces.
"""

import time
import numpy as np
import sounddevice as sd


DEVICE = 1          # your working mic
SAMPLE_RATE = 16000
BLOCK_SIZE = 2048

peaks = []


def rms(block):
    return float(np.sqrt(np.mean(np.square(block))))


def callback(indata, frames, time_info, status):
    if status:
        return
    v = rms(indata)
    peaks.append((time.time(), v))
    # Print a live bar
    bar = "#" * int(min(v * 200, 60))
    print(f"{v:.3f}  {bar}")


print(f"Listening on device {DEVICE}.")
print("Sit quiet for 2 seconds, then:")
print("  1. Talk normally")
print("  2. Snap your fingers")
print("  3. Clap once softly")
print("  4. Clap once LOUD")
print("Then press Ctrl+C.\n")

stream = sd.InputStream(
    device=DEVICE,
    samplerate=SAMPLE_RATE,
    blocksize=BLOCK_SIZE,
    channels=1,
    callback=callback,
)
stream.start()

try:
    while True:
        sd.sleep(100)
except KeyboardInterrupt:
    pass
finally:
    stream.stop()
    stream.close()

print("\n--- SUMMARY ---")
if peaks:
    values = [v for _, v in peaks]
    print(f"Max volume seen:  {max(values):.3f}")
    print(f"Avg volume:       {sum(values)/len(values):.3f}")
    print(f"Total blocks:     {len(values)}")