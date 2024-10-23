# # app/putils.py

# import cv2
# import numpy as np
# from skimage.transform import resize
# import pickle

# # Constants for empty and non-empty parking spot statuses
# EMPTY = True
# NOT_EMPTY = False

# # Load the pre-trained model for ParkClassifier
# MODEL = pickle.load(open("model.p", "rb"))

# def calc_diff(im1, im2):
#     """
#     Calculate the absolute difference between the average pixel values of two images.
    
#     Parameters:
#     - im1: First image (numpy array).
#     - im2: Second image (numpy array).

#     Returns:
#     - float: The difference value.
#     """
#     return np.abs(np.mean(im1) - np.mean(im2))

# def empty_or_not(spot_bgr):
#     """
#     Determine if a parking spot is empty or not.

#     Parameters:
#     - spot_bgr: Image of the parking spot in BGR format.

#     Returns:
#     - bool: True if the spot is empty, False otherwise.
#     """
#     img_resized = resize(spot_bgr, (15, 15, 3))  # Resize the image to 15x15x3
#     flat_data = img_resized.flatten().reshape(1, -1)  # Flatten and reshape for prediction
#     y_output = MODEL.predict(flat_data)  # Predict using the trained model
#     return EMPTY if y_output == 0 else NOT_EMPTY

# def get_parking_spots_bboxes(connected_components):
#     """
#     Extract parking spot bounding boxes from connected components.

#     Parameters:
#     - connected_components: Connected components output from OpenCV.

#     Returns:
#     - list: List of bounding boxes for parking spots.
#     """
#     (total_labels, _, values, _) = connected_components
#     slots = []
#     for i in range(1, total_labels):
#         x1 = int(values[i, cv2.CC_STAT_LEFT])
#         y1 = int(values[i, cv2.CC_STAT_TOP])
#         w = int(values[i, cv2.CC_STAT_WIDTH])
#         h = int(values[i, cv2.CC_STAT_HEIGHT])
#         slots.append((x1, y1, w, h))  # Append each bounding box to the slots list
#     return slots


# def process_parking_video(mask_path, video_path):
#     """
#     Process the video to detect parking spaces and display their status.

#     Parameters:
#     - mask_path: Path to the mask image defining parking spots.
#     - video_path: Path to the video file to be processed.
#     """
#     # Load the mask image in grayscale
#     mask = cv2.imread(mask_path, 0)

#     # Capture the video
#     cap = cv2.VideoCapture(video_path)

#     # Get connected components from the mask to identify parking spots
#     connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)

#     # Get bounding boxes for the parking spots
#     spots = get_parking_spots_bboxes(connected_components)

#     # Initialize lists for parking spot status and frame differences
#     spots_status = [None for _ in spots]
#     diffs = [None for _ in spots]

#     previous_frame = None  # Previous frame for comparison
#     frame_nmr = 0  # Frame number
#     step = 30  # Step for frame skipping to reduce computation

#     # Main loop for processing the video
#     while True:
#         ret, frame = cap.read()  # Read a frame from the video

#         if not ret:
#             break  # Exit if no more frames are available

#         if frame_nmr % step == 0:
#             if previous_frame is not None:
#                 # Calculate the difference between the current and previous frames for each spot
#                 for spot_indx, spot in enumerate(spots):
#                     x1, y1, w, h = spot
#                     spot_crop = frame[y1:y1 + h, x1:x1 + w]  # Crop the current spot from the frame
#                     diffs[spot_indx] = calc_diff(previous_frame[y1:y1 + h, x1:x1 + w], spot_crop)  # Calculate the difference

#             # Update the parking spot status based on differences
#             arr_ = range(len(spots)) if previous_frame is None else [j for j in np.argsort(diffs) if diffs[j] / np.amax(diffs) > 0.4]
#             for spot_indx in arr_:
#                 spot = spots[spot_indx]
#                 x1, y1, w, h = spot
#                 spot_crop = frame[y1:y1 + h, x1:x1 + w]  # Crop the current spot from the frame
#                 spot_status = empty_or_not(spot_crop)  # Predict if spot is empty or not
#                 spots_status[spot_indx] = spot_status  # Update the status

#         if frame_nmr % step == 0:
#             previous_frame = frame.copy()  # Save the current frame as previous

#         # Draw rectangles on the frame depending on spot status (green for available, red for occupied)
#         for spot_indx, spot in enumerate(spots):
#             spot_status = spots_status[spot_indx]
#             x1, y1, w, h = spot
#             color = (0, 255, 0) if spot_status == EMPTY else (0, 0, 255)  # Green if available, Red if not
#             frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), color, 2)

#         # Display the number of available spots in the video
#         cv2.rectangle(frame, (80, 20), (550, 80), (0, 0, 0), -1)
#         cv2.putText(frame, f'Available spots: {sum(status is EMPTY for status in spots_status)} / {len(spots_status)}',
#                     (100, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

#         # Show the frame in a window
#         cv2.namedWindow('Parking Spot Detector', cv2.WINDOW_NORMAL)
#         cv2.imshow('Parking Spot Detector', frame)

#         # Exit the video when 'q' is pressed
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             break

#         # Increment frame number
#         frame_nmr += 1

