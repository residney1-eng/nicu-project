import numpy as np # Import the NumPy library for numerical operations on arrays.

def limit_audio(signal, threshold=0.15): # Limit the audio signal to a specified threshold to prevent clipping.
    signal = np.asarray(signal, dtype=np.float32)

    if signal.size == 0:
        raise ValueError("signal cannot be empty")

    if not np.all(np.isfinite(signal)):
        raise ValueError("signal contains NaN or infinity values")

    if not isinstance(threshold, (int, float)):
        raise TypeError("threshold must be a number, like 0.15")

    if threshold <= 0:
        raise ValueError("threshold must be greater than 0")

    if threshold > 1.0:
        raise ValueError("threshold should be 1.0 or less for normal audio signals")

    return np.clip(signal, -threshold, threshold)