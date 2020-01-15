import json

from core.eventhandler import EventHandler
from core.mouse import Mouse


_eventhandler = None
_mouse = None
theme = {}


def get_eventhandler():
    return _eventhandler


def get_mouse():
    return _mouse


def set_theme(name):
    global theme
    with open("themes.json", "r") as f:
        theme = json.load(f)[name]


def init():
    global _eventhandler, _mouse
    _eventhandler = EventHandler()
    _mouse = Mouse()
    set_theme("white")


class handler:
    def __init__(self, event):
        self.event = event
    
    def __call__(self, func):
        return self.handler_decorator(func)
    
    def handler_decorator(self, func):
        _eventhandler.add_handler(self.event, func)
        return func

