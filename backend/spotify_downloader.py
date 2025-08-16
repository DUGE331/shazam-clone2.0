# backend/spotify_downloader.py
import os
import requests
from flask import Flask, request, jsonify
from main import get_spotify_token  # your existing token function

app = Flask(__name__)

DOWNLOAD_FOLDER = "recordings"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/add_track", methods=["POST"])
def add_track():
    """
    Expects JSON: { "spotify_url": "https://open.spotify.com/track/..." }
    Downloads the 30-second preview and saves it locally.
    """
    data = request.get_json()
    spotify_url = data.get("spotify_url")
    if not spotify_url:
        return jsonify({"error": "No Spotify URL provided"}), 400

    # Extract track ID from the URL
    try:
        track_id = spotify_url.split("track/")[1].split("?")[0]
    except IndexError:
        return jsonify({"error": "Invalid Spotify URL"}), 400

    # Get Spotify token
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch track info from Spotify API
    response = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers)
    if response.status_code != 200:
        return jsonify({"error": f"Spotify API error: {response.text}"}), 400

    track_info = response.json()
    preview_url = track_info.get("preview_url")
    if not preview_url:
        return jsonify({"error": "No preview available for this track"}), 400

    # Download preview MP3
    mp3_data = requests.get(preview_url).content
    file_path = os.path.join(DOWNLOAD_FOLDER, f"{track_id}.mp3")
    with open(file_path, "wb") as f:
        f.write(mp3_data)

    return jsonify({"message": "Track downloaded successfully", "file_path": file_path})

if __name__ == "__main__":
    app.run(port=5000)
