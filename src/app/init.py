import app
from ui import widgets


def init_ui(width, height):
    layout = widgets.Layout(0, 0, width, height)

    file_dialog = app.utils.FileDialog()
    menu = widgets.Menu()
    menu.color = app.colors.MENU_BACKGROUND_COLOR
    menu.add_dropdown(
        name='Arquivo',
        options=(
            ('Salvar', file_dialog.save_file_dialog),
            ('Carregar', file_dialog.open_file_dialog),
        )
    )
    menu.add_button('Editar', None)
    menu.add_button('Ajuda', None)

    context_frame = app.widgets.ContextFrame(0, 0, 10, 10)
    toolbox = app.widgets.ToolBox()
    content_layout = widgets.Layout(0, 0, 0, 0, orientation='vertical')
    content_layout.add(toolbox)
    content_layout.add(context_frame)

    layout.add(menu)
    layout.add(content_layout)
    return layout
