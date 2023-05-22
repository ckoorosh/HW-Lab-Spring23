import pyautogui
from enum import Enum

class Command(Enum):
    MOVE = 1
    CLICK = 2
    DOUBLE_CLICK = 3
    RIGHT_CLICK = 4
    SCROLL_UP = 5


def get_data():
    '''
    Get the command from server socket
    '''
    pass


def run(data: dict):
    if 'type' in data:
        if data['type'] == Command.MOVE:
            pass
        elif data['type'] == Command.CLICK:
            pass
        elif data['type'] == Command.DOUBLE_CLICK:
            pass
        elif data['type'] == Command.RIGHT_CLICK:
            pass
        elif data['type'] == Command.SCROLL_UP:
            pass
    else:
        pass


while True:
    data = get_data()
    if data:
        run(data)