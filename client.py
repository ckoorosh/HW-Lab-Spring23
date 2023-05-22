import pyautogui
from enum import Enum
import numpy as np
from tkinter import messagebox
import socket
import json


class Command(Enum):
    MOVE = 1
    CLICK = 2
    DOUBLE_CLICK = 3
    RIGHT_CLICK = 4
    SCROLL_UP = 5


class Client:
    def __init__(self) -> None:
        self.camera_width = 224
        self.camera_height = 224
        self.screen_width, self.screen_height = pyautogui.size()
        self.x_mid = self.screen_width // 2
        self.y_mid = self.screen_height // 2
        self.smoothening = 7
        self.frame_rate = 30
        pyautogui.PAUSE = 0.02
        # self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server_socket.bind(('localhost', 12345))
        # self.client_socket.connect(('localhost', 12345))
        # print("Connected to server successfully")

    def get_data(self, connection):
        '''
        Get the command from server socket
        '''
        data = connection.recv(1024).decode()
        if data:
            print(data)
            return json.loads(data)
        else:
            return None

    def move_curser(self, x, y):
        x1 = np.interp(x, (self.frame_rate, self.camera_width - self.frame_rate), (0, self.screen_width))
        y1 = np.interp(y, (self.frame_rate, self.camera_height - self.frame_rate), (0, self.screen_height))

        x2 = self.x_mid + (x1 - self.x_mid) / self.smoothening
        y2 = self.y_mid + (y1 - self.y_mid) / self.smoothening

        pyautogui.moveTo(self.screen_width - x2, y2)


    def run(self, data: dict):
        if 'type' in data:
            if data['type'] == Command.MOVE:
                self.move_curser(data['x'], data['y'])
            elif data['type'] == Command.CLICK:
                pyautogui.click()
                messagebox.showinfo("Clicked", "You clicked!")
            elif data['type'] == Command.DOUBLE_CLICK:
                pyautogui.doubleClick()
            elif data['type'] == Command.RIGHT_CLICK:
                pyautogui.rightClick()
            elif data['type'] == Command.SCROLL_UP:
                offset = -int(data['offset']) * 10
                pyautogui.scroll(offset)
        else:
            pass


    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('localhost', 12345))
            connection, address = self.server_socket.accept()
            with connection:
                print(f"Connected by {address}")
                while True:
                    data = self.get_data(connection)
                    if data is not None:
                        self.run(data)


if __name__ == "__main__":
    client = Client()
    client.start()