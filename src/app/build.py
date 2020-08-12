from ui import Frame, Button, Entry

from context.contextframe import ContextFrame


def build_GUI(width, height):
    frame = Frame(0, 0, width, height)
    
    context = ContextFrame(0, 0, width, height, parent=frame)
    
    return frame