# from pymongo import MongoClient

# client = MongoClient("mongodb+srv://prethiveerajan40:MjfQ2Rnja0ZE7rsi@prethivee.wa4bjod.mongodb.net/")
# db = client["SmartParking"]
# users_collection = db["Parking"]

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import logging

logger = logging.getLogger(__name__)

# MongoDB connection string
MONGO_URI = "mongodb+srv://prethiveerajan40:MjfQ2Rnja0ZE7rsi@prethivee.wa4bjod.mongodb.net/"

def get_db_connection():
    try:
        # Connect to MongoDB using the URI
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # Timeout after 5 seconds
        
        # Test the connection
        client.admin.command('ping')
        logger.info("MongoDB connection successful")
        
        # Access the specific database and collection
        db = client["SmartParking"]  # Access the 'SmartParking' database
        users_collection = db["Parking"]  # Access the 'Parking' collection
        return users_collection  # You can return the collection or client if needed
    except ServerSelectionTimeoutError as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise e

# Example usage (inside your backend function)
users_collection = get_db_connection()  # Establish connection and get collection
