# services.py
import os
from fastapi import BackgroundTasks
from app.putils import process_parking_video, get_available_spaces  # Ensure correct import
from app.utils import ParkClassifier  # Import your ParkClassifier
from app.db import users_collection
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client
import re
from dotenv import load_dotenv


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
    users_collection.insert_one(booking_data)
    
    # Send SMS notification to the contact number provided
    send_sms(contact, user_name)
    
    # Send email notification to the user's email address
    send_email(email, user_name, booking_data)
    
    return "Booking saved successfully, and notifications sent (SMS and Email)"