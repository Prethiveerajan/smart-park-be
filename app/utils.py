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


