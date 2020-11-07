from ui import widgets
from context.context_frame import ContextFrame
from utils.filedialog import FileDialog
from app import colors

file_dialog = FileDialog()


def init_ui(width, height):
    layout = widgets.Layout(0, 0, width, height)

    context_frame = ContextFrame(0, 0, 10, 10)
    menu = widgets.Menu()
    menu.color = colors.MENU_BACKGROUND_COLOR
    menu.add_dropdown(
        name='Arquivo',
        options=(
            ('Salvar', file_dialog.save_file_dialog),
            ('Carregar', file_dialog.open_file_dialog),
        )
    )
    menu.add_button('Editar', None)
    menu.add_button('Ajuda', None)

    layout.add(menu)
    layout.add(context_frame)
    return layout
