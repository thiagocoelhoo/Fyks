import pyglet

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
    menu.z_index = 1
    
    content_layout = widgets.Layout(0, 0, 0, 0, orientation='vertical')
    context_frame = app.widgets.ContextFrame(0, 0, 0, 0)
    
    toolbox = app.widgets.ToolBox()

    toolbox.add_tool_bt(
        icon=pyglet.image.load('assets/add_object_icon.png'), 
        command=context_frame.add_object_window.show)
    toolbox.add_tool_bt(
        icon=pyglet.image.load('assets/add_force_icon.png'), 
        command=context_frame.add_object_window.show)
    toolbox.add_tool_bt(
        icon=pyglet.image.load('assets/ruler_icon.png'), 
        command=context_frame.add_object_window.show)

    content_layout.add(toolbox)
    content_layout.add(context_frame)

    layout.add(menu)
    layout.add(content_layout)

    return layout
