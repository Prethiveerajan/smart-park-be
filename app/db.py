from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import logging
from dotenv import load_dotenv
import os
import bcrypt
logger = logging.getLogger(__name__)
load_dotenv()

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

def get_db_connection():
    try:
        # Connect to MongoDB using the URI
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # Timeout after 5 seconds
        
        # Test the connection
        client.admin.command('ping')
        logger.info("MongoDB connection successful")
        
        # Access the specific database
        db = client["SmartParking"]

        # Define separate collections
        users_collection = db["userdata"]   # Collection for user-related data
        parking_collection = db["Parking"]  # Collection for parking booking data
        
        return users_collection, parking_collection  # Return both collections
    except ServerSelectionTimeoutError as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise e

# Get the user and parking collections
users_collection, parking_collection = get_db_connection()
