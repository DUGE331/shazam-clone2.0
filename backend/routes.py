# backend/routes.py
from flask import Flask, request, jsonify
from backend.spotify_api import get_spotify_token, add_track_from_spotify

app = Flask(__name__)
@app.route("/add_spotify_track", methods=["POST"])
def add_spotify_track():
    data = request.json
    spotify_url = data.get("spotify_url")
    if not spotify_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        token = get_spotify_token()
        print("Token received:", token[:20], "...")

        try:
            message = add_track_from_spotify(spotify_url, token)
            if not message.get("preview_url"):
                return jsonify({"status": "error", "message": "No preview available for this track"}), 400
            print("add_track_from_spotify result:", message)

            print("add_track_from_spotify result:", message)
        except Exception as e:
            print("Error in add_track_from_spotify:", e)
            raise

        return jsonify({"success": True, "message": message})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/add_track', methods=['POST'])
def add_track():
    # Delayed imports to avoid circular import
    from backend.audio_processing import process_recorded_audio
    from backend.fingerprinting import find_peaks, generate_fingerprints
    from backend.spotify_downloader import download_spotify_preview
    from backend.database import add_fingerprints_to_db

    data = request.get_json()
    spotify_url = data.get("spotify_url")
    if not spotify_url:
        return jsonify({"status": "error", "message": "No Spotify URL provided"}), 400

    try:
        # Step 1: Download the Spotify preview (MP3)
        audio_path = download_spotify_preview(spotify_url)

        # Step 2: Process audio to get spectrogram
        S_db, sr = process_recorded_audio(audio_path)

        # Step 3: Detect peaks
        peaks = find_peaks(S_db)

        # Step 4: Generate fingerprints
        fingerprints = generate_fingerprints(peaks, sr)

        # Step 5: Add fingerprints to database
        add_fingerprints_to_db(fingerprints, track_url=spotify_url)

        return jsonify({"status": "success", "track_url": spotify_url, "num_fingerprints": len(fingerprints)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def index():
    return """
    <h1>Shazam-like App UI</h1>
    <h2>Add Spotify Track</h2>
    <form action="/add_spotify_track" method="post" enctype="application/json" onsubmit="submitSpotify(event)">
        <input type="text" id="spotify_url" placeholder="Spotify URL">
        <button type="submit">Add Track</button>
    </form>

    <h2>Test Endpoints</h2>
    <ul>
        <li>POST /add_spotify_track</li>
        <li>POST /add_track</li>
        <li>POST /process_audio</li>
    </ul>

    <script>
    async function submitSpotify(event) {
        event.preventDefault();
        const url = document.getElementById("spotify_url").value;

        const response = await fetch("/add_spotify_track", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ spotify_url: url })
        });

        const result = await response.json();
        alert(JSON.stringify(result));
    }
    </script>
    """

if __name__ == "__main__":
    app.run(debug=True, port=5000)
