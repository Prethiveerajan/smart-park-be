# import os
# from fastapi import APIRouter, UploadFile, File
# from app.services import process_video_putils, process_video_utils, get_parking_status

# router = APIRouter()

# @router.get("/parking/status")
# async def get_parking_status_route():
#     available_count = get_parking_status()
#     return {"available_spaces": available_count}

# @router.get("/parking/status")
# async def get_parking_status_route():
#     available_count = get_parking_status()
#     return {"available_spaces": available_count}

# @router.post("/upload")
# async def upload_video(file: UploadFile = File(...)):
#     video_path = f"data/source/{file.filename}"
    
#     # Save the uploaded video
#     with open(video_path, "wb") as f:
#         f.write(await file.read())
    
#     # Determine which processing function to use based on the video name
#     if file.filename == "carPark.mp4":
#         process_video_putils(video_path)  # Use putils.py for carPark.mp4
#     else:
#         process_video_utils(video_path)    # Use utils.py for other videos
    
#     # Fetch the available spaces after processing
#     available_spaces = get_parking_status()
#     return {
#         "message": "Video uploaded and processed successfully",
#         "available_spaces": available_spaces
#     }

# @router.get("/parking/videos")
# async def get_videos():
#     video_folder = "data/source"
#     videos = [file for file in os.listdir(video_folder) if file.endswith(".mp4")]
#     return {"videos": videos}

# @router.get("/parking/select/{video_name}")
# async def select_parking(video_name: str):
#     video_path = f"data/source/{video_name}"
    
#     # Check if the file exists before processing
#     if os.path.exists(video_path):
#         # Determine which processing function to use based on the video name
#         if video_name == "carPark.mp4":
#             process_video_putils(video_path)  # Use putils.py for carPark.mp4
#         else:
#             process_video_utils(video_path)    # Use utils.py for other videos
        
#         # Fetch the available spaces after processing
#         available_count = get_parking_status()
#         return {"available_spaces": available_count}
#     else:
#         return {"error": "Video not found"}, 404



# app/routes.py

# import os
# from fastapi import APIRouter, UploadFile, File
# from app.services import process_video_putils, process_video_utils, get_parking_status

# router = APIRouter()

# @router.get("/parking/status")
# async def get_parking_status_route():
#     available_count = get_parking_status()
#     return {"available_spaces": available_count}

# @router.post("/upload")
# async def upload_video(file: UploadFile = File(...)):
#     video_path = f"data/source/{file.filename}"
    
#     # Save the uploaded video
#     with open(video_path, "wb") as f:
#         f.write(await file.read())
    
#     # Determine which processing function to use based on the video name
#     if file.filename == "carPark.mp4":
#         available_spaces = process_video_putils(video_path)  # Use putils.py for carPark.mp4
#     else:
#         available_spaces = process_video_utils(video_path)    # Use utils.py for other videos
    
#     # Return the available spaces after processing
#     return {
#         "message": "Video uploaded and processed successfully",
#         "available_spaces": available_spaces
#     }

# @router.get("/parking/videos")
# async def get_videos():
#     video_folder = "data/source"
#     videos = [file for file in os.listdir(video_folder) if file.endswith(".mp4")]
#     return {"videos": videos}

# @router.get("/parking/select/{video_name}")
# async def select_parking(video_name: str):
#     video_path = f"data/source/{video_name}"
    
#     # Check if the file exists before processing
#     if os.path.exists(video_path):
#         # Determine which processing function to use based on the video name
#         if video_name == "carPark.mp4":
#             available_count = process_video_putils(video_path)  # Use putils.py for carPark.mp4
#         else:
#             available_count = process_video_utils(video_path)    # Use utils.py for other videos
        
#         return {"available_spaces": available_count}
#     else:
#         return {"error": "Video not found"}, 404


# import os
# from fastapi import APIRouter, UploadFile, File
# from app.services import process_video_putils, process_video_utils, get_parking_status,get_space_utils

# router = APIRouter()

# @router.get("/parking/status")
# async def get_parking_status_route():
#     available_count = get_parking_status()
#     return {"available_spaces": available_count}

# @router.get("/parking/status2")
# async def get_space_utils():
#     available_count = get_space_utils()
#     return {"available_spaces": available_count}

# @router.post("/upload")
# async def upload_video(file: UploadFile = File(...)):
#     video_path = f"data/source/{file.filename}"
#     with open(video_path, "wb") as f:
#         f.write(await file.read())
#     if file.filename == "carPark.mp4":
#         process_video_putils(video_path)
#     else:
#         process_video_utils(video_path)
#     available_spaces = get_parking_status()
#     return {
#         "message": "Video uploaded and processed successfully",
#         "available_spaces": available_spaces
#     }

# @router.get("/parking/videos")
# async def get_videos():
#     video_folder = "data/source"
#     videos = [file for file in os.listdir(video_folder) if file.endswith(".mp4")]
#     return {"videos": videos}



# @router.get("/parking/select/{video_name}")
# async def select_parking(video_name: str):
#     video_path = f"data/source/{video_name}"
#     mask_path = f"./mask_1920_1080.png" 
#     if os.path.exists(video_path):
#         if video_name == "carPark.mp4":
#             process_video_putils(video_path,mask_path)
#         else:
#             process_video_utils(video_path)
#         available_count = get_parking_status()
#         return {"available_spaces": available_count}
#     else:
#         return {"error": "Video not found"}, 404


import os
from fastapi import APIRouter, UploadFile, File
from app.services import process_video_putils, process_video_utils, get_parking_status, get_space_utils

router = APIRouter()

@router.get("/parking/status")
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
        process_video_putils(video_path,mask_path)  # Make sure this function updates the available spaces count
    else:
        process_video_utils(video_path)  # Ensure this function also updates the count

    available_spaces = get_parking_status()  # Get the updated available spaces count
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
