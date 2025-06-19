import librosa
import numpy as np

def load_audio_crepe(filepath, sr=16000):
    # Load and resample audio to 16kHz, mono
    y, _ = librosa.load(filepath, sr=sr, mono=True)

    # Normalize to avoid amplitude-related issues
    y = librosa.util.normalize(y)
    print(f"Audio duration: {len(y)/sr:.2f} seconds")

    return y, sr
