from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from app.database import get_database
from app.schemas.playlist import PlaylistCreate, PlaylistResponse
from app.services.playlist_service import PlaylistService

router = APIRouter()

def get_playlist_service():
    db = get_database()
    return PlaylistService(db)

@router.post("/playlists", response_model=PlaylistResponse, status_code=201)
async def create_playlist(
    playlist: PlaylistCreate,
    service: PlaylistService = Depends(get_playlist_service)
):
    """
    Create a new playlist.
    
    Example:
    {
      "user_id": "user123",
      "device_id": "device_abc",
      "name": "My Rock Collection",
      "parent_id": null
    }
    
    To create a nested playlist, set parent_id to an existing playlist ID.
    """
    try:
        return await service.create_playlist(playlist)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/playlists", response_model=List[PlaylistResponse])
async def get_playlists(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    skip: int = 0,
    limit: int = 100,
    service: PlaylistService = Depends(get_playlist_service)
):
    """Get all playlists, optionally filtered by user"""
    if user_id:
        return await service.get_playlists_by_user(user_id, skip=skip, limit=limit)
    return await service.get_playlists(skip=skip, limit=limit)

@router.get("/playlists/{playlist_id}", response_model=PlaylistResponse)
async def get_playlist(
    playlist_id: str,
    service: PlaylistService = Depends(get_playlist_service)
):
    """Get a specific playlist with its songs"""
    playlist = await service.get_playlist(playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist

@router.delete("/playlists/{playlist_id}", status_code=200)
async def delete_playlist(
    playlist_id: str,
    service: PlaylistService = Depends(get_playlist_service)
):
    """Delete a playlist"""
    result = await service.delete_playlist(playlist_id)
    if not result:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return {"message": "Playlist deleted successfully"}
