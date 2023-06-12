import cv2
import numpy as np
import importlib.util
# Import TensorFlow libraries
# If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
else:
    from tensorflow.lite.python.interpreter import Interpreter


class Detector:
    def __init__(self, model_checkpoint, input_size=224) -> None:
        self.model = Interpreter(model_path=model_checkpoint)
        self.model.allocate_tensors()
        self.input_size = input_size
        self.input_details = self.model.get_input_details()
        self.output_details = self.model.get_output_details()
        self.num_fingers = 5


    def process_hands(self, image, draw=False):
        keypoints = self.get_keypoints(image)

        for keypoint in keypoints:
            cx, cy = int(keypoint[0]), int(keypoint[1])
            if draw:
                cv2.circle(image, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        bbox = []
        xmin, xmax = min(keypoints[:, 0]), max(keypoints[:, 0])
        ymin, ymax = min(keypoints[:, 1]), max(keypoints[:, 1])
        bbox = xmin, ymin, xmax, ymax

        if draw:
            cv2.rectangle(image, (int(xmin) - 20, int(ymin) - 20), (int(xmax) + 20, int(ymax) + 20), (0, 255, 0), 2)
            cv2.imwrite('./results/test.jpg', image)

        return keypoints, bbox
    
    
    def get_keypoints(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
        image = cv2.resize(image, (self.input_size, self.input_size))
        # image = image / 127.5
        # image -= 1
        image = np.expand_dims(image, axis=0) / 255.0

        self.model.set_tensor(self.input_details[0]['index'], image)
        self.model.invoke()
        y_pred = self.model.get_tensor(self.output_details[0]['index'])
        # y_pred = np.squeeze(y_pred, axis=0)
        # return self.find_fingers(y_pred)
        return np.squeeze(y_pred, axis=0).reshape(21, 3)[:, :2]


    def find_finger(self, P, X, Y, img_size=224, k=7):
        ind = np.unravel_index(np.argmax(P, axis=None), P.shape)
        P = P[ind]

        thresh = -10
        if P < thresh:
            points = [-1, -1]
            return points

        X, Y = X[ind], Y[ind]

        cell_size = img_size // k

        X = (ind[1] + X) * cell_size
        Y = (ind[0] + Y) * cell_size

        points = [X, Y]

        return points


    def find_fingers(self, y_pred):
        p_pred = y_pred[:, :, :self.num_fingers]

        C = 7
        xy_pred = y_pred[:, :, self.num_fingers:].reshape(C, C, 2, self.num_fingers)
        xy_pred = np.transpose(xy_pred, (0, 1, 3, 2))

        # sigmoid
        xy_pred = 1 / (1 + np.exp(-xy_pred))

        fingers = []
        for i in range(self.num_fingers):
            fingers.append(self.find_finger(p_pred[:, :, i], xy_pred[:, :, i, 0], xy_pred[:, :, i, 1]))

        return np.array(fingers)


    def check_fingers(self, points):
        finger_tips = [4, 8, 12, 16, 20]
        fingers = [0, 0, 0, 0, 0]
        
        if not points.any():
            return fingers

        if points[finger_tips[0]][0] > points[finger_tips[0] - 1][0]:
            fingers.append(1)
        else:
            fingers.append(0)

        for i in range(1, 5):
            if points[finger_tips[i]][1] < points[finger_tips[i] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
        


