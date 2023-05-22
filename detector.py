import numpy as np
import tensorflow as tf
import cv2


class Detector:
    def __init__(self, model_checkpoint) -> None:
        self.model = tf.lite.Interpreter(model_checkpoint)
        self.model.allocate_tensors()


    def process_hands(self, image, draw=False):
        keypoints = self.get_keypoints(image)

        for keypoint in enumerate(keypoints):
            cx, cy = int(keypoint[0]), int(keypoint[1])
            if draw:
                cv2.circle(image, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        bbox = []
        xmin, xmax = min(keypoints[:, 0]), max(keypoints[:, 0])
        ymin, ymax = min(keypoints[:, 1]), max(keypoints[:, 1])
        bbox = xmin, ymin, xmax, ymax

        if draw:
            cv2.rectangle(image, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)
            cv2.imwrite('test.jpg', image)

        return keypoints, bbox


    def check_fingers(points):
        fingers = []
        
        # todo

        return fingers


    def get_keypoints(self, image):
        image = tf.image.decode_jpeg(image, channels=3)
        image = tf.image.convert_image_dtype(image, tf.float32)
        image = tf.image.resize_with_pad(image, input_size, input_size)
