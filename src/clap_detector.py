"""
Garry - Clap Detector
Listens to the microphone and detects claps based on volume spikes.
"""

import numpy as np
import sounddevice as sd


# --- Configuration ---
SAMPLE_RATE = 44100          # Audio samples per second (standard)
BLOCK_SIZE = 1024            # How many samples to read at once
CLAP_THRESHOLD = 0.35        # Volume needed to count as a clap (0.0 - 1.0)
COOLDOWN_SECONDS = 0.25      # Ignore extra noise right after a clap


def rms(audio_block):
    """Root Mean Square - measures the loudness of an audio block."""
    return float(np.sqrt(np.mean(np.square(audio_block))))


def main():
    print("Garry is listening... clap once to test.")
    print("Press Ctrl+C to stop.\n")

    last_clap_time = 0.0
    import time

    def callback(indata, frames, time_info, status):
        nonlocal last_clap_time

        if status:
            print(f"[audio warning] {status}")

        volume = rms(indata)
        now = time.time()

        if volume > CLAP_THRESHOLD and (now - last_clap_time) > COOLDOWN_SECONDS:
            last_clap_time = now
            print(f"CLAP!  (volume: {volume:.2f})")

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
            print("\nStopped. Goodbye.")


if __name__ == "__main__":
    main()