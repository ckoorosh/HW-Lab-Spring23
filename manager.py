from detector import process_hands, check_fingers, get_models
import numpy as np
import time
import cv2
from handler import *


wCam, hCam = 320, 240 # webcam resuloution
frameR = 50
smoothening = 7

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
mouseDown = False
clicked = False
rclicked = False
dclicked = False
last_pos_scroll = -1

last_ss = time.time_ns()

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector, pose_estimator = get_models()

client = initialize_client()

while True:
    # 1. Find hand Landmarks
    fingers = [0, 0, 0, 0, 0]
    success, img = cap.read()
    points, bbox = process_hands(img, detector, pose_estimator, draw=True)
    x1, y1, x2, y2 = 0, 0, 0, 0
    # 2. Get the tip of the index and middle fingers
    if len(points) != 0:
        x1, y1 = points[8][1:3]
        x2, y2 = points[12][1:3]
        # print(x1, y1, x2, y2)

    # 3. Check which fingers are up
    fingers = check_fingers(points)

    handle_gesture(fingers, client, co1=(x1, y1), co2=(x2, y2))


