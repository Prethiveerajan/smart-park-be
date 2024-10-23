# import os
# from app.putils import process_parking_video  # Adjust this import based on your function name
# from app.utils import ParkClassifier  # Import your ParkClassifier

# classifier = ParkClassifier()

# def process_video(video_path):
#     # Check if the selected video is 'carPark.mp4'
#     if os.path.basename(video_path) == "carPark.mp4":
#         process_video_putils(video_path)
#     else:
#         process_video_utils(video_path)

# def process_video_putils(video_path):
#     from app.putils import process_parking_video
#     mask_path = './mask_1920_1080.png'  # Define the mask path
#     process_parking_video(mask_path, video_path)  # Pass both mask_path and video_path

# def process_video_utils(video_path):
#     classifier.classify_video(video_path)  # Call the classify_video function from utils.py

# def get_parking_status():
#     # Return the latest count of available spaces
#     return classifier.get_available_spaces()


# app/services.py

# import os
# from app.putils import process_parking_video  # Adjust this import based on your function name
# from app.utils import ParkClassifier  # Import your ParkClassifier

# classifier = ParkClassifier()

# def process_video(video_path):
#     # Check if the selected video is 'carPark.mp4'
#     if os.path.basename(video_path) == "carPark.mp4":
#         return process_video_putils(video_path)  # Return the count of available spaces
#     else:
#         return process_video_utils(video_path)  # Adjust to return available space count

# def process_video_putils(video_path):
#     mask_path = './mask_1920_1080.png'  # Define the mask path
#     available_spaces = process_parking_video(mask_path, video_path)  # Pass both mask_path and video_path
#     return available_spaces  # Return the available spaces count

# def process_video_utils(video_path):
#     classifier.classify_video(video_path)  # Call the classify_video function from utils.py
#     return classifier.get_available_spaces()  # Return available spaces after classification

# def get_parking_status():
#     # Return the latest count of available spaces
#     return classifier.get_available_spaces()


# import os
# from app.putils import process_parking_video  # Ensure correct import
# from app.utils import ParkClassifier  # Import your ParkClassifier

# classifier = ParkClassifier()

# def process_video(video_path):
#     mask_path = './mask_1920_1080.png'  # Set your mask path here
#     if os.path.basename(video_path) == "carPark.mp4":
#         return process_video_putils(video_path, mask_path)
#     else:
#         return process_video_utils(video_path)

# def process_video_putils(video_path, mask_path):
#     from app.putils import process_parking_video
#     return process_parking_video(mask_path, video_path)

# def process_video_utils(video_path):
#     classifier.classify_video(video_path)

# def get_parking_status():
#     return classifier.get_available_spaces()  

# def get_space_utils():
#     return get_available_spaces()  # Update this to call the correct function


# services.py
import os
from app.putils import process_parking_video, get_available_spaces  # Ensure correct import
from app.utils import ParkClassifier  # Import your ParkClassifier

classifier = ParkClassifier()

def process_video(video_path):
    mask_path = './mask_1920_1080.png'  # Set your mask path here
    if os.path.basename(video_path) == "carPark.mp4":
        return process_video_putils(video_path, mask_path)
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
