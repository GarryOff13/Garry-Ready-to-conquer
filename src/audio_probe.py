"""
Audio device probe - finds which input device actually works.
"""

import sounddevice as sd


print("=" * 60)
print("SOUNDDEVICE DIAGNOSTIC")
print("=" * 60)
print()

# Default devices
try:
    default_in, default_out = sd.default.device
    print(f"Default input device:  {default_in}")
    print(f"Default output device: {default_out}")
except Exception as e:
    print(f"Could not read default devices: {e}")
print()

# Host APIs
print("Host APIs available:")
for i, api in enumerate(sd.query_hostapis()):
    print(f"  [{i}] {api['name']}  (default in={api['default_input_device']}, out={api['default_output_device']})")
print()

# All devices
print("All devices:")
devices = sd.query_devices()
for i, d in enumerate(devices):
    ins = d["max_input_channels"]
    outs = d["max_output_channels"]
    name = d["name"]
    api = sd.query_hostapis(d["hostapi"])["name"]
    marker = "  <-- input" if ins > 0 else ""
    print(f"  [{i}] in={ins} out={outs} | {name} | {api}{marker}")

print()
print("=" * 60)
print("TRYING EACH INPUT DEVICE")
print("=" * 60)
print()

for i, d in enumerate(devices):
    if d["max_input_channels"] == 0:
        continue

    print(f"[{i}] {d['name']} ...", end=" ", flush=True)

    try:
        stream = sd.InputStream(
            device=i,
            samplerate=16000,
            blocksize=2048,
            channels=1,
            callback=lambda *a: None,
        )
        stream.start()
        stream.stop()
        stream.close()
        print("OK  <-- WORKS")
    except Exception as e:
        print(f"FAIL ({e})")

print()
print("Done.")