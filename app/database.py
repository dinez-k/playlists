from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    
mongodb = MongoDB()

async def connect_to_mongo():
    mongodb.client = AsyncIOMotorClient(settings.mongodb_url)
    print(f"Connected to MongoDB at {settings.mongodb_url}")

async def close_mongo_connection():
    mongodb.client.close()
    print("Closed MongoDB connection")

def get_database():
    return mongodb.client[settings.mongodb_db_name]
