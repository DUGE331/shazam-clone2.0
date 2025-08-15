import soundcard as sc
import soundfile as sf
import librosa
import numpy as np

def record_audio(output_file="recordings/recorded_audio.wav", duration=5, sample_rate=44100):
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    """Records system audio via loopback and saves to a WAV file."""
    print("Recording system audio using loopback...")
    default_speaker = sc.default_speaker()
    
    with sc.get_microphone(id=str(default_speaker.name), include_loopback=True).recorder(samplerate=sample_rate) as mic:
        data = mic.record(numframes=sample_rate * duration)
        print("Recording done.")
    
    # Convert to mono if needed
    if data.ndim > 1 and data.shape[1] > 1:
        data = data.mean(axis=1)
    
    # Save WAV
    sf.write(file=output_file, data=data, samplerate=sample_rate)
    print(f"Saved recording to {output_file}")
    return output_file

def process_recorded_audio(file_path):
    """Load audio and generate a spectrogram in dB."""
    y, sr = librosa.load(file_path, sr=None, mono=True)
    print(f"Loaded audio: {y.shape}, Sample rate: {sr}")
    S = np.abs(librosa.stft(y))
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    return S_db, sr

def load_audio(file_path, sample_rate=44100):
    """Load audio from a file and return waveform + sample rate."""
    import librosa
    y, sr = librosa.load(file_path, sr=sample_rate, mono=True)
    print(f"Loaded audio: {y.shape}, Sample rate: {sr}")
    return y, sr
