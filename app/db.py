# from pymongo import MongoClient
# from pymongo.errors import ServerSelectionTimeoutError
# import logging
# from dotenv import load_dotenv
# import os
# logger = logging.getLogger(__name__)
# load_dotenv()
# # MongoDB connection string
# # MONGO_URI = "mongodb+srv://prethiveerajan40:MjfQ2Rnja0ZE7rsi@prethivee.wa4bjod.mongodb.net/"
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# def get_db_connection():
#     try:
#         # Connect to MongoDB using the URI
#         client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # Timeout after 5 seconds
        
#         # Test the connection
#         client.admin.command('ping')
#         logger.info("MongoDB connection successful")
        
#         # Access the specific database and collection
#         db = client["SmartParking"]  # Access the 'SmartParking' database
#         users_collection = db["Parking"]  # Access the 'Parking' collection
#         return users_collection  # You can return the collection or client if needed
#     except ServerSelectionTimeoutError as e:
#         logger.error(f"MongoDB connection failed: {e}")
#         raise e

# # Example usage (inside your backend function)
# users_collection = get_db_connection()  # Establish connection and get collection


from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import logging
from dotenv import load_dotenv
import os

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
        parking_collection = db["parking"]  # Collection for parking booking data
        
        return users_collection, parking_collection  # Return both collections
    except ServerSelectionTimeoutError as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise e

# Get the user and parking collections
users_collection, parking_collection = get_db_connection()
