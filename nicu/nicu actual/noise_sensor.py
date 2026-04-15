### For mic audio

import sounddevice as sd
import numpy as np
import math
from config import offset_db

# Audio settings
SAMPLE_RATE = 48000 # 41000
CHANNELS = 1
DURATION = 0.1 # changed from 0.2

NOISE_FLOOR = 1e-8

def get_noise_level(device):
    recording = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=CHANNELS,
                        dtype='float32' device=device)

    samples = recording.flatten().astype(np.float64)
    samples = samples - np.mean(samples)
    rms = np.sqrt(np.mean(samples ** 2))
#    print (f"DEBUG rms={rms:.8f} db_raw={20 * np.log10(rms) + 90 :.1f}")
    peak = np.max(np.abs(samples))
    level = 0.8 * rms + 0.2 * peak

    if rms <=0:
        return 0
    db = 20 * np.log10(rms) + offset_db
    db = max(0, min(db, 120))
    return round(db, 1)

def get_average_noise(device_list):
    readings = []

    for device in device_list:
        try:
            db = get_noise_level(device)
            readings.append(db)
        except Exception as e:
            print("Mic error on device", device, e)

    if len(readings) == 0:
        return 0

    avg_db = sum(readings) / len(readings)
    return round(avg_db, 1)