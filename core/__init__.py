import json

from .eventhandler import EventHandler
from .mouse import Mouse

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
