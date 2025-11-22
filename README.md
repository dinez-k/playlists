# Playlist API - Simple & Scalable

A clean REST API for managing playlists with cloud-stored audio files from mobile devices.

## Key Features

- **Simple Playlist Creation**: Create playlists with user_id and device_id
- **Parent-Child Relationships**: Backend handles nested playlist structure
- **Audio File Upload**: Upload songs with audio files, automatically stored in cloud
- **Cloud Storage**: Audio files uploaded to S3/GCS, URLs saved in database

## Quick Start

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure MongoDB** (`.env`):
```
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=playlist_db
```

3. **Run**:
```bash
python run.py
```

API: http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs

## API Endpoints

### Playlists

**Create Playlist**
```
POST /api/v1/playlists
{
  "user_id": "user123",
  "device_id": "device_abc",
  "name": "My Rock Collection",
  "parent_id": null
}
```

**Get Playlists**
```
GET /api/v1/playlists?user_id=user123
GET /api/v1/playlists/{playlist_id}
```

**Delete Playlist**
```
DELETE /api/v1/playlists/{playlist_id}
```

### Songs

**Add Song to Playlist** (with audio file upload)
```
POST /api/v1/songs/add-to-playlist
Form Data:
- playlist_id: "playlist123"
- user_id: "user123"
- device_id: "device_abc"
- audio_file: (file upload)
- title: "Song Title"
- artist: "Artist Name" (optional)
- album: "Album Name" (optional)
- duration: 240 (optional, in seconds)
```

**Get Song**
```
GET /api/v1/songs/{song_id}
```

**Delete Song**
```
DELETE /api/v1/songs/{song_id}?playlist_id=playlist123
```

## Workflow Example

1. **User creates a playlist**:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/playlists \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","device_id":"device_abc","name":"Rock Music","parent_id":null}'
```

2. **User adds songs with audio files**:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/songs/add-to-playlist \
  -F "playlist_id=673abc..." \
  -F "user_id=user123" \
  -F "device_id=device_abc" \
  -F "audio_file=@song1.mp3" \
  -F "title=Rock Anthem" \
  -F "artist=Rock Band" \
  -F "duration=240"
```

3. **Create nested playlist** (child of first playlist):
```bash
curl -X POST http://127.0.0.1:8000/api/v1/playlists \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","device_id":"device_abc","name":"Classic Rock","parent_id":"673abc..."}'
```

4. **Get playlist with all songs**:
```bash
curl http://127.0.0.1:8000/api/v1/playlists/673abc...
```

## Data Structure

### Playlist Document
```json
{
  "_id": "673abc123...",
  "user_id": "user123",
  "device_id": "device_abc",
  "name": "My Rock Collection",
  "parent_id": null,
  "songs": [
    {
      "_id": "song_id_1",
      "title": "Rock Anthem",
      "artist": "Rock Band",
      "duration": 240,
      "file_url": "https://cdn.example.com/users/user123/audio/uuid.mp3",
      "file_size": 5242880,
      "created_at": "2024-01-01T12:00:00"
    }
  ],
  "created_at": "2024-01-01T10:00:00"
}
```

## Cloud Storage

Audio files are automatically uploaded to cloud storage (AWS S3, Google Cloud Storage, etc.).

**Current**: Simulates cloud storage with mock URLs
**Production**: Configure in `app/services/cloud_storage.py`

For AWS S3:
```python
# Set environment variables
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_BUCKET_NAME=your_bucket
```

## Collections

- **playlists**: Playlist metadata and song references
- **songs**: Song metadata and cloud URLs

## Tech Stack

- FastAPI - Modern async web framework
- MongoDB - Flexible document database
- Motor - Async MongoDB driver
- Pydantic - Data validation
- Boto3 - AWS SDK (for S3 integration)
