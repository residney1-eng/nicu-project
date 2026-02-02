### NOISE FROM MICS

import random

def get_noise_level():
    """
    Simulates reading noise level from microphone.
    Returns noise level in dB.
    """
    return random.randint(40, 80)
