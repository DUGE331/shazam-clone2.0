# 🎵 Shazam Clone (Portfolio Project)

A simplified clone of **Shazam**, built using **Python (Flask)** for the backend and a **HTML/CSS/JS frontend**.  
This project recognizes songs by generating audio fingerprints, comparing them against a local database, and integrates with the **Spotify API** to fetch metadata.

⚠️ **Note:** The Spotify API limits preview availability. Not all tracks return playable previews, and tokens expire hourly.  
For portfolio purposes, a clean frontend is included to showcase the app’s functionality and theme.

---

## 🚀 Features

- 🎤 **Song Recognition** – Records audio from the user and generates fingerprints.  
- 🗂 **Fingerprint Database** – Stores and compares unique hashes of tracks.  
- 🔗 **Spotify Integration** – Fetches song details (title, artist, album, preview link if available).  
- 🎨 **Frontend UI** – Shazam-inspired theme with:
  - Search bar to add songs via Spotify link
  - "Shazam" button to recognize audio
  - Display panel for matched song details  

---

## 📂 Project Structure
Shazam0825/
│ .env # Spotify API keys
│ requirements.txt # Python dependencies
│ main.py # Entry point (Flask app)
│ README.md # Documentation
│ fingerprint_database.pk1 # Fingerprint database
│
├───backend
│ │ audio_processing.py # Recording & preprocessing
│ │ database.py # Database operations
│ │ fingerprinting.py # Audio fingerprint generation
│ │ matching.py # Song matching logic
│ │ routes.py # Flask API routes
│ │ spotify_api.py # Spotify token + API calls
│ │ spotify_add.py # Add tracks via Spotify
│ │ spotify_downloader.py# (Optional) Download previews
│ │ init.py
│
├───frontend
│ │ main.js # UI logic (connects to backend)
│ │ preload.js
│ └───renderer
│ app.js
│ index.html # Shazam-style web UI
│ style.css
│
├───recordings
│ recorded_audio.wav # Temporary recording storage
│
├───tests
│ test_audio.py
│ test_fingerprints.py


---

## ⚙️ How It Works

1. User presses the **Shazam button** in the frontend.  
2. Audio is recorded and sent to the backend.  
3. The backend:
   - Processes the audio (`audio_processing.py`)
   - Generates a fingerprint (`fingerprinting.py`)
   - Searches against the database (`matching.py`)  
4. If a match is found:
   - Fetches metadata from Spotify (`spotify_api.py`)
   - Returns JSON to the frontend  
5. The frontend updates the UI with the **song title, artist, and album cover**.  

---

## 🛠 Tech Stack

- **Backend**: Python, Flask, Requests  
- **Audio**: Numpy, Librosa (fingerprinting & analysis)  
- **Database**: Pickle-based fingerprint storage  
- **Frontend**: HTML, CSS (Shazam-inspired theme), Vanilla JS  
- **APIs**: Spotify Web API  

---

## 📦 Installation & Setup

```bash
# Clone repo
git clone https://github.com/yourusername/Shazam0825.git
cd Shazam0825

# Install dependencies
pip install -r requirements.txt

# Add your Spotify keys to .env
SPOTIFY_CLIENT_ID=your_id
SPOTIFY_CLIENT_SECRET=your_secret

# Run backend
python -m backend.routes

# Open frontend (static)
cd frontend/renderer
open index.html   # or double-click in file explorer

🌍 Hosting for Portfolio

Frontend only can be deployed easily on GitHub Pages, Netlify, or Vercel.

This allows visitors to interact with the UI demo without needing to install Flask/Python.

Backend runs locally (Flask), but portfolio focus is on UI + architecture demonstration.

📚 Learnings

Hands-on practice with digital signal processing (DSP).

How audio fingerprinting algorithms are structured.

Working with Spotify OAuth tokens and understanding rate limits.

Building and connecting a Flask backend with a modern frontend.

Structuring a project for portfolio presentation.
