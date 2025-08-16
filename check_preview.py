import base64
import requests

CLIENT_ID = "105eb6e3bd924b2caeb327e993650645"
CLIENT_SECRET = "5e730d20872541d088e36605c547f035"

# Encode as base64
auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
b64_auth_str = base64.b64encode(auth_str.encode()).decode()

headers = {
    "Authorization": f"Basic {b64_auth_str}"
}

data = {"grant_type": "client_credentials"}

response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
token_info = response.json()
access_token = token_info["access_token"]

print("Access token:", access_token)

import requests

track_id = "6qqrTXSdwiJaq8SO0X2lSe"
url = f"https://api.spotify.com/v1/tracks/{track_id}"

headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN"
}

response = requests.get(url, headers=headers)
data = response.json()

print("Track name:", data.get("name"))
print("Preview URL:", data.get("preview_url"))
