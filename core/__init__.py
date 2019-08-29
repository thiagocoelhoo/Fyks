from .eventhandler import EventHandler
from .mouse import Mouse

_eventhandler = None
_mouse = None


def init():
    global _eventhandler, _mouse
    _eventhandler = EventHandler()
    _mouse = Mouse()


def get_eventhandler():
    return _eventhandler


def get_mouse():
    return _mouse
