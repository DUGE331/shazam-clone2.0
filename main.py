# main.py
from backend.audio_processing import process_recorded_audio
from backend.fingerprinting import find_peaks, generate_fingerprints
from backend.audio_processing import record_audio, process_recorded_audio
import pickle

with open("fingerprint_database.pk1", "rb") as f:
    fingerprint_db = pickle.load(f)

import os
import base64
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

print("CLIENT_ID:", CLIENT_ID)
print("CLIENT_SECRET:", CLIENT_SECRET)

# Prepare authorization
auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
auth_b64 = base64.b64encode(auth_str.encode()).decode()

# Request token
url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": f"Basic {auth_b64}",
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {"grant_type": "client_credentials"}

response = requests.post(url, headers=headers, data=data)
print("Status code:", response.status_code)
print("Response:", response.text)

def search_spotify_track(token, track_name, artist_name=None):
    """
    Search for a track on Spotify.
    """
    query = f"track:{track_name}"
    if artist_name:
        query += f" artist:{artist_name}"

    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": 1}
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    response.raise_for_status()
    items = response.json().get("tracks", {}).get("items", [])
    if items:
        return items[0]  # return the first match
    return None

# --- Main process ---
def main():
    print("Recording audio...")
    audio_path = record_audio()  # from backend.audio_processing
    print(f"Saved recording to {audio_path}")

    print("Loading audio...")
    # Load audio and generate spectrogram
    S_db, sr = process_recorded_audio(audio_path)

    # Detect peaks in the spectrogram
    peaks = find_peaks(S_db)
    # fingerprints = [(hash, time), ...]
    fingerprints = generate_fingerprints(peaks, sr)
    print(f"Generated {len(fingerprints)} fingerprints.")

    # Generate fingerprints from peaks
    fingerprints = generate_fingerprints(peaks, sr)
    print("Sample fingerprints:", fingerprints[:5])

    matches = {}

    for hash_val, time in fingerprints:
        if hash_val in fingerprint_db:
            track_name = fingerprint_db[hash_val]['track_name']  # or however you stored it
            matches[track_name] = matches.get(track_name, 0) + 1


def get_spotify_token(client_id, client_secret):
    auth_str = f"{client_id}:{client_secret}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()
    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": f"Basic {auth_b64}",
               "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

    print("Connecting to Spotify...")
    token = get_spotify_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    
    track_info = search_spotify_track(token, track_name, artist_name)
    if track_info:
        print(f"Track found: {track_info['name']} by {track_info['artists'][0]['name']}")
        print(f"Listen: {track_info['external_urls']['spotify']}")
    else:
        print("No match found on Spotify.")

if __name__ == "__main__":
    main()


