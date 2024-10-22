# import os

# from fastapi import APIRouter, UploadFile, File
# from app.services import process_video, get_parking_status

# router = APIRouter()

# @router.get("/parking/status")
# async def get_parking_status_route():
#     available_count = get_parking_status()
#     return {"available_spaces": available_count}

# @router.post("/upload")
# async def upload_video(file: UploadFile = File(...)):
#     video_path = f"data/source/{file.filename}"
#     with open(video_path, "wb") as f:
#         f.write(await file.read())
#     process_video(video_path)
#     return {"message": "Video uploaded and processed successfully"}


# @router.get("/parking/videos")
# async def get_videos():
#     video_folder = "data/source"
#     videos = [file for file in os.listdir(video_folder) if file.endswith(".mp4")]
#     return {"videos": videos}

# @router.get("/parking/select/{video_name}")
# async def select_parking(video_name: str):
#     video_path = f"data/source/{video_name}"
#     process_video(video_path)  # Process the video
#     available_count = get_parking_status()
#     return {"available_spaces": available_count}


import os
from fastapi import APIRouter, UploadFile, File
from app.services import process_video, get_parking_status

router = APIRouter()

@router.get("/parking/status")
async def get_parking_status_route():
    available_count = get_parking_status()
    return {"available_spaces": available_count}

@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    video_path = f"data/source/{file.filename}"
    
    # Save the uploaded video
    with open(video_path, "wb") as f:
        f.write(await file.read())
    
    # Process the video for available parking spaces
    process_video(video_path)
    
    # Fetch the available spaces after processing
    available_spaces = get_parking_status()
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
    
    # Process the selected video for available parking spaces
    process_video(video_path)
    
    # Fetch the available spaces after processing
    available_count = get_parking_status()
    return {"available_spaces": available_count}
