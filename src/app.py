"""
Garry - Main Application
Clap detection runs in the audio callback. Main loop pops events and shows/hides the window.

Usage:
    python app.py

Behavior:
    - Single clap (window hidden)  -> shows the Garry window
    - Single clap (window visible) -> ignored (waits for a second clap)
    - Two claps within 0.8s        -> hides the window
    - Ctrl+C                       -> quits Garry
"""

import queue
import time

import numpy as np
import sounddevice as sd

from window import GarryWindow


# --- Audio config ---
DEVICE           = 1         # Microphone Array (MME)
SAMPLE_RATE      = 16000
BLOCK_SIZE       = 2048
CLAP_THRESHOLD   = 0.06
CLAP_COOLDOWN    = 0.20      # ignore rapid-fire duplicates from the same clap
DOUBLE_CLAP_MAX  = 0.80      # two claps within this = double clap


# --- Shared state ---
events = queue.Queue()       # "open" / "close" events from audio callback
window_visible = False       # mirrored in callback for state decisions
last_clap_time = 0.0


# ----------------------------------------------------------------------
# Audio
# ----------------------------------------------------------------------

def rms(block):
    return float(np.sqrt(np.mean(np.square(block))))


def clap_callback(indata, frames, time_info, status):
    """
    Runs on the audio thread. Detects claps and decides open/close.
    This is the ONLY place that makes clap state decisions.
    """
    global last_clap_time, window_visible

    if status:
        return

    volume = rms(indata)
    now = time.time()

    # Ignore anything below threshold
    if volume <= CLAP_THRESHOLD:
        return

    # Ignore rapid-fire noise from the same physical clap
    if (now - last_clap_time) < CLAP_COOLDOWN:
        return

    # A real clap was detected
    print(f"[clap] volume={volume:.3f}  gap={now - last_clap_time:.2f}s")

    if not window_visible:
        # Window closed → single clap opens it
        print("[event] -> open")
        events.put("open")
        window_visible = True           # reflect immediately to avoid double triggers
        last_clap_time = now
    else:
        # Window open → check if this is a double clap
        if (now - last_clap_time) <= DOUBLE_CLAP_MAX:
            print("[event] -> close (double clap)")
            events.put("close")
            window_visible = False
            last_clap_time = 0.0        # reset so next clap opens cleanly
        else:
            # Single clap while open → ignore, but record time for potential second clap
            print("[event] -> single clap while open, waiting...")
            last_clap_time = now


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    global window_visible

    print("Garry is listening... clap once to open.")
    print("Double clap to close. Ctrl+C to quit.\n")

    # 1. Create the single Tk window (hidden at start)
    win = GarryWindow()

    # 2. Open the microphone
    try:
        stream = sd.InputStream(
            device=DEVICE,
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            channels=1,
            callback=clap_callback,
        )
        stream.start()
        print(f"[audio] Microphone opened (device {DEVICE}).\n")
    except Exception as e:
        print(f"[audio] Failed: {e}")
        return

    # 3. Poll the event queue on the Tk main loop
    def poll():
        global window_visible

        try:
            while True:
                event = events.get_nowait()

                if event == "open":
                    print("[action] showing window")
                    win.show_window()

                elif event == "close":
                    print("[action] hiding window")
                    win.hide_window()

        except queue.Empty:
            pass

        win.after(80, poll)

    win.after(80, poll)

    # 4. Run Tk mainloop
    try:
        win.mainloop()
    except KeyboardInterrupt:
        print("\nGarry stopped.")
    finally:
        try:
            stream.stop()
            stream.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()