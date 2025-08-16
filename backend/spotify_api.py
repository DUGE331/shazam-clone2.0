# backend/spotify_api.py
import base64
import requests
import os

# Load your client ID and secret from environment variables
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "your_client_id_here")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "your_client_secret_here")

def get_spotify_token():
    """
    Request a Spotify API access token using Client Credentials Flow.
    """
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    token_info = response.json()
    return token_info["access_token"]

def add_track_from_spotify(spotify_url, token):
    """
    Example function: retrieves track preview URL from Spotify API.
    """
    # Extract the track ID from the Spotify URL
    if "track/" in spotify_url:
        track_id = spotify_url.split("track/")[1].split("?")[0]
    else:
        raise ValueError("Invalid Spotify track URL")

    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    track_data = response.json()
    preview_url = track_data.get("preview_url")
    if not preview_url:
        preview_url = None  # instead of raising an error

    return {"track_name": track_data["name"], "preview_url": preview_url, "track_id": track_id}
