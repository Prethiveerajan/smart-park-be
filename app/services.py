# services.py
import os
from fastapi import BackgroundTasks
from app.putils import process_parking_video, get_available_spaces  # Ensure correct import
from app.utils import ParkClassifier  # Import your ParkClassifier
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client
import re
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import jwt,random
from datetime import datetime, timedelta
import bcrypt
from fastapi import HTTPException
from app.models import UserRegisterRequest
from typing import Optional
from app.db import users_collection, parking_collection
import smtplib

from app.config import SECRET_KEY


# Load environment variables from .env file
load_dotenv()

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




# Access environment variables
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
twilio_client = Client(account_sid, auth_token)
messaging_service_sid = os.getenv('MESSAGING_SERVICE_SID')

# SMTP settings
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = int(os.getenv('SMTP_PORT'))
smtp_user = os.getenv('SMTP_USER')
smtp_password = os.getenv('SMTP_PASSWORD')
# SECRET_KEY = os.getenv('SECRET_KEY')



def format_contact_number(contact):
    """Ensure the contact number is in E.164 format, adding country code if missing."""
    if not contact.startswith('+'):
        # Assuming India (+91) as the default; change if needed or make configurable
        contact = '+91' + contact
    return contact

def send_sms(to_number, user_name):
    """Send SMS using Twilio API to notify user of successful booking."""
    try:
        to_number = format_contact_number(to_number)
        message = twilio_client.messages.create(
            messaging_service_sid=messaging_service_sid,
            to=to_number,
            body=f"Hello {user_name}, your parking space has been successfully booked!"
        )
        logging.info(f"SMS sent to {to_number}: {message.sid}")
    except Exception as e:
        logging.error(f"Failed to send SMS: {e}")

def send_email(to_email, user_name, booking_data):
    """Send email notification to the user regarding their booking."""
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = 'Parking Space Booking Confirmation'
        
        body = f"""
        Hello {user_name},

        Your booking for parking space ID {booking_data['parking_id']} has been successfully confirmed.
        
        Details:
        - Parking ID: {booking_data['parking_id']}
        - User ID: {booking_data['user_id']}
        - Status: {booking_data['status']}
        
        Thank you for choosing our service!
        """
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        
        logging.info(f"Email sent to {to_email}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def book_parking_space(parking_id, user_name, contact, email, user_id):
    """Save booking to MongoDB, send an SMS, and send an email to the user."""
    booking_data = {
        "parking_id": parking_id,
        "user_name": user_name,
        "contact": contact,
        "email": email,
        "user_id": user_id,
        "status": "occupied"
    }
    # Insert booking data into MongoDB
    parking_collection.insert_one(booking_data)
    
    # Send SMS notification to the contact number provided
    send_sms(contact, user_name)
    
    # Send email notification to the user's email address
    send_email(email, user_name, booking_data)
    
    return "Booking saved successfully, and notifications sent (SMS and Email)"


def register_user(user: UserRegisterRequest):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    users_collection.insert_one({
        "email": user.email,
        "password": hashed_password,
        "full_name": user.full_name
    })
    return {"message": "User registered successfully"}

# Function to authenticate user (login)
def authenticate_user(email: str, password: str):
    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Check if the password matches
    if not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return {"message": "User authenticated successfully"}

# Function to reset the password
def reset_password(email: str, new_password: str):
    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    
    users_collection.update_one({"email": email}, {"$set": {"password": hashed_password}})
    
    return {"message": "Password reset successfully"}



  # Set a strong secret key in your environment variables

def generate_reset_code_token(email: str) -> str:
    reset_code = random.randint(100000, 999999)  # Generate a 6-digit reset code
    expiration = datetime.utcnow() + timedelta(minutes=10)  # Token expires in 10 minutes

    token_data = {
        "sub": email,
        "reset_code": reset_code,
        "exp": expiration,
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")

    # Send the reset code to the user's email
    send_reset_code_email(email, reset_code)

    return token

def send_reset_code_email(to_email: str, reset_code: int):
    """Function to send the reset code to the user's email."""
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = 'Your Password Reset Code'
        
        body = f"Hello,\n\nYour password reset code is: {reset_code}\n\nThe code is valid for 10 minutes."
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        
        logging.info(f"Reset code email sent to {to_email}")
    except Exception as e:
        logging.error(f"Failed to send reset code email: {e}")