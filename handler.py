import socket
import json

port = 12345

def initialize_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', port))
    print('Connected to server')
    return client


def handle_gesture(gesture, client, co1=(0, 0), co2=(0, 0)):
    # move mouse
    if gesture == [0, 1, 0, 0, 0]:
        data = {'type': 'move', 'x': co1[0], 'y': co1[1]}
        client.send(json.dumps(data).encode('utf-8'))
        print("Move mouse case")
    # double click
    elif gesture == [0, 1, 1, 0, 0]:
        data = {'type': 'double_click'}
        client.send(json.dumps(data).encode('utf-8'))
        print("Double click case")
    # right click
    elif gesture == [0, 1, 1, 1, 0]:
        data = {'type': 'right_click'}
        client.send(json.dumps(data).encode('utf-8'))
        print("Right click case")
    # scroll up
    elif gesture == [0, 1, 1, 1, 1]:
        data = {'type': 'scroll', 'direction': 'up'}
        client.send(json.dumps(data).encode('utf-8'))
        print("Scroll up case")
    # click
    elif gesture == [1, 1, 1, 1, 1]:
        data = {'type': 'click'}
        client.send(json.dumps(data).encode('utf-8'))
        print("Click case")

