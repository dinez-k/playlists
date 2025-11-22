from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List, Optional
from datetime import datetime
from app.schemas.playlist import PlaylistCreate

class PlaylistService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["playlists"]
    
    async def create_playlist(self, playlist: PlaylistCreate) -> dict:
        """Create a simple playlist"""
        playlist_dict = playlist.model_dump()
        
        # Validate parent_id if provided
        if playlist_dict.get("parent_id"):
            if not ObjectId.is_valid(playlist_dict["parent_id"]):
                raise ValueError("Invalid parent_id")
            parent = await self.collection.find_one({"_id": ObjectId(playlist_dict["parent_id"])})
            if not parent:
                raise ValueError("Parent playlist not found")
        
        # Initialize empty songs list and add timestamp
        playlist_dict["songs"] = []
        playlist_dict["created_at"] = datetime.utcnow().isoformat()
        
        result = await self.collection.insert_one(playlist_dict)
        playlist_dict["_id"] = str(result.inserted_id)
        return playlist_dict
    
    async def get_playlist(self, playlist_id: str) -> Optional[dict]:
        """Get a playlist by ID"""
        if not ObjectId.is_valid(playlist_id):
            return None
        playlist = await self.collection.find_one({"_id": ObjectId(playlist_id)})
        if playlist:
            playlist["_id"] = str(playlist["_id"])
        return playlist
    
    async def get_playlists(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all playlists"""
        playlists = []
        cursor = self.collection.find().skip(skip).limit(limit)
        async for playlist in cursor:
            playlist["_id"] = str(playlist["_id"])
            playlists.append(playlist)
        return playlists
    
    async def get_playlists_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all playlists for a user"""
        playlists = []
        cursor = self.collection.find({"user_id": user_id}).skip(skip).limit(limit)
        async for playlist in cursor:
            playlist["_id"] = str(playlist["_id"])
            playlists.append(playlist)
        return playlists
    
    async def delete_playlist(self, playlist_id: str) -> bool:
        """Delete a playlist"""
        if not ObjectId.is_valid(playlist_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(playlist_id)})
        return result.deleted_count > 0
