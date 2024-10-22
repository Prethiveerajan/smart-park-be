# import cv2
# from src.utils import Park_classifier

# class ParkClassifier:
#     def __init__(self, car_park_positions_path="data/source/CarParkPos", rect_width=107, rect_height=48):
#         self.classifier = Park_classifier(car_park_positions_path, rect_width, rect_height)
#         self.car_park_positions_path = car_park_positions_path
#         self.rect_width = rect_width
#         self.rect_height = rect_height
#         self.parking_status = []  # List to store the status of parking spots

#     def classify_video(self, video_path):
#         # Open the video file
#         cap = cv2.VideoCapture(video_path)

#         # Check if video opened successfully
#         if not cap.isOpened():
#             print("Error: Could not open video.")
#             return

#         # Process the video frame by frame
#         while True:
#             ret, frame = cap.read()

#             if not ret:
#                 break  # Exit loop if no more frames

#             # Process the frame
#             processed_frame = self.classifier.implement_process(frame)

#             # Get classification result
#             result = self.classifier.classify(frame, processed_frame)
#             print("Result from classify:", result)  # Check what is being returned
            
#             # Adjust unpacking based on what you find
#             if isinstance(result, tuple) and len(result) == 2:
#                 denoted_image, status = result
#             elif isinstance(result, dict):  # Example for dictionary return
#                 denoted_image = result.get('denoted_image')
#                 status = result.get('status')
#             else:
#                 print("Unexpected return value from classify")
#                 continue

#             # Update parking status
#             self.parking_status = status  # Assuming status is a list of boolean values indicating occupancy

#             # Display the processed frame
#             cv2.imshow("Car Park Image (empty/occupied)", denoted_image)

#             # Exit condition
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         # Release resources
#         cap.release()
#         cv2.destroyAllWindows()

#     def get_status(self):
#     # Return the parking status (e.g., a list of booleans)
#         return {"parking_status": self.parking_status}
# backend/app/utils.py


# import cv2
# from src.utils import Park_classifier

# class ParkClassifier:
#     def __init__(self, car_park_positions_path="data/source/CarParkPos", rect_width=107, rect_height=48):
#         self.classifier = Park_classifier(car_park_positions_path, rect_width, rect_height)
#         self.car_park_positions_path = car_park_positions_path
#         self.rect_width = rect_width
#         self.rect_height = rect_height
#         self.parking_status = []  # List to store the status of parking spots

#     def classify_video(self, video_path):
#         # Open the video file
#         cap = cv2.VideoCapture(video_path)

#         # Check if video opened successfully
#         if not cap.isOpened():
#             print("Error: Could not open video.")
#             return

#         # Process the video frame by frame
#         while True:
#             ret, frame = cap.read()

#             if not ret:
#                 break  # Exit loop if no more frames

#             # Process the frame
#             processed_frame = self.classifier.implement_process(frame)

#             # Get classification result
#             result = self.classifier.classify(frame, processed_frame)
#             print("Result from classify:", result)  # Debugging output

#             if isinstance(result, tuple) and len(result) == 2:
#                 denoted_image, status = result
#             elif isinstance(result, dict):  # Example for dictionary return
#                 denoted_image = result.get('denoted_image')
#                 status = result.get('status')
#             else:
#                 print("Unexpected return value from classify")
#                 continue

#             # Update parking status
#             self.parking_status = status  # Assuming status is a list of boolean values indicating occupancy

#             # Display the processed frame (optional, for debugging)
#             cv2.imshow("Car Park Image (empty/occupied)", denoted_image)

#             # Exit condition
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         # Release resources
#         cap.release()
#         cv2.destroyAllWindows()

#     def get_status(self):
#         print("Parking status being returned:", self.parking_status)  # Debug output
#         return self.parking_status


# import cv2
# import pandas as pd
# import numpy as np
# from ultralytics import YOLO

# class ParkClassifier:
#     def __init__(self, car_park_positions_path="data/source/CarParkPos", rect_width=107, rect_height=48):
#         self.model = YOLO('yolov8s.pt')  # Load the YOLO model
#         self.class_list = self.load_class_names()
#         self.areas = self.define_parking_areas()
#         self.parking_status = []

#     def load_class_names(self):
#         with open("coco.txt", "r") as my_file:
#             return my_file.read().split("\n")

