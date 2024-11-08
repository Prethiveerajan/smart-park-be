import os
import asyncio
from fastapi import WebSocket
from fastapi import UploadFile, File
from sse_starlette.sse import EventSourceResponse
from app.services import process_video_putils, process_video_utils, get_parking_status, get_space_utils
import logging
import jwt,random
from fastapi import HTTPException
from app.services import book_parking_space
from app.services import register_user, authenticate_user
from fastapi import Depends
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from app.models import BookingRequest, UserRegisterRequest, LoginRequest
from app.services import register_user, authenticate_user, reset_password,generate_reset_code_token
from app.db import users_collection, parking_collection
import smtplib
import bcrypt
from app.config import SECRET_KEY

router = APIRouter()
# router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

class PasswordResetRequest(BaseModel):
    email: str
    new_password: str

class PasswordResetVerifyRequest(BaseModel):
    token: str
    reset_code: int
    new_password: str

# Define a schema for the email request
class EmailRequest(BaseModel):
    email: str


@router.get("/parking/status1")
async def get_parking_status_route():
    available_count = get_parking_status()
    return {"available_spaces": available_count}

@router.get("/parking/status2")
async def get_space_utils_route():
    available_count = get_space_utils()  # Ensure this function is correctly implemented in services.py
    return {"available_spaces": available_count}


@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    video_path = f"data/source/{file.filename}"
    mask_path = f"./mask_1920_1080.png" 
    with open(video_path, "wb") as f:
        f.write(await file.read())
    
    if file.filename == "carPark.mp4":
        process_video_putils(video_path, mask_path)
        available_spaces  = get_space_utils()
    else:
        process_video_utils(video_path)
        available_spaces = get_parking_status()

    
    
    print(f"Available spaces after processing {file.filename}: {available_spaces}")  # Debugging line

    return {
        "message": "Video uploaded and processed successfully",
        "available_spaces": available_spaces
    }


@router.get("/parking/videos")
async def get_videos():
    video_folder = "data/source"
    videos = [file for file in os.listdir(video_folder) if file.endswith(".mp4")]
    return {"videos": videos}

@router.get("/parking/select/{video_name}")
async def select_parking(video_name: str):
    video_path = f"data/source/{video_name}"
    mask_path = f"./mask_1920_1080.png"
    if os.path.exists(video_path):
        if video_name == "carPark.mp4":
            process_video_putils(video_path, mask_path)  # Ensure this function updates the available spaces
        else:
            process_video_utils(video_path)  # Ensure this function updates the available spaces

        available_count = get_parking_status()  # Get the updated available spaces count
        return {"available_spaces": available_count}
    else:
        return {"error": "Video not found"}, 404


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@router.post("/booking")
async def book_parking(booking_request: BookingRequest):
    logger.info(f"Received booking request: {booking_request}")
    try:
        # Extract data from the Pydantic model
        parking_id = booking_request.parking_id
        user_name = booking_request.user_name
        contact = booking_request.contact
        email = booking_request.email
        user_id = booking_request.user_id

        # Call the function to store booking data and send SMS
        booking_message = book_parking_space(parking_id, user_name, contact, email, user_id)
        logger.info(f"Booking successful: {booking_message}")
        return {"message": booking_message}
    except Exception as e:
        logger.error(f"Error during booking: {e}")
        raise HTTPException(status_code=500, detail="Booking failed") from e
    

@router.post("/register")
async def register_user_route(user: UserRegisterRequest):
    try:
        register_user(user)
        return {"message": "User registered successfully!"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

# User login endpoint
@router.post("/login")
async def login_user_route(login_data: LoginRequest):
    try:
        response = authenticate_user(login_data.email, login_data.password)
        return response  # Return a token or user details as needed
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@router.post("/forgot-password/verify")
async def verify_reset_code_and_reset_password(request: PasswordResetVerifyRequest):
    try:
        # Decode and validate the JWT token
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=["HS256"])
        email = payload["sub"]
        code_from_token = payload["reset_code"]

        # Check if the code matches
        if request.reset_code != code_from_token:
            raise HTTPException(status_code=400, detail="Invalid reset code")

        # Reset the password
        hashed_password = bcrypt.hashpw(request.new_password.encode("utf-8"), bcrypt.gensalt())
        users_collection.update_one({"email": email}, {"$set": {"password": hashed_password}})

        return {"message": "Password reset successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Reset code has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    except Exception as e:
        logger.error(f"Password reset failed: {e}")
        raise HTTPException(status_code=500, detail="Password reset failed")


@router.post("/forgot-password/request")
async def request_password_reset(request: EmailRequest):
    email = request.email  # Extract the email from the request object
    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a reset code token and send it via email
    token = generate_reset_code_token(email)
    return {"message": "Password reset code sent", "token": token}