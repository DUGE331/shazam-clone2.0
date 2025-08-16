# backend/spotify_add.py
import os
from backend.audio_processing import process_recorded_audio, download_audio_preview
from backend.fingerprinting import find_peaks, generate_fingerprints
from backend.database import add_fingerprints_to_db  # now works

def add_track_from_spotify(spotify_url):
    try:
        # Step 1: Download Spotify preview MP3
        audio_path = download_audio_preview(spotify_url)
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Failed to download audio from {spotify_url}")

        # Step 2: Process audio
        S_db, sr = process_recorded_audio(audio_path)

        # Step 3: Detect peaks
        peaks = find_peaks(S_db)

        # Step 4: Generate fingerprints
        fingerprints = generate_fingerprints(peaks, sr)

        # Step 5: Save fingerprints
        track_id = spotify_url.split("/")[-1]
        add_fingerprints_to_db(fingerprints, track_id)

        return f"Added {len(fingerprints)} fingerprints for track {track_id}"

    except Exception as e:
        print(f"[ERROR] Failed to add Spotify track: {e}")
        raise
