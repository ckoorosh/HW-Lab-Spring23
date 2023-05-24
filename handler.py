import socket
import json
from enum import Enum

class Command(Enum):
    MOVE = 1
    CLICK = 2
    DOUBLE_CLICK = 3
    RIGHT_CLICK = 4
    SCROLL = 5


class Handler:
    def __init__(self) -> None:
        self.port = 12345
        # self.mouse_down = False
        self.clicked = False
        self.right_clicked = False
        self.double_clicked = False
        self.last_scroll = -1
        self.initialize_server()


    def initialize_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('127.0.0.1', self.port))
            server_socket.listen(1)
            print(f'Server is listening at port {self.port}')
            connection, address = server_socket.accept()
            with connection:
                print(f"Connected by {address}")
                self.client = connection


    def handle_gesture(self, gesture, co1=(0, 0)):
        # move mouse
        if gesture == [0, 1, 0, 0, 0]:
            data = {'type': Command.MOVE, 'x': co1[0], 'y': co1[1]}
            self.client.send(json.dumps(data).encode('utf-8'))
            print("Move mouse case")
        # click
        elif gesture == [0, 1, 1, 0, 0]:
            if not self.clicked:
                data = {'type': Command.CLICK}
                self.client.send(json.dumps(data).encode('utf-8'))
                print("Click case")
            else:
                self.clicked = False
        # double click
        elif gesture == [1, 1, 0, 0, 0]:
            if not self.double_clicked:
                data = {'type': Command.DOUBLE_CLICK}
                self.client.send(json.dumps(data).encode('utf-8'))
                print("Double click case")
            else:
                self.double_clicked = False
        # right click
        elif gesture == [1, 1, 1, 0, 0]:
            if not self.right_clicked:
                data = {'type': Command.RIGHT_CLICK}
                self.client.send(json.dumps(data).encode('utf-8'))
                print("Right click case")
            else:
                self.right_clicked = False
        # scroll
        elif gesture == [1, 1, 1, 1, 1]:
            if self.last_scroll == -1:
                self.last_scroll = co1[1]
            elif abs(last_pos_scroll - co1[1]) > 10:
                    offset = int((self.last_scroll - co1[1]))
                    last_pos_scroll = co1[1]
                    data = {'type': Command.SCROLL, 'offset': offset}
                    self.client.send(json.dumps(data).encode('utf-8'))
                    print("Scroll case")
        else:
            self.last_scroll = -1

