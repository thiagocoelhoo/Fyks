import pyglet

import app
from ui import widgets


class Interface(widgets.Frame):
    def __init__(self, width, height):
        super().__init__(0, 0, width, height)
        self.init_ui()
    
    def init_ui(self):
        layout = widgets.Layout(0, 0, self.width, self.height)

        # Menu
        file_dialog = app.utils.FileDialog()
        
        menu = widgets.Menu()
        menu.color = app.colors.MENU_BACKGROUND_COLOR
        dropdown = menu.add_dropdown(
            name='Arquivo',
            options=(
                ('Salvar', file_dialog.save_file_dialog),
                ('Carregar', file_dialog.open_file_dialog),
            )
        )
        menu.add_button('Editar', None)
        menu.add_button('Ajuda', None)
        menu.z_index = 1
        
        overlayer = widgets.Layer(0, 0, self.width, self.height)
        overlayer.z_index = 1
        overlayer.add(dropdown)

        # Context
        content_layout = widgets.Layout(0, 0, 1, 1, orientation='vertical')
        context_frame = app.widgets.ContextFrame(0, 0, 1, 1)
        
        # Toolbox
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

        # Add
        content_layout.add(toolbox)
        content_layout.add(context_frame)

        layout.add(menu)
        layout.add(content_layout)

        self.add(layout)
        self.add(overlayer)

    def on_resize(self, w, h):
        self.resize(w, h)
        for widget in self.elements:
            widget.resize(w, h)