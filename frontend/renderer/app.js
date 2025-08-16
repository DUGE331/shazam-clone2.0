const addTrackBtn = document.getElementById("add-track-btn");
const recognizeBtn = document.getElementById("recognize-btn");
const spotifyInput = document.getElementById("spotify-url");
const songNameEl = document.getElementById("song-name");
const songArtistEl = document.getElementById("song-artist");
const songPreviewEl = document.getElementById("song-preview");

// Add track via backend
addTrackBtn.addEventListener("click", async () => {
    const url = spotifyInput.value.trim();
    if (!url) return alert("Please paste a Spotify track link.");

    try {
        const response = await fetch("http://127.0.0.1:5000/add_track", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ spotify_url: url })
        });

        const data = await response.json();

        if (response.ok) {
            songNameEl.textContent = `Track added!`;
            songArtistEl.textContent = data.file_path;
            songPreviewEl.src = data.file_path;  // play downloaded preview
        } else {
            alert(data.error || "Error adding track");
        }
    } catch (err) {
        console.error(err);
        alert("Failed to contact backend");
    }
});

// Stub for Recognize button (replace with actual recognition logic)
recognizeBtn.addEventListener("click", () => {
    alert("Recognition feature not implemented yet! This is a placeholder.");
});
