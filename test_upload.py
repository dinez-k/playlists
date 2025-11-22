"""
Example script to test playlist upload with audio files.
This simulates a mobile app uploading a playlist with audio files.
"""

import requests
import json

# API endpoint
API_URL = "http://127.0.0.1:8000/api/v1/playlists/upload"

# User info
user_data = {
    "user_id": "user123",
    "username": "john_doe",
    "email": "john@example.com"
}

# Device info
device_data = {
    "device_id": "device_abc123",
    "device_type": "android",
    "device_model": "Samsung Galaxy S21",
    "os_version": "Android 13",
    "app_version": "1.2.3"
}

# Playlist structure (from example_upload.json)
with open("example_upload.json", "r") as f:
    playlist_structure = json.load(f)

# Prepare form data
form_data = {
    **user_data,
    **device_data,
    "playlist_structure": json.dumps(playlist_structure)
}

# Prepare audio files (you need actual audio files for this)
# For testing, create dummy files or use real audio files
files = [
    ("audio_files", ("song1.mp3", open("path/to/song1.mp3", "rb"), "audio/mpeg")),
    ("audio_files", ("song2.mp3", open("path/to/song2.mp3", "rb"), "audio/mpeg")),
    ("audio_files", ("song3.mp3", open("path/to/song3.mp3", "rb"), "audio/mpeg")),
    ("audio_files", ("song4.mp3", open("path/to/song4.mp3", "rb"), "audio/mpeg")),
    ("audio_files", ("song5.mp3", open("path/to/song5.mp3", "rb"), "audio/mpeg")),
]

# Make the request
try:
    response = requests.post(API_URL, data=form_data, files=files)
    
    if response.status_code == 201:
        print("✅ Playlist uploaded successfully!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

# Close files
for _, file_tuple in files:
    file_tuple[1].close()
