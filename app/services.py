# from app.utils import ParkClassifier

# classifier = ParkClassifier()

# def process_video(video_path):
#     # Process the video using the classifier
#     classifier.classify_video(video_path)

# def get_parking_status():
#     # Return the latest count of available spaces
#     return classifier.get_available_spaces()



from app.utils import ParkClassifier

classifier = ParkClassifier()

def process_video(video_path):
    # Process the video using the classifier
    classifier.classify_video(video_path)

def get_parking_status():
    # Return the latest count of available spaces
    return classifier.get_available_spaces()
