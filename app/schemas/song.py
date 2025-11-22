from pydantic import BaseModel, Field
from typing import Optional

class SongBase(BaseModel):
    title: str
    artist: Optional[str] = None
    album: Optional[str] = None
    duration: Optional[int] = None
    file_url: str
    user_id: str

class SongCreate(SongBase):
    pass

class SongResponse(SongBase):
    id: str = Field(alias="_id")
    
    class Config:
        populate_by_name = True
        from_attributes = True

class SongUpload(BaseModel):
    title: str
    artist: Optional[str] = None
    album: Optional[str] = None
    duration: Optional[int] = None
    user_id: str
