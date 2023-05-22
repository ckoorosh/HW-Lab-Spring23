import socket
import json
from enum import Enum

class Command(Enum):
    MOVE = 1
    CLICK = 2
    DOUBLE_CLICK = 3
    RIGHT_CLICK = 4
    SCROLL_UP = 5


class Handler:
    def __init__(self) -> None:
        self.port = 12345
        # self.mouse_down = False
        self.clicked = False
        self.right_clicked = False
        self.double_clicked = False
        self.last_scroll = -1


    def initialize_client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', self.port)) # 5.208.214.153
        print('Connected to server')
        self.client = client


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
        # scroll up
        elif gesture == [1, 1, 1, 1, 1]:
            if self.last_scroll == -1:
                self.last_scroll = co1[1]
            elif abs(last_pos_scroll - co1[1]) > 10:
                    offset = int((self.last_scroll - co1[1]))
                    last_pos_scroll = co1[1]
                    data = {'type': Command.SCROLL_UP, 'offset': offset}
                    self.client.send(json.dumps(data).encode('utf-8'))
                    print("Scroll up case")
        else:
            self.last_scroll = -1

