# Shazam Clone

A fun Shazam-inspired audio recognition project built in Python and Flask, with a simple front-end interface to showcase it.  

## Overview

This project demonstrates:

- Audio fingerprinting and matching
- Spotify API integration (preview downloads)
- Flask backend for processing and serving data
- Quick front-end to interact with the backend

> **Note:** The Spotify API requires a valid token, which is only valid for a short period (hourly). Because of this, the demo front-end is a showcase version for portfolio purposes rather than a fully live product.

## Frontend

The `frontend/` folder contains:

- `index.html` — Simple web interface with a search bar and “Shazam” clone button.
- `style.css` — Basic styling following a Shazam-like theme.
- `main.js` — Handles front-end logic and interaction with the backend.

Users can:

- Input Spotify track links to add to the library
- Click the “Shazam” button to recognize audio (mocked for portfolio purposes)
- View matched track details

## Backend

The `backend/` folder includes:

- Audio processing, fingerprinting, and matching modules
- Routes for adding tracks and serving data
- Spotify integration for fetching track info and previews

## Installation & Run (For Local Testing)

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
2. Install dependencies:

pip install -r requirements.txt

3. Start the backend server:

python -m backend.spotify_downloader

4. Open frontend/index.html in your browser.

5. Portfolio Note
This project was primarily a learning exercise. Because API tokens expire quickly, the front-end is designed to showcase functionality visually rather than rely on live Spotify data.
It was a fun way to practice full-stack development, audio processing, and integrating third-party APIs.

---
If you want, I can also **add a super short version with a fun “portfolio-friendly” tone** that reads more like a personal project showcase.  
Do you want me to do that?
