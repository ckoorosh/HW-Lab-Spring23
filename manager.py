import numpy as np
import time
import cv2
from detector import *
from handler import *


MODEL_CHECKPOINT = '/checkpoints/model.tflite'


class Manager:
    def __init__(self) -> None:
        self.camera_width = 224
        self.camera_height = 224
        self.frame_rate = 50
        self.smoothening = 7

        self.pTime = 0
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0
        self.mouseDown = False
        self.clicked = False
        self.rclicked = False
        self.dclicked = False
        self.last_pos_scroll = -1

        self.last_ss = time.time_ns()

        self.capture = cv2.VideoCapture(0)
        self.capture.set(3, self.camera_width)
        self.capture.set(4, self.camera_height)

        self.detector = Detector(MODEL_CHECKPOINT)
        self.client = initialize_client()

    def start(self):
        while True:
            fingers = [0, 0, 0, 0, 0]
            _, image = self.capture.read()
            keypoints, bbox = self.detector.process_hands(image, draw=True)
            x1, y1 = 0, 0

            if len(keypoints) != 0:
                x1, y1 = keypoints[0]
                # print(x1, y1)

            fingers = self.detector.check_fingers(keypoints)
            handle_gesture(fingers, self.client, co1=(x1, y1))


if __name__ == "__main__":
    manager = Manager()
    manager.start()