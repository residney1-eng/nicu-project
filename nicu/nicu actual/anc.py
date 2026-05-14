### ANC coding on pi 2 ###
#pi.py

import sounddevice as sd
import numpy as np
import socket
import threading

# Pi to pi connector

HOST = "10.13.140.136"
PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


FS = 48000
BLOCK = 512
INPUT_DEVICE_R = 1   # ref mic
INPUT_DEVICE_E = 2   # err mic
OUTPUT_DEVICE = 1

FILTER_LEN = 512
MU = 0.005
EPSILON = 1e-6
MAX_WEIGHT_NORM = 10.0

S_hat = np.load('S_hat.npy', allow_pickle=True)
print(f"peak {np.argmax(np.abs(S_hat))}")

lock = threading.Lock()
w = [np.zeros(FILTER_LEN), np.zeros(FILTER_LEN)]
x_fil_buf = [np.zeros(FILTER_LEN), np.zeros(FILTER_LEN)]
x_ref_buf = np.zeros(FILTER_LEN)
x_filter = [np.zeros(FILTER_LEN), np.zeros(FILTER_LEN)]
s_buf = np.zeros(FILTER_LEN)
ref_signal_global = np.zeros(BLOCK)
baseline_db = 0

MAX_WEIGHT_NORM = 10.0
print_counter = 0

def ref_callback(indata, frames, time, status):
    global ref_signal_global
    if status:
        print("ref status:", status)
    ref_signal_global = indata[:, 0].copy()

def fxlms_block(ref_block, err_block, spk_idx):
    global w, x_ref_buf, x_fil_buf, s_buf

    output = np.zeros(len(ref_block))

    for i in range(len(ref_block)):
        x_ref_buf[1:] = x_ref_buf[:-1]
        x_ref_buf[0] = ref_block[i]

        y = np.dot(w[spk_idx], x_ref_buf)
        output[i] = y

        s_buf[1:] = s_buf[:-1]
        s_buf[0] = ref_block[i]
        x_filtered = np.dot(S_hat, s_buf)

        x_fil_buf[spk_idx][1:] = x_fil_buf[spk_idx][:-1]
        x_fil_buf[spk_idx][0] = x_filtered

        norm = ( np.dot(x_fil_buf[spk_idx], x_fil_buf[spk_idx])+ EPSILON)

        w[spk_idx] = (w[spk_idx] - (2 * MU / norm) * err_block[i] * x_fil_buf[spk_idx])

        if np.linalg.norm(w[spk_idx]) > MAX_WEIGHT_NORM:
            w[spk_idx] = np.zeros(FILTER_LEN)
    return output


def audio_callback(indata, outdata, frames, time, status):
    global print_counter, baseline_db

    ref_signal = ref_signal_global
    err_signal = indata[:, 0]

    with lock:
        out_l = fxlms_block(ref_signal, err_signal, spk_idx=0)
        out_r = fxlms_block(ref_signal, err_signal, spk_idx=1)

    out_l = np.clip(out_l * 0.1, -0.5, 0.5)
    out_r = np.clip(out_r * 0.1, -0.5, 0.5)

    outdata[:, 0] = out_l
    outdata[:, 1] = out_r

    print_counter += 1
    if print_counter % 1 == 0:
        rms = np.sqrt(np.mean(err_signal ** 2))
        db = 20 * np.log10(rms + 1e-8) + 83   #87 or 81
        if baseline_db is None:
            baseline_db = db
        else:
            attenuation = baseline_db - db
        print(f"dB: {db:.1f}")
        try:
            sock.sendto(f"{db:.1f}".encode(),(HOST, PORT))
        except Exception:
            pass


ref_stream = sd.InputStream(
    device=INPUT_DEVICE_R,
    channels=1,
    samplerate=FS,
    blocksize=BLOCK,
    dtype='float32',
    callback=ref_callback
)


main_stream = sd.Stream(
    device=(INPUT_DEVICE_E, OUTPUT_DEVICE),
    channels=(1, 2),
    samplerate=FS,
    blocksize=BLOCK,
    dtype='float32',
    callback=audio_callback
)


print("ANC running...")
with ref_stream, main_stream:
    sd.sleep(100000000)
