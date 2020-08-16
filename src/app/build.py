from ui import Frame, Menu
from context.contextframe import ContextFrame


def build_GUI(width, height):
    frame = Frame(0, 0, width, height)

    context = ContextFrame(0, 0, width, height-30, parent=frame)
    menu = Menu(frame)
    menu.add_button('Arquivo', None)
    menu.add_button('Editar', None)
    menu.add_button('Ajuda', None)
    
    return frame