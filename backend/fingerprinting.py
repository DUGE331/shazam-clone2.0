import numpy as np
import scipy.ndimage
import hashlib
import librosa

def find_peaks(S_db, threshold=-25, neighborhood_size=(60,60)):
    """Detects peaks in a spectrogram above a threshold."""
    print(f"Using neighborhood_size: {neighborhood_size}")
    local_max = scipy.ndimage.maximum_filter(S_db, size=neighborhood_size)
    detected_peaks = local_max.astype(bool) & (S_db > threshold).astype(bool)
    peaks = np.argwhere(detected_peaks)
    print(f"Detected {len(peaks)} peaks with threshold {threshold}")
    return peaks

def generate_fingerprints(peaks, sr, hop_length=512, fan_out=5):
    """Generates SHA1 fingerprints from pairs of peaks."""
    fingerprints = []
    for i in range(len(peaks)):
        freq1, time1 = peaks[i]
        for j in range(1, fan_out):
            if i + j < len(peaks):
                freq2, time2 = peaks[i + j]
                delta_t = time2 - time1
                if 0 < delta_t < 200:  # max time difference between peaks
                    hash_input = f"{freq1}|{freq2}|{delta_t}"
                    hash_val = hashlib.sha1(hash_input.encode()).hexdigest()
                    time1_sec = librosa.frames_to_time(time1, sr=sr, hop_length=hop_length)
                    fingerprints.append((hash_val, time1_sec))
    return fingerprints
