from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import playlist, song
from app.database import connect_to_mongo, close_mongo_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="Playlist API",
    description="A scalable API for managing playlists and songs with MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(playlist.router, prefix="/api/v1", tags=["playlists"])
app.include_router(song.router, prefix="/api/v1", tags=["songs"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Playlist API with MongoDB"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "mongodb"}
