from pydantic import BaseModel, Field
from typing import Optional, List

class PlaylistBase(BaseModel):
    user_id: str
    device_id: str
    name: str
    parent_id: Optional[str] = None

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    device_id: str
    name: str
    parent_id: Optional[str] = None
    songs: List[dict] = []
    created_at: Optional[str] = None
    
    class Config:
        populate_by_name = True
        from_attributes = True