#         # Print the available spots count in the terminal
#         print(f'Available free spots: {sum(status is EMPTY for status in spots_status)}')

#     # Release video capture and close all OpenCV windows
#     cap.release()
#     cv2.destroyAllWindows()

# # Call the process_parking_video function with appropriate paths
# if __name__ == "__main__":
#     mask_path = './mask_1920_1080.png'
#     video_path = os.path.join('data', 'source', 'carPark.mp4')

#     process_parking_video(mask_path, video_path)





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

#     # Initialize lists for parking spot status and frame differences
#     spots_status = [None for _ in spots]
#     diffs = [None for _ in spots]

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
#                     diffs[spot_indx] = calc_diff(previous_frame[y1:y1 + h, x1:x1 + w], spot_crop)

#             arr_ = range(len(spots)) if previous_frame is None else [j for j in np.argsort(diffs) if diffs[j] / np.amax(diffs) > 0.4]
#             for spot_indx in arr_:
#                 spot = spots[spot_indx]
#                 x1, y1, w, h = spot
#                 spot_crop = frame[y1:y1 + h, x1:x1 + w]
#                 spot_status = empty_or_not(spot_crop)
#                 spots_status[spot_indx] = spot_status

#         if frame_nmr % step == 0:
#             previous_frame = frame.copy()

#         # Draw rectangles on the frame
#         for spot_indx, spot in enumerate(spots):
#             spot_status = spots_status[spot_indx]
#             x1, y1, w, h = spot
#             color = (0, 255, 0) if spot_status == EMPTY else (0, 0, 255)
#             frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), color, 2)

#         if frame_nmr % step == 0:
#             available_spaces_count = sum(status is EMPTY for status in spots_status)  # Update the count
#             print(f'Available free spots: {available_spaces_count}')  # Log available spaces count

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



# putils.py
import os
import cv2
import numpy as np
from skimage.transform import resize
import pickle

# Constants for empty and non-empty parking spot statuses
EMPTY = True
NOT_EMPTY = False

# Load the pre-trained model for ParkClassifier
MODEL = pickle.load(open("model.p", "rb"))

# Variable to store the count of available spaces
available_spaces_count = 0  # Initialize a global variable to maintain the count

def calc_diff(im1, im2):
    """Calculate the absolute difference between the average pixel values of two images."""
    return np.abs(np.mean(im1) - np.mean(im2))

def empty_or_not(spot_bgr):
    """Determine if a parking spot is empty or not."""
    img_resized = resize(spot_bgr, (15, 15, 3))  # Resize the image to 15x15x3
    flat_data = img_resized.flatten().reshape(1, -1)  # Flatten and reshape for prediction
    y_output = MODEL.predict(flat_data)  # Predict using the trained model
    return EMPTY if y_output == 0 else NOT_EMPTY

def get_parking_spots_bboxes(connected_components):
    """Extract parking spot bounding boxes from connected components."""
    (total_labels, _, values, _) = connected_components
    slots = []
    for i in range(1, total_labels):
        x1 = int(values[i, cv2.CC_STAT_LEFT])
        y1 = int(values[i, cv2.CC_STAT_TOP])
        w = int(values[i, cv2.CC_STAT_WIDTH])
        h = int(values[i, cv2.CC_STAT_HEIGHT])
        slots.append((x1, y1, w, h))  # Append each bounding box to the slots list
    return slots

def get_available_spaces():
    """Get the current count of available parking spaces."""
    return available_spaces_count

def process_parking_video(mask_path, video_path):
    """Process the parking video and update the available spaces count."""
    global available_spaces_count  # Use the global variable

    # Load the mask image in grayscale
    mask = cv2.imread(mask_path, 0)

    # Capture the video
    cap = cv2.VideoCapture(video_path)

    # Get connected components from the mask to identify parking spots
    connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)

    # Get bounding boxes for the parking spots
    spots = get_parking_spots_bboxes(connected_components)

    # Initialize lists for parking spot status
    spots_status = [None for _ in spots]
    
    previous_frame = None  # Previous frame for comparison
    frame_nmr = 0  # Frame number
    step = 30  # Step for frame skipping to reduce computation

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_nmr % step == 0:
            if previous_frame is not None:
                for spot_indx, spot in enumerate(spots):
                    x1, y1, w, h = spot
                    spot_crop = frame[y1:y1 + h, x1:x1 + w]
                    spot_status = empty_or_not(spot_crop)
                    spots_status[spot_indx] = spot_status

        if frame_nmr % step == 0:
            previous_frame = frame.copy()

        # Update the count of available spaces
        available_spaces_count = sum(status is EMPTY for status in spots_status if status is not None)
        print(f'Available free spots: {available_spaces_count}')  # Log available spaces count

    cap.release()
    cv2.destroyAllWindows()
    
    # Return the count of available spaces
    return available_spaces_count

# Call the process_parking_video function with appropriate paths
if __name__ == "__main__":
    mask_path = './mask_1920_1080.png'
    video_path = os.path.join('data', 'source', 'carPark.mp4')
    available_spaces = process_parking_video(mask_path, video_path)
    print(f"Total available spaces: {available_spaces}")
