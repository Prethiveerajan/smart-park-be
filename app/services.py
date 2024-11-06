# services.py
import os
from fastapi import BackgroundTasks
from app.putils import process_parking_video, get_available_spaces  # Ensure correct import
from app.utils import ParkClassifier  # Import your ParkClassifier
from app.db import users_collection
import logging

logger = logging.getLogger(__name__)
classifier = ParkClassifier()

def process_video(video_path,background_tasks: BackgroundTasks):
    mask_path = './mask_1920_1080.png'  # Set your mask path here
    if os.path.basename(video_path) == "carPark.mp4":
        # return process_video_putils(video_path, mask_path)
        background_tasks.add_task(process_parking_video, mask_path, video_path)
    else:
        return process_video_utils(video_path)

def process_video_putils(video_path, mask_path):
    from app.putils import process_parking_video
    return process_parking_video(mask_path, video_path)

def process_video_utils(video_path):
    classifier.classify_video(video_path)

def get_parking_status():
    return classifier.get_available_spaces()  

def get_space_utils():
    return get_available_spaces()  # Call the correct function to get available spaces

def book_parking_space(parking_id, user_name, contact, user_id):
    booking_data = {
        "parking_id": parking_id,
        "user_name": user_name,
        "contact": contact,
        "user_id": user_id,
        "status": "occupied"
    }
    # Insert booking data into MongoDB
    users_collection.insert_one(booking_data)
    # Optionally, you can retrieve the updated available spaces count if needed
    return "Booking saved successfully"