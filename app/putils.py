# # putils.py
# import os
# import cv2
# import numpy as np
# from skimage.transform import resize
# import pickle

# # Constants for empty and non-empty parking spot statuses
# EMPTY = True
# NOT_EMPTY = False

# # Load the pre-trained model for ParkClassifier
# MODEL = pickle.load(open("model.p", "rb"))

# # Variable to store the count of available spaces
# available_spaces_count = 0  # Initialize a global variable to maintain the count

# def calc_diff(im1, im2):
#     """Calculate the absolute difference between the average pixel values of two images."""
#     return np.abs(np.mean(im1) - np.mean(im2))

# def empty_or_not(spot_bgr):
#     """Determine if a parking spot is empty or not."""
#     img_resized = resize(spot_bgr, (15, 15, 3))  # Resize the image to 15x15x3
#     flat_data = img_resized.flatten().reshape(1, -1)  # Flatten and reshape for prediction
#     y_output = MODEL.predict(flat_data)  # Predict using the trained model
#     return EMPTY if y_output == 0 else NOT_EMPTY

# def get_parking_spots_bboxes(connected_components):
#     """Extract parking spot bounding boxes from connected components."""
#     (total_labels, _, values, _) = connected_components
#     slots = []
#     for i in range(1, total_labels):
#         x1 = int(values[i, cv2.CC_STAT_LEFT])
#         y1 = int(values[i, cv2.CC_STAT_TOP])
#         w = int(values[i, cv2.CC_STAT_WIDTH])
#         h = int(values[i, cv2.CC_STAT_HEIGHT])
#         slots.append((x1, y1, w, h))  # Append each bounding box to the slots list
#     return slots

# def get_available_spaces():
#     """Get the current count of available parking spaces."""
#     return available_spaces_count

# def process_parking_video(mask_path, video_path):
#     """Process the parking video and update the available spaces count."""
#     global available_spaces_count  # Use the global variable

#     # Load the mask image in grayscale
#     mask = cv2.imread(mask_path, 0)

#     # Capture the video
#     cap = cv2.VideoCapture(video_path)

#     # Get connected components from the mask to identify parking spots
#     connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)

#     # Get bounding boxes for the parking spots
#     spots = get_parking_spots_bboxes(connected_components)

#     # Initialize lists for parking spot status
#     spots_status = [None for _ in spots]
    
#     previous_frame = None  # Previous frame for comparison
#     frame_nmr = 0  # Frame number
#     step = 30  # Step for frame skipping to reduce computation

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         if frame_nmr % step == 0:
#             if previous_frame is not None:
#                 for spot_indx, spot in enumerate(spots):
#                     x1, y1, w, h = spot
#                     spot_crop = frame[y1:y1 + h, x1:x1 + w]
#                     spot_status = empty_or_not(spot_crop)
#                     spots_status[spot_indx] = spot_status

#         if frame_nmr % step == 0:
#             previous_frame = frame.copy()

#         # Update the count of available spaces
#         available_spaces_count = sum(status is EMPTY for status in spots_status if status is not None)
#         print(f'Available free spots: {available_spaces_count}')  # Log available spaces count

#     cap.release()
#     cv2.destroyAllWindows()
    
#     # Return the count of available spaces
#     return available_spaces_count

# # Call the process_parking_video function with appropriate paths
# if __name__ == "__main__":
#     mask_path = './mask_1920_1080.png'
#     video_path = os.path.join('data', 'source', 'carPark.mp4')
#     available_spaces = process_parking_video(mask_path, video_path)
#     print(f"Total available spaces: {available_spaces}")


import os
import cv2
import numpy as np
from skimage.transform import resize
import pickle

EMPTY = True
NOT_EMPTY = False
MODEL = pickle.load(open("model.p", "rb"))
available_spaces_count = 0  # Initialize a global variable to maintain the count

def empty_or_not(spot_bgr):
    img_resized = resize(spot_bgr, (15, 15, 3))
    flat_data = img_resized.flatten().reshape(1, -1)
    y_output = MODEL.predict(flat_data)
    return EMPTY if y_output == 0 else NOT_EMPTY

def get_parking_spots_bboxes(connected_components):
    (total_labels, _, values, _) = connected_components
    slots = []
    for i in range(1, total_labels):
        x1 = int(values[i, cv2.CC_STAT_LEFT])
        y1 = int(values[i, cv2.CC_STAT_TOP])
        w = int(values[i, cv2.CC_STAT_WIDTH])
        h = int(values[i, cv2.CC_STAT_HEIGHT])
        slots.append((x1, y1, w, h))
    return slots
def get_available_spaces():
    """Get the current count of available parking spaces."""
    return available_spaces_count
def process_parking_video(mask_path, video_path):
    global available_spaces_count
    mask = cv2.imread(mask_path, 0)
    cap = cv2.VideoCapture(video_path)
    connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
    spots = get_parking_spots_bboxes(connected_components)
    spots_status = [None for _ in spots]

    # Analyze the first frame
    ret, frame = cap.read()
    if ret:
        for spot_indx, spot in enumerate(spots):
            x1, y1, w, h = spot
            spot_crop = frame[y1:y1 + h, x1:x1 + w]
            spot_status = empty_or_not(spot_crop)
            spots_status[spot_indx] = spot_status

        available_spaces_count = sum(status is EMPTY for status in spots_status if status is not None)
        print(f'Available free spots at start: {available_spaces_count}')

    # Jump to the last frame of the video
    cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1)
    ret, frame = cap.read()
    if ret:
        spots_status = [None for _ in spots]  # Reset status for fresh count
        for spot_indx, spot in enumerate(spots):
            x1, y1, w, h = spot
            spot_crop = frame[y1:y1 + h, x1:x1 + w]
            spot_status = empty_or_not(spot_crop)
            spots_status[spot_indx] = spot_status

        available_spaces_count = sum(status is EMPTY for status in spots_status if status is not None)
        print(f'Available free spots at end: {available_spaces_count}')

    cap.release()
    cv2.destroyAllWindows()
    return available_spaces_count

# Main call for testing
if __name__ == "__main__":
    mask_path = './mask_1920_1080.png'
    video_path = os.path.join('data', 'source', 'carPark.mp4')
    available_spaces = process_parking_video(mask_path, video_path)
    print(f"Total available spaces at end: {available_spaces}")
