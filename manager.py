import numpy as np
import time
import cv2
from detector import *
from handler import *


MODEL_CHECKPOINT = './checkpoints/model.tflite'

image_path = './sample/1402.jpg'


class Manager:
    def __init__(self) -> None:
        self.camera_width = 224
        self.camera_height = 224
        self.frame_rate = 30
        self.smoothening = 7

        self.stream = cv2.VideoCapture(0)
        self.stream.set(3, self.camera_width)
        self.stream.set(4, self.camera_height)

        self.detector = Detector(MODEL_CHECKPOINT)
        self.handler = Handler()

    def start(self):
        self.handler.initialize_client()
        while True:
            fingers = [0, 0, 0, 0, 0]
            # _, image = self.stream.read()
            image = cv2.imread(image_path)
            keypoints, bbox = self.detector.process_hands(image, draw=True)
            x1, y1 = 0, 0

            if len(keypoints) != 0:
                x1, y1 = keypoints[0]
                print(x1, y1)

            fingers = self.detector.check_fingers(keypoints)
            self.handler.handle_gesture(fingers, co1=(x1, y1))

            break


if __name__ == "__main__":
    manager = Manager()
    manager.start()