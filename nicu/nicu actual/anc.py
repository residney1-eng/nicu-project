### ANC coding on pi 2 ###

import sounddevice as sd
import numpy as np
import socket
import queue
import time
#import math ---left, right---


# Pi to pi connector
HOST = "10.13.140.19"
PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

SAMPLE_RATE = 44100
BLOCK_SIZE = 4096 
OUTPUT_RATE = 48000
INPUT_DEVICE = 2 #1
OUTPUT_DEVICE = 3 #2
last_freq = 0
freq_queue = queue.Queue(max_size=1)
last_rms = 0
print_counter = 0

def audio_callback(indata, frames, time, status):
    global last_freq, last_rms, print_counter
    print_counter += 1

    fft = np.fft.rfft(indata[:, 0])
    freqs = np.fft.rfftfreq(frames, 1 / SAMPLE_RATE)
    dominant_freq = int(freqs[np.argmax(np.abs(fft))])
    rms = np.sqrt(np.mean(indata ** 2))
    last_rms = rms
    db = round(20 * np.log10(rms + 1e-8) + 87, 1) # offset to calibrate with real dB, 87 calibrated (small mic)
    
    if print_counter % 10 == 0: 
        print(f"db: {db:.1f}")
    #if rms > 0.8: # threshold to avoid sending noise when mic is quiet
        try:
            freq_queue.put_nowait(dominant_freq)
            except queue.Full:
                pass
        sock.sendto(str(db).encode(), (HOST, PORT))
        print(f"Freq: {dominant_freq} Hz, DB: {db}")
stream = sd.InputStream(device=INPUT_DEVICE, channels=1, samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE,
                         callback=audio_callback)
stream.start()
print("anc running...")

while True:
    try:
        freq= freq_queue.get(timeout=1)
        if abs(freq - last_freq) < 50: 
            freq = last_freq
        last_freq = freq

        if freq > 50 and freq < 1000: #3000 too high(using foam), 1000 for best result 
            t = np.linspace(0, 0.15, int(OUTPUT_RATE * 0.15)) 
            gain = min(last_rms * 2, 1.0) 
            anti_noise = - 1.0 * np.sin(2 * np.pi * freq * t)
            silence = np.zeros(lens(anti_noise))
            stereo = np.column_stack((silence, anti_noise))
            sd.play(stereo, OUTPUT_RATE, device=OUTPUT_DEVICE)
            sd.wait()

    except queue.Empty:
        pass
    except Exception as e:
        print("audio error: {e}")

(### left and right speakers , if needed

#        if freq> 50 and freq < 3000: 
#            t = np.linspace(0, 0.15, int(OUTPUT_RATE * 0.15))
                
#                left = 1.0 * np.sin(2 * np.pi * freq * t)
#                right = - 1.0 * np.sin(2 * np.pi * freq * t)
            
#                stereo = np.column_stack((left, right))
#                sd.play(stereo, OUTPUT_RATE, device=OUTPUT_DEVICE)
#            except Exception as e:
#                pass
)
