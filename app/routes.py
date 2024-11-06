import os
import asyncio
from fastapi import WebSocket
from fastapi import APIRouter, UploadFile, File
from sse_starlette.sse import EventSourceResponse
from app.services import process_video_putils, process_video_utils, get_parking_status, get_space_utils

router = APIRouter()


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

# @router.post("/upload")
# async def upload_video(file: UploadFile = File(...)):
#     video_path = f"data/source/{file.filename}"
#     mask_path = f"./mask_1920_1080.png" 
#     with open(video_path, "wb") as f:
#         f.write(await file.read())
    
#     if file.filename == "carPark.mp4":
#         process_video_putils(video_path,mask_path)  # Make sure this function updates the available spaces count
#     else:
#         process_video_utils(video_path)  # Ensure this function also updates the count

#     available_spaces = get_parking_status()  # Get the updated available spaces count
#     return {
#         "message": "Video uploaded and processed successfully",
#         "available_spaces": available_spaces
#     }

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



