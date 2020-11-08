import pyglet

from ui import widgets
from core.rigidbody import RigidBody
from app import colors
from constants import *

add_object_icon = pyglet.image.load('assets/add_object_icon.png')
add_force_icon = pyglet.image.load('assets/add_force_icon.png')
ruler_icon = pyglet.image.load('assets/ruler_icon.png')


class ToolBox(widgets.Layout):
    def __init__(self):
        super().__init__(0, 0, 0, 0)
        self.max_width = 60
        self.color = colors.TOOLBOX_COLOR
        self.border_color = (0, 0, 0, 0.2)
        self.button_size = 48
        self.init_ui()
    
    def init_ui(self):
        tool_list = [
            (add_object_icon, self.add_bt_function),
            (add_force_icon, self.force_bt_function),
            (ruler_icon, self.ruler_bt_function),
        ]
        self.set_tools(tool_list)
        
    def set_tools(self, tools):
        self.elements.clear()
        for icon, command in tools:    
            bt = widgets.Iconbutton(6, 0, 0, 0, image=icon, command=command)
            bt.min_height = self.button_size
            bt.max_height = self.button_size
            bt.margin_top = 6
            self.add(bt)
    
    def add_bt_function(self):
        self.parent.add_object_window.show()

    def force_bt_function(self):
        self.parent.add_force_window.show()
    
    def ruler_bt_function(self):
        pass
