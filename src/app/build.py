from ui import Frame, Menu
from context.contextframe import ContextFrame
from app.fileswindow import FileManagerWindow

def show_file_manager():
    FileManagerWindow()

def build_main_frame(width, height):
    frame = Frame(0, 0, width, height)

    context = ContextFrame(0, 0, width, height-30, parent=frame)
    menu = Menu(frame)
    menu.add_dropdown(
        name='Arquivo',
        options=(
            ('Salvar', show_file_manager),
            ('Carregar', context.load),
        )
    )
    menu.add_button('Arquivo', None)
    menu.add_button('Editar', None)
    menu.add_button('Ajuda', None)

    return frame
