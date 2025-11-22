from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Query
from typing import Optional
from app.database import get_database
from app.schemas.song import SongResponse
from app.services.song_service import SongService
from app.services.cloud_storage import CloudStorageService

router = APIRouter()

def get_song_service():
    db = get_database()
    return SongService(db)

def get_cloud_storage():
    return CloudStorageService()

@router.post("/songs/add-to-playlist", response_model=SongResponse, status_code=201)
async def add_song_to_playlist(
    playlist_id: str = Form(...),
    user_id: str = Form(...),
    device_id: str = Form(...),
    audio_file: UploadFile = File(...),
    title: str = Form(...),
    artist: Optional[str] = Form(None),
    album: Optional[str] = Form(None),
    duration: Optional[int] = Form(None),
    song_service: SongService = Depends(get_song_service),
    cloud_storage: CloudStorageService = Depends(get_cloud_storage)
):
    """
    Add a song to a playlist by uploading audio file.
    
    This endpoint:
    1. Receives audio file from mobile
    2. Uploads to cloud storage (S3/GCS)
    3. Creates song record with cloud URL
    4. Adds song to specified playlist
    
    Form Data:
    - playlist_id: Playlist to add song to
    - user_id: User identifier
    - device_id: Device identifier
    - audio_file: Audio file (mp3, wav, etc.)
    - title: Song title
    - artist: Artist name (optional)
    - album: Album name (optional)
    - duration: Duration in seconds (optional)
    """
    try:
        # Upload audio file to cloud storage
        upload_result = await cloud_storage.upload_audio_file(audio_file, user_id)
        
        # Create song record
        song = await song_service.create_song_and_add_to_playlist(
            playlist_id=playlist_id,
            user_id=user_id,
            device_id=device_id,
            title=title,
            artist=artist,
            album=album,
            duration=duration,
            file_id=upload_result["file_id"],
            file_url=upload_result["file_url"],
            storage_path=upload_result["storage_path"],
            file_size=upload_result["file_size"],
            original_filename=upload_result["original_filename"]
        )
        
        return song
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/songs/{song_id}", response_model=SongResponse)
async def get_song(
    song_id: str,
    service: SongService = Depends(get_song_service)
):
    """Get a specific song by ID"""
    song = await service.get_song(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@router.delete("/songs/{song_id}", status_code=200)
async def delete_song(
    song_id: str,
    playlist_id: Optional[str] = Query(None, description="Remove from specific playlist"),
    service: SongService = Depends(get_song_service)
):
    """
    Delete a song or remove it from a playlist.
    - If playlist_id is provided: removes song from that playlist only
    - If playlist_id is not provided: deletes song completely
    """
    if playlist_id:
        result = await service.remove_song_from_playlist(song_id, playlist_id)
        if not result:
            raise HTTPException(status_code=404, detail="Song or playlist not found")
        return {"message": "Song removed from playlist", "song_id": song_id, "playlist_id": playlist_id}
    else:
        result = await service.delete_song(song_id)
        if not result:
            raise HTTPException(status_code=404, detail="Song not found")
        return {"message": "Song deleted successfully", "song_id": song_id}
