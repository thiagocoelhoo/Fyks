import pyglet

import app
from ui import widgets
from app import update


class Interface(widgets.Frame):
    def __init__(self, width, height):
        super().__init__(0, 0, width, height)
        self.init_ui()
    
    def init_ui(self):
        main_layout = widgets.Layout(0, 0, self.width, self.height)
        menu, overlayer = self.create_menu()
        
        content_layout = widgets.Layout(0, 0, 1, 1, orientation='vertical')
        context_frame = app.widgets.ContextFrame(0, 0, 1, 1)
        toolbox = self.create_toolbox(context_frame)
        
        content_layout.add(toolbox)
        content_layout.add(context_frame)
        
        main_layout.add(menu)
        main_layout.add(content_layout)

        self.add(main_layout)
        self.add(overlayer)
    
    def create_menu(self):
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
        if update.check_updates():
            menu.add_button('Atualizar', update.update)
            button = menu.elements[-1]
            button.label.lab.color = (255, 50, 10, 255)
        menu.z_index = 1
        
        overlayer = widgets.Layer(0, 0, self.width, self.height)
        overlayer.z_index = 1
        overlayer.add(dropdown)

        return menu, overlayer
    
    def create_toolbox(self, context_frame):
        toolbox = app.widgets.ToolBox()
    
        toolbox.add_tool_bt(
            icon=pyglet.image.load('assets/cursor_icon.png'),
            command=context_frame.ctx_wrapper.set_select_mode)
        toolbox.add_tool_bt(
            icon=pyglet.image.load('assets/move_icon.png'),
            command=context_frame.ctx_wrapper.set_move_mode)
        toolbox.add_tool_bt(
            icon=pyglet.image.load('assets/ruler_icon.png'), 
            command=context_frame.ctx_wrapper.set_ruler_mode)
        toolbox.add_tool_bt(
            icon=pyglet.image.load('assets/add_object_icon.png'), 
            command=context_frame.add_object_window.show)
        toolbox.add_tool_bt(
            icon=pyglet.image.load('assets/add_force_icon.png'), 
            command=context_frame.add_force_window.show)
        
        return toolbox
    
    def on_resize(self, w, h):
        self.resize(w, h)
        for widget in self.elements:
            widget.resize(w, h)