#     def define_parking_areas(self):
#         return [
#             [(52, 364), (30, 417), (73, 412), (88, 369)],
#             [(105, 353), (86, 428), (137, 427), (146, 358)],
#             [(159, 354), (150, 427), (204, 425), (203, 353)],
#             [(217, 352), (219, 422), (273, 418), (261, 347)],
#             [(274, 345), (286, 417), (338, 415), (321, 345)],
#             [(336, 343), (357, 410), (409, 408), (382, 340)],
#             [(396, 338), (426, 404), (479, 399), (439, 334)],
#             [(458, 333), (494, 397), (543, 390), (495, 330)],
#             [(511, 327), (557, 388), (603, 383), (549, 324)],
#             [(564, 323), (615, 381), (654, 372), (596, 315)],
#             [(616, 316), (666, 369), (703, 363), (642, 312)],
#             [(674, 311), (730, 360), (764, 355), (707, 308)]
#         ]

#     def classify_video(self, video_path):
#         cap = cv2.VideoCapture(video_path)

#         if not cap.isOpened():
#             print("Error: Could not open video.")
#             return

#         car_counts = [0] * len(self.areas)

#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             frame = cv2.resize(frame, (1020, 500))
#             results = self.model.predict(frame)
#             a = results[0].boxes.data
#             px = pd.DataFrame(a).astype("float")

#             for index, row in px.iterrows():
#                 x1, y1, x2, y2, conf, d = map(int, row)
#                 c = self.class_list[d]

#                 if 'car' in c:
#                     cx = (x1 + x2) // 2
#                     cy = (y1 + y2) // 2

#                     for i, area in enumerate(self.areas):
#                         results_area = cv2.pointPolygonTest(np.array(area, np.int32), (cx, cy), False)
#                         if results_area >= 0:  # Car is in the parking area
#                             car_counts[i] += 1
#                             break

#         total_spaces = len(self.areas)
#         total_occupied = sum(car_counts)
#         self.parking_status = [count == 0 for count in car_counts]  # True if available

#         cap.release()

#     def get_status(self):
#         return self.parking_status

import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO

class ParkClassifier:
    def __init__(self, car_park_positions_path="data/source/CarParkPos", rect_width=107, rect_height=48):
        self.model = YOLO('yolov8s.pt')  # Load the YOLO model
        self.class_list = self.load_class_names()
        self.areas = self.define_parking_areas()
        self.latest_available_spaces = 0  # To store the latest available spaces count

    def load_class_names(self):
        with open("coco.txt", "r") as my_file:
            return my_file.read().split("\n")

    def define_parking_areas(self):
        return [
            [(52, 364), (30, 417), (73, 412), (88, 369)],
            [(105, 353), (86, 428), (137, 427), (146, 358)],
            [(159, 354), (150, 427), (204, 425), (203, 353)],
            [(217, 352), (219, 422), (273, 418), (261, 347)],
            [(274, 345), (286, 417), (338, 415), (321, 345)],
            [(336, 343), (357, 410), (409, 408), (382, 340)],
            [(396, 338), (426, 404), (479, 399), (439, 334)],
            [(458, 333), (494, 397), (543, 390), (495, 330)],
            [(511, 327), (557, 388), (603, 383), (549, 324)],
            [(564, 323), (615, 381), (654, 372), (596, 315)],
            [(616, 316), (666, 369), (703, 363), (642, 312)],
            [(674, 311), (730, 360), (764, 355), (707, 308)]
        ]

    def classify_video(self, video_path):
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("Error: Could not open video.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (1020, 500))
            results = self.model.predict(frame)
            a = results[0].boxes.data
            px = pd.DataFrame(a).astype("float")

            car_counts = [0] * len(self.areas)

            for index, row in px.iterrows():
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                c = self.class_list[d]

                if 'car' in c:
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    for i, area in enumerate(self.areas):
                        results_area = cv2.pointPolygonTest(np.array(area, np.int32), (cx, cy), False)
                        if results_area >= 0:  # Car is in the parking area
                            car_counts[i] += 1
                            break

            total_occupied = sum(car_counts)
            total_spaces = len(self.areas)
            self.latest_available_spaces = total_spaces - total_occupied

            print(f"Available spaces: {self.latest_available_spaces}")  # Debugging output

        cap.release()

    def get_available_spaces(self):
        return self.latest_available_spaces
