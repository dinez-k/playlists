from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import Optional
from datetime import datetime

class SongService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["songs"]
        self.playlists_collection = db["playlists"]
    
    async def create_song_and_add_to_playlist(
        self,
        playlist_id: str,
        user_id: str,
        device_id: str,
        title: str,
        file_id: str,
        file_url: str,
        storage_path: str,
        file_size: int,
        original_filename: str,
        artist: Optional[str] = None,
        album: Optional[str] = None,
        duration: Optional[int] = None
    ) -> dict:
        """Create a song record and add it to a playlist"""
        
        # Verify playlist exists
        if not ObjectId.is_valid(playlist_id):
            raise ValueError("Invalid playlist_id")
        
        playlist = await self.playlists_collection.find_one({"_id": ObjectId(playlist_id)})
        if not playlist:
            raise ValueError("Playlist not found")
        
        # Create song document
        song_dict = {
            "user_id": user_id,
            "device_id": device_id,
            "title": title,
            "artist": artist,
            "album": album,
            "duration": duration,
            "file_id": file_id,
            "file_url": file_url,
            "storage_path": storage_path,
            "file_size": file_size,
            "original_filename": original_filename,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Insert song
        result = await self.collection.insert_one(song_dict)
        song_id = str(result.inserted_id)
        song_dict["_id"] = song_id
        
        # Add song to playlist
        await self.playlists_collection.update_one(
            {"_id": ObjectId(playlist_id)},
            {"$push": {"songs": song_dict}}
        )
        
        return song_dict
    
    async def get_song(self, song_id: str) -> Optional[dict]:
        """Get a song by ID"""
        if not ObjectId.is_valid(song_id):
            return None
        song = await self.collection.find_one({"_id": ObjectId(song_id)})
        if song:
            song["_id"] = str(song["_id"])
        return song
    
    async def remove_song_from_playlist(self, song_id: str, playlist_id: str) -> bool:
        """Remove a song from a playlist"""
        if not ObjectId.is_valid(playlist_id):
            return False
        
        result = await self.playlists_collection.update_one(
            {"_id": ObjectId(playlist_id)},
            {"$pull": {"songs": {"_id": song_id}}}
        )
        return result.modified_count > 0
    
    async def delete_song(self, song_id: str) -> bool:
        """Delete a song completely"""
        if not ObjectId.is_valid(song_id):
            return False
        
        # Remove from all playlists
        await self.playlists_collection.update_many(
            {},
            {"$pull": {"songs": {"_id": song_id}}}
        )
        
        # Delete song document
        result = await self.collection.delete_one({"_id": ObjectId(song_id)})
        return result.deleted_count > 0
