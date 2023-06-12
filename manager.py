import numpy as np
import time
import cv2
from detector import *
from handler import *


MODEL_CHECKPOINT = './checkpoints/hand_detector.tflite'

image_path = './sample/1402.jpg'


class Manager:
    def __init__(self) -> None:
        self.camera_width = 224
        self.camera_height = 224

        self.handler = Handler()
        self.detector = Detector(MODEL_CHECKPOINT)
        
        self.stream = cv2.VideoCapture(0)
        self.stream.set(3, self.camera_width)
        self.stream.set(4, self.camera_height)

    def start(self):
        while True:
            fingers = [0, 0, 0, 0, 0]
            success, image = self.stream.read()
            # print(success, image, self.stream)
            # image = cv2.imread(image_path)
            keypoints, bbox = self.detector.process_hands(image, draw=True)
            x1, y1 = 0, 0

            if len(keypoints) > 0:
                x1, y1 = keypoints[4]
                print(x1, y1)

            fingers = self.detector.check_fingers(keypoints)
            print(fingers)
            self.handler.handle_gesture(fingers, co1=(x1, y1))

            # break


if __name__ == "__main__":
    manager = Manager()
    manager.start()
