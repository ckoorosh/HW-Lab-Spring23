import socket
import json
from enum import Enum

class Command(Enum):
    MOVE = 1
    CLICK = 2
    DOUBLE_CLICK = 3
    RIGHT_CLICK = 4
    SCROLL_UP = 5


port = 12345

def initialize_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', port))
    print('Connected to server')
    return client


def handle_gesture(gesture, client, co1=(0, 0), co2=(0, 0)):
    # move mouse
    if gesture == [0, 1, 0, 0, 0]:
        data = {'type': Command.MOVE, 'x': co1[0], 'y': co1[1]}
        client.send(json.dumps(data).encode('utf-8'))
        print("Move mouse case")
    # click
    elif gesture == [0, 1, 1, 0, 0]:
        data = {'type': Command.CLICK}
        client.send(json.dumps(data).encode('utf-8'))
        print("Click case")
    # double click
    elif gesture == [1, 1, 0, 0, 0]:
        data = {'type': Command.DOUBLE_CLICK}
        client.send(json.dumps(data).encode('utf-8'))
        print("Double click case")
    # right click
    elif gesture == [1, 1, 1, 0, 0]:
        data = {'type': Command.RIGHT_CLICK}
        client.send(json.dumps(data).encode('utf-8'))
        print("Right click case")
    # scroll up
    elif gesture == [1, 1, 1, 1, 1]:
        data = {'type': Command.SCROLL_UP, 'direction': 'up'}
        client.send(json.dumps(data).encode('utf-8'))
        print("Scroll up case")

