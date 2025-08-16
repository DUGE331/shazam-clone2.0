// frontend/renderer/app.js or main.js
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("spotify-form");
  const input = document.getElementById("spotify-url");
  const message = document.getElementById("status-message");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const spotifyUrl = input.value.trim();
    if (!spotifyUrl) {
      message.textContent = "Please enter a Spotify track URL.";
      return;
    }

    message.textContent = "Downloading track preview...";

    try {
      const response = await fetch("http://localhost:5000/add_track", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ spotify_url: spotifyUrl }),
      });

      const result = await response.json();
      if (response.ok) {
        message.textContent = `Track saved! File path: ${result.file_path}`;
        input.value = ""; // clear input
      } else {
        message.textContent = `Error: ${result.error}`;
      }
    } catch (err) {
      message.textContent = `Request failed: ${err}`;
    }
  });
});
