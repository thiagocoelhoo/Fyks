from ui import Frame, Menu
from context.context_frame import ContextFrame
from utils.filedialog import FileDialog

file_dialog = FileDialog()


def init_ui(width, height):
    frame = Frame(0, 0, width, height)

    context_frame = ContextFrame(0, 0, width, height-30, parent=frame)
    menu = Menu(frame)
    menu.add_dropdown(
        name='Arquivo',
        options=(
            ('Salvar', file_dialog.save_file_dialog),
            ('Carregar', file_dialog.open_file_dialog),
        )
    )
    menu.add_button('Editar', None)
    menu.add_button('Ajuda', None)

    return frame
