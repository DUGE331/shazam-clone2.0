# main.py

# --- Existing imports ---
import os
import time
import requests
import base64
from backend.audio_processing import record_audio, load_audio
from backend.fingerprinting import generate_fingerprints

# --- Spotify API setup ---
SPOTIFY_CLIENT_ID = "YOUR_CLIENT_ID_HERE"
SPOTIFY_CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"

def get_spotify_token(client_id, client_secret):
    """
    Request a Spotify access token using Client Credentials flow.
    """
    auth_string = f"{client_id}:{client_secret}"
    b64_auth_string = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_string}",
    }
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

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
    y, sr = load_audio(audio_path)
    
    print("Generating fingerprints...")
    fingerprints = generate_fingerprints(y, sr)
    
    # TODO: Implement logic to convert fingerprints to track name
    track_name = "Unknown Song"  # placeholder for detected track
    artist_name = None  # placeholder

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
